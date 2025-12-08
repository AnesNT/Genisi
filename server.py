import time
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import requests

app = Flask(__name__)
# السماح للواجهة بالاتصال بالسيرفر
CORS(app) 

# ==========================================
# 🔐 الخزنة (The Vault) - مفاتيحك آمنة هنا
# ==========================================
GRID_KEYS = [
    "AIzaSyCkUhP0VSdA-XiCpBle5s8N0wVTqzYnjFk", "AIzaSyBfw1RUccXYLgz1jx31pXBs2v8mNc9UVhE",
    "AIzaSyDVRu7tfXgmpDUCf0vwkG08gGP3HD2S3bw", "AIzaSyBLvP9OqGOaW70XBnqMGPfNKi1uldQQbbs",
    "AIzaSyB0Lt_TizvCHdM7wkGn1Q4Qsc3gBF8tdpw", "AIzaSyAI3-Z87ytRDeQzQmgyHv4Aa3f1ANzsoIU",
    "AIzaSyCLZlc50Gouu30TlvjWkYZieACxTbohcfM", "AIzaSyDfOyvu4y932Sud7yzgr-z4P5sDvbKc8DA",
    "AIzaSyA5IODgGmTqGauRsiZmCeQ087imoRsKm2k", "AIzaSyCJJWHR-S74aruBjs__L3UidBioOgkowvU",
    "AIzaSyAkMHthkVHGykjeLcpoGN-fdDWCB7c49GU", "AIzaSyDk3dm3aUryxXYlp_tdMGh9ZPVyV-9yd4g",
    "AIzaSyDWqpgRTJA3wYi8Hm-H3DikUroN_836Rto", "AIzaSyAXBBud7VcB-o6I7YmPRFRLQM-oIX6-TIU",
    "AIzaSyB-ILoGD8iV6y3YmvVGRjmkW4uKRCS96_k", "AIzaSyD7rDmDvojLncPNi_68QgFVK9dn-Mu5APY",
    "AIzaSyDyR4p9LuDeEJyfODJvR8-PrS-9l9zov_o", "AIzaSyDZjwU_nHd4ulvY4_JCHeVLspdnuODZE6s",
    "AIzaSyDVyZ-KmHQid8brne-4ki0xWnZ61Mz1FKw", "AIzaSyCLdIMi-yz4ARjiObvKVafmI8gs5UD7Pj0",
    "AIzaSyCrFawrGYZbt6fO_AupIW6gMWwnyAIAapM", "AIzaSyBBCyWiGo-H6Yxu5PwED0gMLkFS_5bmx1I",
    "AIzaSyBBCPp3C-3fUWMF7reZE7eiKEAJSqV0gQ0", "AIzaSyCowg54FCclWWTOe67hFxRCXN90HdMn1Jk",
    "AIzaSyDAiwqjNkoxwdaAiQAZuehukOLhWedtkVw", "AIzaSyDLhJwBwu1azap5md_HXDtLDAzNuPHG3-Q",
    "AIzaSyC5k4Slts-MNroLOgPwh_j2QvZARYzd8Lg"
]

HF_KEY = "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"
DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"

# مؤشر المفتاح الحالي
key_pointer = 0
history_store = {} # ذاكرة بسيطة في الرام

# -------------------------------------------
# وظائف النظام (System Functions)
# -------------------------------------------

def get_next_key():
    global key_pointer
    key_pointer = (key_pointer + 1) % len(GRID_KEYS)
    return GRID_KEYS[key_pointer]

def call_google_grid(prompt, session_id, is_pro_mode=False):
    """نظام التدوير النووي للاتصال بجوجل"""
    global key_pointer
    
    model_name = "gemini-2.5-flash-lite" if is_pro_mode else "gemini-2.5-flash-lite"
    
    # تعليمات النظام بناء على الوضع
    sys_instruct = "You are Genisi. Helpful and fast."
    if is_pro_mode:
        sys_instruct = "You are Genisi Pro (DeepSeek Emulator). Reason deeply. Provide code, math, and technical details expertly."

    attempts = 0
    max_retries = len(GRID_KEYS) # نجرب كل المفاتيح

    while attempts < max_retries:
        key = get_next_key()
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(model_name, system_instruction=sys_instruct)
            
            # استرجاع الذاكرة
            chat_history = history_store.get(session_id, [])
            chat = model.start_chat(history=chat_history)
            
            response = chat.send_message(prompt)
            
            # تحويل الرد إلى نص نقي لتخزينه في الذاكرة اليدوية إذا لزم الأمر
            # لكن SDK جوجل يدير الذاكرة في start_chat بشكل جيد،
            # هنا سنحدث الذاكرة المخزنة لدينا لاستخدامها في حال تبديل المفتاح
            # ملاحظة: لتحقيق نقل سياق مثالي بين مفاتيح مختلفة، يجب تحويل history جوجل لقاموس
            # للتبسيط هنا نعتمد على أن الموديل يعيد رداً واحداً.
            
            return response.text
            
        except Exception as e:
            print(f"⚠️ Node Fail ({key[:5]}...): {e}")
            attempts += 1
            # المحاولة مع المفتاح التالي
    
    raise Exception("System Overload: All 27 Nodes are busy.")


def call_deepseek_real(prompt):
    """الاتصال الحقيقي بـ Hugging Face (بدون مشاكل CORS)"""
    print("📡 Connecting to DeepSeek...")
    api_url = f"https://api-inference.huggingface.co/models/{DEEPSEEK_MODEL}"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    payload = {
        "inputs": f"<|user|>\n{prompt}\n<|assistant|>\n",
        "parameters": {"max_new_tokens": 1500, "temperature": 0.6, "return_full_text": False}
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"DeepSeek Error: {response.text}")
        
    result = response.json()
    # استخراج النص
    if isinstance(result, list):
        return result[0]['generated_text']
    return result.get('generated_text', '')


# -------------------------------------------
# الواجهة البرمجية (API Routes)
# -------------------------------------------

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    prompt = data.get('text', '')
    mode = data.get('mode', 'std') # 'std' or 'pro' (deepseek)
    session_id = data.get('session', 'guest')

    print(f"📨 Incoming: {prompt[:20]}... [Mode: {mode}]")

    try:
        reply = ""
        
        # 1. Image Generation Check
        if any(x in prompt.lower() for x in ['image', 'draw', 'رسم', 'ارسم', 'صورة', 'تخيل']):
            # نرسل وصفاً للصورة
            return jsonify({
                "type": "image", 
                "prompt": prompt, 
                "reply": "Generating Flux Image..."
            })

        # 2. Text Logic
        if mode == 'pro':
            try:
                # محاولة الاتصال بـ DeepSeek الحقيقي
                reply = call_deepseek_real(prompt)
                reply = reply.replace("<|assistant|>", "").replace("<|user|>", "").strip()
            except Exception as e:
                # نظام الحماية: إذا فشل ديبسيك، حول لجوجل برو
                print(f"❌ DeepSeek Fail, Fallback to Grid Pro. Error: {e}")
                reply = call_google_grid(prompt, session_id, is_pro_mode=True)
                reply = "⚠️ [Backup System Active]\n" + reply
        else:
            # الوضع العادي
            reply = call_google_grid(prompt, session_id, is_pro_mode=False)

        return jsonify({"type": "text", "reply": reply})

    except Exception as e:
        return jsonify({"type": "error", "reply": str(e)}), 500

if __name__ == '__main__':
    print("🔥 Genisi Core Server Online at http://localhost:5000")
    print("🔒 27 Google Keys Loaded | DeepSeek Access Ready")

    app.run(port=5000, debug=True)
