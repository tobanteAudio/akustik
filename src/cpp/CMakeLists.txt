project(akustik)

add_library(akustik)
add_library(akustik::akustik ALIAS akustik)
target_include_directories(akustik PUBLIC ${PROJECT_SOURCE_DIR})
target_compile_definitions(akustik PUBLIC PRECISION=2)

target_link_libraries(akustik
    PUBLIC
        fmt::fmt
        HDF5::HDF5
        opencv_videoio
        std::mdspan
        TBB::tbb
)

target_sources(akustik
    PRIVATE
        akustik/engine_native_2d.cpp
        akustik/engine_native_2d.hpp
        akustik/exception.hpp
        akustik/hdf.hpp
        akustik/mdspan.hpp
        akustik/simulation_2d.cpp
        akustik/simulation_2d.hpp
        akustik/sycl.hpp
        akustik/video.cpp
        akustik/video.hpp
)

if(AKUSTIK_ENABLE_ACPP_SYCL OR AKUSTIK_ENABLE_INTEL_SYCL)
    target_sources(akustik PRIVATE akustik/engine_sycl_2d.cpp)
    add_sycl_to_target(TARGET akustik SOURCES akustik/engine_sycl_2d.cpp)
    target_compile_definitions(akustik PUBLIC AKUSTIK_HAS_SYCL=1)
endif()
