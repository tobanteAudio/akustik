#include "simulation_2d.hpp"

#include "akustik/hdf.hpp"

#include <fmt/format.h>

#include <opencv2/imgproc.hpp>

namespace akustik {

auto loadSimulation2D(
    std::filesystem::path const& path,
    bool exportVideo,
    bool progress
) -> Simulation2D {
  auto file = H5FReader{path.string().c_str()};

  auto const Nx = file.read<int64_t>("Nx");
  auto const Ny = file.read<int64_t>("Ny");

  auto const videoRatio   = static_cast<double>(Ny) / static_cast<double>(Nx);
  auto const videoWidth   = std::min<size_t>(2000, static_cast<size_t>(Nx));
  auto const videoOptions = VideoWriter::Options{
      .file      = path.parent_path() / "out.avi",
      .width     = videoWidth,
      .height    = static_cast<size_t>(videoWidth * videoRatio),
      .fps       = file.read<double>("video_fps"),
      .withColor = false,
  };

  return Simulation2D{
      .file = path,

      .Nx = Nx,
      .Ny = Ny,
      .Nt = file.read<int64_t>("Nt"),

      .in_mask     = file.read<std::vector<uint8_t>>("in_mask"),
      .adj_bn      = file.read<std::vector<int64_t>>("adj_bn"),
      .bn_ixy      = file.read<std::vector<int64_t>>("bn_ixy"),
      .loss_factor = file.read<double>("loss_factor"),

      .inx     = file.read<int64_t>("inx"),
      .iny     = file.read<int64_t>("iny"),
      .src_sig = file.read<std::vector<double>>("src_sig"),

      .out_ixy = file.read<std::vector<int64_t>>("out_ixy"),

      .showProgress = progress,
      .videoOptions = exportVideo ? std::optional{videoOptions} : std::nullopt,
  };
}

auto summary(Simulation2D const& sim) -> void {
  fmt::print("Nt: {}\n", sim.Nt);
  fmt::print("Nx: {}\n", sim.Nx);
  fmt::print("Ny: {}\n", sim.Ny);
  fmt::print("N: {}\n", sim.Nx * sim.Ny);
  fmt::print("inx: {}\n", sim.inx);
  fmt::print("iny: {}\n", sim.iny);
  fmt::print("in_mask: {}\n", sim.in_mask.size());
  fmt::print("bn_ixy: {}\n", sim.bn_ixy.size());
  fmt::print("adj_bn: {}\n", sim.adj_bn.size());
  fmt::print("out_ixy: {}\n", sim.out_ixy.size());
  fmt::print("src_sig: {}\n", sim.src_sig.size());
  fmt::print("loss_factor: {}\n", sim.loss_factor);
}

BackgroundVideoWriter::BackgroundVideoWriter(VideoWriter::Options const& opt)
    : writer{opt}
    , useColor{opt.withColor} {}

auto BackgroundVideoWriter::run(Simulation2D const& sim) -> void {

  auto frame      = std::vector<double>{};
  auto normalized = cv::Mat{};
  auto colored    = cv::Mat{};
  auto rotated    = cv::Mat{};

  while (not done or not queue.empty()) {
    auto shouldSleep = false;
    {
      auto lock   = std::scoped_lock{mutex};
      shouldSleep = queue.empty();
    }

    if (shouldSleep) {
      std::this_thread::sleep_for(std::chrono::milliseconds{10});
      continue;
    }

    {
      auto lock = std::scoped_lock{mutex};
      frame     = queue.front();
      queue.pop();
    }

    if (not useColor) {
      std::ranges::transform(frame, frame.begin(), [](auto v) {
        return std::abs(v);
      });
    }

    auto input = cv::Mat{
        static_cast<int>(sim.Nx),
        static_cast<int>(sim.Ny),
        CV_64F,
        static_cast<void*>(frame.data()),
    };

    cv::normalize(input, normalized, 0, 255, cv::NORM_MINMAX);
    normalized.convertTo(normalized, CV_8U);

    if (useColor) {
      cv::applyColorMap(normalized, colored, cv::COLORMAP_VIRIDIS);
      for (auto ix{0L}; ix < sim.Nx; ++ix) {
        for (auto iy{0L}; iy < sim.Ny; ++iy) {
          if (not sim.in_mask[ix * sim.Ny + iy]) {
            colored.at<cv::Vec3b>(ix, iy) = cv::Vec3b(255, 255, 255);
          }
        }
      }
    } else {
      colored = normalized;
      for (auto ix{0L}; ix < sim.Nx; ++ix) {
        for (auto iy{0L}; iy < sim.Ny; ++iy) {
          if (not sim.in_mask[ix * sim.Ny + iy]) {
            colored.at<uint8_t>(ix, iy) = 255;
          }
        }
      }
    }

    cv::rotate(colored, rotated, cv::ROTATE_90_COUNTERCLOCKWISE);

    writer.write(rotated);
  }
}

auto BackgroundVideoWriter::push(std::vector<double> frame) -> void {
  while (true) {
    auto const wait = [&] {
      auto lock = std::scoped_lock{mutex};
      return queue.size() > 10;
    }();

    if (wait) {
      std::this_thread::sleep_for(std::chrono::milliseconds{10});
    } else {
      break;
    }
  }

  {
    auto lock = std::scoped_lock{mutex};
    queue.push(std::move(frame));
  }
}

auto BackgroundVideoWriter::finish() -> void { done.store(true); }

} // namespace akustik
