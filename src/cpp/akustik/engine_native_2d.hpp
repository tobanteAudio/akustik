#pragma once

#include "akustik/mdspan.hpp"
#include "akustik/simulation_2d.hpp"

#include <cstddef>

namespace akustik {

struct EngineNative2D {
  [[nodiscard]] auto operator()(Simulation2D const& sim
  ) const -> stdex::mdarray<double, stdex::dextents<size_t, 2>>;
};

} // namespace akustik
