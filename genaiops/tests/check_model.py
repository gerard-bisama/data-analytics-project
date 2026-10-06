import os

from dotenv import load_dotenv
from huggingface_hub import model_info


load_dotenv()

MODEL_ID = os.getenv(
    "HF_MODEL_ID",
    "Qwen/Qwen3-4B-Instruct-2507"
)

print("Model:", MODEL_ID)

info = model_info(
    MODEL_ID,
    expand="inferenceProviderMapping"
)

providers = info.inference_provider_mapping

print("\nAvailable inference providers:")

if providers:
    for provider in providers:
        print(
            f"- {provider.provider}: "
            f"{provider.status} "
            f"({provider.task})"
        )
else:
    print(
        "No Inference Provider currently available."
    )