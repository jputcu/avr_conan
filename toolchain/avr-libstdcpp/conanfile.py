import os
import shutil

from conan import ConanFile
from conan.tools.files import get, copy

class ZakKembleAvrGccConan(ConanFile):
    name = "avr-libstdcpp"
    version = "1.0.0"
    package_type = "header-library"
    exports_sources = "include/*"
    no_copy_source = True

    def build(self):
        # Add a stdc++ library for AVR
        get(self, "https://github.com/modm-io/avr-libstdcpp/archive/123a0d7.zip",
            sha256="03f2ba6fe6d922144ff0a154fa4c774ef0992de12b97f46235843c12c74d4154",
            strip_root=True)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_info(self):
        self.conf_info.append("tools.build:cxxflags", "-I" + os.path.join(self.package_folder, "include"))

