import express from "express";
import fetch from "node-fetch";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

// نقطة النهاية الخاصة بالـ Space
const HF_SPACE_URL = "https://huggingface.co/spaces/McLoviniTtt/Reasoner4All/api/predict";

app.post("/api/chat", async (req, res) => {
  try {
    const { messages } = req.body;

    // نرسل آخر رسالة للموديل
    const userMessage = messages[messages.length - 1].content;

    const hfResp = await fetch(HF_SPACE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: [userMessage] })
    });

    const data = await hfResp.json();

    // الرد يجي غالبًا في data[0]
    const reply = data?.data?.[0] || "ما جاوبش النموذج.";

    res.json({ reply });
  } catch (err) {
    console.error("Error:", err);
    res.status(500).json({ error: "internal_error" });
  }
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`GENISI backend running on http://localhost:${port}`));
