from tests.sample_data import (
    generate_sample_dataframe
)

from src.processing.dataframe_summary import (
    summarize_prediction_dataframe
)

from src.prompts.interpretation import (
    build_interpretation_messages
)

from src.llm.generator import (
    generate_interpretation
)


# ==========================================
# 1. Generate 20 synthetic records
# ==========================================

df = generate_sample_dataframe(
    number_of_records=20,
    seed=42
)


print("\n=== SAMPLE DATA ===")

print(
    df[
        [
            "index",
            "product_group",
            "facility_type",
            "zone_type",
            "stock_status",
            "months_of_stock",
            "amc",
            "predicted_ordered_quantity"
        ]
    ].to_string(index=False)
)


# ==========================================
# 2. Deterministic summarization
# ==========================================

summary = summarize_prediction_dataframe(df)


print("\n=== DETERMINISTIC SUMMARY ===")

print(summary)


# ==========================================
# 3. Controlled prompt
# ==========================================

messages = build_interpretation_messages(
    summary=summary,
    user_prompt=(
        "Provide a management-level interpretation "
        "of these malaria commodity order predictions. "
        "Identify the most important supply risks, "
        "stock concerns and ordering priorities. "
        "Do not introduce information that is not "
        "contained in the analytical context."
    )
)


# ==========================================
# 4. Hugging Face inference
# ==========================================

print(
    "\nSending analytical context "
    "to Hugging Face..."
)

interpretation = generate_interpretation(
    messages
)


# ==========================================
# 5. Basic output validation
# ==========================================

assert interpretation is not None
assert isinstance(interpretation, str)
assert len(interpretation.strip()) > 0


print("\n=== GENAI INTERPRETATION ===")

print(interpretation)


print(
    "\nDATAFRAME -> INTERPRETATION "
    "PIPELINE PASSED"
)