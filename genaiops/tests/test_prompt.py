from src.prompts.interpretation import (
    build_interpretation_messages
)


summary = {
    "records_analyzed": 10,

    "prediction_statistics": {
        "total_predicted_quantity": 2500,
        "average_predicted_quantity": 250,
        "maximum_predicted_quantity": 700
    },

    "stock_status_distribution": [
        {
            "stock_status": "Stockout",
            "records": 3,
            "percentage": 30
        }
    ]
}


messages = build_interpretation_messages(
    summary=summary,
    user_prompt=(
        "Provide a short management summary "
        "of the main supply risks."
    )
)


for message in messages:

    print(
        f"\n--- {message['role'].upper()} ---"
    )

    print(message["content"])