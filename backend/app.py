from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from openai import OpenAI
from vectordb import Memory

app = Flask(__name__)
CORS(app)

# Lade Umgebungsvariablen und initialisiere OpenAI
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Lade die Vektordatenbank
memory = Memory(memory_file="./memory.txt",
                chunking_strategy={'mode': 'sliding_window', 'window_size': 80, 'overlap': 20},
                embeddings="normal")

# Funktion zur Beantwortung der Fragen
def askgpt(user_question, context):
    msgs = [
        {"role": "system", "content": "Nutze den Kontext, um die Nutzerfrage zu beantworten:" + context},
        {"role": "user", "content": user_question}
    ]
    return client.chat.completions.create(model="gpt-4", messages=msgs)

def find_relevant_articles(question):
    result = memory.search(question, top_n=1)
    return result

def ask_question_with_rag(question):
    rag_context = find_relevant_articles(question)
    gpt_response = askgpt(user_question=question, context=rag_context[0]["chunk"])
    return gpt_response.choices[0].message.content

@app.route("/", methods=["POST"])
def ask_gpt():
    data = request.json
    question = data.get('question', '')
    gpt_response = ask_question_with_rag(question)
    return jsonify(gpt_response)

if __name__ == "__main__":
    app.run(debug=True)
