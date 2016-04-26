cmake_minimum_required(VERSION 3.2)

find_program(PYTHON3 "python3")
include(GNUInstallDirs)

set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
set(SETUP_PY    "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(DEPS        "${CMAKE_CURRENT_SOURCE_DIR}/scripts/dockerlaunchd")
set(OUTPUT      "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")
set(OUTPUT2     "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp2")

set(ETC_LOCATION ${CMAKE_INSTALL_SYSCONFDIR}/dockerlaunch)
set(ETC_FULL_LOCATION ${CMAKE_INSTALL_FULL_SYSCONFDIR}/dockerlaunch)
message(${ETC_FULL_LOCATION})

configure_file(${SETUP_PY_IN} ${SETUP_PY})

add_custom_command(OUTPUT ${OUTPUT}
                   COMMAND ${PYTHON3} ${SETUP_PY} build
                   COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
                   DEPENDS ${DEPS})

add_custom_command(OUTPUT ${OUTPUT2}
                   COMMAND ${PYTHON3} ${SETUP_PY} dockerlaunch_setup
                   COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT2}
                   DEPENDS ${DEPS})

add_custom_target(dockerlaunch ALL DEPENDS ${OUTPUT})
add_custom_target(dockerlaunch_setup DEPENDS ${OUTPUT2})

install(CODE "execute_process(COMMAND ${PYTHON3} ${SETUP_PY} install --prefix=${CMAKE_INSTALL_PREFIX})")
file(GLOB CONFIG_FILES "${CMAKE_CURRENT_SOURCE_DIR}/conf/*")
install(FILES ${CONFIG_FILES} DESTINATION ${ETC_LOCATION} COMPONENT config)
