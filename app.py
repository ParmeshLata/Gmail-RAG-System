from pipeline import save_and_run
from llm.chatbot import chatbot
import gradio as gr
import threading

def save_run_and_close(email, password):

    result = save_and_run(email, password)
    
    def close():
        import time
        time.sleep(3)
        demo.close()
    
    threading.Thread(target=close).start()
    
    return result + "\n\n🔄 Launching chatbot window..."

def main():
    global demo
    
    with gr.Blocks() as demo:
        gr.Markdown("Save Credentials & Run Pipeline")

        email_input = gr.Textbox(label="Email", placeholder="Enter your email")
        password_input = gr.Textbox(label="Password", placeholder="Enter your password", type="password")
        
        submit_btn = gr.Button("Save & Run Pipeline")
        output = gr.Textbox(label="Output")
        
        submit_btn.click(fn=save_run_and_close, inputs=[email_input, password_input], outputs=output)

    demo.launch()
    
    print("Credentials server closed. Launching chatbot...")
    launch_chatbot()


def launch_chatbot():
    chatbot_demo = gr.ChatInterface(fn=chatbot, title="Gmail RAG Assistant")
    chatbot_demo.launch()


if __name__ == "__main__":
    main()