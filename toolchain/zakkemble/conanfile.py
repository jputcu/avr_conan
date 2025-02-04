import os
import shutil

from conan import ConanFile
from conan.tools.files import get, copy
from conan.tools.layout import basic_layout

class ZakKembleAvrGccConan(ConanFile):
    name = "zakkembleavrgcc"
    settings = "os", "arch"
    package_type = "application"
    no_copy_source = True

    def build(self):
        get(self, self.conan_data["sources"][self.version][str(self.settings.os).lower()]['url'], strip_root=True)
        # Add a stdc++ library for AVR
        get(self, "https://github.com/modm-io/avr-libstdcpp/archive/123a0d7.zip", destination='avr-libstdcpp', strip_root=True)

    def layout(self):
        basic_layout(self)

    def package(self):
        copy(self, "*", self.build_folder, self.package_folder)

    def package_info(self):
        suffix = ".exe" if self.settings.os == "Windows" else ""
        toolchain = os.path.join(self.package_folder, "bin", "avr")
        self.conf_info.define("tools.build:compiler_executables", {
            "c": f"{toolchain}-gcc{suffix}",
            "cpp": f"{toolchain}-g++{suffix}"
        })
        self.conf_info.append("tools.build:cxxflags", "-I" + os.path.join(self.package_folder, "avr-libstdcpp", "include"))

