import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load configuration from .env
load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_ID = os.getenv(
    "HF_MODEL_ID",
    "openai/gpt-oss-20b"
)
PROVIDER = os.getenv(
    "HF_PROVIDER",
    "auto"
)


# Validate configuration
if not HF_TOKEN:
    raise ValueError(
        "HF_TOKEN is not defined in the .env file."
    )


print("=== Hugging Face Inference Test ===")
print(f"Model    : {MODEL_ID}")
print(f"Provider : {PROVIDER}")
print()


# Initialize Hugging Face client
client = InferenceClient(
    provider=PROVIDER,
    api_key=HF_TOKEN
)


# Simple test message
messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful supply chain data analyst. "
            "Answer clearly and concisely."
        )
    },
    {
        "role": "user",
        "content": (
            "Explain in no more than three sentences what "
            "a stockout means in a medical supply chain."
        )
    }
]


print("Sending request to Hugging Face...")


response = client.chat.completions.create(
    model=MODEL_ID,
    messages=messages,
    max_tokens=200,
    temperature=0.1
)


answer = response.choices[0].message.content


print("\n=== Model Response ===")
print(answer)

print("\n=== Test completed successfully ===")