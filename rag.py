from langchain_google_genai import(
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI
)

from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(
    model = "models/gemini-embedding-001"
)
def load_retriever():
    vectorstore = FAISS.load_local("faiss_index",
                                embeddings,
                                allow_dangerous_deserialization=True)

    return vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )
'''
question = "What is the Transformer architecture?"

results =  retriever.invoke(question)

print("\nRelevant Chunks:\n")

for i, doc in enumerate(results, 1):
    print(f"--- Chunk {i} ---")
    print(doc.page_content)
    print()
'''
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful question-answering assistant.

Answer the user's question using ONLY the context provided below.

If the answer cannot be found in the context, say:
"I could not find the answer in the provided document."

Context:
{context}

Question:
{question}

Answer:
""")

'''
question = "What is the Transformer architecture?"

results = retriever.invoke(question)

context = "\n\n".join(
    doc.page_content for doc in results
)

messages = prompt.invoke({
    "context": context,
    "question": question
})

response = llm.invoke(messages)

print("\nAnswer:\n")
print(response.content)
'''

def answer_question(question):
    retriever = load_retriever()

    results = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in results
    )

    messages = prompt.invoke({
        "context": context,
        "question": question
    })

    response = llm.invoke(messages)

    return {
        "answer": response.content[0]["text"],
        "sources": [
            doc.metadata.get("page","Unknown")
            for doc in results
        ]
    }
if __name__ == "__main__":
    question = "What is the Transformer architecture?"
    result = answer_question(question)
    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:\n")
    for page in result["sources"]:
        print("Page:", page)