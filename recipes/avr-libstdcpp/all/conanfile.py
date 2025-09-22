import os
import shutil

from conan import ConanFile
from conan.tools.files import get, copy

class ZakKembleAvrGccConan(ConanFile):
    name = "avr-libstdcpp"
    version = "1.0.1"
    package_type = "header-library"
    exports_sources = "include/*"
    no_copy_source = True

    def build(self):
        # Add a stdc++ library for AVR
        get(self, "https://github.com/modm-io/avr-libstdcpp/archive/5354296040a2289c911062daa82336762231e897.zip",
            sha256="5c8cc46ea11856c53134ba1f8fb7e710df501cb9b2aeca75ed304762f2c6eb81",
            strip_root=True)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_info(self):
        self.conf_info.append("tools.build:cxxflags", "-I" + os.path.join(self.package_folder, "include"))

