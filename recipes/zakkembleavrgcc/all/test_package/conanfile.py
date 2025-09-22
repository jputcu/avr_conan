import os

from conan import ConanFile
from conan.tools.layout import basic_layout
from conan.tools.build import can_run

class helloTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def build(self):
        src_file=os.path.join(self.source_folder, "main.cpp")
        self.run(f"avr-g++ -o main.elf {src_file}", env="conanrun")

    def layout(self):
        basic_layout(self, src_folder="src")

    def test(self):
        pass

