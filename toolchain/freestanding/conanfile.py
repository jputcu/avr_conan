import os
from conan.tools.files import get, copy, mkdir, rmdir, chdir, rm
from conan.tools.build import build_jobs
from conan.tools.layout import basic_layout
from conan import ConanFile

class AvrGccConan(ConanFile):
    name = "avr-gcc"
    version = "14.2.0"
    settings = "os", "arch"
    no_copy_source = True
    package_type = "application"
    config_fl = "--disable-doc"
    logfile = "avr-gcc_build.log"

    def layout(self):
        basic_layout(self)

    def _run(self, cmd):
        with open(os.path.join(self.build_folder, self.logfile), "a") as log:
            self.run(cmd, stdout=log, stderr=log)

    def source(self):
        get(self, "https://ftp.gnu.org/gnu/gcc/gcc-14.2.0/gcc-14.2.0.tar.xz", destination="gcc", strip_root=True)
        with chdir(self, "gcc"):
            # self.run("bash ./contrib/download_prerequisites")
            get(self, "http://gcc.gnu.org/pub/gcc/infrastructure/gettext-0.22.tar.gz", destination="gettext", strip_root=True)
            get(self, "http://gcc.gnu.org/pub/gcc/infrastructure/gmp-6.2.1.tar.bz2", destination="gmp", strip_root=True)
            get(self, "http://gcc.gnu.org/pub/gcc/infrastructure/mpfr-4.1.0.tar.bz2", destination="mpfr", strip_root=True)
            get(self, "http://gcc.gnu.org/pub/gcc/infrastructure/mpc-1.2.1.tar.gz", destination="mpc", strip_root=True)
            get(self, "http://gcc.gnu.org/pub/gcc/infrastructure/isl-0.24.tar.bz2", destination="isl", strip_root=True)
        get(self, "https://ftp.gnu.org/gnu/binutils/binutils-2.44.tar.xz", destination="binutils", strip_root=True)
        get(self, "https://github.com/avrdudes/avr-libc/releases/download/avr-libc-2_2_1-release/avr-libc-2.2.1.tar.bz2", destination="avr-libc", strip_root=True)
        with chdir(self, "avr-libc"):
            self.run("bash ./bootstrap")

    def _build_binutils(self):
        self.output.info("Building binutils")
        config_file = os.path.relpath(os.path.join(self.source_folder, "binutils", "configure"), "binutils")
        mkdir(self, "binutils")
        with chdir(self, "binutils"):
            self._run(f"bash {config_file} --prefix={self.prefix} {self.config_fl} --target=avr --disable-nls "
                    + "--disable-sim")
            self._run(f"make -j{build_jobs(self)}")
            self._run(f"make -j{build_jobs(self)} install-strip")
        #rmdir(self, "binutils")

    def _build_gcc(self):
        self.output.info("Building gcc 1st stage")
        config_file = os.path.relpath(os.path.join(self.source_folder, "gcc", "configure"), "gcc")
        mkdir(self, "gcc")
        with chdir(self, "gcc"):
            self._run(f"bash {config_file} --prefix={self.prefix} {self.config_fl} "
                + "--target=avr --enable-languages=c,c++ --disable-nls --disable-libssp "
                + "--disable-libada --disable-libgomp --with-avrlibc=yes --with-dwarf2 --disable-shared")
            self._run(f"make -j{build_jobs(self)}")
            self._run(f"make -j{build_jobs(self)} install-strip")

    def _build_avrlibc(self):
        self.output.info("Building avr-libc")
        rel_src_path = os.path.relpath(os.path.join(self.source_folder, "avr-libc"), "avr-libc")
        config_file = os.path.join(rel_src_path, "configure")
        mkdir(self, "avr-libc")
        with chdir(self, "avr-libc"):
            self._run(f"bash {config_file} --prefix={self.prefix} {self.config_fl} "
                + "--host=avr --build=\`{rel_src_path}/config.guess\`")
            self._run(f"make -j{build_jobs(self)}")
            self._run(f"make -j{build_jobs(self)} install")

    def _build_freestanding(self):
        self.output.info("Building gcc final stage")
        config_file = os.path.relpath(os.path.join(self.source_folder, "gcc", "configure"), "gcc")
        with chdir(self, "gcc"):
            self._run(f"bash {config_file} --prefix={self.prefix} {self.config_fl} "
                + "--target=avr --enable-languages=c,c++ --disable-nls --disable-libssp --disable-libada "
                + "--disable-libgomp --with-avrlibc=yes --with-newlib --with-dwarf2 --disable-__cxa_atexit "
                + "--disable-threads --disable-shared --disable-sjlj-exceptions --enable-libstdcxx --disable-hosted-libstdcxx "
                + "--disable-bootstrap")
            self._run(f"make -j{build_jobs(self)}")
            self._run(f"make -j{build_jobs(self)} install-strip")

    def build(self):
        rm(self, self.logfile, self.build_folder)
        self.prefix=os.path.join(self.build_folder, "install")

        self._build_binutils()
        self._build_gcc()
        self._build_avrlibc()
        self._build_freestanding()

    def package(self):
        copy(self, "*", os.path.join(self.build_folder, "install"), self.package_folder)

    def package_info(self):
        suffix = ".exe" if self.settings.os == "Windows" else ""
        toolchain = os.path.join(self.package_folder, "bin", "avr")
        self.conf_info.define("tools.build:compiler_executables", {
            "c": f"{toolchain}-gcc{suffix}",
            "cpp": f"{toolchain}-g++{suffix}"
        })
