import os
import shutil

from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.layout import basic_layout

class ZakKembleAvrGccConan(ConanFile):
    name = "zakkembleavrgcc"
    homepage = "https://github.com/ZakKemble/avr-gcc-build"
    settings = "os", "arch"
    package_type = "application"

    def source(self):
        pass

    def build(self):
        pass

    def layout(self):
        basic_layout(self)

    def package(self):
        # url and sha256: a download that changed upstream fails instead of slipping in
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os).lower()],
            strip_root=True, destination=self.package_folder)

    def package_info(self):
        suffix = ".exe" if self.settings.os == "Windows" else ""
        toolchain = os.path.join(self.package_folder, "bin", "avr")
        self.conf_info.define("tools.build:compiler_executables", {
            "c": f"{toolchain}-gcc{suffix}",
            "cpp": f"{toolchain}-g++{suffix}"
        })

