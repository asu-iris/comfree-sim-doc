# Installation Guide

This guide provides step-by-step instructions to install the ComFree-Warp project and its dependencies.

## Prerequisites

Before installing, ensure you have:
- Python 3.8 or higher
- Git for cloning repositories
- A CUDA-capable GPU (recommended for optimal performance)

## Required Dependencies

The ComFree-Warp project requires the following packages:

1. **MuJoCo**: Physics engine for simulation
2. **Warp**: NVIDIA's framework for GPU-accelerated computing
3. **comfree_warp**: The main project repository

## Installation Methods

### Option 1: Using pip

#### Step 1: Install MuJoCo

```bash
pip install mujoco
```

#### Step 2: Install Warp

```bash
pip install warp-lang
```

#### Step 3: Clone and Install ComFree-Warp

```bash
git clone https://github.com/asu-iris/comfree_warp.git
cd comfree_warp
pip install -e .
```

### Option 2: Using Conda

#### Step 1: Create a Conda Environment

```bash
conda create -n comfree-warp python=3.10
conda activate comfree-warp
```

#### Step 2: Install MuJoCo

```bash
conda install -c conda-forge mujoco
```

#### Step 3: Install Warp

```bash
pip install warp-lang
```

**Note:** Warp-lang is currently available through pip. If conda packages are available for your system, you can attempt `conda install -c nvidia warp-lang`.

#### Step 4: Clone and Install ComFree-Warp

```bash
git clone https://github.com/asu-iris/comfree_warp.git
cd comfree_warp
pip install -e .
```

## Complete Installation Script

### For pip users:

```bash
#!/bin/bash
# Install MuJoCo
pip install mujoco

# Install Warp
pip install warp-lang

# Clone and install ComFree-Warp
git clone https://github.com/asu-iris/comfree_warp.git
cd comfree_warp
pip install -e .

# Verify installation
python -c "import mujoco; import warp as wp; import comfree_warp; print('Installation successful!')"
```

### For Conda users:

```bash
#!/bin/bash
# Create conda environment
conda create -n comfree-warp python=3.10
conda activate comfree-warp

# Install MuJoCo
conda install -c conda-forge mujoco

# Install Warp
pip install warp-lang

# Clone and install ComFree-Warp
git clone https://github.com/asu-iris/comfree_warp.git
cd comfree_warp
pip install -e .

# Verify installation
python -c "import mujoco; import warp as wp; import comfree_warp; print('Installation successful!')"
```

## Verification

After installation, verify that all components are properly installed by running:

```python
import mujoco
import warp as wp
import comfree_warp

print(f"MuJoCo version: {mujoco.__version__}")
print(f"Warp version: {wp.__version__}")
print("All dependencies installed successfully!")
```

## Troubleshooting

### MuJoCo Installation Issues

If you encounter issues with MuJoCo, ensure you have the required system libraries:
- On Ubuntu: `sudo apt-get install libgl1-mesa-glx libxrender1`
- On macOS: Xcode command-line tools may be required

### Warp Installation Issues

Ensure you're using a compatible Python version (3.8+) and that pip is up-to-date:

```bash
pip install --upgrade pip
pip install warp-lang
```

### ComFree-Warp Installation Issues

If cloning fails, verify your Git configuration and SSH/HTTPS credentials:

```bash
git clone https://github.com/asu-iris/comfree_warp.git
```

If the installation fails with `pip install -e .`, ensure you're in the correct directory and have all prerequisites installed.

## Next Steps

Once installation is complete, refer to the [Basic Usage](basic-usage.md) guide to get started with your first simulation.
