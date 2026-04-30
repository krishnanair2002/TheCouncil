# 🧠 LLM Deliberation Pipeline (Single GGUF Model)

A lightweight multi-role reasoning system using a single local GGUF model.
Simulates multiple agents (Writer, Critic, Refiner, Judge) using structured prompts.

Designed to work well even with **low-bit quantized models (including 1-bit)**.

---

# 📦 Project Structure

```
llm-deliberation-pipeline/
│
├── main.py
├── config.json
├── requirements.txt
├── README.md
│
└── models/
    └── (your .gguf files go here)
```

---

# 📄 `requirements.txt`

Minimal:

```
gpt4all>=2.7.0
```

Optional (recommended for nicer UX):

```
gpt4all>=2.7.0
colorama>=0.4.6
tqdm>=4.66.0
```

---

## 📦 Installation

### 1. Clone or download this project

```bash
git clone https://github.com/{yourname}/TheCouncil.git
cd TheCouncil
```

---

## 🧪 2. Create Virtual Environment (Recommended)

### macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (CMD):

```bash
python -m venv venv
venv\Scripts\activate
```

### Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

You should now see `(venv)` in your terminal.

---

## 📦 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🤖 Model Setup

1. Download a `.gguf` model compatible with GPT4All
2. Place it inside the `models/` folder

Example:

```
models/mistral-7b-instruct.gguf
```

3. Update `config.json`:

```json
"model": {
  "name": "models/mistral-7b-instruct.gguf",
  "max_tokens": 256
}
```

---
## Model Links
Verified working models live in modelsites.txt

## ⚙️ Configuration

Edit `config.json` to control behavior:

### Example

```json
{
  "model": {
    "name": "models/mistral-7b-instruct.gguf",
    "max_tokens": 256,
    "device": "cpu"
  },
  "pipeline": {
    "max_rounds": 2,
    "show_discourse": true
  },
  "roles": {
    "writer": {
      "system": "You are a writer. Answer clearly in under 150 words. Do not repeat yourself.",
      "temperature": 0.6
    },
    "critic": {
      "system": "Return EXACTLY:\nISSUES:\n- ...\nMax 5 bullets. Be strict.",
      "temperature": 0.2
    },
    "refiner": {
      "system": "Rewrite the answer using the critique. Keep it concise and correct.",
      "temperature": 0.5
    },
    "judge": {
      "system": "Default to FAIL unless clearly correct.\nOutput ONLY:\nVERDICT: PASS or FAIL\nREASON: one sentence",
      "temperature": 0.1
    }
  }
}
```

---

## 🚀 Usage

Run the program:

```bash
python main.py
```

Then enter a question:

```
Ask a question: What is a black hole?
```

---

## 🔍 Example Output

```
USER QUESTION:
What is a black hole?

=== WRITER ===
A black hole is...

=== CRITIC ===
ISSUES:
- Too vague
- Missing explanation of gravity

=== REFINER ===
A black hole is a region...

=== JUDGE ===
VERDICT: PASS
REASON: Clear and accurate

=== FINAL ANSWER ===
A black hole is...
```

---

## ⚡ Performance Tips (Important for 1-bit Models)

Low-bit models are fragile. Follow these rules:

### ✅ Keep outputs short

* max_tokens ≤ 256
* answers ≤ 150 words

### ✅ Use strict formats

Force structure like:

```
ISSUES:
- ...
```

### ✅ Lower temperature

| Role    | Temperature |
| ------- | ----------- |
| Writer  | 0.5–0.7     |
| Critic  | 0.1–0.3     |
| Refiner | 0.4–0.6     |
| Judge   | 0.0–0.2     |

### ✅ Limit rounds

* Recommended: 1–2 max

### ✅ Expect tradeoffs

1-bit models:

* ✅ Good at formatting
* ❌ Weak at deep reasoning

---

## 🧩 How It Works

The system runs a fixed pipeline:

1. **Writer** → generates initial answer
2. **Critic** → identifies flaws
3. **Refiner** → improves answer
4. **Judge** → decides if it's good enough

Loop stops when:

* Judge returns `PASS`
* OR max rounds reached

---

## 🛠 Customization Ideas

* Add a **Compressor role** (final cleanup)
* Add **multiple critics** (voting system)
* Save outputs to logs
* Build a web UI (Gradio, FastAPI)

---

## ⚠️ Limitations

* Not a true multi-agent system (single model reused)
* Quality depends heavily on prompt design
* Small models may:

  * Repeat themselves
  * Approve weak answers
  * Miss subtle errors

---

## 🧼 Deactivate Virtual Environment

When you're done:

```bash
deactivate
```

---

## 📜 License

MIT

---

## 🤝 Contributing

Feel free to improve prompts, add roles, or optimize for new models.

