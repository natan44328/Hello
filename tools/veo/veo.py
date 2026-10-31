#!/usr/bin/env python3
"""Erzeugt ein Video mit Google Veo 3.1 über die Gemini API.

Benötigt die Umgebungsvariable GEMINI_API_KEY.

Beispiele:
  python3 tools/veo/veo.py "A cat on a windowsill at sunset" --out katze.mp4
  python3 tools/veo/veo.py --prompt-file prompt.txt --quality fast --aspect 9:16
  python3 tools/veo/veo.py --list-models
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://generativelanguage.googleapis.com/v1beta"
QUALITY_HINTS = {"lite": "lite", "fast": "fast", "standard": None}


def api(method, url, key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("x-goog-api-key", key)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"API-Fehler {e.code}: {e.read().decode(errors='replace')}")


def veo_models(key):
    out, token = [], ""
    while True:
        url = f"{BASE}/models?pageSize=100" + (f"&pageToken={token}" if token else "")
        res = api("GET", url, key)
        for m in res.get("models", []):
            name = m["name"].split("/", 1)[1]
            if name.startswith("veo-3.1"):
                out.append(name)
        token = res.get("nextPageToken")
        if not token:
            return sorted(out)


def pick_model(key, quality):
    models = veo_models(key)
    if not models:
        sys.exit("Kein Veo-3.1-Modell für diesen API-Schlüssel gefunden.")
    hint = QUALITY_HINTS[quality]
    if hint:
        matches = [m for m in models if hint in m]
    else:
        matches = [m for m in models if "fast" not in m and "lite" not in m]
    if not matches:
        sys.exit(f"Kein Modell für Qualität '{quality}'. Verfügbar: {', '.join(models)}")
    # Stabile Versionen vor Previews bevorzugen
    matches.sort(key=lambda m: ("preview" in m, m))
    return matches[0]


def main():
    p = argparse.ArgumentParser(description="Video mit Veo 3.1 erzeugen")
    p.add_argument("prompt", nargs="?")
    p.add_argument("--prompt-file")
    p.add_argument("--out", default="video.mp4")
    p.add_argument("--quality", choices=QUALITY_HINTS, default="fast")
    p.add_argument("--model", help="Modell-ID direkt angeben")
    p.add_argument("--aspect", choices=["9:16", "16:9"], default="9:16")
    p.add_argument("--resolution", choices=["720p", "1080p", "4k"], default="720p")
    p.add_argument("--seconds", type=int, choices=[4, 6, 8], default=8)
    p.add_argument("--negative", help="Was nicht vorkommen soll")
    p.add_argument("--list-models", action="store_true")
    a = p.parse_args()

    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        sys.exit("GEMINI_API_KEY ist nicht gesetzt.")

    if a.list_models:
        print("\n".join(veo_models(key)))
        return

    prompt = open(a.prompt_file, encoding="utf-8").read() if a.prompt_file else a.prompt
    if not prompt:
        sys.exit("Bitte einen Prompt angeben.")

    model = a.model or pick_model(key, a.quality)
    params = {"aspectRatio": a.aspect, "resolution": a.resolution,
              "durationSeconds": a.seconds}
    if a.negative:
        params["negativePrompt"] = a.negative
    print(f"Modell: {model} | {a.aspect} | {a.resolution} | {a.seconds}s", flush=True)

    op = api("POST", f"{BASE}/models/{model}:predictLongRunning", key,
             {"instances": [{"prompt": prompt}], "parameters": params})
    name = op["name"]
    start = time.time()
    while not op.get("done"):
        if time.time() - start > 900:
            sys.exit(f"Zeitüberschreitung. Operation: {name}")
        time.sleep(10)
        op = api("GET", f"{BASE}/{name}", key)
        print(f"  … läuft ({int(time.time() - start)}s)", flush=True)

    if "error" in op:
        sys.exit(f"Erzeugung fehlgeschlagen: {json.dumps(op['error'], ensure_ascii=False)}")
    resp = op.get("response", {}).get("generateVideoResponse", {})
    samples = resp.get("generatedSamples") or []
    if not samples:
        sys.exit("Kein Video erhalten (evtl. vom Sicherheitsfilter blockiert): "
                 + json.dumps(resp, ensure_ascii=False))

    req = urllib.request.Request(samples[0]["video"]["uri"])
    req.add_header("x-goog-api-key", key)
    with urllib.request.urlopen(req, timeout=300) as r, open(a.out, "wb") as f:
        f.write(r.read())
    print(f"Fertig: {a.out} ({os.path.getsize(a.out) // 1024} KB, "
          f"{int(time.time() - start)}s)")


if __name__ == "__main__":
    main()
