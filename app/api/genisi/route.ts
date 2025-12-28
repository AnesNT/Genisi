import { NextRequest } from "next/server";

const OPENROUTER_API = "https://openrouter.ai/api/v1/chat/completions";

const MODELS: Record<"pro" | "light", string> = {
  pro: "meta-llama/llama-3.3-70b-instruct",
  light: "nex-agi/deepseek-v3.1-nex-n1"
};

export async function POST(req: NextRequest) {
  const { mode, prompt } = await req.json();
  if (mode === "basic") {
    const endpoint = process.env.BASIC_ENDPOINT!;
    try {
      const r = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt })
      });
      const j = await r.json();
      return Response.json({ reply: j.reply ?? j.text ?? "رد بسيط من Basic." });
    } catch {
      return Response.json({ reply: "Basic غير متاح حالياً." }, { status: 200 });
    }
  }

  const model = MODELS[mode as "pro" | "light"] ?? MODELS.pro;
  try {
    const r = await fetch(OPENROUTER_API, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model,
        messages: [
          { role: "system", content: "You are GENISI: premium, concise, helpful, multilingual." },
          { role: "user", content: prompt }
        ]
      })
    });
    const j = await r.json();
    const reply = j?.choices?.[0]?.message?.content ?? "ماكانش رد.";
    return Response.json({ reply });
  } catch {
    return Response.json({ reply: "تعذر الوصول لـ OpenRouter. نحاول Basic كـ احتياط." }, { status: 200 });
  }
}
