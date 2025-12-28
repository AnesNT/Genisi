"use client";

import { useState } from "react";
import { clsx } from "clsx";

type Mode = "pro" | "light" | "basic";

export default function Home() {
  const [mode, setMode] = useState<Mode>("pro");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: "user" | "ai"; text: string; latency?: number }[]>([]);
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!input.trim()) return;
    const userMsg = { role: "user" as const, text: input };
    setMessages((m) => [...m, userMsg]);
    setLoading(true);
    const t0 = performance.now();

    try {
      const res = await fetch("/api/genisi", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mode, prompt: input })
      });
      const data = await res.json();
      const t1 = performance.now();
      setMessages((m) => [...m, { role: "ai", text: data.reply, latency: Math.round(t1 - t0) }]);
    } catch {
      setMessages((m) => [...m, { role: "ai", text: "تعذر الرد. نحاول التحويل إلى Basic تلقائيًا..." }]);
      setMode("basic");
    } finally {
      setLoading(false);
      setInput("");
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <Header />
      <Hero />
      <ModeTabs mode={mode} setMode={setMode} />
      <ActionDock />
      <PromptBar
        mode={mode}
        input={input}
        setInput={setInput}
        loading={loading}
        onSend={send}
      />
      <Chat messages={messages} mode={mode} />
    </div>
  );
}

function Header() {
  return (
    <header className="flex items-center justify-between border-b border-[#1A1D22] px-7 py-5">
      <h1 className="tracking-[0.12em] font-extrabold text-xl">GENISI</h1>
      <div className="flex items-center gap-3">
        <span className="px-3 py-1 rounded-lg border border-[#2A2E35] bg-[#121212] text-sm">GENISI Plus</span>
        <span className="text-muted text-sm">Stable</span>
        <div className="w-9 h-9 rounded-full bg-[#1A1D22] grid place-items-center">A</div>
      </div>
    </header>
  );
}

function Hero() {
  return (
    <section className="px-7 py-6 text-muted">
      <p>أهلا يا أنس — حان وقت تأليف 2026 مع GENISI.</p>
    </section>
  );
}

function ModeTabs({ mode, setMode }: { mode: Mode; setMode: (m: Mode) => void }) {
  return (
    <nav className="flex gap-2 px-7 py-3">
      <button
        className={clsx(
          "px-4 py-2 rounded-full border bg-[#121418] text-[#C9CED8]",
          mode === "pro" ? "border-gold shadow-glowGold" : "border-[#1F232B]"
        )}
        onClick={() => setMode("pro")}
      >
        Pro ✨
      </button>
      <button
        className={clsx(
          "px-4 py-2 rounded-full border bg-[#121418] text-[#C9CED8]",
          mode === "light" ? "border-blue shadow-glowBlue" : "border-[#1F232B]"
        )}
        onClick={() => setMode("light")}
      >
        Light ⚡
      </button>
      <button
        className={clsx(
          "px-4 py-2 rounded-full border bg-[#121418] text-[#C9CED8] border-grayx",
          mode === "basic" && "ring-1 ring-grayx"
        )}
        onClick={() => setMode("basic")}
      >
        Basic 🟦
      </button>
    </nav>
  );
}

function ActionDock() {
  return (
    <section className="flex gap-2 px-7 py-2">
      {["الأدوات","إنشاء صورة","اكتب أي شيء","ساعدني أتعلم","ارفع يومي"].map((label) => (
        <button key={label} className="bg-[#121418] border border-[#1F232B] text-[#C9CED8] px-3 py-2 rounded-lg">
          {label}
        </button>
      ))}
    </section>
  );
}

function PromptBar({
  mode, input, setInput, loading, onSend
}: {
  mode: Mode; input: string; setInput: (v: string) => void; loading: boolean; onSend: () => void;
}) {
  return (
    <section className="flex gap-2 px-7 py-4 border-t border-[#1A1D22] sticky top-0 bg-bg/90 backdrop-blur">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="اسأل GENISI…"
        className="flex-1 bg-[#0F1115] border border-[#1A1D22] text-fg px-4 py-3 rounded-xl outline-none"
      />
      <select
        value={mode}
        onChange={(e) => {/* optional sync with tabs */}}
        className="bg-[#161920] border border-[#262A33] text-[#DDE3ED] px-3 py-2 rounded-lg"
      >
        <option value="pro">Pro</option>
        <option value="light">Light</option>
        <option value="basic">Basic</option>
      </select>
      <button
        disabled={loading}
        onClick={onSend}
        className="bg-[#161920] border border-[#262A33] text-[#DDE3ED] px-4 py-2 rounded-lg"
      >
        {loading ? "يرد…" : "أرسل"}
      </button>
    </section>
  );
}

function Chat({ messages, mode }: { messages: { role: "user" | "ai"; text: string; latency?: number }[]; mode: Mode }) {
  return (
    <main className="px-7 py-4 flex flex-col gap-3">
      {messages.map((m, i) => (
        <div
          key={i}
          className={clsx(
            "p-3 rounded-xl max-w-3xl border",
            m.role === "user" ? "bg-[#121418] border-[#1F232B]" : "bg-[#14161C]/70 backdrop-blur border-[#1F232B]",
            m.role === "ai" && mode === "pro" && "ring-1 ring-gold",
            m.role === "ai" && mode === "light" && "ring-1 ring-blue"
          )}
        >
          {m.role === "ai" && m.latency !== undefined && (
            <div className="text-xs text-muted mb-1">GENISI {mode} • {m.latency} ms</div>
          )}
          <div>{m.text}</div>
        </div>
      ))}
    </main>
  );
}
