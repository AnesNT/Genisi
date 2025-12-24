from fastapi import FastAPI, HTTPException
import httpx, os, base64, datetime, json

app = FastAPI()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")  # مثال: "AnesNT/genisi-data"
FILE_PATH = "answers.json"

OLLAMA_URL = "https://api.ollama.com/v1/chat/completions"

@app.post("/ask")
async def ask_question(payload: dict):
    question = payload.get("question")
    mode = payload.get("mode", "fast")  # fast=20B, deep=120B

    if not question:
        raise HTTPException(status_code=400, detail="السؤال مطلوب")

    model = "gpt-oss:20b-cloud" if mode == "fast" else "gpt-oss:120b-cloud"

    headers = {"Authorization": f"Bearer {OLLAMA_API_KEY}", "Content-Type": "application/json"}
    body = {"model": model, "messages": [{"role": "user", "content": question}]}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(OLLAMA_URL, headers=headers, json=body)

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)

    data = resp.json()
    answer = data["choices"][0]["message"]["content"]

    # 📝 إدخال جديد للتخزين
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "question": question,
        "answer": answer,
        "model": model
    }

    # تحديث الملف في GitHub
    gh_headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}", headers=gh_headers)
        if resp.status_code == 200:
            content = resp.json()
            old_data = json.loads(base64.b64decode(content["content"]).decode("utf-8"))
            old_data.append(entry)
            sha = content["sha"]
        else:
            old_data = [entry]
            sha = None

        encoded = base64.b64encode(json.dumps(old_data, indent=2).encode("utf-8")).decode("utf-8")
        update_body = {"message": f"Add answer {entry['timestamp']}", "content": encoded, "branch": "main"}
        if sha: update_body["sha"] = sha

        await client.put(f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}", headers=gh_headers, json=update_body)

    return {"model": model, "answer": answer}
