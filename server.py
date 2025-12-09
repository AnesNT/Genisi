import os
import time
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# =======================================================
# 🔐 الإعدادات: Llama 3.1 Engine
# =======================================================
# المفتاح يتم جلبه من متغيرات بيئة Render
# تأكد أنك وضعت متغير اسمه HF_KEY في إعدادات Render
HF_TOKEN = os.environ.get("HF_KEY") 

# رابط النموذج الرسمي في Hugging Face
API_URL = "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct?inference_provider=sambanova"

# دالة الاتصال بـ Llama
def query_llama(prompt, retries=3):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    # 1. إعداد البرومبت الخاص بـ Llama 3
    # Llama 3 يفهم هيكلية خاصة للأوامر (System > User > Assistant)
    full_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are Genisi, an advanced AI developed by AnesNT.
Your goal is to provide helpful, accurate, and concise answers.
You speak the user's language fluently (Arabic/English/etc).
<|eot_id|><|start_header_id|>user<|end_header_id|>
{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

    payload = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 1024,  # طول الإجابة
            "temperature": 0.7,      # نسبة الإبداع
            "top_p": 0.9,
            "return_full_text": False
        }
    }

    # محاولة الاتصال مع تكرار المحاولة في حالة "السيرفر مشغول"
    for i in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
            
            # حالة تحميل الموديل (تحدث في HF Free Tier)
            if response.status_code == 503:
                print(f"Model loading... wait {i+1}s")
                time.sleep(2)
                continue # نعيد المحاولة
                
            if response.status_code != 200:
                raise Exception(f"HF Error {response.status_code}: {response.text}")

            result = response.json()
            
            # استخراج النص
            if isinstance(result, list):
                return result[0]['generated_text']
            elif 'generated_text' in result:
                return result['generated_text']
            else:
                return str(result)
                
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            if i == retries - 1: # آخر محاولة
                raise e

    return "Llama server is busy right now. Please try again."

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({"type": "error", "reply": "Empty message"})

    try:
        # فحص بسيط للصور (سنبقي الميزة فهي لا علاقة لها بجوجل)
        if any(x in text.lower() for x in ['image', 'draw', 'رسم', 'صورة', 'تخيل']):
            return jsonify({
                "type": "image", 
                "reply": "Flux Generator"
            })

        # الاتصال بـ Llama
        reply = query_llama(text)
        return jsonify({"type": "text", "reply": reply.strip()})

    except Exception as e:
        return jsonify({"type": "error", "reply": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
