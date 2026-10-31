#!/usr/bin/env python3
"""Erzeugt ein TikTok-/Shorts-Video (1080x1920) zum nächsten unbenutzten Fakt aus fakten.json.

Stil: neuronale deutsche Stimme (Piper), Wort-für-Wort-Untertitel mit gelb
hervorgehobenem Wort, großes Emoji, Fortschrittsbalken.
Ausgabe in shorts/out/: <nr>.mp4 und <nr>.txt (Beschreibung + Hashtags).
Vorher einmal: bash shorts/setup.sh
"""
import json, subprocess, sys, tempfile, unicodedata, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from piper import PiperVoice
from piper.config import SynthesisConfig

ROOT = Path(__file__).resolve().parent
FACTS, STATE, OUT = ROOT / "fakten.json", ROOT / "state.json", ROOT / "out"
VOICE = ROOT / "voices" / "de-thorsten-low.onnx"
W, H, FPS = 1080, 1920, 30
FONT_DIR = "/usr/share/fonts/opentype/inter"
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"
SPEED = 0.92          # <1 = schneller sprechen (TikTok-Tempo)
GAP = 0.22            # Pause zwischen den Sätzen (Sekunden)
PALETTES = [((25, 8, 70), (160, 30, 140)), ((0, 35, 75), (0, 160, 150)),
            ((70, 10, 10), (230, 100, 20)), ((5, 35, 25), (40, 170, 90)),
            ((12, 12, 40), (80, 70, 220))]


def sh(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])


def background(path, pal, emoji):
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, bot = pal
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    d.text((W / 2, 250), "KRASSE FAKTEN", font=ImageFont.truetype(f"{FONT_DIR}/InterDisplay-Black.otf", 64),
           fill=(255, 214, 0), anchor="mm", stroke_width=4, stroke_fill=(0, 0, 0))
    # Emoji: Noto rendert nur in 109 px, danach hochskalieren
    em = Image.new("RGBA", (160, 160), (0, 0, 0, 0))
    ImageDraw.Draw(em).text((80, 80), emoji, font=ImageFont.truetype(EMOJI_FONT, 109),
                            embedded_color=True, anchor="mm")
    em = em.resize((420, 420), Image.LANCZOS)
    img.paste(em, ((W - 420) // 2, 420), em)
    img.save(path)


def ass_time(t):
    cs = int(round(t * 100))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def groups(words, maxlen=16):
    out, cur = [], []
    for w in words:
        if cur and (len(" ".join(cur + [w])) > maxlen or len(cur) == 3):
            out.append(cur)
            cur = []
        cur.append(w)
    out.append(cur)
    return out


def subtitles(path, timed):
    head = (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {W}\nPlayResY: {H}\nWrapStyle: 2\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
            "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, "
            "Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: W,Inter Display Black,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,"
            "100,100,0,0,1,9,4,5,60,60,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = []
    for words, start, end in timed:
        weights = [len(w) + 2 for w in words]
        total, t = sum(weights), start
        times = []
        for wt in weights:
            times.append(t)
            t += (end - start) * wt / total
        times.append(end)
        k = 0
        for g in groups(words):
            for j in range(len(g)):
                txt = " ".join(r"{\c&H00D7FF&}" + w + r"{\c&HFFFFFF&}" if i == j else w
                               for i, w in enumerate(g))
                pop = r"{\fscx85\fscy85\t(0,90,\fscx100\fscy100)}" if j == 0 else ""
                ev.append(f"Dialogue: 0,{ass_time(times[k + j])},{ass_time(times[k + j + 1])},W,,0,0,0,,"
                          + r"{\pos(540,1180)}" + pop + txt)
            k += len(g)
    Path(path).write_text(head + "\n".join(ev) + "\n")


def main():
    facts = json.loads(FACTS.read_text())
    state = json.loads(STATE.read_text()) if STATE.exists() else {"next": 0}
    i = state["next"]
    if i >= len(facts):
        sys.exit("Alle Fakten verbraucht – neue in fakten.json ergänzen.")
    f = facts[i]
    nr = f"{i + 1:03d}"
    OUT.mkdir(exist_ok=True)
    voice = PiperVoice.load(str(VOICE))
    # Piper zerlegt "ç" (ich-Laut) in c + Cedille; das Modell kennt aber nur "ç" am Stück.
    raw = voice.phonemize
    voice.phonemize = lambda text: [list(unicodedata.normalize("NFC", "".join(s))) for s in raw(text)]
    cfg = SynthesisConfig(length_scale=SPEED)
    texts = [f["hook"], f["fakt"], f["detail"], "Folg mir für mehr krasse Fakten!"]
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        frames, timed, t, rate = b"", [], 0.0, None
        for n, text in enumerate(texts):
            p = tmp / f"{n}.wav"
            with wave.open(str(p), "wb") as wf:
                voice.synthesize_wav(text, wf, syn_config=cfg)
            with wave.open(str(p)) as wf:
                rate, width = wf.getframerate(), wf.getsampwidth()
                data = wf.readframes(wf.getnframes())
            dur = len(data) / (rate * width)
            timed.append((text.split(), t, t + dur))
            frames += data + b"\0" * (int(rate * GAP) * width)
            t += dur + GAP
        total = t + 0.4
        frames += b"\0" * (int(rate * 0.4) * width)
        with wave.open(str(tmp / "voice.wav"), "wb") as wf:
            wf.setnchannels(1); wf.setsampwidth(width); wf.setframerate(rate)
            wf.writeframes(frames)
        background(tmp / "bg.png", PALETTES[i % len(PALETTES)], f.get("emoji", "🤯"))
        subtitles(tmp / "subs.ass", timed)
        n_frames = int(total * FPS)
        sh("ffmpeg", "-y", "-loop", "1", "-i", str(tmp / "bg.png"), "-i", str(tmp / "voice.wav"),
           "-f", "lavfi", "-i", f"color=c=0xFFD600:s={W}x16:r={FPS}",
           "-filter_complex",
           f"[0:v]scale=1188:2112,zoompan=z='1+0.0006*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
           f":d={n_frames}:s={W}x{H}:fps={FPS}[bg];"
           f"[bg][2:v]overlay=x='-W+W*t/{total:.2f}':y=H-16:shortest=1,"
           f"ass={tmp / 'subs.ass'}:fontsdir={FONT_DIR},format=yuv420p[v];"
           f"[1:a]highpass=f=70,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-14:TP=-1,"
           f"aresample=44100[a]",
           "-map", "[v]", "-map", "[a]", "-t", f"{total:.2f}",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-movflags", "+faststart",
           str(OUT / f"{nr}.mp4"))
    tags = " ".join("#" + t for t in f["tags"] + ["fakten", "wusstestdu", "krassefakten", "fyp", "shorts"])
    (OUT / f"{nr}.txt").write_text(
        f"{f['hook']} {f.get('emoji', '')}\n\n{f['fakt']} {f['detail']}\n\n"
        f"Folg mir für täglich neue krasse Fakten!\n(Stimme: KI-Computerstimme)\n\n{tags}\n")
    state["next"] = i + 1
    STATE.write_text(json.dumps(state))
    print(OUT / f"{nr}.mp4")


if __name__ == "__main__":
    main()
