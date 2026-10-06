import json


SYSTEM_PROMPT = """
You are a data interpretation assistant specialized in
public-health supply chain analytics.

Your role is to interpret malaria commodity prediction
results that have already been calculated by a machine
learning model.

Rules:

1. Use only the data and statistics provided in the
   analytical context.

2. Never invent facilities, products, quantities,
   percentages, trends, or other facts.

3. Do not modify or recalculate the machine-learning
   predictions.

4. Clearly distinguish factual observations from
   interpretation.

5. When discussing quantities, use the exact values
   provided in the analytical context.

6. If the available data is insufficient to answer the
   user's question, explicitly state that the available
   data does not support the requested conclusion.

7. Focus on operationally useful supply-chain insights.

8. Keep the interpretation concise unless the user
   explicitly requests a detailed analysis.
""".strip()

def build_interpretation_messages(summary: dict,user_prompt: str) -> list[dict]:
    """
    Build controlled chat messages for interpretation.
    """

    if not user_prompt.strip():
        raise ValueError(
            "User prompt cannot be empty."
        )

    summary_json = json.dumps(
        summary,
        indent=2,
        ensure_ascii=False,
        default=str
    )

    context_message = f"""
Below is the analytical context generated deterministically
from the malaria prediction dataset.

ANALYTICAL CONTEXT:

{summary_json}

USER REQUEST:

{user_prompt}

Interpret the results according to the system rules in 
max 250 words and don't include summary tables in the reponse.
""".strip()

    return [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": context_message
        }
    ]