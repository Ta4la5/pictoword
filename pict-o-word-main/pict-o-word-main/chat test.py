# chatbot.py
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from flask import Flask, request, jsonify

MODEL_NAME = "gpt2"  # small and easy to run; replace with larger models if you have GPU/VRAM

# Load tokenizer & model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Create a simple generation pipeline
gen = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # device=0 for GPU

app = Flask(name)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "send {'prompt': '...'}"}), 400

    out = gen(prompt, max_length=200, do_sample=True, top_p=0.9, temperature=0.8, num_return_sequences=1)
    reply = out[0]["generated_text"]
    # Optionally strip the prompt from reply
    if reply.startswith(prompt):
        reply = reply[len(prompt):].strip()
    return jsonify({"reply": reply})

if name == "main":
    print("Starting local chatbot on http://127.0.0.1:5000")
    app.run(debug=True)