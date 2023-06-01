""" chat-bison@001 demo in Gradio """

from google.cloud import aiplatform
from google.cloud import logging

import google.auth

import vertexai
from vertexai.preview.language_models import ChatModel

import gradio as gr

PROJECT_ID = "argolis-rafaelsanchez-ml-dev" 
LOCATION = "us-central1" # no funciona europe-west4

# add credentials from GOOGLE_APPLICATION_CREDENTIALS env variable
#credentials, projectid = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])

vertexai.init(project=PROJECT_ID, location=LOCATION)#, credentials=credentials)

client = logging.Client(project=PROJECT_ID)
client.setup_logging()

chat_model = ChatModel.from_pretrained("chat-bison@001")

chat = chat_model.start_chat()

def add_text(history, text):
    history = history + [(text, None)]
    return history, ""

def add_file(history, file):
    history = history + [((file.name,), None)]
    return history

def bot(history):
    print(history)
    
    text_response = chat.send_message(str(history[-1][0]))
    print(text_response)
    history[-1][1] = str(text_response)
    print(history)
    return history

with gr.Blocks() as io:
    gr.Markdown(
        """
    # Vertex AI LLM demo - Chat
    ## This demo shows text-bison@001
    """
    )

    chatbot = gr.Chatbot([], elem_id="chatbot").style(height=750)

    with gr.Row():
        with gr.Column(scale=0.85):
            txt = gr.Textbox(
                show_label=False,
                placeholder="Enter text and press enter, or upload an image",
            ).style(container=False)
        with gr.Column(scale=0.15, min_width=0):
            btn = gr.UploadButton("📁", file_types=["image", "video", "audio"])

    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )
    btn.upload(add_file, [chatbot, btn], [chatbot]).then(
        bot, chatbot, chatbot
    )

io.launch(server_name="0.0.0.0", server_port=7860)