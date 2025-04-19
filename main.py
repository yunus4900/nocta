from flask import Flask, render_template, request, jsonify
import openai
import os

# Flask uygulamasını başlat
app = Flask(__name__)

# OpenAI API anahtarı
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ana sayfa
@app.route("/")
def home():
    return render_template("sohbet.html")

# Sohbet API
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
        print("OpenAI HATASI:", e)
        return jsonify({"reply": "Bot şu anda cevap veremiyor. Lütfen sonra tekrar dene."})

# Sunucu çalıştırma (Render için özel ayar)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
