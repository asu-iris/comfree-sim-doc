# ComFree-Warp Basic Usage

ComFree-Warp extends the base mujoco-warp package with ComFree (Compliant Friction Everywhere) physics simulation on GPU. This page provides a reference for using the ComFree-Warp API.

## Imports

```python
import numpy as np
import warp as wp
import comfree_warp as cf_warp
```

## Minimal Example

```python
import mujoco
import comfree_warp as cf_warp
import warp as wp

# 1) Load and compile a MuJoCo model
model_path = "path/to/your/model.xml"
mjm = mujoco.MjSpec.from_file(model_path).compile()
mjd = mujoco.MjData(mjm)
mujoco.mj_forward(mjm, mjd)

# 2) Move model/data into ComFree-Warp with comfree parameters
m = cf_warp.put_model(mjm, comfree_stiffness=0.1, comfree_damping=0.001)
d = cf_warp.put_data(mjm, mjd, nworld=1, nconmax=1000, njmax=5000)

# 3) Warm up and capture a graph for fast repeated stepping
cf_warp.step(m, d)
cf_warp.step(m, d)
with wp.ScopedCapture() as capture:
    cf_warp.step(m, d)
graph = capture.graph

# 4) Run simulation steps and sync back to MuJoCo data if needed
for i in range(1000):
    wp.capture_launch(graph)
    wp.synchronize()
    cf_warp.get_data_into(mjd, mjm, d)
    
    # Access simulation state
    print(f"Step {i}: qpos = {d.qpos}")
```

## Core Functions

### Model Conversion

#### `put_model(mjspec, comfree_stiffness=0.1, comfree_damping=0.001, ...)`

Converts a compiled MuJoCo model specification into a ComFree-Warp GPU model.

**Parameters:**
- `mjspec`: Compiled MuJoCo model specification
- `comfree_stiffness`: Stiffness parameter for ComFree constraints (default: 0.1)
- `comfree_damping`: Damping parameter for ComFree constraints (default: 0.001)
- Additional parameters passed to underlying mujoco-warp

**Returns:** GPU-accelerated ComFree-Warp model

### Data Conversion

#### `put_data(mjspec, mjdata, nworld=1, nconmax=1000, njmax=5000, ...)`

Converts MuJoCo data arrays into ComFree-Warp GPU tensors.

**Parameters:**
- `mjspec`: MuJoCo model specification
- `mjdata`: MuJoCo data object
- `nworld`: Number of simulation worlds (for batched simulations)
- `nconmax`: Maximum number of contacts
- `njmax`: Maximum number of constraints
- Additional parameters passed to underlying mujoco-warp

**Returns:** GPU-accelerated ComFree-Warp data object with ComFree fields

#### `make_data(mjspec, nworld=1, nconmax=1000, njmax=5000, ...)`

Creates new ComFree-Warp data from scratch without converting existing MuJoCo data.

**Returns:** GPU-accelerated ComFree-Warp data object

#### `get_data_into(mjdata, mjspec, warp_data)`

Synchronizes ComFree-Warp GPU data back to MuJoCo CPU arrays.

**Parameters:**
- `mjdata`: Target MuJoCo data object to fill
- `mjspec`: MuJoCo model specification
- `warp_data`: ComFree-Warp GPU data object

**Returns:** Updated MuJoCo data object

### Reset

#### `reset_data(mjspec, warp_data)`

Resets the simulation state to initial conditions.

**Parameters:**
- `mjspec`: MuJoCo model specification
- `warp_data`: ComFree-Warp data object to reset

## Simulation Functions

### `step(model, data)`

Performs a single ComFree physics simulation step.

**Parameters:**
- `model`: ComFree-Warp GPU model (from `put_model`)
- `data`: ComFree-Warp GPU data (from `put_data` or `make_data`)

### `forward(model, data)`

Runs forward kinematics and constraint computations without integration.

**Parameters:**
- `model`: ComFree-Warp GPU model
- `data`: ComFree-Warp GPU data

## Advanced Example: Batch Simulation

```python
import mujoco
import comfree_warp as cf_warp
import warp as wp

# Load model
mjm = mujoco.MjSpec.from_file("model.xml").compile()

# Create ComFree-Warp model with custom parameters
m = cf_warp.put_model(mjm, comfree_stiffness=0.2, comfree_damping=0.002)

# Create multiple simulation worlds
nworlds = 4
d = cf_warp.make_data(mjm, nworld=nworlds, nconmax=2000, njmax=10000)

# Capture computation graph for fast execution
cf_warp.step(m, d)
cf_warp.step(m, d)
with wp.ScopedCapture() as capture:
    cf_warp.step(m, d)
graph = capture.graph

# Run batch simulation
num_steps = 500
for step_idx in range(num_steps):
    wp.capture_launch(graph)
    wp.synchronize()
    
    # Periodically sync back to CPU for analysis
    if step_idx % 100 == 0:
        cf_warp.get_data_into(mjd, mjm, d)
        print(f"Step {step_idx}: min_qpos={d.qpos.numpy().min()}, max_qpos={d.qpos.numpy().max()}")
```

## Notes

- ComFree-Warp parameters (`comfree_stiffness` and `comfree_damping`) control the compliance behavior. Higher stiffness means stiffer constraints, higher damping means more energy dissipation.
- Use `wp.ScopedCapture()` to capture the computation graph and reuse it for many steps, improving performance.
- Call `wp.synchronize()` after `wp.capture_launch()` to ensure GPU operations complete before reading data.
- Use `cf_warp.get_data_into()` sparingly as it transfers data from GPU to CPU, which is slow. Only sync when you need to inspect or modify state.
- For best performance, keep simulations on GPU and avoid frequent CPU-GPU synchronization.
