cmake_minimum_required(VERSION 3.15)
project(blink CXX)

if(CMAKE_SYSTEM_PROCESSOR STREQUAL "avr")
  include(${CMAKE_CURRENT_SOURCE_DIR}/../cmake/generic-gcc-avr.cmake)
  add_avr_executable(blink src/main.cpp)
else()
  add_executable(blink src/main.cpp)
endif()

target_compile_options(blink PRIVATE -Wall -Wextra)

install(TARGETS blink DESTINATION "."
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )
