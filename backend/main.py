# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import our knowledge base functions
from knowledge_base import sync_knowledge_base, query_knowledge_base
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# Initialize the LLM you want to use for the final answer synthesis
# This could be from TRAE's SDK or another provider like OpenAI
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# This is the prompt template that instructs the AI how to behave
PROMPT_TEMPLATE = """
Answer the user's question based only on the following context:

{context}

---

Answer the user's question based on the above context: {question}
"""

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Status": "CogniSync AI Backend is Running"}

# New endpoint to manually trigger the data sync
@app.post("/sync")
def sync_handler():
    return sync_knowledge_base()

@app.post("/chat")
def chat_handler(query: dict):
    user_query = query.get('text')
    print(f"Received query: {user_query}")
    
    # 1. Query the knowledge base to get relevant context
    context_chunks = query_knowledge_base(user_query)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in context_chunks])

    # 2. Create a prompt with the context and user's question
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_query)
    
    # 3. Call the LLM to synthesize the final answer
    response = llm.invoke(prompt)
    
    ai_answer = response.content
    
    return {"sender": "ai", "text": ai_answer}