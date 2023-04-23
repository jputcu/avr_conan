
function(add_avr_executable EXECUTABLE_NAME)
    if (NOT ARGN)
        message(FATAL_ERROR "No source files given for ${EXECUTABLE_NAME}.")
    endif (NOT ARGN)

    set(elf_file ${CMAKE_BINARY_DIR}/${EXECUTABLE_NAME}.elf)
    set(hex_file ${CMAKE_BINARY_DIR}/${EXECUTABLE_NAME}.hex)

    add_executable(${EXECUTABLE_NAME} EXCLUDE_FROM_ALL ${ARGN})
    set_target_properties(
            ${EXECUTABLE_NAME}
            PROPERTIES
            RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}
            SUFFIX ".elf"
    )

    add_custom_command(
            OUTPUT ${hex_file}
            COMMAND
            ${CMAKE_OBJCOPY} -R .eeprom -R .fuse -R .lock -R .signature -R .user_signatures -O ihex ${elf_file} ${hex_file}
            DEPENDS ${EXECUTABLE_NAME}
    )

endfunction(add_avr_executable)
