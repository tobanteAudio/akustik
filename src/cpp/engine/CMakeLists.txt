project(akustik-engine)

add_executable(akustik-engine main.cpp)
target_link_libraries(akustik-engine PRIVATE CLI11::CLI11 akustik::akustik)
target_compile_options(akustik-engine PRIVATE -Wall -Wextra -Wpedantic)
