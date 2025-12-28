import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DOCS_PATH = "rag/medical_docs"
INDEX_PATH = "rag/faiss.index"

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = []
for file in os.listdir(DOCS_PATH):
    with open(os.path.join(DOCS_PATH, file), "r", encoding="utf-8") as f:
        documents.append(f.read())

embeddings = model.encode(documents, convert_to_numpy=True)

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)

print("Medical FAISS index created")
