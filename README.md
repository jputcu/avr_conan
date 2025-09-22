Description
===========
Use conan to provide a C++ toolchain, including standard C++ library.

Install toolchain and C++ standard library
------------------------------------------

This repository is origanized to allow it to be used as a local conan index.

~~~~
$ git clone https://github.com/jputcu/avr_conan.git
$ conan remote add avr_center ./avr_conan
$ conan search "*" -r avr_center
Found 4 pkg/version recipes matching * in avr_center
avr_center
  avr-libstdcpp
    avr-libstdcpp/1.0.1
  microchipavrgcc
    microchipavrgcc/3.7.0
  zakkembleavrgcc
    zakkembleavrgcc/13.2.0
    zakkembleavrgcc/15.2.0
~~~~

The correct packages will be installed as dependency by the profile.


### Compile GNU C++ cross compiler from source

~~~~
$ cd toolchain/freestanding
$ conan create .
...
$ cd ../..
~~~~

Provide the conan AVR settings
------------------------------

Install `conan/settings_user.yml` into `~/.conan2/`.

Compile the example project
---------------------------
~~~~
$ cd blink
$ conan build . -pr:h ../conan/profiles/arduino_uno --build missing
...
$ conan build . -pr:h ../conan/profiles/arduino_uno -s build_type=Debug --build missing
...
~~~~

Advanced editors, like Clion, can use `cmake presets`, now we have:
~~~~
$ cmake --list-presets
Available configure presets:

  "conan-atmega328p-minsizerel" - 'conan-atmega328p-minsizerel' config
  "conan-atmega328p-debug"      - 'conan-atmega328p-debug' config
~~~~

~~~~
$ conan install . -pr:h ../conan/profiles/arduino_uno --build missing
...
$ source build/Debug/generators/conanbuildenv-debug-avr.sh
...
$ cmake --preset conan-debug
...
$ cmake --build --preset conan-debug --verbose
...
$ source build/Debug/generators/deactivate_conanbuildenv-debug-avr.sh
Restoring environment
~~~~

~~~~
$ file build/Debug/blink.elf
build/Debug/blink.elf: ELF 32-bit LSB executable, Atmel AVR 8-bit, version 1 (SYSV), statically linked, with debug_info, not stripped
~~~~

Potential
=========

Other compiler
--------------
* Arduino AVR toolchain
* PlatformIO AVR toolchain
* https://github.com/modm-io/avr-gcc
* https://blog.zakkemble.net/avr-gcc-builds/
* Build AVR toolchain from source
* crosstool-ng, more specifically: https://github.com/crosstool-ng/crosstool-ng/issues/2234

Offer HALs
----------
* TODO

AVR friendly libraries
----------------------
* ETL
* ArduinoJson

AVR architecture
----------------
Conan settings have the MCU specified as arch, this means no reuse between other atmegas.
Perhaps we can use the `arch` there.

