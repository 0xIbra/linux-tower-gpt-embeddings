from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os


embeddings = OpenAIEmbeddings(disallowed_special=())

db = DeepLake(
    dataset_path="hub://ibra/linux-tower-experiment",
    read_only=True,
    embedding_function=embeddings,
)

retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["fetch_k"] = 100
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 10

def filter(x):
    # filter based on source code
    if "com.google" in x["text"].data()["value"]:
        return False

    # filter based on path e.g. extension
    metadata = x["metadata"].data()["value"]
    return "scala" in metadata["source"] or "py" in metadata["source"]


### turn on below for custom filtering
# retriever.search_kwargs['filter'] = filter

chat_history = []

model = ChatOpenAI(model="gpt-3.5-turbo-16k")
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

while True:
    query = input("You: ")
    if query == "exit":
        break

    result = qa({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    print(f"AI: {result['answer']} \n")
