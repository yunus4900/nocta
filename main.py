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

    try:
        response = requests.post(
            HUGGING_FACE_API_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        json_data = response.json()

        if isinstance(json_data, list) and "generated_text" in json_data[0]:
            reply = json_data[0]["generated_text"]
        else:
            reply = "Bot şu an cevap veremiyor, lütfen daha sonra tekrar dene."

    except Exception as e:
        reply = f"HATA: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
