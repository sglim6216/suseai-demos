import gradio as gr
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_community.chat_message_histories import SQLChatMessageHistory

def get_ollama_models():
    """
    Get the list of available models from the Ollama API.
    """
    import requests
    response = requests.get("http://localhost:11434/v1/models")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch models from Ollama API")
# Get the list of available models
models = get_ollama_models()



model_name = "gemma3:1b-it-qat"

llm = ChatOllama(model=model_name)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You're an assistant who's good at {ability}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

chain = prompt | llm.bind(stop=["<|eot_id|>"]) | StrOutputParser()

with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///sqlite.db"
    ),
    input_messages_key="question",
    output_messages_key="output",
    history_messages_key="history"
)

def chatbot(input_value, history):
    response = with_message_history.stream(
            {"ability": "everything", "question": input_value},
            config={"configurable": {"session_id": os.getsid(0)}},
            )
    full_response = ''
    for item in response:
        full_response += item
        yield full_response
    yield full_response

iface = gr.ChatInterface(fn=chatbot, title="🦙💬 Chatbot using Gemma3 via Ollama")
iface.launch(inbrowser=True)

