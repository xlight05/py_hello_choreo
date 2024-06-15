from fastapi import FastAPI
from langchain import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough
from langchain_pinecone import Pinecone
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel
import os
from pinecone import Pinecone as pc

api = FastAPI()

class Query(BaseModel):
    message: str

@api.get("/")
async def root():
    return {"message": "Hello World"}

@api.post("/ask")
async def ask(request: Query):
    index_name = "langchain-demo"
    gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = Pinecone.from_existing_index(
        index_name=index_name,
        embedding=gemini_embeddings,
    )
    retriever = vectorstore.as_retriever()
    llm = ChatGoogleGenerativeAI(model="gemini-pro",
                 temperature=0.7, top_p=0.85)
    
    llm_prompt_template = """You are an assistant for question-answering tasks.
    Use the following context to answer the question.
    If you don't know the answer, just say that you don't know.
    Use five sentences maximum and keep the answer concise.

    Question: {question}
    Context: {context}
    Answer:"""

    llm_prompt = PromptTemplate.from_template(llm_prompt_template)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | llm_prompt
        | llm
        | StrOutputParser()
    )
    response = rag_chain.invoke(request.message)
    return {"response" : response}