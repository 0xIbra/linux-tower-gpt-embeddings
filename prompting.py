from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import DeepLake
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import gradio as gr
import os


embeddings = OpenAIEmbeddings(disallowed_special=())

db = DeepLake(
    dataset_path="hub://ibra/linux-tower-experiment",
    read_only=True,
    embedding_function=embeddings
)

retriever = db.as_retriever()
retriever.search_kwargs["distance_metric"] = "cos"
retriever.search_kwargs["fetch_k"] = 100
retriever.search_kwargs["maximal_marginal_relevance"] = True
retriever.search_kwargs["k"] = 10

chat_history = []

model = ChatOpenAI()
qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)


def prompt(text: str, history: list):
    global qa
    global chat_history

    result = qa({"question": text, "chat_history": chat_history})
    chat_history.append((text, result["answer"]))

    return chat_history, chat_history


css = "gradio-app {background-color: #111 !important;}"
with gr.Blocks(css=css) as demo:
    gr.Markdown("<h1>Linux Tower - LangChain experiment</h1>")
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="What do you have in mind for linux tower ?", lines=5)
    state = gr.State()
    submit = gr.Button("Let's get to work !")
    submit.click(prompt, inputs=[message, state], outputs=[chatbot, state])

demo.launch()
