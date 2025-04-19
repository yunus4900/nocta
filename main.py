from flask import Flask, render_template, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


# Ana sayfa - sohbet arayüzünü açar
@app.route("/")
def home():
    return render_template("sohbet.html")


# Sohbet isteklerini işler
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    role = data.get("role", "samimi")

    system_prompts = {
        "tutku":
        "You are a seductive, bold AI partner. Speak openly about desire.",
        "eglence": "You are playful and humorous. Keep the chat light.",
        "samimi": "You are caring and sincere. Focus on feelings.",
        "gizemli": "You are mysterious and poetic. Speak with intrigue."
    }

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                            messages=[{
                                                "role":
                                                "system",
                                                "content":
                                                system_prompts.get(role, "")
                                            }, {
                                                "role": "user",
                                                "content": message
                                            }])

    return jsonify({"reply": response.choices[0].message["content"]})


@app.errorhandler(404)
def page_not_found(e):
    return render_template('sohbet.html'), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
