# Contact Stiffness and Damping in comfree_warp

`comfree_warp.cf_warp` extends `mjwarp` with extra contact tuning fields.

## Imports

```python
import mujoco
import warp as wp
from comfree_warp import cf_warp as cfwarp
```

## Set Contact Parameters

Use `cfwarp.put_model(...)` and pass `comfree_stiffness` and `comfree_damping`.

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

## Optional: Set Geom Margin in cf_warp

`cfwarp.put_model(...)` also accepts `geom_margin`.

```python
geom_margin_vec = [0.0, 0.1]

m = cfwarp.put_model(
    mjm,
    comfree_stiffness=comfree_stiffness_vec,
    comfree_damping=comfree_damping_vec,
    geom_margin=geom_margin_vec,
)
```

Supported `geom_margin` input forms:

- Scalar: one value for all worlds/geometries
- 1D vector: per-world modulo values, broadcast across all geoms
- 2D array: explicit batched margins with shape `(k, 1)` or `(k, ngeom)`

## Defaults

If not provided:

- `comfree_stiffness` defaults to `100.0`
- `comfree_damping` defaults to `2.0`
