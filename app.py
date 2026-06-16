import streamlit as st
import chromadb
import google.generativeai as genai

# Sayfa ayarları
st.set_page_config(
    page_title="Beslenme Bilgi Asistanı",
    page_icon="🥗"
)

st.title("🥗 Sağlıklı Beslenme Bilgi Asistanı")

# Çalışma modu seçimi
mode = st.radio(
    "Sistem Modu",
    [
        "RAG",
        "RAG + LLM"
    ]
)

# Gemini ayarı
if mode == "RAG + LLM":

    genai.configure(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

    model = genai.GenerativeModel(
        "gemini-2.5-flash"
    )

# ChromaDB bağlantısı
client = chromadb.PersistentClient(
    path="vector_db"
)

collection = client.get_collection(
    "nutrition_docs"
)

# Sohbet geçmişi
if "history" not in st.session_state:
    st.session_state.history = []

# Kullanıcı sorusu
question = st.text_input(
    "Beslenme hakkında soru sor:"
)

if st.button("Sor"):

    if question.strip() == "":

        st.warning(
            "Lütfen bir soru giriniz."
        )

    else:

        # RAG kısmı
        results = collection.query(
            query_texts=[question],
            n_results=3
        )

        context = "\n\n".join(
            results["documents"][0]
        )

        # SADECE RAG
        if mode == "RAG":

            answer = context

        # RAG + LLM
        else:

            prompt = f"""
Sen beslenme konusunda uzman bir asistansın.

Aşağıdaki bilgileri kullanarak soruyu cevapla.

Bilgiler:
{context}

Soru:
{question}

Kurallar:
- Türkçe cevap ver.
- Açık ve anlaşılır ol.
- Sadece verilen bilgileri kullan.
- Bilgi yoksa:
'Bu konuda elimde yeterli bilgi bulunmamaktadır.'
de.
"""

            response = model.generate_content(
                prompt
            )

            answer = response.text

        st.session_state.history.append(
            {
                "mode": mode,
                "question": question,
                "answer": answer
            }
        )

# Sohbet geçmişi
if st.session_state.history:

    st.subheader(
        "💬 Sohbet Geçmişi"
    )

    for chat in reversed(
        st.session_state.history
    ):

        st.markdown(
            f"**Mod:** {chat['mode']}"
        )

        st.markdown(
            f"**❓ Soru:** {chat['question']}"
        )

        st.markdown(
            f"**🥗 Cevap:** {chat['answer']}"
        )

        st.divider()