"""
CodeAlpha Internship - Task 1: Language Translation Tool
--------------------------------------------------------
A professional web-based translation tool built with Streamlit.

Features:
- Enter any text and select source & target languages
- Translation powered by Google Translate (via deep-translator)
- Auto-detect source language
- Copy-friendly output (built-in copy button on the result box)
- Text-to-Speech: listen to the translated text (gTTS)
- Swap languages with one click

Run with:
    streamlit run app.py
"""

import io

import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from gtts.lang import tts_langs

# ----------------------------- Page config -----------------------------
st.set_page_config(
    page_title="AI Language Translator | CodeAlpha",
    page_icon="🌐",
    layout="centered",
)

# ----------------------------- Styling ---------------------------------
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0;
    }
    .subtitle {
        text-align: center;
        color: #6c757d;
        margin-top: 0.2rem;
        margin-bottom: 1.5rem;
    }
    .stTextArea textarea { font-size: 1.05rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<p class="main-title">🌐 AI Language Translation Tool</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Translate text between 100+ languages instantly — CodeAlpha AI Internship Project</p>',
    unsafe_allow_html=True,
)

# ----------------------------- Languages --------------------------------


@st.cache_data(show_spinner=False)
def get_supported_languages():
    """Return {Language Name: code} dict of supported languages."""
    langs = GoogleTranslator().get_supported_languages(as_dict=True)
    # Capitalize names for a cleaner UI
    return {name.title(): code for name, code in langs.items()}


LANGUAGES = get_supported_languages()
LANG_NAMES = sorted(LANGUAGES.keys())

# ----------------------------- Session state ----------------------------
if "src_lang" not in st.session_state:
    st.session_state.src_lang = "Auto Detect"
if "tgt_lang" not in st.session_state:
    st.session_state.tgt_lang = "Urdu" if "Urdu" in LANGUAGES else LANG_NAMES[0]
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""


def swap_languages():
    """Swap source and target languages (only when source is not auto)."""
    if st.session_state.src_lang != "Auto Detect":
        st.session_state.src_lang, st.session_state.tgt_lang = (
            st.session_state.tgt_lang,
            st.session_state.src_lang,
        )


# ----------------------------- Language selectors -----------------------
col1, col2, col3 = st.columns([5, 1, 5])

with col1:
    src_lang = st.selectbox(
        "From (Source Language)",
        ["Auto Detect"] + LANG_NAMES,
        key="src_lang",
    )

with col2:
    st.write("")
    st.write("")
    st.button("🔄", on_click=swap_languages, help="Swap languages", use_container_width=True)

with col3:
    tgt_lang = st.selectbox(
        "To (Target Language)",
        LANG_NAMES,
        key="tgt_lang",
    )

# ----------------------------- Input ------------------------------------
text_input = st.text_area(
    "Enter text to translate",
    height=150,
    placeholder="Type or paste your text here...",
)

translate_btn = st.button("🚀 Translate", type="primary", use_container_width=True)

# ----------------------------- Translation ------------------------------
if translate_btn:
    if not text_input.strip():
        st.warning("⚠️ Please enter some text to translate.")
    else:
        try:
            source_code = "auto" if src_lang == "Auto Detect" else LANGUAGES[src_lang]
            target_code = LANGUAGES[tgt_lang]

            with st.spinner("Translating..."):
                translator = GoogleTranslator(source=source_code, target=target_code)
                st.session_state.translated_text = translator.translate(text_input)
        except Exception as exc:
            st.error(f"❌ Translation failed: {exc}")
            st.info("Please check your internet connection and try again.")

# ----------------------------- Output -----------------------------------
if st.session_state.translated_text:
    st.subheader(f"✅ Translation ({tgt_lang})")

    # st.code gives a built-in copy button in the top-right corner
    st.code(st.session_state.translated_text, language=None)

    # ------------------------- Text to Speech ---------------------------
    target_code = LANGUAGES[tgt_lang]
    if target_code in tts_langs():
        if st.button("🔊 Listen to translation"):
            try:
                with st.spinner("Generating audio..."):
                    tts = gTTS(text=st.session_state.translated_text, lang=target_code)
                    audio_buffer = io.BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                st.audio(audio_buffer, format="audio/mp3")
            except Exception as exc:
                st.error(f"❌ Audio generation failed: {exc}")
    else:
        st.caption("🔇 Text-to-speech is not available for this language.")

# ----------------------------- Footer -----------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit & deep-translator | CodeAlpha AI Internship — Task 1")
