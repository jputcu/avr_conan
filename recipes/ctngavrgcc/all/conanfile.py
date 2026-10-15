import os
import re

from conan import ConanFile
from conan.errors import ConanException, ConanInvalidConfiguration
from conan.tools.build import build_jobs
from conan.tools.files import get, copy, load, save, chdir
from conan.tools.layout import basic_layout

# avr-gcc with a freestanding libstdc++, built by crosstool-ng. source() fetches every
# component tarball (checked against crosstool-ng's own digests), build() is offline.
class CtngAvrGccConan(ConanFile):
    name = "ctngavrgcc"
    homepage = "https://crosstool-ng.github.io"
    license = "GPL-3.0-or-later"
    settings = "os", "arch"
    package_type = "application"
    no_copy_source = True
    exports_sources = "defconfigs/*"

    def layout(self):
        basic_layout(self)

    def validate(self):
        # crosstool-ng builds for the machine it runs on, a canadian cross is not set up
        if self.settings.os != "Linux":
            raise ConanInvalidConfiguration("ctngavrgcc builds on Linux only")
        if self.settings_build and self.settings.arch != self.settings_build.arch:
            raise ConanInvalidConfiguration("ctngavrgcc cannot be cross built")

    @property
    def _ct_ng(self):
        return os.path.join(self.source_folder, "crosstool-ng", "ct-ng")

    @property
    def _tarballs(self):
        return os.path.join(self.source_folder, "tarballs")

    def _run_ct_ng(self, args):
        # crosstool-ng aborts on a CFLAGS or LD_LIBRARY_PATH from the environment
        self.run(f"env -u CFLAGS -u CXXFLAGS -u LDFLAGS -u LD_LIBRARY_PATH {self._ct_ng} {args}")

    def _configure(self, extra):
        save(self, "defconfig", load(self, os.path.join(self.source_folder, "defconfigs", self.version))
             + "".join(f"{line}\n" for line in extra))
        self._run_ct_ng("defconfig")
        gcc = re.search(r'^CT_GCC_VERSION="(.*)"$', load(self, ".config"), re.MULTILINE).group(1)
        if gcc != self.version:
            raise ConanException(f"defconfig selects gcc {gcc}, not {self.version}")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], destination="crosstool-ng", strip_root=True)
        with chdir(self, "crosstool-ng"):
            self.run("./configure --enable-local && make")
        # The sources the build needs, in the source folder so `conan cache save` keeps them.
        # crosstool-ng only saves into a folder that exists
        os.makedirs(self._tarballs, exist_ok=True)
        os.makedirs("work", exist_ok=True)
        with chdir(self, "work"):
            self._configure([f'CT_LOCAL_TARBALLS_DIR="{self._tarballs}"', "CT_SAVE_TARBALLS=y",
                             "CT_ONLY_DOWNLOAD=y"])
            self._run_ct_ng("build")

    def build(self):
        self._configure([f'CT_LOCAL_TARBALLS_DIR="{self._tarballs}"', "CT_FORBID_DOWNLOAD=y",
                         f'CT_PREFIX_DIR="{os.path.join(self.build_folder, "install")}"',
                         "# CT_PREFIX_DIR_RO is not set", "# CT_LOG_PROGRESS_BAR is not set"])
        self._run_ct_ng(f"build.{build_jobs(self)}")

    def package(self):
        install = os.path.join(self.build_folder, "install")
        copy(self, "*", src=install, dst=self.package_folder)
        copy(self, "*", src=os.path.join(install, "share", "licenses"),
             dst=os.path.join(self.package_folder, "licenses"))
        # How it was built: the input defconfig and the full configuration crosstool-ng used
        # (copy() skips the hidden .config)
        ctng = os.path.join(self.package_folder, "share", "ctng")
        copy(self, "defconfig", src=self.build_folder, dst=ctng)
        save(self, os.path.join(ctng, "config"), load(self, os.path.join(self.build_folder, ".config")))

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        toolchain = os.path.join(self.package_folder, "bin", "avr")
        self.conf_info.define("tools.build:compiler_executables", {
            "c": f"{toolchain}-gcc",
            "cpp": f"{toolchain}-g++"
        })
