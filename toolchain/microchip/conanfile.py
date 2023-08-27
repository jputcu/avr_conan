import os
import shutil

from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.layout import basic_layout

class MicrochipAvrGccConan(ConanFile):
    name = "microchipavrgcc"
    version = "3.7.0"
    homepage = "https://www.microchip.com/en-us/tools-resources/develop/microchip-studio/gcc-compilers"
    settings = "os", "arch"
    package_type = "application"
    no_copy_source = True

    def build(self):
        base_url = "https://ww1.microchip.com/downloads/aemDocuments/documents/DEV/ProductDocuments/SoftwareTools/"
        if self.settings.os in ["Linux", "FreeBSD"]:
            # for FreeBSD, install linux_base-c7 and enable linux support
            get(self, base_url + "avr8-gnu-toolchain-3.7.0.1796-linux.any.x86_64.tar.gz", strip_root=True)
        elif self.settings.os == "Windows":
            get(self, base_url + "avr8-gnu-toolchain-3.7.0.1796-win32.any.x86_64.zip", strip_root=True)
        elif self.settings.os == "Macos":
            get(self, base_url + "avr8-gnu-toolchain-osx-3.7.0.518-darwin.any.x86_64.tar.gz", strip_root=True)

    def layout(self):
        basic_layout(self)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_info(self):
        suffix = ".exe" if self.settings.os == "Windows" else ""
        compiler_executables = {
            "c": os.path.join(self.package_folder, "bin", "avr-gcc" + suffix),
            "cpp": os.path.join(self.package_folder, "bin", "avr-g++" + suffix)
        }
        self.conf_info.update("tools.build:compiler_executables", compiler_executables)

