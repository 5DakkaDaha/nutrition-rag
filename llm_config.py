import streamlit as st
import google.generativeai as genai

LLM_NAME = "Gemini"

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def generate_answer(prompt):

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        return f"Hata oluştu: {e}"