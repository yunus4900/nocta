@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    role = data.get("role", "samimi")

    system_prompts = {
        "tutku": "You are a seductive, bold AI partner. Speak openly about desire.",
        "eglence": "You are playful and humorous. Keep the chat light.",
        "samimi": "You are caring and sincere. Focus on feelings.",
        "gizemli": "You are mysterious and poetic. Speak with intrigue."
    }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompts.get(role, "")},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        print("OpenAI HATASI:", e)  # logs'da hata görmen için
        return jsonify({"reply": "Bot şu anda cevap veremiyor. Lütfen daha sonra tekrar dene."})
from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("sohbet.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    role = data.get("role", "samimi")

    system_prompts = {
        "tutku": "You are a seductive, bold AI partner. Speak openly about desire.",
        "eglence": "You are playful and humorous. Keep the chat light.",
        "samimi": "You are caring and sincere. Focus on feelings.",
        "gizemli": "You are mysterious and poetic. Speak with intrigue."
    }

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompts.get(role, "")},
                {"role": "user", "content": message}
            ]
        )
        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
