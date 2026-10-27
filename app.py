import os
import gradio as gr

def chat_with_gemini(message, history):
    contents = []

    # Include previous messages for conversation memory
    for item in history:
        if isinstance(item, dict):
            # Support newer history formats
            if item.get("role") in ["user", "assistant"]:
                contents.append({
                    "role": "user" if item["role"] == "user" else "model",
                    "parts": [{"text": item.get("content", "")}]
                })
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user_msg, assistant_msg = item
            if user_msg:
                contents.append({
                    "role": "user",
                    "parts": [{"text": user_msg}]
                })
            if assistant_msg:
                contents.append({
                    "role": "model",
                    "parts": [{"text": assistant_msg}]
                })

    contents.append({
        "role": "user",
        "parts": [{"text": message}]
    })

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=contents
        )
        return response.text or "Gemini returned an empty response."

    except Exception as e:
        return f"Gemini error: {e}"


app = gr.ChatInterface(
    fn=chat_with_gemini,
    title="My AI Chatbot",
    description="Chat with Gemini AI"
)

app.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", "10000"))
)
