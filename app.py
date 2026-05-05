import streamlit as st
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN")
)

st.set_page_config(page_title="Visual Business Analyst", layout="wide")

st.title("📊 Visual Business Analyst (HF Version)")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    user_query = st.text_input("Ask a question about the image (optional)")

    if st.button("Analyze Image"):
        with st.spinner("Analyzing..."):

            image_bytes = uploaded_file.read()
            encoded_image = base64.b64encode(image_bytes).decode("utf-8")

            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_query or "Analyze this image"},
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    ]
                }
            ]

            response = client.chat.completions.create(
                model="llava-hf/llava-1.5-7b-hf",
                messages=messages,
                max_tokens=300
            )

            st.markdown("###  Analysis")
            st.write(response.choices[0].message.content)