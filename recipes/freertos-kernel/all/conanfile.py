import os

from conan import ConanFile
from conan.tools.files import copy, get, save


class FreeRtosKernelConan(ConanFile):
    name = "freertos-kernel"
    description = "The FreeRTOS kernel as sources: the application builds it with its own FreeRTOSConfig.h and port"
    license = "MIT"
    homepage = "https://github.com/FreeRTOS/FreeRTOS-Kernel"
    package_type = "header-library"  # nothing is compiled here, see package_info()
    no_copy_source = True

    def source(self):
        # url and sha256: a download that changed upstream fails instead of slipping in
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package(self):
        copy(self, "*", self.source_folder, os.path.join(self.package_folder, "kernel"))
        save(self, os.path.join(self.package_folder, "cmake", "freertos-kernel-path.cmake"),
             'set(FREERTOS_KERNEL_PATH "${CMAKE_CURRENT_LIST_DIR}/../kernel")\n')

    def package_id(self):
        self.info.clear()  # the same sources for every board and host

    def package_info(self):
        # The consumer's CMake builds the kernel with add_subdirectory(${FREERTOS_KERNEL_PATH} ...)
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
        self.cpp_info.builddirs = ["cmake"]
        self.cpp_info.set_property("cmake_build_modules", [os.path.join("cmake", "freertos-kernel-path.cmake")])
