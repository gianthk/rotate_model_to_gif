# Turntable GIF / MP4 of a textured 3D model (Blender)

Renders a textured OBJ model (e.g. a Kiri Engine export) rotating 360 degrees on a white background with a soft
shadow, and saves it as a GIF and an MP4.

## Requirements

- [Blender](https://www.blender.org/download/) 4.2 or newer (no GPU needed, runs without a display)
- Python 3 with Pillow (`pip install pillow`)
- ffmpeg (optional, for the MP4)

## Usage

1. Render the frames (the OBJ, its `.mtl` file and the texture images must be in the same folder structure as exported):

   ```
   blender -b -P turntable.py -- --obj path/to/model.obj --out out/model --tilt 90 0 0 --elev 8
   ```

2. Make the GIF and MP4:

   ```
   python make_gif.py out/model
   ```

   This writes `out/model/model.gif` and `out/model/model.mp4`.

`render.sh` runs both steps: `bash render.sh path/to/model.obj out/model`
(set `BLENDER` to your Blender executable if `blender` is not on your PATH).

## Main options (`turntable.py`)

| Option | Default | Meaning |
|---|---|---|
| `--frames` | 120 | frames for one full turn (more = slower, smoother rotation) |
| `--size` | 800 | image size in pixels |
| `--samples` | 64 | render quality (higher = less noise, slower) |
| `--light` | 1.0 | brightness of the lights (e.g. 0.5 for a softer look) |
| `--elev` | 12 | camera height above the model, in degrees |
| `--tilt X Y Z` | 0 0 0 | rotation in degrees if the model is not upright (Kiri models: `90 0 0`) |
| `--spin` | 0 | start angle in degrees, to choose the front view |
| `--still` | off | render only the first frame, for a quick check |

`make_gif.py` options: `--fps` (MP4 frame rate, default 24), `--step` (GIF uses every n-th frame, default 2),
`--gif-size` (GIF size in pixels, default 600).

Rendering 240 frames at 800 px takes about 20 minutes on a 32-core CPU.
