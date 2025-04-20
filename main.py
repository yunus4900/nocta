from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HUGGING_FACE_API_KEY = os.getenv("HF_API_KEY")

headers = {
    "Authorization": f"Bearer {HUGGING_FACE_API_KEY}"
}

@app.route("/")
def home():
    return render_template("sohbet.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")

    payload = {
        "inputs": user_input
    }

    response = requests.post(
        HUGGING_FACE_API_URL,
        headers=headers,
        json=payload
    )

    try:
        bot_reply = response.json()[0]["generated_text"]
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"reply": f"HATA: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
