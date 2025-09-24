from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import os
import uuid
import sys
import sqlite3

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",  # or use "mixtral-8x7b-32768", etc.
    api_key=os.getenv("GROQ_API_KEY"))

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state: ChatState):
    messages = state['messages']
    
    # Ensure run_id is always a string when passed internally
    response = llm.invoke(messages)
    if hasattr(response, "run_id") and not isinstance(response.run_id, str):
        response.run_id = str(response.run_id)
    elif isinstance(response, dict) and "run_id" in response and not isinstance(response["run_id"], str):
        response["run_id"] = str(response["run_id"])
    
    return {"messages": [response]}

conn = sqlite3.connect(database= 'chatbot.db', check_same_thread= False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)



DB_PATH = os.path.join(os.path.dirname(__file__), "chatbot.db")

def ensure_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        thread_id TEXT,
        role TEXT,
        content TEXT
    )
    """)
    conn.commit()
    conn.close()

def retrieve_all_threads():
    ensure_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT thread_id FROM conversations")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def save_message(thread_id: str, role: str, content: str):
    ensure_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO conversations (thread_id, role, content) VALUES (?, ?, ?)",
        (thread_id, role, content),
    )
    conn.commit()
    conn.close()

def delete_thread(thread_id: str):
    ensure_tables()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM conversations WHERE thread_id = ?", (thread_id,))
    conn.commit()
    conn.close()