Description
===========
Use conan to provide a C++ toolchain, including standard C++ library.

Provide the toolchain
---------------------

### Microchip

~~~~
> cd toolchain/microchip
> conan create .
...
> cd ../..
~~~~

### Zak Kemble

Alternative toolchain using Zak Kemble:
~~~~
> cd toolchain/zakkemble
> conan create . --version 14.1.0
...
> cd ../..
~~~~

### Optional C++ lib

~~~~
> cd toolchain/avr-libstdcpp
> conan create .
...
> cd ../..
~~~~

### Compile GNU C++ cross compiler from source

~~~~
> cd toolchain/freestanding
> conan create .
...
> cd ../..
~~~~

Provide the conan AVR settings
------------------------------

Install `conan/settings_user.yml` into `~/.conan2/`.

Compile the example project
---------------------------
~~~~
> cd blink
> conan build . -pr:h ../conan/profiles/arduino_uno
...
> conan build . -pr:h ../conan/profiles/arduino_uno -s build_type=Debug
...
~~~~

Advanced editors, like Clion, can use `cmake presets`, now we have:
~~~~
> cmake --list-presets
Available configure presets:

  "conan-atmega328p-minsizerel" - 'conan-atmega328p-minsizerel' config
  "conan-atmega328p-debug"      - 'conan-atmega328p-debug' config
~~~~

~~~~
> conan install . -pr:h ../conan/profiles/arduino_uno
...
> source build/Debug/generators/conanbuildenv-debug-avr.sh
...
> cmake --preset conan-debug
...
> cmake --build --preset conan-debug --verbose
...
> source build/Debug/generators/deactivate_conanbuildenv-debug-avr.sh
Restoring environment
~~~~

~~~~
> file build/Debug/blink.elf
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

