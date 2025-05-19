from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# اسم النموذج من Hugging Face (يمكن تغييره لاحقًا)
MODEL = "HuggingFaceH4/zephyr-7b-beta"
@app.route("/")
def home():
    return "✅ خادم HuggingFace جاهز."

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        text = data.get("text", "")
        health = data.get("health", "")

        if not text:
            return jsonify({"error": "❌ النص فارغ"}), 400

        prompt = f"""
أنت أخصائي نفسي محترف. اقرأ النص التالي بعناية، وقدم تحليلًا نفسيًا إنسانيًا وعميقًا باللغة العربية الفصحى.

- لا تعيد صياغة النص.
- تحدث إلى كاتب النص مباشرة.
- استخرج المشاعر الظاهرة والمخفية من خلال كلماته.
- اربط بين ما يشعر به وسياق ما مر به.
- لا تذكر وجود نص أو بيانات صحية، فقط استنتج منها ما يفيد التحليل.

النص:
{text}

البيانات الصحية:
{health}

التحليل:
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

        # استخراج النص الناتج
        text_output = result[0]["generated_text"].replace(prompt, "").strip()

        return jsonify({"analysis": text_output})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)