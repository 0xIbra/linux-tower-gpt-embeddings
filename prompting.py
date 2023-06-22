from utils.context_injector import ContextInjector
import gradio as gr
import openai
import json
import os


openai.api_key = os.environ.get('OPENAI_API_KEY')
GPT_MODEL = 'gpt-3.5-turbo-16k'
GPT_ROLE = """
You are an expert python coder, for each task, generate python code without explanations or comments.
Provide the filepath to where the code goes as well and wrap the code around ```python```.
""".strip()

CONTEXT_INJECTOR = None


def gpt_request(prompt: str, model=GPT_MODEL):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {'role': 'system', 'content': GPT_ROLE},
            {'role': 'user', 'content': prompt}
        ]
    )

    print('prompt usage: ', response['usage'])

    return response['choices'][0]['message']['content']


def prompt_gpt(text: str, history: list):
    global CONTEXT_INJECTOR

    context_data = CONTEXT_INJECTOR.get_context_for_prompt(text, 20)
    context_data = [f"{x['code']}" for i, x in context_data.iterrows()]
    if len(context_data) > 0:
        context = '\n'.join(context_data)
        text = f"Context:\n{context}\n\nQuestion:\n{text}"
    
    result = gpt_request(text)

    history = history or []
    history.append((text, result))

    return history, history


def main():
    global DF
    global CONTEXT_INJECTOR

    CONTEXT_INJECTOR = ContextInjector()

    css = "gradio-app {background-color: #111 !important;}"
    with gr.Blocks(css=css) as demo:
        gr.Markdown("<h1>Linux Tower - GPT Embedding autonomy experiment</h1>")
        chatbot = gr.Chatbot()
        message = gr.Textbox(placeholder="What do you have in mind for linux tower ?", lines=5)
        state = gr.State()
        submit = gr.Button("Let's get to work !")
        submit.click(prompt_gpt, inputs=[message, state], outputs=[chatbot, state])

    demo.launch()


if __name__ == '__main__':
    main()
