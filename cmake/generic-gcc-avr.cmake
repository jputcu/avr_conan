
function(add_avr_executable EXECUTABLE_NAME)
    if (NOT ARGN)
        message(FATAL_ERROR "No source files given for ${EXECUTABLE_NAME}.")
    endif (NOT ARGN)

    set(elf_file ${EXECUTABLE_NAME}.elf)
    set(hex_file ${EXECUTABLE_NAME}.hex)

    add_executable(${EXECUTABLE_NAME} ${ARGN})
    set_target_properties(
            ${EXECUTABLE_NAME}
            PROPERTIES
            SUFFIX ".elf"
    )

    add_custom_command(
      TARGET ${EXECUTABLE_NAME}
          POST_BUILD
          COMMAND ${CMAKE_OBJCOPY} -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures -O ihex ${elf_file} ${hex_file}
          BYPRODUCTS ${hex_file}
    )

endfunction(add_avr_executable)
