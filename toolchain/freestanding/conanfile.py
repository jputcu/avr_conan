import os
from io import StringIO
from conan.tools.files import get, copy, mkdir, chdir
from conan.tools.layout import basic_layout
from conan.tools.gnu import AutotoolsToolchain, Autotools
from conan import ConanFile

class AvrGccConan(ConanFile):
    name = "avr-gcc"
    version = "14.2.0"
    settings = "os", "arch"
    no_copy_source = True
    package_type = "application"

    def layout(self):
        basic_layout(self)

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

    def generate(self):
        at = AutotoolsToolchain(self, prefix=os.path.join(self.build_folder, "install"))
        at.configure_args.append("--disable-doc")
        env = at.environment()
        env.prepend_path("PATH", os.path.join(self.build_folder, "install", "bin"))
        at.generate(env)

    def _build_binutils(self):
        self.output.info("Building binutils")
        mkdir(self, "binutils")
        with chdir(self, "binutils"):
            at = Autotools(self)
            at.configure(build_script_folder=os.path.join(self.source_folder, "binutils"),
                                args=["--target=avr", "--disable-sim", "--disable-nls"])
            at.make()
            #at.install(args=[f"DESTDIR={os.path.join(self.build_folder, 'install')}"])
            self.run("make install")

    def _build_gcc(self):
        self.output.info("Building gcc 1st stage")
        mkdir(self, "gcc")
        with chdir(self, "gcc"):
            at = Autotools(self)
            at.configure(build_script_folder=os.path.join(self.source_folder, "gcc"),
                                args=["--target=avr", "--enable-languages=c,c++", "--disable-libssp",
                                      "--disable-libada", "--disable-libgomp", "--with-avrlibc=yes",
                                      "--with-dwarf2", "--disable-shared", "--disable-nls"])
            at.make()
            #at.install(args=[f"DESTDIR={os.path.join(self.build_folder, 'install')}"])
            self.run("make install")

    def _build_avrlibc(self):
        self.output.info("Building avr-libc")
        build_str = StringIO()
        self.run(os.path.join(self.source_folder, "avr-libc", "config.guess"), build_str)
        mkdir(self, "avr-libc")
        with chdir(self, "avr-libc"):
            at = Autotools(self)
            at.configure(build_script_folder=os.path.join(self.source_folder, "avr-libc"),
                                args=["--host=avr", f"--build={build_str.getvalue()}"])
            at.make()
            #at.install(args=[f"DESTDIR={os.path.join(self.build_folder, 'install')}"])
            self.run("make install")

    def _build_freestanding(self):
        self.output.info("Building gcc final stage")
        with chdir(self, "gcc"):
            at = Autotools(self)
            at.configure(build_script_folder=os.path.join(self.source_folder, "gcc"),
                                args=["--target=avr", "--enable-languages=c,c++", "--disable-libssp",
                                      "--disable-libada", "--disable-libgomp", "--with-avrlibc=yes",
                                      "--with-newlib", "--with-dwarf2", "--disable-__cxa_atexit",
                                      "--disable-threads", "--disable-shared", "--disable-sjlj-exceptions",
                                      "--enable-libstdcxx", "--disable-hosted-libstdcxx", "--disable-bootstrap",
                                      "--disable-nls"])
            at.make()
            self.run("make install")

    def build(self):
        self._build_binutils()
        self._build_gcc()
        self._build_avrlibc()
        self._build_freestanding()

    def package(self):
        copy(self, pattern="*", src=os.path.join(self.build_folder, "install"), dst=self.package_folder)

    def package_info(self):
        suffix = ".exe" if self.settings.os == "Windows" else ""
        toolchain = os.path.join(self.package_folder, "bin", "avr")
        self.conf_info.define("tools.build:compiler_executables", {
            "c": f"{toolchain}-gcc{suffix}",
            "cpp": f"{toolchain}-g++{suffix}"
        })
