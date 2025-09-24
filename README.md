# 🤖 LangGraph + Streamlit + Groq Chatbot

This repository contains a Streamlit-based AI chatbot built using LangGraph for conversation state management and Groq LLMs for fast and cost-effective inference.

The chatbot supports:

Multiple conversations (threaded chats): Each chat session is stored in an SQLite database.

Smart session management: Chats are automatically named based on user prompts, and can be renamed or deleted manually.

Persistent memory: Conversations are checkpointed and restored between app restarts.

Streaming responses: The chatbot streams LLM outputs in real-time for a smoother user experience.

Clean UI: Built with Streamlit, offering a sidebar for session control (create, switch, rename, delete chats).

This project is designed as a starter template for AI-driven applications that use LangGraph for workflow orchestration and Streamlit for deployment. It is production-ready for Streamlit Cloud and easily adaptable to other LLM providers by swapping out the Groq integration. 

---

## 🚀 Features
- ✅ Chat with Groq LLMs (streamed responses)  
- ✅ Multi-session chat memory (SQLite-powered)  
- ✅ Rename & delete conversations  
- ✅ Automatic smart chat titles  
- ✅ Minimal UI with Streamlit  

---

## 📦 Installation

### 1. Clone this repo
```bash
git clone https://github.com/Anaspro72/smart_memory_chatbot.git
cd smart_memory_chatbot
