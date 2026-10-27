
import os
import gradio as gr
from google import genai

# Get Gemini API key from Render environment variables
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it in Render -> Environment Variables."
    )

# Connect to Gemini
client = genai.Client(api_key=api_key)
MODEL = "gemini-3.5-flash-lite"


def chat_with_gemini(message, history):
    contents = []

    # Add previous conversation messages
    for item in history:
        if isinstance(item, dict):
            role = item.get("role")
            text = item.get("content", "")

            if role in ("user", "assistant") and isinstance(text, str):
                if text:
                    contents.append({
                        "role": "user" if role == "user" else "model",
                        "parts": [{"text": text}]
                    })

        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, assistant_msg = item

            if user_msg:
                contents.append({
                    "role": "user",
                    "parts": [{"text": str(user_msg)}]
                })

            if assistant_msg:
                contents.append({
                    "role": "model",
                    "parts": [{"text": str(assistant_msg)}]
                })

    # Add the latest user message
    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents
        )

        return response.text or "Gemini returned an empty response."

    except Exception as e:
        print(f"Gemini API error: {e}")
        return f"Gemini error: {e}"


# Create the Gradio chatbot
app = gr.ChatInterface(
    fn=chat_with_gemini,
    title="My AI Chatbot",
    description="Chat with Gemini AI",
    textbox=gr.Textbox(
        placeholder="Ask me anything...",
        lines=2
    )
)

# Start the web server on Render's assigned port
app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "10000"))
)
