import requests
from django.http import JsonResponse
from django.shortcuts import render
from rag.rag_engine import retrieve_context

OLLAMA_URL = "http://localhost:11434/api/generate"

def home(request):
    return render(request, "chat/index.html")

def chat_api(request):
    question = request.GET.get("message")

    # Initialize memory
    if "history" not in request.session:
        request.session["history"] = []

    history = request.session["history"]

    # Retrieve RAG context
    context = retrieve_context(question)

    # Build conversation text
    conversation = ""
    for turn in history[-4:]:  # last 4 turns only
        conversation += f"User: {turn['user']}\nAssistant: {turn['assistant']}\n"

    prompt = f"""
You are a heart health medical information assistant.
You provide educational information only.
Do NOT diagnose or prescribe medication.

If symptoms suggest emergency, advise seeking immediate medical care.

Previous Conversation:
{conversation}

Medical Context:
{context}

User Question:
{question}

Answer clearly and safely.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": 2048,
                "num_predict": 256
            }
        }
    )

    reply = response.json()["response"]

    # Save memory
    history.append({
        "user": question,
        "assistant": reply
    })
    request.session["history"] = history

    return JsonResponse({"reply": reply})
