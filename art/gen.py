#!/usr/bin/env python3
"""Gemini (Nano Banana Pro) ile oyun görseli üretir.

Kullanım:
    GEMINI_KEY=... python3 gen.py <cikti.png> <en-boy-orani> <prompt dosyasi>
en-boy-orani: 1:1 | 9:16 | 16:9 | 3:4 ...
"""
import base64, json, os, sys, urllib.request

MODEL = "gemini-3-pro-image"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"


def generate(prompt, out_path, aspect="1:1", resolution="2K"):
    key = os.environ["GEMINI_KEY"]
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": aspect, "imageSize": resolution},
        },
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode()[:900]}")

    for cand in data.get("candidates", []):
        for part in cand.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline:
                os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
                with open(out_path, "wb") as f:
                    f.write(base64.b64decode(inline["data"]))
                return out_path
    raise SystemExit("Görsel dönmedi: " + json.dumps(data)[:800])


if __name__ == "__main__":
    out, aspect, pfile = sys.argv[1], sys.argv[2], sys.argv[3]
    res = sys.argv[4] if len(sys.argv) > 4 else "2K"
    print(generate(open(pfile).read(), out, aspect, res))
