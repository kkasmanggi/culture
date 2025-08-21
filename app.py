import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# PENGATURAN API KEY DAN MODEL
# ==============================================================================

# Gunakan Streamlit Secrets untuk menyimpan API Key dengan aman
# Buka menu hamburger di sidebar Streamlit -> Settings -> Secrets
# Lalu tambahkan: GOOGLE_API_KEY="AIzaSyBWzMBC6hVzvooktYrFkO5fvrDuJKVxqio"
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Nama model Gemini
MODEL_NAME = 'gemini-1.5-flash'

# ==============================================================================
# KONTEKS AWAL CHATBOT
# ==============================================================================
INITIAL_CHATBOT_CONTEXT = [
    {"role": "user", "parts": ["Kamu adalah seorang Budayawan. Tuliskan tentang kebudayaan yang ingin diketahui. Jawaban singkat dan jelas. Tolak pertanyaan selain tentang budaya"]},
    {"role": "model", "parts": ["Baik! Saya akan menjawab tentang budaya!."]}
]

# ==============================================================================
# FUNGSI UTAMA UNTUK MENGHUBUNGKAN DENGAN GEMINI
# ==============================================================================

# Atur konfigurasi API Key
genai.configure(api_key=API_KEY)

# Buat model generatif
model = genai.GenerativeModel(
    MODEL_NAME,
    generation_config=genai.types.GenerationConfig(
        temperature=0.4,
        max_output_tokens=500
    )
)

# Inisialisasi riwayat chat di Streamlit Session State jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = INITIAL_CHATBOT_CONTEXT

# Inisialisasi sesi chat Gemini jika belum ada
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=st.session_state.messages)

# ==============================================================================
# ANTARMUKA STREAMLIT
# ==============================================================================

st.title("🤖 Chatbot Budaya")
st.caption("Sebuah chatbot sederhana yang dibuat dengan Streamlit dan Google Gemini. Bertanya tentang budaya!")

# Tampilkan riwayat chat di layar
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user"):
            st.write(message["parts"][0])
    elif message["role"] == "model":
        with st.chat_message("assistant"):
            st.write(message["parts"][0])

# Tangani input dari pengguna
if prompt := st.chat_input("Apa yang ingin Anda ketahui tentang budaya?"):
    # Tampilkan input pengguna di layar
    with st.chat_message("user"):
        st.write(prompt)
    
    # Tambahkan input pengguna ke riwayat chat
    st.session_state.messages.append({"role": "user", "parts": [prompt]})
    
    # Kirim input pengguna ke Gemini dan dapatkan respons
    try:
        response = st.session_state.chat.send_message(prompt)
        
        # Tampilkan respons dari model di layar
        with st.chat_message("assistant"):
            st.write(response.text)
        
        # Tambahkan respons model ke riwayat chat
        st.session_state.messages.append({"role": "model", "parts": [response.text]})

    except Exception as e:
        st.error(f"Maaf, terjadi kesalahan: {e}")
        st.warning("Penyebab: Masalah koneksi, API Key, atau kuota.")
