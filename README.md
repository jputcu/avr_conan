Description
===========
AVR development using `conan-2.0.3`.

~~~~
> cd toolchain
> conan create .
> cd ../blink
> conan install . -pr:h ../conan/profiles/avr_profile
...
> source build/Debug/generators/conanbuildenv-debug-avr.sh
...
> cmake --preset conan-debug
...
> cmake --build --preset conan-debug --verbose --target blink
...
> file build/Debug/blink.elf
build/Debug/blink.elf: ELF 32-bit LSB executable, Atmel AVR 8-bit, version 1 (SYSV), statically linked, with debug_info, not stripped
> source build/Debug/generators/deactivate_conanbuildenv-debug-avr.sh
Restoring environment
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

