"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                 Multi-LLM Chat Interface - Main Application                 ║
║                 واجهة الدردشة متعددة النماذج - التطبيق الرئيسي              ║
╚══════════════════════════════════════════════════════════════════════════════╝

المطور | Developer: MiniMax Agent
الإصدار | Version: 1.0.0
التاريخ | Date: 2025-12-28

الوصف | Description:
واجهة دردشة حديثة ومتطورة تدعم التبديل بين خمسة نماذج ذكاء اصطناعي متقدمين.
تدعم الواجهة اللغة العربية مع اتجاه RTL الكامل وتصميم متجاوب وعصري.

A modern chat interface supporting five advanced AI language models with full
Arabic language support and RTL direction, featuring a responsive and modern design.

النماذج المدعومة | Supported Models:
- Llama 4 (Meta)
- Gemini 2.5 (Google)
- Qwen2.5 (Alibaba)
- Mistral (Mistral AI)
- Deepseek-R1 (DeepSeek with reasoning)
"""

import gradio as gr
import json
import re
from datetime import datetime
from typing import Optional, Dict, List, Tuple

# ════════════════════════════════════════════════════════════════════════════
# القسم الأول: الإعدادات والثوابت | Section 1: Configuration and Constants
# ════════════════════════════════════════════════════════════════════════════

# معلومات النماذج | Model Information
MODELS_INFO = {
    "llama4": {
        "name_ar": "Llama 4",
        "name_en": "Llama 4",
        "provider": "Meta",
        "description_ar": "أحدث نموذج لغوي كبير من ميتا",
        "description_en": "Meta's latest large language model",
        "icon": "🦙",
        "color": "#ff6b35",
        "endpoint": None  # سيتم تعيينه لاحقاً
    },
    "gemini2.5": {
        "name_ar": "Gemini 2.5",
        "name_en": "Gemini 2.5",
        "provider": "Google",
        "description_ar": "نموذج متعدد الوسائط متقدم من جوجل",
        "description_en": "Google's advanced multimodal AI model",
        "icon": "✨",
        "color": "#4285f4",
        "endpoint": None
    },
    "qwen2.5": {
        "name_ar": "Qwen 2.5",
        "name_en": "Qwen 2.5",
        "provider": "Alibaba",
        "description_ar": "نموذج لغوي قوي من علي بابا",
        "description_en": "Alibaba's powerful language model",
        "icon": "🌟",
        "color": "#0066cc",
        "endpoint": None
    },
    "mistral": {
        "name_ar": "Mistral",
        "name_en": "Mistral",
        "provider": "Mistral AI",
        "description_ar": "نموذج فعال وقوي من فرنسا",
        "description_en": "Efficient and capable French AI model",
        "icon": "💨",
        "color": "#cb8a27",
        "endpoint": None
    },
    "deepseek-r1": {
        "name_ar": "Deepseek-R1",
        "name_en": "Deepseek-R1",
        "provider": "DeepSeek",
        "description_ar": "نموذج تفكير متقدم مع عرض عملية التفكير",
        "description_en": "Advanced reasoning model with thinking process display",
        "icon": "🧠",
        "color": "#00bcd4",
        "endpoint": None,
        "has_reasoning": True
    }
}

# نصوص واجهة المستخدم | UI Text Translations
UI_TEXTS = {
    "ar": {
        "title": "💬 دردشة ذكاء اصطناعي",
        "subtitle": "تحدث مع أحدث النماذج اللغوية",
        "select_model": "اختر النموذج",
        "current_model": "النموذج الحالي",
        "type_message": "اكتب رسالتك هنا...",
        "send": "إرسال",
        "clear_chat": "مسح المحادثة",
        "new_chat": "محادثة جديدة",
        "settings": "الإعدادات",
        "language": "اللغة",
        "arabic": "العربية",
        "english": "الإنجليزية",
        "theme": "المظهر",
        "dark": "داكن",
        "light": "فاتح",
        "auto": "تلقائي",
        "welcome_title": "👋 مرحباً بك!",
        "welcome_subtitle": "كيف يمكنني مساعدتك اليوم؟",
        "suggestion_coding": "💻 برمجة",
        "suggestion_coding_desc": "ساعدني في كتابة كود",
        "suggestion_writing": "📝 كتابة",
        "suggestion_writing_desc": "ساعدني في كتابة مقال",
        "suggestion_analysis": "📊 تحليل",
        "suggestion_analysis_desc": "حلل هذه البيانات",
        "suggestion_translation": "🌐 ترجمة",
        "suggestion_translation_desc": "ترجم نص من الإنجليزية",
        "thinking": "🤔 التفكير",
        "show_thinking": "إظهار عملية التفكير",
        "hide_thinking": "إخفاء عملية التفكير",
        "copy_code": "نسخ الكود",
        "code_copied": "تم نسخ الكود!",
        "loading": "جاري التحميل...",
        "error": "حدث خطأ",
        "retry": "إعادة المحاولة",
        "try_again": "حدث خطأ، يرجى المحاولة مرة أخرى",
        "model_busy": "النموذج مشغول حالياً، يرجى الانتظار...",
        "history_saved": "تم حفظ المحادثة",
        "history_cleared": "تم مسح المحادثة",
        "about": "حول",
        "version": "الإصدار",
        "powered_by": "مشغل بواسطة"
    },
    "en": {
        "title": "💬 AI Chat",
        "subtitle": "Chat with the latest language models",
        "select_model": "Select Model",
        "current_model": "Current Model",
        "type_message": "Type your message here...",
        "send": "Send",
        "clear_chat": "Clear Chat",
        "new_chat": "New Chat",
        "settings": "Settings",
        "language": "Language",
        "arabic": "Arabic",
        "english": "English",
        "theme": "Theme",
        "dark": "Dark",
        "light": "Light",
        "auto": "Auto",
        "welcome_title": "👋 Welcome!",
        "welcome_subtitle": "How can I help you today?",
        "suggestion_coding": "💻 Coding",
        "suggestion_coding_desc": "Help me write code",
        "suggestion_writing": "📝 Writing",
        "suggestion_writing_desc": "Help me write an article",
        "suggestion_analysis": "📊 Analysis",
        "suggestion_analysis_desc": "Analyze this data",
        "suggestion_translation": "🌐 Translation",
        "suggestion_translation_desc": "Translate text from English",
        "thinking": "🤔 Thinking",
        "show_thinking": "Show thinking process",
        "hide_thinking": "Hide thinking process",
        "copy_code": "Copy Code",
        "code_copied": "Code copied!",
        "loading": "Loading...",
        "error": "Error",
        "retry": "Retry",
        "try_again": "An error occurred, please try again",
        "model_busy": "Model is currently busy, please wait...",
        "history_saved": "Chat saved",
        "history_cleared": "Chat cleared",
        "about": "About",
        "version": "Version",
        "powered_by": "Powered by"
    }
}

# ════════════════════════════════════════════════════════════════════════════
# القسم الثاني: دوال المساعد | Section 2: Helper Functions
# ════════════════════════════════════════════════════════════════════════════

def get_text(key: str, lang: str = "ar") -> str:
    """
    الحصول على نص معين بناءً على اللغة المحددة.
    
    Args:
        key (str): مفتاح النص
        lang (str): اللغة المطلوبة ("ar" أو "en")
    
    Returns:
        str: النص المترجم
    """
    return UI_TEXTS.get(lang, UI_TEXTS["en"]).get(key, UI_TEXTS["en"].get(key, key))

def format_message(text: str, lang: str = "ar") -> str:
    """
    تنسيق الرسالة مع معالجة الروابط والكود والروابط.
    
    Args:
        text (str): النص المراد تنسيقه
        lang (str): اللغة
    
    Returns:
        str: النص المنسق بتنسيق Markdown
    """
    if not text:
        return ""
    
    # معالجة الكود البرمجي | Code blocks processing
    text = re.sub(r'```(\w*)\n([\s\S]*?)```', r'```\n\2```', text)
    
    # معالجة الروابط | Links processing
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'[\1](\2)', text)
    
    # معالجة النص العريض | Bold text processing
    text = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', text)
    
    # معالجة النص المائل | Italic text processing
    text = re.sub(r'\*([^*]+)\*', r'*\1*', text)
    
    return text

def extract_thinking(text: str) -> Tuple[str, str]:
    """
    استخراج جزء التفكير من نص Deepseek-R1.
    
    Args:
        text (str): النص الأصلي
    
    Returns:
        Tuple[str, str]: (جزء التفكير, الجزء الفعلي من الإجابة)
    """
    if not text:
        return "", ""
    
    # البحث عن علامات التفكير | Search for thinking markers
    thinking_pattern = r'<thinking>([\s\S]*?)</thinking>'
    match = re.search(thinking_pattern, text)
    
    if match:
        thinking = match.group(1).strip()
        response = re.sub(thinking_pattern, '', text).strip()
        return thinking, response
    
    # البحث عن أنماط التفكير البديلة | Alternative thinking patterns
    alt_pattern = r'【([^\]]+)】'
    matches = re.findall(alt_pattern, text)
    
    if matches:
        thinking = '\n'.join(matches)
        response = re.sub(alt_pattern, '', text).strip()
        return thinking, response
    
    return "", text

def create_message_html(
    text: str,
    is_user: bool = False,
    lang: str = "ar",
    show_thinking: bool = False
) -> str:
    """
    إنشاء تنسيق HTML للرسالة.
    
    Args:
        text (str): نص الرسالة
        is_user (bool): هل الرسالة من المستخدم
        lang (str): اللغة
        show_thinking (bool): هل إظهار عملية التفكير
    
    Returns:
        str: HTML الرسالة
    """
    direction = "rtl" if lang == "ar" else "ltr"
    align = "left" if lang == "ar" else "left"
    
    # استخراج التفكير | Extract thinking
    thinking, response = extract_thinking(text)
    
    # تنسيق الاستجابة | Format response
    response = format_message(response, lang)
    
    # إنشاء HTML الرسالة | Create message HTML
    html = f"""
    <div class="message {'' if is_user else 'assistant'}">
        <div class="message-avatar">
            {"👤" if is_user else "🤖"}
        </div>
        <div class="message-content">
            {response}
        </div>
    </div>
    """
    
    return html

def get_model_info(model_key: str) -> Dict:
    """
    الحصول على معلومات النموذج.
    
    Args:
        model_key (str): مفتاح النموذج
    
    Returns:
        Dict: معلومات النموذج
    """
    return MODELS_INFO.get(model_key, MODELS_INFO["llama4"])

def get_current_datetime(lang: str = "ar") -> str:
    """
    الحصول على التاريخ والوقت الحاليين.
    
    Args:
        lang (str): اللغة
    
    Returns:
        str: التاريخ والوقت المنسقان
    """
    now = datetime.now()
    
    if lang == "ar":
        months = [
            "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
            "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"
        ]
        return f"{now.day} {months[now.month - 1]} {now.year}"
    else:
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return f"{months[now.month - 1]} {now.day}, {now.year}"

# ════════════════════════════════════════════════════════════════════════════
# القسم الثالث: دوال المنطق الرئيسية | Section 3: Main Logic Functions
# ════════════════════════════════════════════════════════════════════════════

def simulate_ai_response(
    message: str,
    model_key: str,
    chat_history: List,
    lang: str = "ar"
) -> Tuple[str, List]:
    """
    محاكاة استجابة الذكاء الاصطناعي (لاختبار الواجهة).
    في التطبيق الفعلي، يتم استبدال هذا بدالة الاتصال بالنموذج الحقيقي.
    
    Args:
        message (str): رسالة المستخدم
        model_key (str): مفتاح النموذج المحدد
        chat_history (List): سجل المحادثة
        lang (str): اللغة
    
    Returns:
        Tuple[str, List]: (الاستجابة، سجل المحادثة المحدث)
    """
    model_info = get_model_info(model_key)
    model_name = model_info.get("name_ar" if lang == "ar" else "name_en", model_key)
    
    # إضافة رسالة المستخدم إلى السجل | Add user message to history
    chat_history.append({
        "role": "user",
        "content": message,
        "model": model_name,
        "timestamp": get_current_datetime(lang)
    })
    
    # محاكاة الاستجابة بناءً على النموذج | Simulate response based on model
    responses = {
        "llama4": {
            "ar": f"أنا نموذج Llama 4 من ميتا._received your message: \"{message}\". كيف يمكنني مساعدتك؟",
            "en": f"I'm Llama 4 from Meta. I received your message: \"{message}\". How can I help you?"
        },
        "gemini2.5": {
            "ar": f"مرحباً! أنا Gemini 2.5 من جوجل.received: \"{message}\". يسعدني مساعدتك.",
            "en": f"Hello! I'm Gemini 2.5 from Google. I received: \"{message}\". Happy to help!"
        },
        "qwen2.5": {
            "ar": f"أهلاً! أنا Qwen 2.5 من علي بابا.message: \"{message}\". ما الذي تحتاجه؟",
            "en": f"Hi! I'm Qwen 2.5 from Alibaba. Message: \"{message}\". What do you need?"
        },
        "mistral": {
            "ar": f"تحية طيبة! أنا Mistral من Mistral AI.\"{message}\" - بالتأكيد، سأساعدك.",
            "en": f"Greetings! I'm Mistral from Mistral AI.\"{message}\" - Certainly, I'll help you."
        },
        "deepseek-r1": {
            "ar": f"<thinking>المستخدم يقول: \"{message}\"\n\nأحتاج لتحليل هذا الطلب...\n- هل هو سؤال برمجي؟\n- هل يحتاج تحليل؟\n- هل يحتاج إجابة سريعة؟\n\nسأقدم إجابة شاملة مع عملية تفكيري.</thinking>\n\nأنا Deepseek-R1. لقد فكرت في طلبك: \"{message}\".\n\nإليك إجابتي المتفكرة:\n\n1. فهم الطلب\n2. تحليل المتطلبات\n3. تقديم الحل الأمثل\n\nهل تريد تفاصيل أكثر؟",
            "en": f"<thinking>User says: \"{message}\"\n\nI need to analyze this request...\n- Is it a coding question?\n- Does it need analysis?\n- Does it need a quick answer?\n\nI'll provide a comprehensive response with my reasoning process.</thinking>\n\nI'm Deepseek-R1. I thought about your request: \"{message}\".\n\nHere's my reasoning response:\n\n1. Understanding the request\n2. Analyzing requirements\n3. Providing the best solution\n\nWould you like more details?"
        }
    }
    
    # الحصول على الاستجابة المناسبة | Get appropriate response
    response_text = responses.get(model_key, responses["llama4"]).get(lang, responses["llama4"]["en"])
    
    # إضافة استجابة المساعد إلى السجل | Add assistant response to history
    chat_history.append({
        "role": "assistant",
        "content": response_text,
        "model": model_name,
        "timestamp": get_current_datetime(lang)
    })
    
    return response_text, chat_history

def clear_chat() -> List:
    """
    مسح سجل المحادثة.
    
    Returns:
        List: سجل محادثة فارغ
    """
    return []

def update_model(
    model_key: str,
    lang: str = "ar"
) -> Tuple[str, Dict, str]:
    """
    تحديث النموذج المحدد.
    
    Args:
        model_key (str): مفتاح النموذج
        lang (str): اللغة
    
    Returns:
        Tuple[str, Dict, str]: (اسم النموذج، معلومات النموذج، وصف النموذج)
    """
    model_info = get_model_info(model_key)
    
    name = model_info.get("name_ar" if lang == "ar" else "name_en", model_key)
    description = model_info.get("description_ar" if lang == "ar" else "description_en", "")
    
    return name, model_info, description

def switch_language(lang: str) -> Dict:
    """
    تبديل لغة الواجهة.
    
    Args:
        lang (str): اللغة الجديدة ("ar" أو "en")
    
    Returns:
        Dict: القاموس مع جميع النصوص المحدثة
    """
    texts = UI_TEXTS.get(lang, UI_TEXTS["en"])
    
    return {
        "title": texts["title"],
        "subtitle": texts["subtitle"],
        "select_model": texts["select_model"],
        "current_model": texts["current_model"],
        "placeholder": texts["type_message"],
        "send": texts["send"],
        "clear": texts["clear_chat"],
        "new_chat": texts["new_chat"],
        "settings": texts["settings"],
        "language_label": texts["language"],
        "arabic": texts["arabic"],
        "english": texts["english"],
        "theme_label": texts["theme"],
        "dark": texts["dark"],
        "light": texts["light"],
        "welcome_title": texts["welcome_title"],
        "welcome_subtitle": texts["welcome_subtitle"],
        "suggestion_coding": texts["suggestion_coding"],
        "suggestion_coding_desc": texts["suggestion_coding_desc"],
        "suggestion_writing": texts["suggestion_writing"],
        "suggestion_writing_desc": texts["suggestion_writing_desc"],
        "suggestion_analysis": texts["suggestion_analysis"],
        "suggestion_analysis_desc": texts["suggestion_analysis_desc"],
        "suggestion_translation": texts["suggestion_translation"],
        "suggestion_translation_desc": texts["suggestion_translation_desc"],
        "loading": texts["loading"],
        "error": texts["error"],
        "try_again": texts["try_again"],
        "model_busy": texts["model_busy"],
        "copy_code": texts["copy_code"],
        "code_copied": texts["code_copied"],
        "thinking": texts["thinking"],
        "show_thinking": texts["show_thinking"],
        "hide_thinking": texts["hide_thinking"]
    }

def create_welcome_html(lang: str = "ar") -> str:
    """
    إنشاء شاشة الترحيب بتنسيق HTML.
    
    Args:
        lang (str): اللغة
    
    Returns:
        str: HTML شاشة الترحيب
    """
    texts = UI_TEXTS.get(lang, UI_TEXTS["en"])
    direction = "rtl" if lang == "ar" else "ltr"
    text_align = "right" if lang == "ar" else "left"
    
    html = f"""
    <div class="welcome-screen" style="direction: {direction}; text-align: {text_align};">
        <div class="welcome-icon">🚀</div>
        <h1 class="welcome-title">{texts["welcome_title"]}</h1>
        <p class="welcome-subtitle">{texts["welcome_subtitle"]}</p>
        
        <div class="suggestions-grid">
            <div class="suggestion-card" onclick="selectSuggestion('💻 برمجة', '{lang}')">
                <div class="suggestion-icon">💻</div>
                <div class="suggestion-title">{texts["suggestion_coding"]}</div>
                <div class="suggestion-desc">{texts["suggestion_coding_desc"]}</div>
            </div>
            
            <div class="suggestion-card" onclick="selectSuggestion('📝 كتابة مقال', '{lang}')">
                <div class="suggestion-icon">📝</div>
                <div class="suggestion-title">{texts["suggestion_writing"]}</div>
                <div class="suggestion-desc">{texts["suggestion_writing_desc"]}</div>
            </div>
            
            <div class="suggestion-card" onclick="selectSuggestion('📊 تحليل البيانات', '{lang}')">
                <div class="suggestion-icon">📊</div>
                <div class="suggestion-title">{texts["suggestion_analysis"]}</div>
                <div class="suggestion-desc">{texts["suggestion_analysis_desc"]}</div>
            </div>
            
            <div class="suggestion-card" onclick="selectSuggestion('🌐 ترجمة نص', '{lang}')">
                <div class="suggestion-icon">🌐</div>
                <div class="suggestion-title">{texts["suggestion_translation"]}</div>
                <div class="suggestion-desc">{texts["suggestion_translation_desc"]}</div>
            </div>
        </div>
    </div>
    """
    
    return html

def create_chat_message_html(
    message_data: Dict,
    lang: str = "ar"
) -> str:
    """
    إنشاء رسالة دردشة بتنسيق HTML.
    
    Args:
        message_data (Dict): بيانات الرسالة
        lang (str): اللغة
    
    Returns:
        str: HTML الرسالة
    """
    role = message_data.get("role", "user")
    content = message_data.get("content", "")
    timestamp = message_data.get("timestamp", "")
    
    is_user = role == "user"
    direction = "rtl" if lang == "ar" else "ltr"
    
    # استخراج التفكير إن وجد | Extract thinking if available
    thinking, response = extract_thinking(content)
    
    # تنسيق الاستجابة | Format response
    response = format_message(response, lang)
    
    # التحقق من وجود كود | Check for code
    has_code = "```" in response
    
    html = f"""
    <div class="message {'user' if is_user else 'assistant'}" style="direction: {direction};">
        <div class="message-avatar">
            {"👤" if is_user else "🤖"}
        </div>
        <div class="message-content">
            {response}
        </div>
    </div>
    """
    
    return html

# ════════════════════════════════════════════════════════════════════════════
# القسم الرابع: بناء الواجهة | Section 4: Building the Interface
# ════════════════════════════════════════════════════════════════════════════

def create_interface() -> gr.Blocks:
    """
    إنشاء واجهة Gradio الرئيسية.
    
    Returns:
        gr.Blocks: كائن الواجهة الرئيسي
    """
    # إنشاء الواجهة | Create interface
    with gr.Blocks(
        title="Multi-LLM Chat | دردشة متعددة النماذج",
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="purple",
            neutral_hue="slate",
            radius_size="large",
            font=gr.themes.GoogleFont("Noto Sans Arabic")
        ),
        css="""
        /* Custom CSS Injection | حقن CSS مخصص */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Noto Sans Arabic', 'Segoe UI', sans-serif !important;
        }
        
        /* RTL Support | دعم RTL */
        .rtl {
            direction: rtl;
            text-align: right;
        }
        
        /* Modern Chat Styling | تنسيق الدردشة الحديث */
        .chat-container {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            border-radius: 1rem;
            overflow: hidden;
        }
        
        /* Message Bubbles | فقاعات الرسائل */
        .message-bubble {
            padding: 1rem 1.25rem;
            border-radius: 1rem;
            margin: 0.5rem 0;
            max-width: 85%;
            animation: fadeIn 0.3s ease;
        }
        
        .user-message {
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 0.25rem;
        }
        
        .assistant-message {
            background: #1e293b;
            border: 1px solid #475569;
            border-bottom-left-radius: 0.25rem;
        }
        
        /* Model Selection Buttons | أزرار اختيار النموذج */
        .model-btn {
            padding: 0.75rem;
            border: 2px solid #475569;
            border-radius: 0.75rem;
            background: #334155;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .model-btn:hover {
            border-color: #6366f1;
            background: rgba(99, 102, 241, 0.1);
        }
        
        .model-btn.selected {
            border-color: #6366f1;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
            box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
        }
        
        /* Animations | الرسوم المتحركة */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        /* Scrollbar | شريط التمرير */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #1e293b;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #475569;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #64748b;
        }
        
        /* Loading Animation | رسم التحميل */
        .loading-dots span {
            display: inline-block;
            width: 8px;
            height: 8px;
            background: #6366f1;
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        
        .loading-dots span:nth-child(1) { animation-delay: -0.32s; }
        .loading-dots span:nth-child(2) { animation-delay: -0.16s; }
        
        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }
        
        /* Code Blocks | كتل الكود */
        .code-block {
            background: #0f172a;
            border-radius: 0.5rem;
            padding: 1rem;
            margin: 0.5rem 0;
            overflow-x: auto;
            font-family: 'Monaco', 'Consolas', monospace;
        }
        
        /* Responsive | المتجاوب */
        @media (max-width: 768px) {
            .model-grid {
                grid-template-columns: 1fr;
            }
            
            .message-bubble {
                max-width: 95%;
            }
        }
        """
    ) as interface:
        
        # ════════════════════════════════════════════════════════════════════
        # الحالة العامة | Global State
        # ════════════════════════════════════════════════════════════════════
        
        # اللغة الحالية | Current language
        current_lang = gr.State("ar")
        
        # النموذج الحالي | Current model
        current_model = gr.State("llama4")
        
        # سجل المحادثة | Chat history
        chat_history = gr.State([])
        
        # إظهار/إخفاء التفكير | Show/hide thinking
        show_thinking = gr.State(False)
        
        # ════════════════════════════════════════════════════════════════════
        # الواجهة الرئيسية | Main Interface
        # ════════════════════════════════════════════════════════════════════
        
        # العنوان الرئيسي | Main Header
        header = gr.HTML("""
        <div class="header" style="
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            padding: 1.5rem;
            border-bottom: 1px solid #475569;
            text-align: center;
        ">
            <h1 style="
                font-size: 1.75rem;
                font-weight: 700;
                background: linear-gradient(135deg, #6366f1, #8b5cf6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
            ">💬 دردشة ذكاء اصطناعي متعدد النماذج</h1>
            <p style="color: #94a3b8; margin: 0.5rem 0 0 0; font-size: 0.9rem;">تحدث مع Llama 4, Gemini 2.5, Qwen2.5, Mistral, Deepseek-R1</p>
        </div>
        """)
        
        # ════════════════════════════════════════════════════════════════════
        # الصف الرئيسي | Main Row
        # ════════════════════════════════════════════════════════════════════
        
        with gr.Row(equal_height=True, variant="panel"):
            
            # ════════════════════════════════════════════════════════════════════
            # اللوحة الجانبية | Sidebar Panel
            # ════════════════════════════════════════════════════════════════════
            
            with gr.Column(scale=1, min_width=280):
                
                # عنوان اللوحة الجانبية | Sidebar Title
                sidebar_title = gr.HTML("""
                <div class="sidebar-header" style="padding: 1rem 0.5rem; border-bottom: 1px solid #475569; margin-bottom: 1rem;">
                    <h2 style="font-size: 1.25rem; font-weight: 700; color: #6366f1;">⚙️ الإعدادات</h2>
                    <p style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">Configure your chat</p>
                </div>
                """)
                
                # اختيار اللغة | Language Selection
                lang_label = gr.HTML("<p style='font-size: 0.875rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem;'>🌐 اللغة | Language</p>")
                
                with gr.Row():
                    arabic_btn = gr.Button(
                        "العربية 🇸🇦",
                        size="sm",
                        variant="primary",
                        elem_classes=["lang-btn"]
                    )
                    english_btn = gr.Button(
                        "English 🇺🇸",
                        size="sm",
                        variant="secondary",
                        elem_classes=["lang-btn"]
                    )
                
                # خط فاصل | Divider
                gr.HTML("<hr style='border: 1px solid #475569; margin: 1rem 0;'>")
                
                # اختيار النموذج | Model Selection
                model_label = gr.HTML("<p style='font-size: 0.875rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.75rem;'>🤖 اختيار النموذج | Select Model</p>")
                
                # أزرار النماذج | Model Buttons
                with gr.Column(variant="panel"):
                    llama4_btn = gr.Button(
                        "🦙 Llama 4",
                        size="lg",
                        variant="primary",
                        elem_classes=["model-btn", "selected"]
                    )
                    gemini_btn = gr.Button(
                        "✨ Gemini 2.5",
                        size="lg",
                        variant="secondary",
                        elem_classes=["model-btn"]
                    )
                    qwen_btn = gr.Button(
                        "🌟 Qwen 2.5",
                        size="lg",
                        variant="secondary",
                        elem_classes=["model-btn"]
                    )
                    mistral_btn = gr.Button(
                        "💨 Mistral",
                        size="lg",
                        variant="secondary",
                        elem_classes=["model-btn"]
                    )
                    deepseek_btn = gr.Button(
                        "🧠 Deepseek-R1",
                        size="lg",
                        variant="secondary",
                        elem_classes=["model-btn"]
                    )
                
                # خط فاصل | Divider
                gr.HTML("<hr style='border: 1px solid #475569; margin: 1rem 0;'>")
                
                # معلومات النموذج الحالي | Current Model Info
                model_info_display = gr.HTML("""
                <div class="model-info" style="
                    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
                    border: 1px solid #6366f1;
                    border-radius: 0.75rem;
                    padding: 1rem;
                    text-align: center;
                ">
                    <p style="font-size: 1rem; font-weight: 600; color: #f1f5f9; margin: 0;">🦙 Llama 4</p>
                    <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.25rem 0 0 0;">Meta's Latest Model</p>
                </div>
                """)
                
                # مسافة فارغة | Spacer
                gr.HTML("<div style='flex: 1;'></div>")
                
                # زر مسح المحادثة | Clear Chat Button
                clear_btn = gr.Button(
                    "🗑️ مسح المحادثة | Clear Chat",
                    size="lg",
                    variant="stop",
                    elem_classes=["action-btn"]
                )
            
            # ════════════════════════════════════════════════════════════════════
            # منطقة الدردشة | Chat Area
            # ════════════════════════════════════════════════════════════════════
            
            with gr.Column(scale=3):
                
                # منطقة عرض الرسائل | Messages Display Area
                chat_display = gr.HTML(
                    value="""
                    <div class="welcome-screen" style="
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        height: 100%;
                        text-align: center;
                        padding: 2rem;
                        direction: rtl;
                    ">
                        <div class="welcome-icon" style="font-size: 4rem; margin-bottom: 1rem;">👋</div>
                        <h1 style="
                            font-size: 2rem;
                            font-weight: 700;
                            background: linear-gradient(135deg, #6366f1, #8b5cf6);
                            -webkit-background-clip: text;
                            -webkit-text-fill-color: transparent;
                            margin-bottom: 0.5rem;
                        ">مرحباً بك!</h1>
                        <p style="color: #94a3b8; margin-bottom: 2rem;">كيف يمكنني مساعدتك اليوم؟</p>
                        
                        <div class="suggestions-grid" style="
                            display: grid;
                            grid-template-columns: repeat(2, 1fr);
                            gap: 1rem;
                            max-width: 500px;
                        ">
                            <div class="suggestion-card" style="
                                padding: 1rem;
                                background: #1e293b;
                                border: 1px solid #475569;
                                border-radius: 0.75rem;
                                cursor: pointer;
                                text-align: right;
                            ">
                                <div style="font-size: 1.5rem;">💻</div>
                                <p style="font-weight: 600; margin: 0.25rem 0;">برمجة</p>
                                <p style="font-size: 0.8rem; color: #64748b; margin: 0;">ساعدني في كتابة كود</p>
                            </div>
                            
                            <div class="suggestion-card" style="
                                padding: 1rem;
                                background: #1e293b;
                                border: 1px solid #475569;
                                border-radius: 0.75rem;
                                cursor: pointer;
                                text-align: right;
                            ">
                                <div style="font-size: 1.5rem;">📝</div>
                                <p style="font-weight: 600; margin: 0.25rem 0;">كتابة</p>
                                <p style="font-size: 0.8rem; color: #64748b; margin: 0;">ساعدني في كتابة مقال</p>
                            </div>
                            
                            <div class="suggestion-card" style="
                                padding: 1rem;
                                background: #1e293b;
                                border: 1px solid #475569;
                                border-radius: 0.75rem;
                                cursor: pointer;
                                text-align: right;
                            ">
                                <div style="font-size: 1.5rem;">📊</div>
                                <p style="font-weight: 600; margin: 0.25rem 0;">تحليل</p>
                                <p style="font-size: 0.8rem; color: #64748b; margin: 0;">حلل هذه البيانات</p>
                            </div>
                            
                            <div class="suggestion-card" style="
                                padding: 1rem;
                                background: #1e293b;
                                border: 1px solid #475569;
                                border-radius: 0.75rem;
                                cursor: pointer;
                                text-align: right;
                            ">
                                <div style="font-size: 1.5rem;">🌐</div>
                                <p style="font-weight: 600; margin: 0.25rem 0;">ترجمة</p>
                                <p style="font-size: 0.8rem; color: #64748b; margin: 0;">ترجم نص من الإنجليزية</p>
                            </div>
                        </div>
                    </div>
                    """,
                    elem_id="chat-display",
                    elem_classes=["chat-display"]
                )
                
                # منطقة الإدخال | Input Area
                with gr.Row(elem_classes=["input-area"]):
                    with gr.Column(scale=1):
                        user_input = gr.Textbox(
                            placeholder="اكتب رسالتك هنا... | Type your message here...",
                            lines=3,
                            max_lines=6,
                            show_label=False,
                            container=False,
                            elem_classes=["chat-input"]
                        )
                
                with gr.Row():
                    send_btn = gr.Button(
                        "📤 إرسال | Send",
                        size="lg",
                        variant="primary",
                        scale=1
                    )
                
                # حالة إرسال الرسائل | Message Sending Status
                status_display = gr.HTML(
                    value="",
                    elem_id="status-display"
                )
        
        # ════════════════════════════════════════════════════════════════════
        # الأحداث والدوال | Events and Functions
        # ════════════════════════════════════════════════════════════════════
        
        # ════════════════════════════════════════════════════════════════════
        # أحداث اختيار اللغة | Language Selection Events
        # ════════════════════════════════════════════════════════════════════
        
        def on_arabic_click():
            """ عند النقر على العربية """
            return "ar"
        
        def on_english_click():
            """ عند النقر على الإنجليزية """
            return "en"
        
        arabic_btn.click(
            fn=on_arabic_click,
            outputs=current_lang
        )
        
        english_btn.click(
            fn=on_english_click,
            outputs=current_lang
        )
        
        # ════════════════════════════════════════════════════════════════════
        # أحداث اختيار النموذج | Model Selection Events
        # ════════════════════════════════════════════════════════════════════
        
        def on_model_select(model_key: str, lang: str) -> Tuple[str, str]:
            """ عند اختيار نموذج جديد """
            model_info = get_model_info(model_key)
            name = model_info.get("name_ar" if lang == "ar" else "name_en", model_key)
            desc = model_info.get("description_ar" if lang == "ar" else "description_en", "")
            
            info_html = f"""
            <div class="model-info" style="
                background: linear-gradient(135deg, {model_info['color']}33, {model_info['color']}22);
                border: 1px solid {model_info['color']};
                border-radius: 0.75rem;
                padding: 1rem;
                text-align: center;
            ">
                <p style="font-size: 1rem; font-weight: 600; color: #f1f5f9; margin: 0;">{model_info['icon']} {name}</p>
                <p style="font-size: 0.75rem; color: #94a3b8; margin: 0.25rem 0 0 0;">{desc}</p>
            </div>
            """
            
            return model_key, info_html
        
        llama4_btn.click(
            fn=lambda lang: on_model_select("llama4", lang),
            inputs=current_lang,
            outputs=[current_model, model_info_display]
        )
        
        gemini_btn.click(
            fn=lambda lang: on_model_select("gemini2.5", lang),
            inputs=current_lang,
            outputs=[current_model, model_info_display]
        )
        
        qwen_btn.click(
            fn=lambda lang: on_model_select("qwen2.5", lang),
            inputs=current_lang,
            outputs=[current_model, model_info_display]
        )
        
        mistral_btn.click(
            fn=lambda lang: on_model_select("mistral", lang),
            inputs=current_lang,
            outputs=[current_model, model_info_display]
        )
        
        deepseek_btn.click(
            fn=lambda lang: on_model_select("deepseek-r1", lang),
            inputs=current_lang,
            outputs=[current_model, model_info_display]
        )
        
        # ════════════════════════════════════════════════════════════════════
        # حدث إرسال الرسالة | Message Sending Event
        # ════════════════════════════════════════════════════════════════════
        
        def on_send_message(
            message: str,
            model_key: str,
            history: List,
            lang: str
        ) -> Tuple[str, str, List]:
            """ عند إرسال رسالة جديدة """
            if not message or not message.strip():
                return "", "", history, ""
            
            # محاكاة استجابة الذكاء الاصطناعي | Simulate AI response
            response, updated_history = simulate_ai_response(
                message.strip(),
                model_key,
                history,
                lang
            )
            
            # إنشاء HTML للرسالة | Create message HTML
            user_msg_html = f"""
            <div class="message user" style="
                display: flex;
                gap: 1rem;
                max-width: 85%;
                align-self: flex-end;
                flex-direction: {'row-reverse' if lang == 'ar' else 'row'};
                margin: 0.5rem 0;
                animation: fadeIn 0.3s ease;
            ">
                <div class="message-avatar" style="
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    flex-shrink: 0;
                ">👤</div>
                <div class="message-content" style="
                    padding: 1rem 1.25rem;
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    color: white;
                    border-radius: 1rem;
                    font-size: 0.95rem;
                    line-height: 1.6;
                    {'border-bottom-right-radius: 0.25rem;' if lang == 'ar' else 'border-bottom-left-radius: 0.25rem;'}
                ">{message}</div>
            </div>
            """
            
            # إنشاء HTML للاستجابة | Create response HTML
            assistant_msg_html = f"""
            <div class="message assistant" style="
                display: flex;
                gap: 1rem;
                max-width: 85%;
                align-self: flex-start;
                margin: 0.5rem 0;
                animation: fadeIn 0.3s ease;
            ">
                <div class="message-avatar" style="
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.25rem;
                    background: linear-gradient(135deg, #10b981, #059669);
                    flex-shrink: 0;
                ">🤖</div>
                <div class="message-content" style="
                    padding: 1rem 1.25rem;
                    background: #1e293b;
                    border: 1px solid #475569;
                    border-radius: 1rem;
                    font-size: 0.95rem;
                    line-height: 1.6;
                    {'border-bottom-left-radius: 0.25rem;' if lang == 'ar' else 'border-bottom-right-radius: 0.25rem;'}
                ">{response}</div>
            </div>
            """
            
            return "", "", updated_history, ""
        
        def on_send_click(
            message: str,
            model_key: str,
            history: List,
            lang: str
        ) -> Tuple[str, str, List]:
            """ عند النقر على زر الإرسال """
            if not message or not message.strip():
                return message, "", history, ""
            
            return on_send_message(message, model_key, history, lang)
        
        # ربط حدث الضغط على Enter | Bind Enter key press event
        user_input.submit(
            fn=on_send_message,
            inputs=[user_input, current_model, chat_history, current_lang],
            outputs=[user_input, chat_display, chat_history, status_display]
        )
        
        # ربط حدث النقر على زر الإرسال | Bind send button click event
        send_btn.click(
            fn=on_send_click,
            inputs=[user_input, current_model, chat_history, current_lang],
            outputs=[user_input, chat_display, chat_history, status_display]
        )
        
        # ════════════════════════════════════════════════════════════════════
        # حدث مسح المحادثة | Clear Chat Event
        # ════════════════════════════════════════════════════════════════════
        
        def on_clear_chat(lang: str) -> Tuple[str, List]:
            """ عند مسح المحادثة """
            welcome_html = create_welcome_html(lang)
            return welcome_html, []
        
        clear_btn.click(
            fn=on_clear_chat,
            inputs=current_lang,
            outputs=[chat_display, chat_history]
        )
        
        # ════════════════════════════════════════════════════════════════════
        # حقن JavaScript | JavaScript Injection
        # ════════════════════════════════════════════════════════════════════
        
        gr.HTML("""
        <script>
        // دوال JavaScript المساعد | Helper JavaScript Functions
        
        // دالة اختيار الاقتراح | Suggestion Selection Function
        function selectSuggestion(text, lang) {
            const inputField = document.querySelector('.chat-input textarea, #user_input textarea');
            if (inputField) {
                inputField.value = text;
                inputField.focus();
            }
        }
        
        // دالة نسخ الكود | Code Copy Function
        function copyCode(button) {
            const codeBlock = button.parentElement.nextElementSibling;
            const code = codeBlock.textContent;
            navigator.clipboard.writeText(code).then(() => {
                button.textContent = '✓ Copied!';
                setTimeout(() => {
                    button.textContent = '📋 Copy';
                }, 2000);
            });
        }
        
        // دالة إظهار/إخفاء التفكير | Show/Hide Thinking Function
        function toggleThinking(button) {
            const content = button.nextElementSibling;
            const icon = button.querySelector('.thinking-toggle');
            
            if (content.style.display === 'none') {
                content.style.display = 'block';
                icon.style.transform = 'rotate(180deg)';
                button.textContent = '😌 إخفاء التفكير';
            } else {
                content.style.display = 'none';
                icon.style.transform = 'rotate(0deg)';
                button.textContent = '🤔 إظهار التفكير';
            }
        }
        
        // تهيئة عند تحميل الصفحة | Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 Multi-LLM Chat Interface Loaded Successfully!');
        });
        
        // معالجة الأخطاء العامة | Global error handling
        window.onerror = function(msg, url, lineNo, columnNo, error) {
            console.error('Error: ', msg, '\\nURL: ', url, '\\nLine: ', lineNo, '\\nColumn: ', columnNo, '\\nError object: ', error);
            return false;
        };
        </script>
        """)
    
    return interface

# ════════════════════════════════════════════════════════════════════════════
# القسم الخامس: نقطة الدخول الرئيسية | Section 5: Main Entry Point
# ════════════════════════════════════════════════════════════════════════════

def main():
    """
    الدالة الرئيسية لتشغيل التطبيق.
    
    Main function to launch the application.
    """
    # إنشاء الواجهة | Create the interface
    interface = create_interface()
    
    # تشغيل التطبيق | Launch the interface
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        enable_queue=True,
        max_threads=10
    )

if __name__ == "__main__":
    main()

"""
═══════════════════════════════════════════════════════════════════════════════
                              نهاية الملف | End of File
═══════════════════════════════════════════════════════════════════════════════
"""
