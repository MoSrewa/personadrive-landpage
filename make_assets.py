"""Regenerate the videos and images in static/ from our demo-video renders.

Expects the video_generation folder (not part of this repo) next to this one:
    python make_assets.py
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
VG = HERE.parent / "video_generation"
sys.path.insert(0, str(VG))
from vg.encode import FFMPEG  # noqa: E402

VIDEOS = HERE / "static" / "videos"
IMAGES = HERE / "static" / "images"
SEG = VG / "build" / "segments"

# the side-by-side clips are cut out of the demo slides (camera views + labels only)
PAIR_CROP = "crop=1920:530:0:150"

# name: (source, crop, width, crf)
CLIPS = {
    "teaser": (VG / "output" / "PersonaDrive_demo_teaser.mp4", "", 1280, 27),
    "demo_full": (VG / "output" / "PersonaDrive_demo_full.mp4", "", 1280, 28),
    "style_cyclist": (SEG / "S10a.mp4", PAIR_CROP, 1600, 25),
    "style_merge": (SEG / "S10b.mp4", PAIR_CROP, 1600, 25),
    "style_turn": (SEG / "S10c.mp4", PAIR_CROP, 1600, 25),
    "safety_red_light": (SEG / "S09a.mp4", PAIR_CROP, 1600, 25),
    "drive_context_rain": (SEG / "S08a.mp4", "", 1280, 26),
    "drive_night": (SEG / "S08b.mp4", "", 1280, 26),
    "drive_junction": (SEG / "S08c.mp4", "", 1280, 26),
    "drive_montage": (SEG / "T07.mp4", "", 1280, 26),
}

# name: (paper figure, max width, format)
FIGURES = {
    "architecture": ("Persona-Drive-Figure.png", 2000, "png"),
    "triplet": ("triplet.png", 2000, "png"),
    "triplet_viewer": ("triplet_viewer.png", 1800, "jpg"),
    "datacollection": ("datacollection.png", 1800, "png"),
    "hardware_rig": ("hardware_rig.png", 1400, "jpg"),
    "agent_behavior": ("agent_behavior.png", 1400, "jpg"),
}


def ffmpeg(*args):
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *map(str, args)], check=True)


def encode(src, crop, width, crf, out):
    vf = ",".join(f for f in (crop, f"scale={width}:-2:flags=lanczos") if f)
    ffmpeg("-i", src, "-vf", vf, "-c:v", "libx264", "-preset", "slow", "-crf", crf, "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", "-an", out)
    # webm too, since some chromium builds can't play h264
    ffmpeg("-i", out, "-c:v", "libvpx-vp9", "-crf", crf + 8, "-b:v", "0", "-row-mt", "1",
           "-cpu-used", "4", "-an", out.with_suffix(".webm"))
    # poster; the full demo fades in, so take it a bit later
    t = 3.0 if out.stem == "demo_full" else 1.0
    ffmpeg("-ss", t, "-i", out, "-frames:v", "1", "-q:v", "3", out.with_suffix(".jpg"))


def retrieval_stills():
    import storyboard as sb
    from vg.segments import build

    for seg_id, name in [("S07a", "retrieval_no_style"), ("S07b", "retrieval_styles")]:
        scene = build(sb.segment(seg_id))
        im = scene.render(scene.duration - 0.5).crop((0, 0, 1920, 1025))
        im.resize((1600, 854), Image.LANCZOS).save(IMAGES / f"{name}.jpg", quality=92)


def main():
    VIDEOS.mkdir(parents=True, exist_ok=True)
    IMAGES.mkdir(parents=True, exist_ok=True)

    for name, (src, crop, width, crf) in CLIPS.items():
        out = VIDEOS / f"{name}.mp4"
        encode(src, crop, width, crf, out)
        print(out.name)

    for name, (src, width, fmt) in FIGURES.items():
        im = Image.open(VG / "assets" / "figures" / src).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        out = IMAGES / f"{name}.{fmt}"
        im.save(out, **({"quality": 90} if fmt == "jpg" else {"optimize": True}))
        print(out.name)

    retrieval_stills()


if __name__ == "__main__":
    main()
