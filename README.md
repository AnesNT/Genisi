# Multi-LLM Chat Interface

واجهة دردشة متعددة النماذج اللغوية

## الوصف | Description

واجهة دردشة حديثة ومتطورة تدعم التبديل بين خمسة نماذج ذكاء اصطناعي متقدمين، مع دعم كامل للغة العربية واتجاه الكتابة من اليمين لليسار (RTL).

A modern chat interface supporting five advanced AI language models with full Arabic language support and RTL direction.

## النماذج المدعومة | Supported Models

- **Llama 4** - Meta's latest large language model
- **Gemini 2.5** - Google's advanced multimodal AI
- **Qwen2.5** - Alibaba's powerful language model
- **Mistral** - Efficient and capable French AI model
- **Deepseek-R1** - Advanced reasoning model with thinking process display

## المميزات | Features

✨ **واجهة حديثة** - تصميم أنيق وعصري مع تدرجات لونية جذابة

🗣️ **دعم ثنائي اللغة** - تبديل سلس بين العربية والإنجليزية

📱 **تصميم متجاوب** - يعمل بشكل ممتاز على جميع الأجهزة

🌙 **الوضع الداكن/الفاتح** - تبديل فوري بين الوضعين

💬 **عرض عمليات التفكير** - عرض خاص لعمليات التفكير لنموذج Deepseek-R1

📝 **تلوين الصيغة البرمجية** - دعم كامل للكود مع تلوين الصيغة

💾 **حفظ المحادثات** - تخزين المحادثات محلياً

## التثبيت | Installation

```bash
# Clone the repository
git clone https://huggingface.co/spaces/McLoviniTtt/Chat-with-Llama-4-Gemini-2.5-Qwen2.5-Mistral-and-Deepseek-R1-reasoning-augmented-LLMs

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## النشر على Hugging Face Spaces

```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login

# Create Space
huggingface_spaces create --name "your-space-name"

# Push to Space
git add .
git commit -m "Initial commit"
git push
```

## هيكل الملفات | File Structure

```
chatbot_interface/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── style.css          # Custom styling
└── README.md          # This file
```

## المتطلبات | Requirements

- Python 3.8+
- Gradio 4.0+
- Additional dependencies in requirements.txt

## الإعدادات | Configuration

### متغيرات البيئة | Environment Variables

```bash
# API Configuration (if needed)
HF_API_TOKEN=your_huggingface_token
```

## الترخيص | License

MIT License

## المساهمة | Contributing

المساهمات مرحب بها! Please feel free to submit issues and pull requests.
