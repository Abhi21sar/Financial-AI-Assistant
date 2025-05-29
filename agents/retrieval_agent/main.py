from fastapi import FastAPI, Query, Body
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

app = FastAPI()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# In-memory store
corpus = []
corpus_ids = []
dimension = 384
index = faiss.IndexFlatL2(dimension)  # L2 distance index

@app.get("/")
def root():
    return {"message": "Retrieval Agent is running."}

@app.post("/add_documents")
def add_documents(
    docs: list[str] = Body(..., description="List of documents to embed and store")
):
    global corpus, corpus_ids
    embeddings = model.encode(docs)
    index.add(np.array(embeddings))
    start_idx = len(corpus)
    corpus += docs
    corpus_ids += list(range(start_idx, start_idx + len(docs)))
    return {"message": f"{len(docs)} documents added to index."}

@app.get("/query")
def query_top_k(
    query: str = Query(...), k: int = Query(3)
):
    if len(corpus) == 0:
        # fallback: mock results when index is empty
        return {"query": query, "results": ["Mock doc 1", "Mock doc 2", "Mock doc 3"]}

    query_embedding = model.encode([query])
    D, I = index.search(np.array(query_embedding), k)

    if I is None or len(I) == 0 or len(I[0]) == 0:
        return {"query": query, "results": []}

    results = []
    for i in I[0]:
        if 0 <= i < len(corpus):
            results.append(corpus[i])

    return {"query": query, "results": results}
