#pragma once

#include <sycl/sycl.hpp>

#include <fmt/format.h>

#include <string>
#include <utility>

namespace akustik {

inline auto toString(sycl::info::device_type type) -> std::string {
  switch (type) {
    case sycl::info::device_type::cpu: return "CPU";
    case sycl::info::device_type::gpu: return "GPU";
    case sycl::info::device_type::accelerator: return "Accelerator";
    case sycl::info::device_type::custom: return "Custom";
    case sycl::info::device_type::automatic: return "Automatic";
    case sycl::info::device_type::host: return "Host";
    case sycl::info::device_type::all: return "All";
  }

  return "Unkown";
}

inline auto summary(sycl::device dev) -> void {
  auto name         = dev.get_info<sycl::info::device::name>();
  auto vendor       = dev.get_info<sycl::info::device::vendor>();
  auto type         = dev.get_info<sycl::info::device::device_type>();
  auto maxAllocSize = dev.get_info<sycl::info::device::max_mem_alloc_size>();

  fmt::print("----------------------------------------\n");
  fmt::print("Name: {}\n", name.c_str());
  fmt::print("Vendor: {}\n", vendor.c_str());
  fmt::print("Type: {}\n", toString(type).c_str());
  fmt::print("Max alloc size: {} MB\n", maxAllocSize / 1024 / 1024);
  // for (auto groupSize : dev.get_info<sycl::info::device::sub_group_sizes>()) {
  //   fmt::print("Subgroup size: {}\n", groupSize);
  // }
  fmt::print("\n");
}

template<typename Accessor>
[[nodiscard]] auto getPtr(Accessor&& a) -> auto* {
  return std::forward<Accessor>(a)
      .template get_multi_ptr<sycl::access::decorated::no>()
      .get();
}

} // namespace akustik
