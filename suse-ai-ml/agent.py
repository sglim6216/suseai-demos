"""Run this model in Python

> pip install openai
"""
from openai import OpenAI
import mlflow
# Enable auto-tracing for OpenAI
mlflow.openai.autolog()

# Optional: Set a tracking URI and an experiment
mlflow.set_tracking_uri("http://192.168.64.11:5000")
mlflow.set_experiment("Ollama")

client = OpenAI(
    base_url = "http://192.168.64.11:31434/v1",
    api_key = "unused", # required for the API but not used
)

response = client.chat.completions.create(
    messages = [
        {
            "role": "system",
            "content": "Your task is to take the text provided and rewrite it in a way that is easy for young learners in grades 3-5 to read and understand. Simplify advanced vocabulary, break down long sentences, explain difficult concepts in plain language, and present the information in a clear, engaging way. The short rewritten text should convey the core ideas of the original text in an age-appropriate manner.",
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "The mitochondria, often referred to as the powerhouses of the cell, are essential organelles that play a crucial role in the production of adenosine triphosphate (ATP) through the process of cellular respiration. ATP is the primary energy currency of the cell, enabling various cellular functions and biochemical reactions to occur.",
                },
            ],
        },
    ],
    model = "gemma3:1b-it-qat",
    max_tokens = 4096,
)

print(response.choices[0].message.content)