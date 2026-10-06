from src.llm.model_loader import (
    load_client,
    HF_MODEL_ID,
    HF_PROVIDER,
    HF_MAX_TOKENS,
    HF_TEMPERATURE,
)


print("=== GenAIOps Model Loader Test ===")

print(f"Model       : {HF_MODEL_ID}")
print(f"Provider    : {HF_PROVIDER}")
print(f"Max tokens  : {HF_MAX_TOKENS}")
print(f"Temperature : {HF_TEMPERATURE}")

client = load_client()

print(f"Client type : {type(client)}")

print("\nMODEL LOADER OK")