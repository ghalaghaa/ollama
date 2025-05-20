from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
import requests
import os

app = Flask(__name__)
CORS(app)
# translator = Translator()

# اسم النموذج من Hugging Face (يمكن تغييره لاحقًا)
MODEL = "HuggingFaceH4/zephyr-7b-beta"
@app.route("/analyze", methods=["GET"])
def home():
    return "✅ خادم HuggingFace جاهز."

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        text_ar = data.get("text", "")
        health_ar = data.get("health", "")

        if not text_ar:
            return jsonify({"error": "❌ النص فارغ"}), 400
        
        text_en = GoogleTranslator(source='ar', target='en').translate(text_ar)
        health_en = GoogleTranslator(source='ar', target='en').translate(health_ar)

        # text_en = translator.translate(text_ar, src='ar', dest='en').text
        # health_en = translator.translate(health_ar, src='ar', dest='en').text

        prompt = f"""
You are a professional psychologist. Carefully read the following text and provide a deep empathetic psychological analysis.

- Do not rephrase the text.
- Speak directly to the writer.
- Extract explicit and hidden feelings.
- Connect what they feel with the context.
- Do not mention text or health data; only provide useful analysis.

Text:
{text_en}

Health data:
{health_en}

Analysis:
"""

        headers = {
            "Authorization": f"Bearer {os.environ.get('HF_API_KEY')}",
            "Content-Type": "application/json"
        }

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": 0.5,
                "max_new_tokens": 400
            }
        }

        response = requests.post(
            f"https://api-inference.huggingface.co/models/{MODEL}",
            headers=headers,
            json=payload
        )
        print("🔵 Raw response text:")
        print(response.text)
        result = response.json()

        if isinstance(result, dict) and "error" in result:
            return jsonify({"error": result["error"]}), 500


 # Extract the English output from the model
        analysis_en = result[0]["generated_text"].replace(prompt, "").strip()

        # Translate the analysis back to Arabic
        analysis_ar = GoogleTranslator(source='en', target='ar').translate(analysis_en)

        # استخراج النص الناتج
        # text_output = result[0]["generated_text"].replace(prompt, "").strip()

        return jsonify({"analysis": analysis_ar})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)