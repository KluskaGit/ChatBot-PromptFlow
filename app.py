import streamlit as st
from promptflow.client import PFClient
from dotenv import load_dotenv
import os

# Wymuszamy wczytanie pliku .env, ale dodajemy też zabezpieczenie na sztywno
load_dotenv(override=True)

# ---------------- ZABEZPIECZENIE ABSOLUTNE ----------------
# Niezależnie od tego, co system ma w pamięci, nadpisujemy kluczowe zmienne.
# Wskazujemy poprawny zasób, na którym znajduje się klasyczny Agent.
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://mundia-bot-test-resource.openai.azure.com/"
# (Zakładam, że AZURE_OPENAI_API_KEY jest poprawnie w pliku .env)
# ----------------------------------------------------------

@st.cache_resource
def init_pf_client():
    pf_client = PFClient()
    return pf_client

pf = init_pf_client()

st.set_page_config(page_title="Kibic-Bot", page_icon="⚽")
st.title("⚽ Chat: Poradnik Kibica")

with st.sidebar:
    st.header("Opcje")
    if st.button("Wyczyść historię (Nowy wątek)"):
        st.session_state.messages = []
        if "thread_id" in st.session_state:
            del st.session_state["thread_id"]
        st.rerun()

# Inicjalizacja pamięci historii czatu
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie dotychczasowej rozmowy na ekranie
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Pole tekstowe na dole ekranu
if prompt := st.chat_input("Napisz coś o piłce nożnej..."):
    
    # 1. Wyświetlamy to, co wpisał użytkownik
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Pobieramy ID wątku z sesji, jeśli już istnieje
    thread_id = st.session_state.get("thread_id", "")
    
    # 3. NA SZTYWNO WPISANE ID NOWEGO, POPRAWNEGO AGENTA (zamiast pobierania z .env)
    agent_id = "asst_2u6X9ZnTysgj4CQYiTngtrME"

    # 4. Wysyłamy zapytanie do modelu
    with st.chat_message("assistant"):
        try:
            result = pf.test(
                flow="my_chat", 
                inputs={
                    "question": prompt,
                    "thread_id": thread_id,
                    "agent_id": agent_id
                }
            )
            
            # PromptFlow z Agentem zwróci gotowy tekst i ID wątku
            answer = result["answer"]
            st.markdown(answer)
            
            if result.get("thread_id"):
                st.session_state.thread_id = result["thread_id"]
                
            # Zapisujemy odpowiedź modelu w historii
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Wystąpił błąd podczas generowania odpowiedzi: {e}")
            st.session_state.messages.pop()  # Usuwamy nieudane zapytanie usera z historii