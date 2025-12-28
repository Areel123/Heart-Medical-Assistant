import faiss
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer("all-MiniLM-L6-v2")

INDEX_PATH = "rag/faiss.index"
DOCS_PATH = "rag/medical_docs"

# Load ONCE
index = faiss.read_index(INDEX_PATH)

documents = []
for file in os.listdir(DOCS_PATH):
    with open(os.path.join(DOCS_PATH, file), "r", encoding="utf-8") as f:
        documents.append(f.read())

def retrieve_context(query, top_k=2):
    query_vec = model.encode([query])
    _, indices = index.search(query_vec, top_k)

    context = []
    for i in indices[0]:
        if i >= 0:
            context.append(documents[i])

    return "\n".join(context)
