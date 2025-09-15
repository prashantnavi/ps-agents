from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
import math
from typing import List, Tuple
import sqlite3
import time


load_dotenv(override=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

# SQLite-backed common Q&A tools
def _db_path() -> str:
    return os.path.join(os.path.dirname(__file__), "knowledge.db")

def add_common_qa(question: str, answer: str):
    conn = sqlite3.connect(_db_path())
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS qa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT UNIQUE,
                answer TEXT,
                updated_at REAL
            )
        """)
        now_ts = time.time()
        cur.execute("INSERT INTO qa (question, answer, updated_at) VALUES (?, ?, ?) ON CONFLICT(question) DO UPDATE SET answer=excluded.answer, updated_at=excluded.updated_at", (question.strip(), answer.strip(), now_ts))
        conn.commit()
        return {"status": "ok", "updated_at": now_ts}
    finally:
        conn.close()

def search_common_qa(query: str, top_k: int = 3):
    conn = sqlite3.connect(_db_path())
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS qa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT UNIQUE,
                answer TEXT,
                updated_at REAL
            )
        """)
        like = f"%{query.strip()}%"
        cur.execute("SELECT question, answer, updated_at FROM qa WHERE question LIKE ? OR answer LIKE ? ORDER BY updated_at DESC LIMIT ?", (like, like, top_k))
        rows = cur.fetchall()
        results = [{"question": q, "answer": a, "updated_at": ts} for (q, a, ts) in rows]
        return {"results": results}
    finally:
        conn.close()

def get_all_qa_pairs():
    """Get all Q&A pairs from the database for debugging"""
    conn = sqlite3.connect(_db_path())
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS qa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT UNIQUE,
                answer TEXT,
                updated_at REAL
            )
        """)
        cur.execute("SELECT question, answer, updated_at FROM qa ORDER BY updated_at DESC")
        rows = cur.fetchall()
        results = [{"question": q, "answer": a, "updated_at": ts} for (q, a, ts) in rows]
        return {"results": results, "count": len(results)}
    finally:
        conn.close()

add_common_qa_json = {
    "name": "add_common_qa",
    "description": "Upsert a common Q&A pair into the SQLite knowledge base for future reuse.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "Canonical user question"},
            "answer": {"type": "string", "description": "Preferred answer to return"}
        },
        "required": ["question", "answer"],
        "additionalProperties": False
    }
}

search_common_qa_json = {
    "name": "search_common_qa",
    "description": "Search the SQLite knowledge base for similar or matching Q&A by keyword.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Search query (keywords)"},
            "top_k": {"type": "integer", "description": "Max results to return", "default": 3}
        },
        "required": ["query"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json},
        {"type": "function", "function": add_common_qa_json},
        {"type": "function", "function": search_common_qa_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Prashant Sharma"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()
        # SQLite init
        self._init_db()
        self.qa_pairs, self.qa_last_updated = self._load_qa_from_db()
        # RAG setup: chunk profile corpus + Q&A and embed once
        self._rebuild_embeddings()


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        system_prompt += "\n\nAdditionally, you have access to tools to manage a SQLite knowledge base of common questions and answers: use search_common_qa to look up existing answers and add_common_qa to store good answers for future use. IMPORTANT: Always search the knowledge base first when answering questions, and if you provide a comprehensive answer, use add_common_qa to store it for future reference. This helps build a knowledge base of frequently asked questions."
        return system_prompt
    
    def chat(self, message, history):
        # Store the original user message
        original_user_message = message
        
        # Refresh embeddings if DB changed
        self._maybe_refresh_embeddings()
        retrieved_context = self._build_rag_context(message)
        rag_preamble = "Use the following retrieved context if relevant. If it's not helpful, ignore it.\n\n" + retrieved_context if retrieved_context else ""
        messages = [{"role": "system", "content": self.system_prompt()}, {"role": "system", "content": rag_preamble}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        
        # Get the final response content
        final_response = response.choices[0].message.content
        
        # Automatically save Q&A pair if it's a meaningful exchange
        if final_response and len(final_response.strip()) > 10:  # Only save if response is substantial
            self._auto_save_qa_pair(original_user_message, final_response)
        
        return final_response

    # -------------------- RAG utilities --------------------
    def _init_db(self):
        conn = sqlite3.connect(_db_path())
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS qa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT UNIQUE,
                    answer TEXT,
                    updated_at REAL
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def _load_qa_from_db(self) -> Tuple[List[Tuple[str, str]], float]:
        conn = sqlite3.connect(_db_path())
        try:
            cur = conn.cursor()
            cur.execute("SELECT question, answer, updated_at FROM qa ORDER BY updated_at DESC")
            rows = cur.fetchall()
            last_updated = 0.0
            qa_pairs: List[Tuple[str, str]] = []
            for q, a, ts in rows:
                qa_pairs.append((q or "", a or ""))
                if ts and ts > last_updated:
                    last_updated = ts
            return qa_pairs, last_updated
        finally:
            conn.close()

    def _rebuild_embeddings(self):
        corpus_items: List[str] = []
        corpus_items.append(self.summary + "\n\n" + self.linkedin)
        for q, a in self.qa_pairs:
            corpus_items.append(f"Q: {q}\nA: {a}")
        combined_text = "\n\n\n".join(corpus_items)
        self.corpus_chunks = self._chunk_text(combined_text)
        self.chunk_embeddings = self._embed_texts(self.corpus_chunks)

    def _maybe_refresh_embeddings(self):
        conn = sqlite3.connect(_db_path())
        try:
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(MAX(updated_at), 0) FROM qa")
            row = cur.fetchone()
            max_updated = row[0] if row and row[0] is not None else 0.0
        finally:
            conn.close()
        if max_updated > (self.qa_last_updated or 0.0):
            self.qa_pairs, self.qa_last_updated = self._load_qa_from_db()
            self._rebuild_embeddings()

    def _chunk_text(self, text: str, max_chars: int = 800, overlap: int = 100) -> List[str]:
        text = (text or "").strip()
        if not text:
            return []
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + max_chars)
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end == len(text):
                break
            start = end - overlap
            if start < 0:
                start = 0
        return chunks

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        # Batch embeddings to keep within token limits
        model = "text-embedding-3-small"
        embeddings: List[List[float]] = []
        batch_size = 64
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            resp = self.openai.embeddings.create(model=model, input=batch)
            embeddings.extend([d.embedding for d in resp.data])
        return embeddings

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = 0.0
        norm_a = 0.0
        norm_b = 0.0
        for x, y in zip(a, b):
            dot += x * y
            norm_a += x * x
            norm_b += y * y
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))

    def _similarity_search(self, query: str, k: int = 4) -> List[Tuple[float, str]]:
        if not self.corpus_chunks:
            return []
        q_emb = self._embed_texts([query])
        if not q_emb:
            return []
        q = q_emb[0]
        scored: List[Tuple[float, str]] = []
        for emb, chunk in zip(self.chunk_embeddings, self.corpus_chunks):
            scored.append((self._cosine_similarity(q, emb), chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[:k]

    def _build_rag_context(self, query: str, k: int = 4) -> str:
        top = self._similarity_search(query, k=k)
        if not top:
            return ""
        lines = []
        for score, chunk in top:
            lines.append(f"[score={score:.3f}]\n{chunk}")
        return "\n\n---\n\n".join(lines)
    
    def _auto_save_qa_pair(self, question: str, answer: str):
        """
        Automatically save Q&A pairs to the database with some filtering logic
        """
        # Skip saving if question is too short or seems like a greeting
        question = question.strip()
        answer = answer.strip()
        
        # Filter out greetings, simple acknowledgments, etc.
        greetings = ['hello', 'hi', 'hey', 'goodbye', 'bye', 'thanks', 'thank you']
        if any(greeting in question.lower() for greeting in greetings):
            return
        
        # Skip if question is too short (likely not a real question)
        if len(question) < 10:
            return
        
        # Skip if answer is too short or seems like a greeting
        if len(answer) < 20:
            return
        
        # Check if this Q&A pair already exists (simple check)
        existing = search_common_qa(question[:50])  # Search with first 50 chars
        if existing.get('results'):
            # If similar question exists, don't duplicate
            return
        
        try:
            # Save the Q&A pair
            result = add_common_qa(question, answer)
            print(f"Auto-saved Q&A pair: {question[:50]}... -> {answer[:50]}...")
            return result
        except Exception as e:
            print(f"Error auto-saving Q&A pair: {e}")
            return None
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
    