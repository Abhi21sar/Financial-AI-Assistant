from fastapi import FastAPI, Body
from openai import OpenAI
import os

app = FastAPI()

# Load your OpenAI API key from environment
#openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt template
TEMPLATE = """
You are a financial assistant. Based on the following market documents and user question, generate a concise spoken market brief.

Context:
{context}

Question:
{question}

Answer in 2-3 sentences.
"""

@app.get("/")
def root():
    return {"message": "LLM Agent is running"}

@app.post("/generate_brief")
def generate_brief(
    question: str = Body(...),
    context_docs: list[str] = Body(...)
):
    context = "\n".join(context_docs)
    prompt = TEMPLATE.format(context=context, question=question)

    try:
        openai_client = OpenAI(api_key="your_openai_api_key_here")  # Replace with your OpenAI API key
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        brief = response.choices[0].message.content
        return {"brief": brief.strip()}
    except Exception as e:
        return {"error": str(e)}
