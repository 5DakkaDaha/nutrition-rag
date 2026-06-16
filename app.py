import streamlit as st
import chromadb
import google.generativeai as genai

# Sayfa ayarları
st.set_page_config(
    page_title="Sağlıklı Beslenme Bilgi Asistanı",
    page_icon="🥗"
)

st.title("🥗 Yapay Zekâ Destekli Sağlıklı Beslenme Bilgi Asistanı")

# Gemini API anahtarı
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error(
        "Gemini API anahtarı bulunamadı.\n"
        "Streamlit Cloud > Settings > Secrets kısmına ekleyin."
    )
    st.stop()

# Gemini yapılandırması
genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")

# Sohbet geçmişi
if "history" not in st.session_state:
    st.session_state.history = []

# ChromaDB bağlantısı
try:
    client = chromadb.PersistentClient(path="vector_db")
    collection = client.get_collection("nutrition_docs")
except:
    st.error(
        "vector_db klasörü veya nutrition_docs koleksiyonu bulunamadı."
    )
    st.stop()

# Kullanıcı sorusu
question = st.text_input(
    "Beslenme hakkında sorunuzu yazın:"
)

if st.button("Sor"):

    if question.strip() == "":
        st.warning("Lütfen bir soru girin.")

    else:

        try:
            # RAG
            results = collection.query(
                query_texts=[question],
                n_results=3
            )

            context = "\n\n".join(
                results["documents"][0]
            )

            prompt = f"""
Sen sağlıklı beslenme konusunda yardımcı olan bir yapay zekâ asistanısın.

Aşağıdaki bilgileri kullanarak kullanıcının sorusunu cevapla.

Bilgiler:
{context}

Kullanıcının sorusu:
{question}

Kurallar:
- Cevabı Türkçe ver.
- Açık ve anlaşılır ol.
- Sadece verilen bilgilerden yararlan.
- Tıbbi teşhis koyma.
- Eğer yeterli bilgi yoksa:
'Bu konuda elimde yeterli bilgi bulunmamaktadır.'
şeklinde cevap ver.
"""

            response = model.generate_content(prompt)

            answer = response.text

        except Exception as e:

            answer = f"Hata oluştu: {e}"

        st.session_state.history.append(
            {
                "question": question,
                "answer": answer
            }
        )

# Sohbet geçmişi
if st.session_state.history:

    st.subheader("💬 Sohbet Geçmişi")

    for chat in reversed(st.session_state.history):

        st.markdown(
            f"**❓ Soru:** {chat['question']}"
        )

        st.markdown(
            f"**🥗 Cevap:** {chat['answer']}"
        )

        st.divider()