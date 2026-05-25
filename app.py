import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS lagane se tumhari Vercel wali website is backend se bina kisi error ke baat kar sakegi
CORS(app)

# Render ki settings se hum tumhari Groq API Key yahan connect karenge
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Janwar is Active and Running smoothly, Bro!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    chat_history = data.get("history", [])

    if not GROQ_API_KEY:
        return jsonify({"reply": "Error: Groq API Key Render par missing hai!"}), 500

    # Yeh tumhare janwar ki coding hai ke use kaisa behave karna hai
    system_prompt = (
        "You are a sophisticated, polite, and elite AI Luxury Concierge for 'ESTATE NO. 88' in Bel Air, Los Angeles. "
        "Your main goal is to assist clients interested in this multi-million dollar property, provide elegant details, "
        "and politely capture their Name, Phone Number, and Email before booking a private tour or sharing deep property specs. "
        "Keep responses short, professional, and mature. Do not use internet slang."
    )

    # Groq API ke liye messages ka dabba taiyar karna
    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        messages.append(msg)
    messages.append({"role": "user", "content": user_message})

    try:
        # Tumhari Groq API key ka use karke Llama model se jawab mangna
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",  # Groq ka super fast aur free model
                "messages": messages,
                "temperature": 0.7
            }
        )
        res_data = response.json()
        
        # AGAR GROQ API NE ERROR BHEJA HAI TOH USAY PAKRO
        if 'error' in res_data:
            return jsonify({"reply": f"Groq Error Bro: {res_data['error']['message']}"})

        # Agar sab theek hai toh jawab dikhao
        bot_reply = res_data['choices'][0]['message']['content']
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"Sorry Bro, dimaag mein glitch aya: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
