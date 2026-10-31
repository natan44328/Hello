#!/usr/bin/env python3
"""Erzeugt ein 9:16-Short (1080x1920) zum nächsten unbenutzten Fakt aus fakten.json.

Ausgabe in shorts/out/: <nr>.mp4 und <nr>.txt (Beschreibung + Hashtags).
Benötigt: ffmpeg, espeak-ng, mbrola-de6 (siehe setup.sh), Pillow.
"""
import json, subprocess, sys, tempfile, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
FACTS = ROOT / "fakten.json"
STATE = ROOT / "state.json"
OUT = ROOT / "out"
W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_REG = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
VOICE = "mb-de6"
PALETTES = [((20, 10, 60), (140, 30, 120)), ((5, 40, 70), (0, 150, 140)),
            ((60, 10, 10), (220, 90, 20)), ((10, 30, 20), (40, 160, 80)),
            ((15, 15, 35), (70, 70, 200))]


def sh(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout)


def wrap(draw, text, font, maxw):
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if draw.textlength(test, font=font) <= maxw:
            cur = test
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def slide(path, text, pal, size, label=None, accent=(255, 214, 0)):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, bot = pal
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    font = ImageFont.truetype(FONT, size)
    lines = wrap(d, text, font, W - 160)
    lh = int(size * 1.2)
    y = (H - lh * len(lines)) // 2
    if label:
        lf = ImageFont.truetype(FONT_REG, 48)
        lw = d.textlength(label, font=lf)
        d.rounded_rectangle([(W - lw) / 2 - 30, y - 140, (W + lw) / 2 + 30, y - 60], 40, fill=accent)
        d.text((W / 2, y - 100), label, font=lf, fill=(20, 20, 20), anchor="mm")
    for ln in lines:
        d.text((W / 2, y + lh / 2), ln, font=font, fill="white", anchor="mm",
               stroke_width=6, stroke_fill=(0, 0, 0))
        y += lh
    d.text((W / 2, 300), "KRASSE FAKTEN", font=ImageFont.truetype(FONT, 44),
           fill=accent, anchor="mm")
    img.save(path)


def main():
    facts = json.loads(FACTS.read_text())
    state = json.loads(STATE.read_text()) if STATE.exists() else {"next": 0}
    i = state["next"]
    if i >= len(facts):
        sys.exit("Alle Fakten verbraucht – neue in fakten.json ergänzen.")
    f = facts[i]
    nr = f"{i + 1:03d}"
    OUT.mkdir(exist_ok=True)
    pal = PALETTES[i % len(PALETTES)]
    segs = [(f["hook"], 96, None), (f["fakt"], 84, "WUSSTEST DU?"),
            (f["detail"], 70, None), ("Folge für täglich krasse Fakten!", 90, None)]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        parts = []
        for n, (text, size, label) in enumerate(segs):
            png, wav, mp4 = tmp / f"{n}.png", tmp / f"{n}.wav", tmp / f"{n}.mp4"
            slide(png, text, pal, size, label)
            sh("espeak-ng", "-v", VOICE, "-s", "155", "-w", str(wav), text)
            dur = duration(wav) + 0.35
            frames = int(dur * 30)
            sh("ffmpeg", "-y", "-loop", "1", "-i", str(png), "-i", str(wav),
               "-filter_complex",
               f"[0:v]scale=1188:2112,zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':"
               f"y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps=30,format=yuv420p[v];"
               f"[1:a]apad,atrim=0:{dur:.2f},aresample=44100[a]",
               "-map", "[v]", "-map", "[a]", "-t", f"{dur:.2f}",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
               "-c:a", "aac", "-b:a", "128k", "-ac", "2", str(mp4))
            parts.append(mp4)
        lst = tmp / "list.txt"
        lst.write_text("".join(f"file '{p}'\n" for p in parts))
        sh("ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
           "-c", "copy", "-movflags", "+faststart", str(OUT / f"{nr}.mp4"))
    tags = " ".join("#" + t for t in f["tags"] + ["fakten", "wusstestdu", "krassefakten", "shorts"])
    (OUT / f"{nr}.txt").write_text(
        f"{f['hook']}\n\n{f['fakt']} {f['detail']}\n\n"
        f"Folge für täglich neue krasse Fakten!\n(Stimme: Computerstimme)\n\n{tags}\n")
    state["next"] = i + 1
    STATE.write_text(json.dumps(state))
    print(OUT / f"{nr}.mp4")


if __name__ == "__main__":
    main()
