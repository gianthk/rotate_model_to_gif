"""Put the RGBA turntable frames on a white background and write a GIF (+ MP4 if ffmpeg is available).

    python make_gif.py out/model --fps 24 --gif-size 600
"""
import argparse
import glob
import os
import shutil
import subprocess

from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--fps", type=int, default=24, help="MP4 frame rate")
ap.add_argument("--step", type=int, default=2, help="GIF uses every STEP-th frame at fps/STEP (same turn speed, smaller file)")
ap.add_argument("--gif-size", type=int, default=600, help="GIF width/height in px (GIFs get large)")
ap.add_argument("--ffmpeg", default=shutil.which("ffmpeg") or "")
a = ap.parse_args()

frames = sorted(glob.glob(os.path.join(a.out, "frames", "f_*.png")))
if not frames:
    raise SystemExit("no frames in " + a.out)
name = os.path.basename(os.path.normpath(a.out))
white = []
wdir = os.path.join(a.out, "frames_white")
os.makedirs(wdir, exist_ok=True)
for f in frames:
    im = Image.open(f).convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    rgb = Image.alpha_composite(bg, im).convert("RGB")
    rgb.save(os.path.join(wdir, os.path.basename(f)))
    white.append(rgb)

# GIF: one shared adaptive palette (from a few frames) so the colours do not flicker between frames
small = [w.resize((a.gif_size, a.gif_size), Image.LANCZOS) for w in white[::a.step]]
strip = Image.new("RGB", (a.gif_size, a.gif_size * 4))
for k, i in enumerate(range(0, len(small), max(1, len(small) // 4))[:4]):
    strip.paste(small[i], (0, k * a.gif_size))
pal = strip.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
gif = [s.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG) for s in small]
gpath = os.path.join(a.out, f"{name}.gif")
gif[0].save(gpath, save_all=True, append_images=gif[1:], duration=round(1000 * a.step / a.fps), loop=0,
            optimize=False, disposal=1)
print(f"GIF  {gpath}  {len(gif)} frames  {os.path.getsize(gpath) / 1e6:.1f} MB")

if a.ffmpeg:
    mp4 = os.path.join(a.out, f"{name}.mp4")
    subprocess.run([a.ffmpeg, "-y", "-loglevel", "error", "-framerate", str(a.fps),
                    "-i", os.path.join(wdir, "f_%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", mp4], check=True)
    print(f"MP4  {mp4}")
