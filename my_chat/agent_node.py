from promptflow import tool
from openai import AzureOpenAI
import os

@tool
def call_agent(question: str, thread_id: str, agent_id: str) -> dict:
    client = AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version="2024-05-01-preview",
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
    )
    
    # Tworzenie nowego wątku, jeśli to pierwsza wiadomość w sesji
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
        
    # Rejestracja pytania użytkownika w wątku
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question
    )
    
    # Uruchomienie Agenta (używamy `create_and_poll`, by asynchronicznie poczekać na wynik)
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id,
        assistant_id=agent_id
    )
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        answer = ""
        for content_block in messages.data[0].content:
            if content_block.type == 'text':
                answer += content_block.text.value
    else:
        answer = f"Wystąpił błąd: status uruchomienia to {run.status}"
        
    return {"answer": answer, "thread_id": thread_id}