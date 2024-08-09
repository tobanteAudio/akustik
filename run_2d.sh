#!/bin/sh

set -e
root_dir="$(cd "$(dirname "$0")" && pwd)"

build_dir=build
python_dir="$root_dir/src/python"
engine_exe="$root_dir/$build_dir/src/cpp/engine/akustik-engine"

sim_name="Diffusor"
sim_dir="$root_dir/data/sim_data/$sim_name/cpu"

fmax=2500
duration=0.050

# Don't use hyperthreads, a lot slower
DPCPP_CPU_CU_AFFINITY=spread
DPCPP_CPU_NUM_CUS=16
DPCPP_CPU_PLACES=cores

# Delete old sim
rm -rf "$sim_dir"

# Generate model & run engine
akustik --verbose wave sim2d --duration="$duration" --engine_exe="$engine_exe" --fmax="$fmax" --save --sim_dir="$sim_dir"

# Report
akustik wave report2d --sim_dir="$sim_dir"
