"""
CodeAlpha Internship - Task 1: Language Translation Tool (Crystal Blue UI)
--------------------------------------------------------------------------
Professional Flask web app with a 3D animated crystal-blue interface.

Backend:
- deep-translator (Google Translate engine) for translation
- gTTS for text-to-speech audio

Run with:
    python web_app.py
Then open:  http://localhost:5000
"""

import io

from deep_translator import GoogleTranslator
from flask import Flask, jsonify, render_template, request, send_file
from gtts import gTTS
from gtts.lang import tts_langs

app = Flask(__name__)

# ------------------------- Supported languages -------------------------
# {name: code}, e.g. {"english": "en", "urdu": "ur", ...}
_raw = GoogleTranslator().get_supported_languages(as_dict=True)
LANGUAGES = {name.title(): code for name, code in sorted(_raw.items())}

try:
    TTS_LANGS = set(tts_langs().keys())
except Exception:
    # Fallback: common gTTS languages if the lookup fails offline
    TTS_LANGS = {"en", "ur", "hi", "ar", "fr", "de", "es", "ja", "ko", "zh-CN",
                 "it", "pt", "ru", "tr", "nl", "pl", "th", "vi", "id", "bn"}


@app.route("/")
def index():
    return render_template("index.html", languages=LANGUAGES)


@app.route("/api/translate", methods=["POST"])
def translate():
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    source = data.get("source") or "auto"
    target = data.get("target") or "en"

    if not text:
        return jsonify({"error": "Please enter some text to translate."}), 400

    try:
        translated = GoogleTranslator(source=source, target=target).translate(text)
        return jsonify({
            "translated": translated,
            "tts_available": True,  # always try; client falls back to browser voice
        })
    except Exception as exc:
        return jsonify({"error": f"Translation failed: {exc}"}), 500


@app.route("/api/tts", methods=["POST"])
def text_to_speech():
    data = request.get_json(force=True)
    text = (data.get("text") or "").strip()
    lang = data.get("lang") or "en"

    if not text:
        return jsonify({"error": "No text provided."}), 400

    try:
        buffer = io.BytesIO()
        gTTS(text=text, lang=lang).write_to_fp(buffer)
        buffer.seek(0)
        return send_file(buffer, mimetype="audio/mpeg", download_name="speech.mp3")
    except Exception as exc:
        return jsonify({"error": f"Audio generation failed: {exc}"}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print("🌐 AI Language Translation Tool")
    print(f"   Open in your browser:  http://localhost:{port}\n")
    app.run(host="0.0.0.0", port=port, debug=False)
