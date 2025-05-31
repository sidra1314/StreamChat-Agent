# AI Chatbot with Chainlit & Gemini API

This is a smart AI chatbot built using **Chainlit**, **LiteLLM**, and **Gemini API**. It streams real-time responses and automatically saves each conversation in a JSON file (`chat_history.json`).

## 🔧 Features

- Uses Gemini API with OpenAI-style wrappers (LiteLLM)
- Real-time streamed replies using Chainlit UI
- Stores full chat history in `chat_history.json`
- Clean, minimal, and beginner-friendly architecture

## 📦 Tech Stack

- Python 🐍
- Chainlit 🧵
- Gemini API (via LiteLLM)
- JSON for storing conversation history

## 🚀 Getting Started

1. Clone the repository
2. Set your `.env` file with Gemini credentials
3. Run the app:
   ```bash
   chainlit run chatbot.py
