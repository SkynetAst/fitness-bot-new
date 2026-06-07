import os
import pathlib
import numpy as np
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

_KB_PATH = pathlib.Path(__file__).parent / "knowledge_base.txt"
_EMBED_MODEL = "models/gemini-embedding-001"


def _load_chunks() -> list[str]:
    text = _KB_PATH.read_text(encoding="utf-8")
    return [c.strip() for c in text.split("\n\n") if c.strip()]


_chunks = _load_chunks()
_doc_embeddings = np.array(
    genai.embed_content(
        model=_EMBED_MODEL,
        content=_chunks,
        task_type="RETRIEVAL_DOCUMENT",
    )["embedding"]
)


def search(query: str, top_k: int = 3) -> list[str]:
    q_emb = np.array(
        genai.embed_content(
            model=_EMBED_MODEL,
            content=query,
            task_type="RETRIEVAL_QUERY",
        )["embedding"]
    )
    scores = _doc_embeddings @ q_emb / (
        np.linalg.norm(_doc_embeddings, axis=1) * np.linalg.norm(q_emb)
    )
    top_idx = np.argsort(scores)[::-1][:top_k]
    return [_chunks[i] for i in top_idx]
