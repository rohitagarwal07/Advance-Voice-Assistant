import streamlit as st
import speech_to_text
import pdf_generator
import database
import base64

# ---------- Set Background ----------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.3);
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background_image.jpg")

# ---------- Page Config ----------
st.set_page_config(page_title="Speech Recognition")

# ---------- Title ----------
st.markdown(
    """
    <h1 style="
        color: #ffffff;
        text-align: left;
        margin-bottom: 10px;
    ">
        🎙️ Speak and Convert to Text
    </h1>
    """,
    unsafe_allow_html=True
)

# ---------- Initialize DB & Session ----------
database.init_db()
if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""

# ---------- Row: Checkbox + Label ----------
col1, col2 = st.columns([0.05, 0.95])
with col1:
    save_as_pdf = st.checkbox("", key="save_pdf")
with col2:
    st.markdown(
        "<p style='color: white; padding-top: 8px; margin: 0 0 0 4px;'>"
        "Save the recognized text as a PDF</p>",
        unsafe_allow_html=True
    )

# ---------- Custom CSS for Start Button ----------
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #ff7043 !important;
        color: white !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.9rem !important;
        border: none !important;
        border-radius: 6px !important;
        width: auto !important;
        min-width: 180px !important;
        max-width: 250px !important;
    }
    .stButton>button:hover {
        background-color: #e64a19 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------- Start Recording Button (Next Line) ----------
start = st.button("🎙️ Start Recording")

# ---------- Recording Logic ----------
if start:
    with st.spinner("🎤 Listening..."):
        text = speech_to_text.recognize_speech()
        st.session_state.recognized_text = text

        if save_as_pdf:
            pdf_path = pdf_generator.save_text_as_pdf(text)
            database.insert_record(text, pdf_path)
            st.success("✅ Speech converted and saved as PDF.")
            st.info(f"📄 PDF saved at: {pdf_path}")
        else:
            database.insert_record(text, None)
            st.success("✅ Speech converted successfully (not saved as PDF).")

# ---------- Recognized Text Header ----------
st.markdown(
    "<h3 style='color: #e0ffff; margin-top: 25px;'>📝 Recognized Text:</h3>",
    unsafe_allow_html=True
)

# ---------- Display Recognized Text with Custom Background ----------
st.markdown(
    f"""
    <textarea readonly
        style="
            background-color: rgba(255, 255, 255, 0.2);
            color: #ffffff;
            width: 100%;
            height: 200px;
            border-radius: 6px;
            border: 1px solid #cccccc;
            padding: 10px;
            font-size: 16px;
            font-family: 'Courier New', monospace;
            resize: none;
        "
    >{st.session_state.recognized_text}</textarea>
    """,
    unsafe_allow_html=True
)
