import streamlit as st
from promptflow.client import PFClient
from promptflow.entities import AzureOpenAIConnection
from dotenv import load_dotenv
import os

# Wczytanie kluczy API z pliku .env
load_dotenv()

# Inicjalizacja klienta Prompt Flow
pf = PFClient()

try:
    conn = AzureOpenAIConnection(
        name="dl-conn",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_base=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version="2024-02-01"
    )
    pf.connections.create_or_update(conn)
except Exception as e:
    st.error(f"Błąd ładowania kluczy: {e}")

st.set_page_config(page_title="ChatBot")
st.title("Chat")

# Inicjalizacja pamięci historii czatu
if "messages" not in st.session_state:
    st.session_state.messages = []

# Wyświetlanie dotychczasowej rozmowy na ekranie
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Pole tekstowe na dole ekranu
if prompt := st.chat_input("Napisz coś ..."):
    
    # 1. Wyświetlamy to, co wpisał użytkownik
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Format historii dla PromptFlow
    chat_history = []
    for i in range(0, len(st.session_state.messages) - 1, 2):
        if st.session_state.messages[i]["role"] == "user" and st.session_state.messages[i+1]["role"] == "assistant":
            chat_history.append({
                "inputs": {"question": st.session_state.messages[i]["content"]},
                "outputs": {"answer": st.session_state.messages[i+1]["content"]}
            })

    # 3. Wysyłamy zapytanie do modelu (z animacją ładowania)
    with st.chat_message("assistant"):
        result = pf.test(
            flow="my_chat", 
            inputs={
                "question": prompt,
                "chat_history": chat_history
            }
        )
        
        answer_generator = result["answer"]
        answer = st.write_stream(answer_generator)
            
    # 4. Zapisujemy odpowiedź modelu w historii
    st.session_state.messages.append({"role": "assistant", "content": answer})