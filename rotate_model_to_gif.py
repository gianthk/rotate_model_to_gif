#!/usr/bin/env python3
"""
Load an OBJ model, rotate it on a specified axis, and export as an animated GIF.

Features:
  - Load OBJ models with optional texture files
  - Rotate around standard axes (x, y, z) or arbitrary axis vectors
  - Customize animation frame count and playback speed
  - Clean white background visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import os
from pathlib import Path
import tempfile
import shutil
import argparse

try:
    import trimesh
except ImportError:
    print("Error: trimesh is required. Install with: pip install trimesh pillow")
    exit(1)


def load_obj_model(obj_path, texture_file=None):
    """Load OBJ model using trimesh and apply texture if provided."""
    print(f"Loading model from: {obj_path}")
    mesh = trimesh.load(obj_path, force='mesh')
    
    # Center and scale the mesh for better visualization
    mesh.apply_translation(-mesh.centroid)
    # Scale to fit in a reasonable size
    scale = 1.0 / mesh.extents.max()
    mesh.apply_scale(scale)
    
    print(f"Model loaded successfully!")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Faces: {len(mesh.faces)}")
    
    # Load texture if file is provided
    if texture_file and os.path.exists(texture_file):
        print(f"\nLoading texture from: {texture_file}")
        try:
            texture_img = Image.open(texture_file)
            # Create a simple texture by assigning vertex colors
            texture_array = np.array(texture_img)
            # Store texture for visualization
            mesh.visual.vertex_colors = np.ones((len(mesh.vertices), 4), dtype=np.uint8) * 200
            print(f"  Loaded texture: {os.path.basename(texture_file)}")
        except Exception as e:
            print(f"  Could not load texture: {e}")
    
    return mesh


def parse_rotation_axis(axis_input):
    """
    Parse rotation axis input.
    
    Accepts:
    - Single letters: 'x', 'y', 'z' for standard axes
    - Comma-separated values: '0.5,0.5,0.707' for arbitrary axis
    
    Returns:
        Normalized rotation axis as [x, y, z]
    """
    axis_input = axis_input.strip().lower()
    
    # Standard axes
    axis_map = {
        'x': [1, 0, 0],
        'y': [0, 1, 0],
        'z': [0, 0, 1]
    }
    
    if axis_input in axis_map:
        return axis_map[axis_input]
    
    # Parse comma-separated values
    try:
        values = [float(x.strip()) for x in axis_input.split(',')]
        if len(values) != 3:
            raise ValueError(f"Axis vector must have 3 components, got {len(values)}")
        
        # Normalize the vector
        axis_array = np.array(values)
        norm = np.linalg.norm(axis_array)
        
        if norm == 0:
            raise ValueError("Rotation axis cannot be zero vector")
        
        normalized = axis_array / norm
        return list(normalized)
    
    except ValueError as e:
        raise ValueError(f"Invalid axis input '{axis_input}': {e}")


def create_rotation_frames(mesh, num_frames=36, axis='z', output_dir=None):
    """
    Create frames of the mesh rotated on a specified axis.
    
    Args:
        mesh: trimesh object
        num_frames: number of rotation frames (default 36)
        axis: rotation axis - 'x', 'y', 'z', or comma-separated values like '0.5,0.5,0.707' (default 'z')
        output_dir: directory to save frames (if None, uses temp directory)
    
    Returns:
        list of frame file paths
    """
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    
    os.makedirs(output_dir, exist_ok=True)
    frame_paths = []
    
    # Parse axis input
    rotation_axis = parse_rotation_axis(axis)
    
    print(f"\nGenerating {num_frames} rotation frames around axis [{rotation_axis[0]:.3f}, {rotation_axis[1]:.3f}, {rotation_axis[2]:.3f}]...")
    
    for i in range(num_frames):
        angle = (360 / num_frames) * i
        
        # Create a copy of the mesh for this frame
        mesh_frame = mesh.copy()
        
        # Rotate around specified axis
        rotation_matrix = trimesh.transformations.rotation_matrix(
            np.radians(angle), rotation_axis
        )
        mesh_frame.apply_transform(rotation_matrix)
        
        # Create figure with white background
        fig = plt.figure(figsize=(8, 8), dpi=100, facecolor='white')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('white')
        
        # Plot the mesh
        vertices = mesh_frame.vertices
        faces = mesh_frame.faces
        
        # Plot triangles with light gray color
        ax.plot_trisurf(
            vertices[:, 0],
            vertices[:, 1],
            vertices[:, 2],
            triangles=faces,
            shade=True,
            color='lightblue',
            edgecolor='lightgray',
            linewidth=0.05,
            alpha=0.9
        )
        
        # Set equal aspect ratio and limits
        max_range = np.array([vertices[:, 0].max() - vertices[:, 0].min(),
                              vertices[:, 1].max() - vertices[:, 1].min(),
                              vertices[:, 2].max() - vertices[:, 2].min()]).max() / 2.0
        
        mid_x = (vertices[:, 0].max() + vertices[:, 0].min()) * 0.5
        mid_y = (vertices[:, 1].max() + vertices[:, 1].min()) * 0.5
        mid_z = (vertices[:, 2].max() + vertices[:, 2].min()) * 0.5
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        # Remove all axes and panes - completely white background
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Remove panes completely
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.xaxis.pane.set_edgecolor('white')
        ax.yaxis.pane.set_edgecolor('white')
        ax.zaxis.pane.set_edgecolor('white')
        
        # Remove grid lines
        ax.grid(False)
        ax.xaxis.grid(False)
        ax.yaxis.grid(False)
        ax.zaxis.grid(False)
        
        # Set viewing angle
        ax.view_init(elev=20, azim=0)
        
        # Save frame
        frame_path = os.path.join(output_dir, f"frame_{i:03d}.png")
        plt.savefig(frame_path, bbox_inches='tight', pad_inches=0, dpi=100, facecolor='white')
        plt.close(fig)
        
        frame_paths.append(frame_path)
        
        if (i + 1) % max(1, num_frames // 6) == 0:
            print(f"  Generated {i + 1}/{num_frames} frames")
    
    print(f"All frames saved to: {output_dir}")
    return frame_paths


def create_gif(frame_paths, output_gif_path, fps=10):
    """
    Create animated GIF from frames.
    
    Args:
        frame_paths: list of frame image file paths
        output_gif_path: path to save the GIF
        fps: frames per second (default 10)
    """
    print(f"\nCreating animated GIF...")
    
    # Convert fps to frame duration in milliseconds
    duration = int(1000 / fps)
    
    images = []
    for frame_path in frame_paths:
        img = Image.open(frame_path)
        images.append(img)
    
    # Save as animated GIF
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=0  # Loop forever
    )
    
    file_size_mb = os.path.getsize(output_gif_path) / (1024*1024)
    print(f"GIF saved to: {output_gif_path}")
    print(f"GIF size: {file_size_mb:.2f} MB")
    print(f"Animation: {len(images)} frames at {fps} fps")


def main():
    """Main function with command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Load an OBJ model, rotate it, and export as animated GIF'
    )
    parser.add_argument(
        '--obj',
        default='3DModel_1/OBJ/3DModel.obj',
        help='Path to OBJ file (default: 3DModel_1/OBJ/3DModel.obj)'
    )
    parser.add_argument(
        '--texture',
        default=None,
        help='Path to texture file (PNG/JPG). Optional. Example: 3DModel_1/OBJ/3DModel/baked_mesh_239e0824_tex0.png'
    )
    parser.add_argument(
        '--output',
        default='3DModel_1/model_rotation.gif',
        help='Output GIF file path (default: 3DModel_1/model_rotation.gif)'
    )
    parser.add_argument(
        '--axis',
        default='z',
        help='Rotation axis: x, y, z, or comma-separated vector (default: z). Examples: --axis x  or  --axis 0.577,0.577,0.577'
    )
    parser.add_argument(
        '--frames',
        type=int,
        default=36,
        help='Number of rotation frames (default: 36)'
    )
    parser.add_argument(
        '--fps',
        type=int,
        default=10,
        help='Frames per second in output GIF (default: 10)'
    )
    
    args = parser.parse_args()
    
    # Define base directory
    base_dir = "/Users/gianthk/Library/CloudStorage/GoogleDrive-gianthk.iori@gmail.com/My Drive/ETH/HES-SO_terracotta/Results/kiri/3D_MODELS_BEST_TO_VIEW_IN_WINDOS_3D_VIEWER_OR_MESHLAB_OR_BLENDER"
    obj_path = os.path.join(base_dir, args.obj)
    
    # Handle texture path
    texture_path = None
    if args.texture:
        texture_path = os.path.join(base_dir, args.texture) if not os.path.isabs(args.texture) else args.texture
    
    output_gif = os.path.join(base_dir, args.output)
    
    # Verify input file exists
    if not os.path.exists(obj_path):
        print(f"Error: OBJ file not found at {obj_path}")
        exit(1)
    
    # Verify texture file exists if provided
    if args.texture and not os.path.exists(texture_path):
        print(f"Error: Texture file not found at {texture_path}")
        exit(1)
    
    print(f"\n{'='*60}")
    print(f"3D Model Rotation to GIF Converter")
    print(f"{'='*60}")
    print(f"Model: {args.obj}")
    print(f"Texture: {args.texture if args.texture else 'None'}")
    print(f"Rotation axis: {args.axis}")
    print(f"Frames: {args.frames}")
    print(f"FPS: {args.fps}")
    print(f"Output: {args.output}")
    print(f"{'='*60}\n")
    
    # Load model
    mesh = load_obj_model(obj_path, texture_path)
    
    # Create rotation frames
    temp_dir = tempfile.mkdtemp(prefix="mesh_frames_")
    frame_paths = create_rotation_frames(mesh, num_frames=args.frames, axis=args.axis, output_dir=temp_dir)
    
    # Create GIF
    create_gif(frame_paths, output_gif, fps=args.fps)
    
    # Clean up temporary files
    print(f"\nCleaning up temporary files...")
    shutil.rmtree(temp_dir)
    
    print("\n✓ Done!")


if __name__ == "__main__":
    main()
