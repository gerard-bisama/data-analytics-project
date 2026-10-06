import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient


# Load environment variables from .env
load_dotenv()


# Hugging Face configuration
HF_TOKEN = os.getenv("HF_TOKEN")

HF_MODEL_ID = os.getenv(
    "HF_MODEL_ID",
    "openai/gpt-oss-20b"
)

HF_PROVIDER = os.getenv(
    "HF_PROVIDER",
    "auto"
)

HF_MAX_TOKENS = int(
    os.getenv("HF_MAX_TOKENS", "500")
)

HF_TEMPERATURE = float(
    os.getenv("HF_TEMPERATURE", "0.1")
)


def validate_configuration():
    """
    Validate required Hugging Face configuration.
    """

    if not HF_TOKEN:
        raise ValueError(
            "HF_TOKEN is not defined. "
            "Configure it in the .env file."
        )

    if not HF_MODEL_ID:
        raise ValueError(
            "HF_MODEL_ID is not defined."
        )


def load_client():
    """
    Initialize and return a Hugging Face InferenceClient.
    """

    validate_configuration()

    client = InferenceClient(
        provider=HF_PROVIDER,
        api_key=HF_TOKEN
    )

    return client