from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.rag_service import RAGService


app = FastAPI()
rag_service: Optional[RAGService] = None

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("templates/index.html")


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1
    )

    top_k: Optional[int] = Field(
        default=None,
        ge=1,
        le=50,
    )

    source: Optional[str] = None


@app.on_event("startup")
def startup() -> None:
    global rag_service

    try:
        rag_service = RAGService()
        print("RAG service started successfully.")

    except Exception as exc:
        print(f"Failed to start RAG service: {exc}")
        rag_service = None


@app.get("/health")
def health():
    if rag_service is None:
        return {
            "status": "starting"
        }

    return {
        "status": "ok",
        "indexed_chunks": rag_service.store.count(),
    }


@app.post("/rag/query")
def query_rag(
    payload: QuestionRequest
):
    if rag_service is None:
        raise HTTPException(
            status_code=503,
            detail="RAG service is not ready.",
        )

    try:
        return rag_service.ask(
            question=payload.question,
            top_k=payload.top_k,
            source=payload.source,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc