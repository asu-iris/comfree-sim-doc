# Preliminary: Basic mujoco-warp Usage

This page is a preliminary reference for the original upstream `mujoco_warp` package.
`mujoco-warp` is a Warp-based simulator backend for MuJoCo models, designed for fast GPU-accelerated simulation while keeping a MuJoCo-like workflow (`MjModel`/`MjData` -> `put_model`/`put_data` -> `step`).

## Imports

```python
import mujoco
import warp as wp
import mujoco_warp as mjwarp
```

## Minimal Example

```python
# 1) Load and compile a MuJoCo model
model_path = "benchmark/test_data/primitives.xml"
mjm = mujoco.MjSpec.from_file(model_path).compile()
mjd = mujoco.MjData(mjm)
mujoco.mj_forward(mjm, mjd)

# 2) Move model/data into mujoco-warp
m = mjwarp.put_model(mjm)
d = mjwarp.put_data(mjm, mjd, nworld=1, nconmax=1000, njmax=5000)

# 3) Warm up and capture a graph for fast repeated stepping
mjwarp.step(m, d)
mjwarp.step(m, d)
with wp.ScopedCapture() as capture:
    mjwarp.step(m, d)
graph = capture.graph

# 4) Run steps and sync back to MuJoCo data if needed
for _ in range(100):
    wp.capture_launch(graph)
    wp.synchronize()
    mjwarp.get_data_into(mjd, mjm, d)
```

## Notes

- `put_model` and `put_data` convert MuJoCo structures into Warp-compatible structures.
- `nconmax` and `njmax` control contact/constraint buffer sizes for Warp simulation.
- `mjwarp.get_data_into(...)` is useful when external tools read from `mjd`.
