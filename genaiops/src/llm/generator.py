from src.llm.model_loader import (
    load_client,
    HF_MODEL_ID,
    HF_MAX_TOKENS,
    HF_TEMPERATURE,
)


def generate_interpretation( messages: list[dict]) -> str:
    """
    Generate an interpretation using the configured
    Hugging Face conversational model.
    """

    if not messages:
        raise ValueError(
            "Messages cannot be empty."
        )

    client = load_client()

    response = client.chat.completions.create(
        model=HF_MODEL_ID,
        messages=messages,
        max_tokens=HF_MAX_TOKENS,
        temperature=HF_TEMPERATURE
    )

    answer = response.choices[0].message.content

    if not answer:
        raise RuntimeError(
            "The Hugging Face model returned "
            "an empty response."
        )

    return answer.strip()