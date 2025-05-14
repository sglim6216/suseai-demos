import gradio as gr
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
import os
from langchain_community.chat_message_histories import SQLChatMessageHistory
import mlflow
import time

import mlflow.openai
import mlflow.tracking

# Enable auto-tracing for OpenAI
mlflow.openai.autolog(log_models=True, log_traces=True)
mlflow.enable_system_metrics_logging()


with mlflow.start_run() as run:
    time.sleep(15)

tags= {
    "model": "gemma3:1b-it-qat",
    "platform": "suse-ai"
}


# Optional: Set a tracking URI and an experiment
mlflow.set_tracking_uri("http://192.168.64.11:5000")
mlflow.set_experiment("Default")
mlflow.set_experiment_tag("platform", "suse-ai-chat")
mlflow.set_tags(tags=tags)

model_name = "gemma3:1b-it-qat"

llm = ChatOllama(base_url="http://192.168.64.11:31434",model=model_name)

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

@mlflow.trace
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

