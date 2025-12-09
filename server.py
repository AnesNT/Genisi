import os
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =======================================================
# 🔐 المحرك: Qwen 2.5 72B (أقوى نموذج مفتوح حالياً)
# =======================================================
HF_TOKEN = os.environ.get("HF_KEY") 

# هذا النموذج وحش، ومجاني، ولا يسبب مشاكل 404 مثل لاما
API_URL = "https://huggingface.co/Qwen/Qwen2.5-7B-Instruct"

def query_huggingface(prompt, retries=5):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # تنسيق الرسالة الخاص بـ Qwen (ChatML)
    # هذا التنسيق مهم جداً ليفهم أنك تتحدث معه وليس تكملة نص
    final_prompt = f"""<|im_start|>system
You are Genisi, an advanced AI developed by AnesNT. 
You are helpful, professional, and precise. 
Answer in the same language as the user (Arabic/English).<|im_end|>
<|im_start|>user
{prompt}<|im_end|>
<|im_start|>assistant
"""

    payload = {
        "inputs": final_prompt,
        "parameters": {
            "max_new_tokens": 1500,  # مساحة للكتابة الطويلة
            "temperature": 0.6,
            "return_full_text": False
        }
    }

    for i in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=40)
            
            # 503 تعني السيرفر يقوم بتحميل النموذج (بارد)
            if response.status_code == 503:
                wait_time = response.json().get("estimated_time", 5)
                print(f"❄️ Model loading... sleeping {wait_time}s")
                time.sleep(wait_time)
                continue
                
            if response.status_code != 200:
                raise Exception(f"HF Error {response.status_code}: {response.text}")

            result = response.json()
            
            # استخراج النص بذكاء
            if isinstance(result, list) and len(result) > 0:
                text = result[0].get('generated_text', '')
            else:
                text = result.get('generated_text', '')
                
            # تنظيف الرموز الخاصة بـ Qwen
            clean_text = text.replace("<|im_end|>", "").strip()
            return clean_text
                
        except Exception as e:
            print(f"⚠️ Attempt {i+1} failed: {e}")
            if i == retries - 1:
                return "Genisi Servers are experiencing high traffic. Please try again in 10 seconds."
            time.sleep(2)

    return "Server Error."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"type": "error", "reply": "No text provided"})

    try:
        # 1. كاشف الصور (لا يتغير)
        if any(x in text.lower() for x in ['image', 'draw', 'رسم', 'صورة', 'تخيل']):
            return jsonify({
                "type": "image", 
                "reply": "Flux"
            })

        # 2. محرك النصوص (Qwen 72B)
        reply = query_huggingface(text)
        return jsonify({"type": "text", "reply": reply})

    except Exception as e:
        return jsonify({"type": "error", "reply": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

