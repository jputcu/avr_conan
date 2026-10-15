import os

from conan import ConanFile
from conan.tools.layout import basic_layout

class TestPackageConan(ConanFile):
    settings = "os", "arch"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        basic_layout(self, src_folder="src")

    def build(self):
        src_file = os.path.join(self.source_folder, "main.cpp")
        self.run(f"avr-g++ -mmcu=atmega128 -Os -std=c++23 -o main.elf {src_file}")

    def test(self):
        self.run("avr-size main.elf")
