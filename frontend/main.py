import gradio as gr
import requests
import uuid
from services.upload_csv import upload_csv
from services.ask_question import ask_question

session_id = str(uuid.uuid4())

with gr.Blocks() as demo:
    gr.Markdown("# GenDataBot")

    session_id_state = gr.State(str(uuid.uuid4()))  # Generate a unique session_id
    
    with gr.Row():
        file = gr.File(label="Upload CSV")
        file_output = gr.JSON()
    
    file.upload(upload_csv, inputs=[file, session_id_state], outputs=file_output)
    
    question_input = gr.Textbox(label="Ask a question about the CSV")
    answer_output = gr.Textbox(label="Answer")
    
    ask_button = gr.Button("Ask")
    ask_button.click(ask_question, inputs=[question_input, session_id_state], outputs=answer_output)

if __name__ == "__main__":

    demo.launch(server_name="0.0.0.0", server_port=7860)
