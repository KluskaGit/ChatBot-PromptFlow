import streamlit as st
from promptflow.client import PFClient
from promptflow.entities import AzureOpenAIConnection
from dotenv import load_dotenv
import os

load_dotenv()

pf = PFClient()

try:
    conn = AzureOpenAIConnection(
        name="dl-conn",
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_base=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version="2024-12-01-preview"
    )
    pf.connections.create_or_update(conn)  # type: ignore
except Exception as e:
    st.error(f"Błąd ładowania kluczy: {e}")

st.set_page_config(page_title="ChatBot Mundial 2026", page_icon="⚽")
st.title("⚽ ChatBot Sportowy - Mundial 2026 🏆")
st.caption("Zapytaj mnie o najświeższe wyniki, składy i ciekawostki z Mistrzostw Świata!")

with st.sidebar:
    st.markdown("### 🏟️ Panel Sterowania")
    st.header("Wybór Modelu")
    dostepne_modele = ["gpt-4.1-mini", "o4-mini"] 
    wybrany_model = st.selectbox("Wybierz model AI:", dostepne_modele)


if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Napisz coś ..."):
    
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    chat_history = []
    for i in range(0, len(st.session_state.messages) - 1, 2):
        if st.session_state.messages[i]["role"] == "user" and st.session_state.messages[i+1]["role"] == "assistant":
            chat_history.append({
                "inputs": {"question": st.session_state.messages[i]["content"]},
                "outputs": {"answer": st.session_state.messages[i+1]["content"]}
            })

    with st.chat_message("assistant"):
        result = pf.test(
            flow="my_chat", 
            inputs={
                "question": prompt,
                "chat_history": chat_history,
                "model_selection": wybrany_model
            }
        )
        
        answer_generator = result["answer"]
        answer = st.write_stream(answer_generator)
            
    st.session_state.messages.append({"role": "assistant", "content": answer})