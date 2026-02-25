#  n8n AI Agent Chat — Streamlit UI

A clean, minimal Streamlit frontend that connects to a **self-hosted n8n AI agent** via webhook, enabling real-time streaming chat with any n8n-powered backend. Initially built as a personal RAG tutor for Database & Machine Learning textbooks, but fully extensible to any n8n workflow.


---

## ✨ Features

- 💬 **Streaming chat interface** — responses stream in real time, token by token
- 🧠 **Connects to any n8n workflow** — just plug in your webhook URL
- 🖼️ **Renders HTML/Markdown safely** — supports rich content including images returned by the agent
- 🔒 **Secure webhook handling** — webhook URL loaded from Streamlit secrets, never hardcoded
- 🗂️ **Persistent chat history** — full conversation context maintained within a session
- ☁️ **One-click deploy** — ready for Streamlit Cloud deployment out of the box

---

## 🏗️ Architecture

```
User (Browser)
     │
     ▼
Streamlit UI (this repo)
     │  POST /webhook  (streaming)
     ▼
n8n Workflow (self-hosted / cloud)
     │
     ├── RAG Pipeline (Supabase Vector Store)
     ├── Cohere Reranker
     ├── SerpAPI Validation
     └── Google Gemini LLM (or Ollama for local/private)
```

The Streamlit app sends user messages to your n8n webhook and streams back the response chunks, rendering them live in the chat interface.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A running n8n instance (self-hosted or [n8n Cloud](https://n8n.io/))
- An n8n workflow with a **Webhook trigger** that returns streaming JSON responses

### 1. Clone the repo

```bash
git clone https://github.com/Raviteja-1851/n8n-streamlit-chat.git
cd n8n-streamlit-chat
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your webhook URL

Create a `.streamlit/secrets.toml` file:

```toml
N8N_WEBHOOK = "https://your-ngrok-or-n8n-url/webhook/your-path"
```

> ⚠️ Never commit your `secrets.toml` — it's already in `.gitignore`.

### 4. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy to Streamlit Cloud

1. Push this repo to your GitHub account.
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and create a new app pointing to this repo.
3. Under **App Settings → Secrets**, add:
   ```toml
   N8N_WEBHOOK = "https://your-n8n-webhook-url"
   ```
4. Deploy — your app will be live with a public URL!

---

## 🔧 n8n Webhook Response Format

Your n8n workflow should return **streaming JSON chunks** in this format:

```json
{ "type": "item", "content": "partial response text here" }
```

Each chunk is parsed and appended to the chat output in real time. Non-matching chunks are safely ignored.

---

## 📁 Project Structure

```
n8n-streamlit-chat/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .devcontainer/
│   └── devcontainer.json   # GitHub Codespaces config
└── .vscode/
    └── settings.json       # VS Code file exclusion settings
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend Orchestration | n8n |
| Vector Store | Supabase (pgvector) |
| LLM | Google Gemini / Ollama |
| Reranker | Cohere |
| Search Validation | SerpAPI |
| OCR (ingestion) | Mistral OCR |
| Tunneling (local dev) | ngrok |

---

## 🔮 Roadmap

- [ ] Smarter query routing between knowledge domains
- [ ] Enhanced UI with file upload support
- [ ] LangChain integration for more complex agent chains
- [ ] Multi-session / user authentication support

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 👨‍💻 Author

**Raviteja Bejawada**  
AI Developer | MS Information Technology, University of Memphis  
🔗 [LinkedIn](https://www.linkedin.com/in/raviteja-bejawada-77906b16b) · [GitHub](https://github.com/Raviteja-1851) · [Portfolio](https://raviteja-bejawada.bolt.host/)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
