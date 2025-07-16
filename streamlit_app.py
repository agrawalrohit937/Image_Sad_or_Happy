import streamlit as st
from utils import predict_emotion
from PIL import Image, UnidentifiedImageError
import io
import random
import base64

# Configuration
st.set_page_config(page_title="Emotion Detector", page_icon="🧠", layout="centered")

# Quotes for emotions
quotes = {
    "Happy 😊": [
        "Happiness is not by chance, but by choice.",
        "Smiles are contagious – keep spreading them!",
        "Enjoy the little things, for one day you'll look back and realize they were the big things."
    ],
    "Sad 😢": [
        "Tears come from the heart, not from the brain.",
        "Sometimes it's okay to not be okay.",
        "Out of difficulties grow miracles."
    ]
}

# Custom CSS
st.markdown("""
    <style>
    .title {
        font-size: 42px;
        font-weight: 700;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 20px;
        color: #333;
        text-align: center;
        margin-bottom: 30px;
    }
    .result {
        font-size: 30px;
        font-weight: bold;
        color: #2196F3;
        text-align: center;
        margin-top: 20px;
    }
    .quote {
        font-size: 22px;
        font-weight: 600;
        color: #222;
        background-color: #f0f0f0;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        text-align: center;
        border-left: 6px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="title">🧠 Emotion Prediction from Image</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Upload an image and let the AI guess the emotion!</div>', unsafe_allow_html=True)

# Upload
uploaded_file = st.file_uploader("Upload your image (jpg/jpeg/png)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        image = Image.open(uploaded_file).convert('RGB')
        # st.image(image, caption="Uploaded Image", use_container_width=True)
        st.image(image, caption="Uploaded Image", width=300)

        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        with st.spinner("Predicting emotion..."):
            prediction = predict_emotion(img_bytes)

        st.markdown(f'<div class="result">🎯 Detected Emotion: {prediction}</div>', unsafe_allow_html=True)

        # Get quote
        quote_list = quotes.get(prediction, [])
        quote = random.choice(quote_list) if quote_list else "No quote available."

        # Display quote
        st.markdown(f'''
            <div class="quote">“{quote}”</div>
        ''', unsafe_allow_html=True)

        # Background audio (hidden)
        audio_file = f"assets/{prediction.split()[0].lower()}.mp3"
        with open(audio_file, "rb") as file:
            audio_bytes = file.read()
            b64 = base64.b64encode(audio_bytes).decode()
            audio_tag = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_tag, unsafe_allow_html=True)

    except UnidentifiedImageError:
        st.error("❌ Could not identify the image. Please upload a valid JPG or PNG.")
    except Exception as e:
        st.error(f"⚠️ Unexpected error: {e}")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by Rohit Agrawal")
