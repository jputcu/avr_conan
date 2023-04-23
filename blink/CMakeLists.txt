cmake_minimum_required(VERSION 3.15)
project(blink CXX)

include(${CMAKE_CURRENT_SOURCE_DIR}/../cmake/generic-gcc-avr.cmake)

add_avr_executable(blink src/main.cpp)

install(TARGETS blink DESTINATION "."
        RUNTIME DESTINATION bin
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        )
