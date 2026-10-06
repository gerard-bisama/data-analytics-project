import pandas as pd

from src.processing.dataframe_summary import (
    summarize_prediction_dataframe
)

from src.prompts.interpretation import (
    build_interpretation_messages
)

from src.llm.generator import (
    generate_interpretation
)
from tests.sample_data import (generate_sample_dataframe)





# ---------------------------------
# Step 1: DataFrame
# ---------------------------------

df = generate_sample_dataframe(number_of_records=20,seed=42)


# ---------------------------------
# Step 2: Deterministic analysis
# ---------------------------------

summary = summarize_prediction_dataframe(df)

print("\n=== DATA SUMMARY ===")
#print(summary)

# ---------------------------------
# Step 3: Controlled prompt
# ---------------------------------

messages = build_interpretation_messages(
    summary=summary,
    user_prompt=(
        "Provide a concise management interpretation "
        "of the main supply situation in this dataset."
    )
)

# ---------------------------------
# Step 4: LLM interpretation
# ---------------------------------

print("\nSending analytical context to Hugging Face...")

interpretation = generate_interpretation(
    messages
)

print("\n=== GENAI INTERPRETATION ===")
print(interpretation)