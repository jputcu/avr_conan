import os
from conan.tools.files import get, copy, mkdir, rmdir, chdir
from conan.tools.build import build_jobs
from conan import ConanFile

class AvrGccConan(ConanFile):
    name = "avr-gcc"
    version = "14.2.0"
    settings = "os", "arch"
    no_copy_source = True
    gcc_src = os.path.join("src","gcc")
    binutils_src = os.path.join("src","binutils")
    avrlibc_src = os.path.join("src","avr-libc")

    def source(self):
        get(self, "https://ftp.gnu.org/gnu/gcc/gcc-14.2.0/gcc-14.2.0.tar.xz", destination=self.gcc_src, strip_root=True)
        get(self, "https://ftp.gnu.org/gnu/binutils/binutils-2.44.tar.xz", destination=self.binutils_src, strip_root=True)
        get(self, "https://github.com/avrdudes/avr-libc/releases/download/avr-libc-2_2_1-release/avr-libc-2.2.1.tar.bz2", destination=self.avrlibc_src, strip_root=True)
        with chdir(self, self.gcc_src):
            self.run("bash ./contrib/download_prerequisites")
        with chdir(self, self.avrlibc_src):
            self.run("bash ./bootstrap")

    def _build_binutils(self):
        config_file = os.path.relpath(os.path.join(self.source_folder, self.binutils_src, "configure"), "build/binutils")
        mkdir(self, "build/binutils")
        with chdir(self, "build/binutils"):
            self.run(f"bash {config_file} --prefix={self.prefix} --target=avr --disable-nls --disable-doc")
            self.run(f"make -s -j{build_jobs(self)}")
            self.run("make -s install")
        rmdir(self, "build/binutils")

    def _build_gcc(self):
        config_file = os.path.relpath(os.path.join(self.source_folder, self.gcc_src, "configure"), "build/gcc")
        mkdir(self, "build/gcc")
        with chdir(self, "build/gcc"):
            self.run(f"bash {config_file} --prefix={self.prefix} "
                + "--target=avr --enable-languages=c,c++ --disable-nls --disable-libssp "
                + "--disable-libada --disable-libgomp --disable-doc --with-avrlibc=yes --with-dwarf2 --disable-shared")
            self.run(f"make -s -j{build_jobs(self)}")
            self.run("make -s install")

    def _build_avrlibc(self):
        config_file = os.path.relpath(os.path.join(self.source_folder, self.avrlibc_src, "configure"), "build/avr-libc")
        mkdir(self, "build/avr-libc")
        with chdir(self, "build/avr-libc"):
            self.run(f"bash {config_file} --prefix={self.prefix} "
                + "--host=avr --build=`../../{self.avrlibc_src}/config.guess` --disable-doc")
            self.run(f"make -s -j{build_jobs(self)}")
            self.run("make -s install")

    def _build_freestanding(self):
        config_file = os.path.relpath(os.path.join(self.source_folder, self.gcc_src, "configure"), "build/gcc")
        with chdir(self, "build/gcc"):
            self.run(f"bash {config_file} --prefix={self.prefix} "
                + "--target=avr --enable-languages=c,c++ --disable-nls --disable-libssp --disable-libada "
                + "--disable-libgomp --disable-doc --with-avrlibc=yes --with-newlib --with-dwarf2 --disable-__cxa_atexit "
                + "--disable-threads --disable-shared --disable-sjlj-exceptions --enable-libstdcxx --disable-hosted-libstdcxx "
                + "--disable-bootstrap")
            self.run(f"make -s -j{build_jobs(self)}")
            self.run("make -s install")

    def build(self):
        self.prefix=os.path.join(self.build_folder, "install")
        mkdir(self, "install")
        mkdir(self, "build")

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
