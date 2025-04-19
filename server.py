from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    role = data.get("role", "samimi")

    system_prompts = {
        "tutku": "You are a seductive and direct AI. Talk about attraction and intimacy without hesitation.",
        "eglence": "You are playful and energetic. Keep the chat fun and lighthearted.",
        "samimi": "You are warm and empathetic. Create emotional connection and trust.",
        "gizemli": "You are mysterious and poetic. Speak with intrigue and subtle passion."
    }

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompts.get(role, "")},
            {"role": "user", "content": message}
        ]
    )

    return jsonify({"reply": response.choices[0].message["content"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
