import argparse
import ollama
import mlflow


parser=argparse.ArgumentParser()
parser.add_argument("--version")
args=parser.parse_args()

client= ollama.Client("http://192.168.64.14:31434")
mlflow.set_tracking_uri("http://192.168.64.14:5000")

target_text = """
MLflow is an open source platform for managing the end-to-end machine learning lifecycle.
It tackles four primary functions in the ML lifecycle: Tracking experiments, packaging ML
code for reuse, managing and deploying models, and providing a central model registry.
MLflow currently offers these functions as four components: MLflow Tracking,
MLflow Projects, MLflow Models, and MLflow Registry.
"""

# Load the prompt
prompt = mlflow.load_prompt("prompts:/summarization-prompt/" + args.version)


response = client.chat(
    messages=[
        {
            "role": "user",
            "content": prompt.format(num_sentences=1, sentences=target_text),
        }
    ],
    model="qwen3:0.6b",
)

print(f"User asked: " + target_text)
print("=====")
print ("")
print(f"Assistant answer: "+ response.message.content)