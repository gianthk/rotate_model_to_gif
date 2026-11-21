"""Turntable render of a textured OBJ (Kiri Engine export) with Blender, headless.

    blender -b -P turntable.py -- --obj path/to/model.obj --out out/model

Writes RGBA PNG frames (transparent background + soft contact shadow) to <out>/frames/.
make_gif.py then puts them on a white background and writes the GIF (and an MP4).

Scene: model centred and scaled to unit height, standing on a shadow-catcher floor, rotating 360 deg about the
vertical axis (linear, seamless loop: last frame != first frame); camera slightly above, three soft area lights +
a dim white world for ambient light; Cycles on CPU (no GPU or display needed) with denoising.
"""
import argparse
import math
import os
import sys

import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument("--obj", required=True)
ap.add_argument("--out", required=True)
ap.add_argument("--frames", type=int, default=120, help="frames per 360 deg")
ap.add_argument("--size", type=int, default=800, help="square image size (px)")
ap.add_argument("--samples", type=int, default=64)
ap.add_argument("--elev", type=float, default=12.0, help="camera elevation (deg)")
ap.add_argument("--up", default="Y", help="up axis of the OBJ file (Kiri exports are Y-up)")
ap.add_argument("--forward", default="NEGATIVE_Z")
ap.add_argument("--tilt", type=float, nargs=3, default=[0, 0, 0],
                help="extra rotation (deg, XYZ) if a model is not upright after import")
ap.add_argument("--spin", type=float, default=0.0, help="start angle (deg), to choose the front view")
ap.add_argument("--direction", type=int, default=1, choices=[1, -1], help="1 = counter-clockwise from above")
ap.add_argument("--roughness", type=float, default=0.75, help="surface roughness (clay is matte); a negative value keeps the value from the MTL file")
ap.add_argument("--threads", type=int, default=0, help="CPU threads (0 = all available)")
ap.add_argument("--light", type=float, default=1.0, help="brightness factor for all lights (e.g. 0.5 = softer)")
ap.add_argument("--still", action="store_true", help="render only frame 1 (quick look)")
a = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

# Model
bpy.ops.wm.obj_import(filepath=os.path.abspath(a.obj), up_axis=a.up, forward_axis=a.forward)
meshes = [o for o in bpy.context.selected_objects if o.type == "MESH"]
if not meshes:
    sys.exit("no mesh imported from " + a.obj)
bpy.context.view_layer.objects.active = meshes[0]
if len(meshes) > 1:
    bpy.ops.object.join()
model = bpy.context.view_layer.objects.active
model.rotation_euler = [math.radians(t) for t in a.tilt]
bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

# centre on the vertical axis, feet on z = 0, unit height
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
model.location = (0, 0, 0)
bpy.context.view_layer.update()
bb = [model.matrix_world @ Vector(c) for c in model.bound_box]
h = max(v.z for v in bb) - min(v.z for v in bb)
s = 1.0 / h
model.scale = (s, s, s)
bpy.ops.object.transform_apply(location=True, rotation=False, scale=True)
bpy.context.view_layer.update()
bb = [model.matrix_world @ Vector(c) for c in model.bound_box]
model.location.z -= min(v.z for v in bb)
radius = max(math.hypot(v.x, v.y) for v in bb)          # widest footprint (for framing)

for m in model.data.materials:                            # matte clay look, keep the texture colour
    if m and m.use_nodes and a.roughness >= 0:
        for n in m.node_tree.nodes:
            if n.type == "BSDF_PRINCIPLED":
                n.inputs["Roughness"].default_value = a.roughness
                if "Specular IOR Level" in n.inputs:
                    n.inputs["Specular IOR Level"].default_value = 0.2

# Kiri's MTL stores the normal map as `map_tangentSpaceNormal`, which Blender's importer ignores -- add it here
mtl = os.path.splitext(os.path.abspath(a.obj))[0] + ".mtl"
nmap = None
if os.path.exists(mtl):
    for line in open(mtl):
        if line.strip().startswith("map_tangentSpaceNormal"):
            nmap = os.path.join(os.path.dirname(mtl), line.split(None, 1)[1].strip())
if nmap and os.path.exists(nmap):
    for m in model.data.materials:
        if not (m and m.use_nodes):
            continue
        nt = m.node_tree
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        if bsdf.inputs["Normal"].is_linked:
            continue
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(nmap)
        tex.image.colorspace_settings.name = "Non-Color"
        nm = nt.nodes.new("ShaderNodeNormalMap")
        nt.links.new(tex.outputs["Color"], nm.inputs["Color"])
        nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    print("normal map:", nmap)

# turntable: parent to an empty that spins linearly
pivot = bpy.data.objects.new("pivot", None)
sc.collection.objects.link(pivot)
model.parent = pivot
pivot.rotation_euler = (0, 0, math.radians(a.spin))
pivot.keyframe_insert("rotation_euler", index=2, frame=1)
pivot.rotation_euler = (0, 0, math.radians(a.spin) + a.direction * 2 * math.pi)
pivot.keyframe_insert("rotation_euler", index=2, frame=a.frames + 1)
for fc in pivot.animation_data.action.fcurves:
    for k in fc.keyframe_points:
        k.interpolation = "LINEAR"
sc.frame_start, sc.frame_end = 1, (1 if a.still else a.frames)

# Floor that only catches the shadow
bpy.ops.mesh.primitive_plane_add(size=20, location=(0, 0, 0))
floor = bpy.context.active_object
floor.is_shadow_catcher = True

# Camera: frame the model's full height + widest turn
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 85
cam = bpy.data.objects.new("cam", cam_data)
sc.collection.objects.link(cam)
sc.camera = cam
target = Vector((0, 0, 0.5))
half = max(0.5, radius) * 1.18                            # 18 % margin
fov = 2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))
dist = half / math.tan(fov / 2) + radius
el = math.radians(a.elev)
cam.location = target + Vector((0, -dist * math.cos(el), dist * math.sin(el)))
cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()


# Lights: key, fill, rim (soft area lights) + dim white world
def area(name, loc, power, size):
    d = bpy.data.lights.new(name, "AREA")
    d.energy, d.size = power, size
    o = bpy.data.objects.new(name, d)
    o.location = loc
    o.rotation_euler = (Vector((0, 0, 0.5)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.collection.objects.link(o)


area("key", (-2.2, -2.6, 2.8), 260 * a.light, 2.5)
area("fill", (2.6, -1.8, 1.4), 90 * a.light, 3.0)
area("rim", (0.5, 2.8, 2.4), 160 * a.light, 2.0)
world = bpy.data.worlds.new("world")
sc.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (1, 1, 1, 1)
world.node_tree.nodes["Background"].inputs[1].default_value = 0.35 * a.light

# Render settings
r = sc.render
r.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = a.samples
sc.cycles.use_denoising = True
if a.threads:
    r.threads_mode, r.threads = "FIXED", a.threads
r.film_transparent = True
r.resolution_x = r.resolution_y = a.size
r.resolution_percentage = 100
r.image_settings.file_format = "PNG"
r.image_settings.color_mode = "RGBA"
sc.view_settings.view_transform = "Standard"              # keeps texture colours as captured
os.makedirs(os.path.join(a.out, "frames"), exist_ok=True)
r.filepath = os.path.join(os.path.abspath(a.out), "frames", "f_")
bpy.ops.render.render(animation=True)
print("DONE", a.out)
