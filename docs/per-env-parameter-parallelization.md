# Per-Env Parameter Parallelization

`comfree_warp.cf_warp` supports per-environment parameter bucketization in multi-world simulation.
The same modulo mapping pattern can be used for parameters that are stored as world-bucketed vectors.

Currently, this page documents the contact-parameter case.

## Imports

```python
import mujoco
import warp as wp
from comfree_warp import cf_warp as cfwarp
```

## Contact Parameters

### Set Contact Parameters

Use `cfwarp.put_model(...)` and pass `comfree_stiffness` and `comfree_damping`.

- `comfree_stiffness`: controls contact spring stiffness. Higher values generally make contacts resist penetration more strongly.
- `comfree_damping`: controls contact damping. Higher values generally add more dissipation and reduce oscillation/bounce.

Both parameters accept either a scalar (single value for all contacts) or a vector (for per-mode/per-bucket tuning used by this solver).

## Bucket Parallelization (Modulo Mapping)

In multi-world simulation, the solver selects the parameter bucket with a modulo rule:

`bucket_id = world_id % k`

- `world_id` is the simulated world index (`0..nworld-1`)
- `k` is the vector length of `comfree_stiffness` (or `comfree_damping`)

This means values are reused cyclically across worlds.

### Case A: Scalar (or length 1)

If you pass a scalar like `100.0`, it is treated as length `k=1`.
All worlds use the same value because `world_id % 1 == 0`.

### Case B: Vector length equals `nworld`

If `k == nworld`, each world gets its own bucket with a 1-to-1 mapping.

Example with `nworld=4`, `k=4`:

- world 0 -> bucket 0
- world 1 -> bucket 1
- world 2 -> bucket 2
- world 3 -> bucket 3

### Case C: Vector shorter than `nworld`

If `k < nworld`, buckets repeat periodically.

Example with `nworld=8`, `k=3`:

- world 0 -> bucket 0
- world 1 -> bucket 1
- world 2 -> bucket 2
- world 3 -> bucket 0
- world 4 -> bucket 1
- world 5 -> bucket 2
- world 6 -> bucket 0
- world 7 -> bucket 1

### Case D: Vector longer than `nworld`

If `k > nworld`, only the first `nworld` buckets are used in that run.
Extra tail buckets are valid but unused unless `nworld` increases.

Practical recommendation: use `k=1` for globally shared contact behavior, and use `k=nworld` when you want per-world tuning for ablation or parameter sweeps.

```python
model_path = "benchmark/test_data/primitives.xml"
mjm = mujoco.MjSpec.from_file(model_path).compile()
mjd = mujoco.MjData(mjm)
mujoco.mj_forward(mjm, mjd)

# Example vectors used in this repository
comfree_stiffness_vec = [100.0, 50.0, 50.0, 50.0, 50.0]
comfree_damping_vec = [2.0, 2.0, 2.0, 2.0, 0.0]

m = cfwarp.put_model(
    mjm,
    comfree_stiffness=comfree_stiffness_vec,
    comfree_damping=comfree_damping_vec,
)
d = cfwarp.put_data(mjm, mjd, nworld=1, nconmax=1000, njmax=5000)

cfwarp.step(m, d)
```

## Defaults

If not provided:

- `comfree_stiffness` defaults to `100.0`
- `comfree_damping` defaults to `2.0`
