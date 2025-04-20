from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

HUGGINGFACE_API_KEY = os.getenv("HF_API_KEY")

@app.route("/")
def home():
    return render_template("sohbet.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }

    payload = {
        "inputs": user_message
    }

    response = requests.post(
        "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
        headers=headers,
        json=payload
    )

    try:
        generated_text = response.json()[0]['generated_text']
        return jsonify({"reply": generated_text})
    except Exception as e:
        return jsonify({"reply": f"HATA: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
