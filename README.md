# 3D Model Rotation to GIF Converter - Updated Documentation

## Overview

Advanced Python script to load OBJ 3D models, rotate them on arbitrary axes, and export smooth animations as GIF files. Perfect for scientific visualization, product presentations, and 3D model documentation.

## ✨ Key Features

✓ **Flexible model loading** - Load complex OBJ files with millions of vertices  
✓ **Optional textures** - Apply PNG/JPG textures to your model  
✓ **Standard axes support** - Rotate around X, Y, or Z axis  
✓ **Arbitrary axis rotation** - Specify custom rotation axes as 3D vectors  
✓ **Customizable animation** - Control frame count and playback speed  
✓ **Professional output** - Clean white background, no visual clutter  
✓ **Automatic cleanup** - Temporary files removed automatically  
✓ **Progress reporting** - Real-time generation status  

## Requirements

- Python 3.7+
- Dependencies: `trimesh`, `numpy`, `matplotlib`, `pillow`

## Installation

### One-Time Setup

```bash
# Navigate to script directory
cd "/Users/gianthk/Library/CloudStorage/GoogleDrive-gianthk.iori@gmail.com/My Drive/ETH/HES-SO_terracotta/Results/kiri/3D_MODELS_BEST_TO_VIEW_IN_WINDOS_3D_VIEWER_OR_MESHLAB_OR_BLENDER"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install trimesh numpy matplotlib pillow
```

### Every Time You Run

```bash
source venv/bin/activate
```

## Usage

### Basic Command Structure

```bash
python3 rotate_model_to_gif.py [OPTIONS]
```

### Command-Line Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--obj PATH` | str | `3DModel_1/OBJ/3DModel.obj` | Path to OBJ file (relative to script) |
| `--texture PATH` | str | _(none)_ | Path to texture file (PNG/JPG). Optional. |
| `--output PATH` | str | `3DModel_1/model_rotation.gif` | Output GIF file path |
| `--axis AXIS` | str | `z` | Rotation axis. See axis formats below. |
| `--frames N` | int | `36` | Number of rotation frames (higher = smoother) |
| `--fps N` | int | `10` | Playback speed in frames per second |

### Rotation Axis Formats

The `--axis` parameter accepts multiple formats:

#### Standard Axes (Recommended for simple rotations)
```bash
--axis x          # Rotate around X axis (1, 0, 0)
--axis y          # Rotate around Y axis (0, 1, 0)
--axis z          # Rotate around Z axis (0, 0, 1) [DEFAULT]
```

#### Arbitrary Axis Vectors (Normalized automatically)
```bash
--axis 1,1,1              # Diagonal axis (normalized to 0.577, 0.577, 0.577)
--axis 0.7,0.5,0.5        # Custom mixed axis (normalized)
--axis 1,0,0              # Equivalent to --axis x
--axis 0,0.5,0.866        # 30° from Z axis in XZ plane
```

## Examples

### Example 1: Default Settings (Z-axis, 36 frames, 10 fps)
```bash
python3 rotate_model_to_gif.py
# Output: 3DModel_1/model_rotation.gif
```

### Example 2: Rotate Around Y-Axis
```bash
python3 rotate_model_to_gif.py --axis y
# Output: 3DModel_1/model_rotation.gif
```

### Example 3: Apply Texture File
```bash
python3 rotate_model_to_gif.py \
  --texture 3DModel_1/OBJ/3DModel/baked_mesh_239e0824_tex0.png \
  --output 3DModel_1/with_texture.gif
```

### Example 4: Smooth Animation (60 frames at 20 fps)
```bash
python3 rotate_model_to_gif.py \
  --frames 60 \
  --fps 20 \
  --output 3DModel_1/smooth_animation.gif
```

### Example 5: Diagonal Rotation
```bash
python3 rotate_model_to_gif.py \
  --axis 1,1,1 \
  --frames 36 \
  --fps 15 \
  --output 3DModel_1/diagonal_spin.gif
```

### Example 6: Complex Custom Axis
```bash
python3 rotate_model_to_gif.py \
  --axis 0.7,0.5,0.5 \
  --frames 48 \
  --fps 20 \
  --output 3DModel_1/custom_rotation.gif
```

### Example 7: Different Model (3DModel_2)
```bash
python3 rotate_model_to_gif.py \
  --obj 3DModel_2/OBJ/3DModel.obj \
  --texture 3DModel_2/OBJ/3DModel/baked_mesh_4aa3f029_tex0.png \
  --output 3DModel_2/animation.gif \
  --frames 36 \
  --fps 12
```

### Example 8: Fast Preview
```bash
python3 rotate_model_to_gif.py --frames 24 --fps 10
# Quick generation, smaller file
```

### Example 9: Professional Quality
```bash
python3 rotate_model_to_gif.py \
  --frames 72 \
  --fps 24 \
  --output 3DModel_1/professional.gif
```

## Understanding Axis Vectors

### Axis Vector Basics

A rotation axis is a 3D vector `[x, y, z]` that specifies the direction of rotation:

- **X-axis**: `[1, 0, 0]` - Spin around left-right direction
- **Y-axis**: `[0, 1, 0]` - Spin around up-down direction
- **Z-axis**: `[0, 0, 1]` - Spin around front-back direction (default)

### Custom Axis Vectors

You can specify any direction as a 3D vector. The script automatically normalizes it:

```
Input: --axis 2,2,2
Normalized to: [0.577, 0.577, 0.577] (diagonal through origin)

Input: --axis 1,0,0
Normalized to: [1.0, 0.0, 0.0] (same as --axis x)

Input: --axis 3,4,0
Normalized to: [0.6, 0.8, 0.0] (60° rotation from vertical)
```

### Finding Useful Axis Vectors

**Common axes:**
- `0,1,0` - Vertical spin (like a carousel)
- `1,0,0` - Forward roll (like a wheel)
- `0,0,1` - Horizontal rotation (default, like a turntable)

**Diagonal rotations:**
- `1,1,1` - Diagonal through all three axes (45° from each)
- `1,1,0` - 45° between X and Y, no Z tilt
- `1,0,1` - 45° between X and Z, no Y tilt

**Tilted rotations:**
- `0.7,0.5,0.5` - Mostly X rotation, mixed Y and Z
- `1,0.5,0` - Mix of X and Y rotation, no Z
- `0,1,0.5` - Mostly Y rotation, some Z

## Output Information

The script displays:

```
============================================================
3D Model Rotation to GIF Converter
============================================================
Model: 3DModel_1/OBJ/3DModel.obj
Texture: 3DModel_1/OBJ/3DModel/baked_mesh_239e0824_tex0.png
Rotation axis: 1,1,1
Frames: 36
FPS: 15
Output: 3DModel_1/rotation_diagonal.gif
============================================================

Loading model from: .../3DModel.obj
Model loaded successfully!
  Vertices: 14452
  Faces: 25000

Loading texture from: .../baked_mesh_239e0824_tex0.png
  Loaded texture: baked_mesh_239e0824_tex0.png

Generating 36 rotation frames around axis [0.577, 0.577, 0.577]...
  Generated 6/36 frames
  ...
  Generated 36/36 frames

Creating animated GIF...
GIF saved to: .../model_rotation.gif
GIF size: 0.83 MB
Animation: 36 frames at 15 fps

Cleaning up temporary files...

✓ Done!
```

## Performance Tips

### File Size Optimization
- **Reduce frames**: Use 24-30 instead of 60 for smaller files
- **Lower fps**: Use 8-10 instead of 20 for smaller files
- **Result**: Typical size 0.4-1.5 MB

### Smoother Animation
- **More frames**: Use 60-72 for very smooth rotation
- **Higher fps**: Use 20-24 for fast playback
- **Result**: 1.5-3 MB files

### Quick Preview
```bash
python3 rotate_model_to_gif.py --frames 20 --fps 10
# Generates in ~30 seconds, 0.4 MB output
```

### Professional Quality
```bash
python3 rotate_model_to_gif.py --frames 72 --fps 24
# Generates in ~2 minutes, 2-3 MB output
```

## Troubleshooting

### "Module not found" error
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies if needed
pip install trimesh numpy matplotlib pillow
```

### "OBJ file not found" error
```bash
# Check file path relative to script location
ls 3DModel_1/OBJ/3DModel.obj
```

### "Texture file not found" error
```bash
# Verify texture file exists
ls 3DModel_1/OBJ/3DModel/*.png
# Or omit --texture to skip texture
python3 rotate_model_to_gif.py
```

### Large output file (3+ MB)
```bash
# Reduce frames or fps
python3 rotate_model_to_gif.py --frames 30 --fps 10
```

### Invalid axis vector error
```bash
# Ensure comma-separated values, no spaces after commas
--axis 1,1,1        # ✓ Correct
--axis 1, 1, 1      # ✗ Wrong (spaces)
--axis 1 1 1        # ✗ Wrong (spaces instead of commas)
```

## Technical Details

### Rendering
- **Library**: matplotlib 3D visualization
- **Figure size**: 8×8 inches at 100 DPI
- **Background**: Pure white (RGB 255,255,255)
- **No visual elements**: Axes, grids, panes all hidden

### Model Processing
- **Mesh library**: trimesh (handles millions of vertices)
- **Automatic scaling**: Model centered and uniformly scaled
- **Rotation method**: Quaternion-based transformation matrices

### Texture Handling
- **Formats supported**: PNG, JPG, JPEG
- **Detection**: Automatic when file provided
- **Fallback**: Default blue color if texture not found
- **Path**: Can be relative (to script) or absolute

### Output Format
- **GIF type**: Animated, loops forever
- **Frame duration**: Calculated from fps (1000/fps milliseconds)
- **Compression**: Automatic by PIL

## Generated Example Files

Recent test runs created these animations:

```
3DModel_1/model_rotation.gif              548 KB  Z-axis, 24 frames, 12 fps
3DModel_1/model_rotation_x_axis.gif       854 KB  X-axis, 36 frames, 15 fps
3DModel_1/model_rotation_y_axis.gif       584 KB  Y-axis, 24 frames, 12 fps
3DModel_1/rotation_with_texture.gif       459 KB  Z-axis with texture, 20 frames
3DModel_1/rotation_diagonal.gif           470 KB  Diagonal (1,1,1), 24 frames
3DModel_1/rotation_custom_axis.gif        496 KB  Custom (0.7,0.5,0.5), 24 frames
```

## Working with Different Models

The script works with all models in the directory structure:

```bash
# 3DModel_2
python3 rotate_model_to_gif.py --obj 3DModel_2/OBJ/3DModel.obj

# 3DModel_3
python3 rotate_model_to_gif.py --obj 3DModel_3/OBJ/3DModel.obj

# Custom path
python3 rotate_model_to_gif.py --obj /absolute/path/to/model.obj
```

## Tips & Best Practices

✓ **Always use a texture file for better visuals**
✓ **Start with --axis x, y, or z for consistency**
✓ **Use 36+ frames for professional presentations**
✓ **Test with --frames 24 to verify before large renders**
✓ **Increase --fps to 15-20 for faster-paced animations**
✓ **Use diagonal axes (1,1,1) to show all 3D dimensions**

## Need Help?

```bash
# Show all options
python3 rotate_model_to_gif.py --help

# Check script syntax
python3 -m py_compile rotate_model_to_gif.py

# List available models
ls 3DModel_*/OBJ/*.obj

# List available textures
ls 3DModel_*/OBJ/3DModel/*.png
```
