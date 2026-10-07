import pandas as pd
from fastapi import (FastAPI,  HTTPException)
from src.api.schemas import (
    InterpretationRequest,
    InterpretationResponse,
)
from src.processing.dataframe_summary import (
    summarize_prediction_dataframe,
)

from src.prompts.interpretation import (
    build_interpretation_messages,
)

from src.llm.generator import (
    generate_interpretation,
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Malaria Supply Chain GenAIOps API",
    description=(
        "GenAI interpretation service for malaria "
        "supply-chain prediction results."
    ),
    version="1.0.0"
)


@app.get("/health")
def health():
    """
    Check whether the GenAIOps API is running.
    """

    return {
        "status": "healthy",
        "service": "genaiops"
    }


# ==========================================
# Interpretation
# ==========================================

@app.post(
    "/interpret",
    response_model=InterpretationResponse
)
def interpret(
    request: InterpretationRequest
):

    try:

        # ----------------------------------
        # 1. Convert validated API records
        #    to Python dictionaries
        # ----------------------------------
        logger.info(
                 "1. Convert validated API records"
            )
        records = [
            record.model_dump()
            for record in request.records
        ]


        # ----------------------------------
        # 2. Same DataFrame as your
        #    successful integration test
        # ----------------------------------
        logger.info("2. Same DataFrame as your successful integration test")
        df_engineered = pd.DataFrame(
            records
        )


        # ----------------------------------
        # 3. Deterministic analysis
        # ----------------------------------
        logger.info("3. Deterministic analysis")
        summary = (
            summarize_prediction_dataframe(
                df_engineered
            )
        )


        # ----------------------------------
        # 4. Controlled prompt
        # ----------------------------------
        logger.info(" 4. Controlled prompt")
        #print(request.prompt)
        messages = (
            build_interpretation_messages(
                summary=summary,
                user_prompt=request.prompt
            )
        )


        # ----------------------------------
        # 5. LLM interpretation
        # ----------------------------------

        interpretation = (
            generate_interpretation(
                messages
            )
        )


        # ----------------------------------
        # 6. Response
        # ----------------------------------

        return InterpretationResponse(
            records_analyzed=len(
                df_engineered
            ),
            interpretation=interpretation
        )


    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )


    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=(
                "Interpretation generation "
                f"failed: {str(exc)}"
            )
        )