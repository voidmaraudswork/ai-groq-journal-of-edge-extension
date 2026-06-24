import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Import the Groq library
from groq import Groq

app = FastAPI()

# 🔴 Paste your free Groq API key here inside the quotes
GROQ_API_KEY = "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"

# Initialize the Groq Client
ai_client = Groq(api_key=GROQ_API_KEY)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Activity(BaseModel):
    source: str
    title: str
    url: str
    timestamp: str

def init_db():
    conn = sqlite3.connect('devflow.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS activity 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     source TEXT, title TEXT, url TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup():
    init_db()

@app.post("/api/log-activity")
def log_activity(activity: Activity):
    print(f"✨ Captured Tracked Page: {activity.title} -> ({activity.url})")
    
    conn = sqlite3.connect('devflow.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO activity (source, title, url, timestamp) VALUES (?, ?, ?, datetime('now', 'localtime'))",
                   (activity.source, activity.title, activity.url))
    conn.commit()
    conn.close()
    return {"status": "saved"}

@app.get("/api/generate-summary")
def generate_summary():
    conn = sqlite3.connect('devflow.db')
    cursor = conn.cursor()
    
    # Clean records older than 24 hours
    cursor.execute("DELETE FROM activity WHERE timestamp <= datetime('now', 'localtime', '-24 hours')")
    conn.commit()
    
    cursor.execute("SELECT title, url FROM activity ORDER BY id DESC LIMIT 30")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return {"summary": "No activity tracked in the last 24 hours! Open some tabs first."}

    raw_logs = ""
    for row in rows:
        raw_logs += f"- Visited Page: {row[0]} (URL: {row[1]})\n"

# Find the prompt string inside generate_summary() and replace it with this:
    prompt = f"""
    You are an elite, highly detailed engineering logger. Do not generalize or condense my activity into generic high-level bullet points. I want a comprehensive, chronological, and descriptive breakdown of my session exactly as reflected in my raw traffic logs.

    Analyze these raw entries and expand on them to tell the complete story of my session:
    {raw_logs}
    
    Rules for your response:
    1. Chronological order: Break down the sequence of what I did step-by-step.
    2. Deep specificity: Explicitly mention every repository name, file name (like 'app.py' or 'requirements.txt'), and platform (GitHub, Render Dashboard, Gemini) that appears in the logs.
    3. Action-oriented description: Explain the progression (e.g., "Navigated to the repository, opened app.py for editing, modified dependencies in requirements.txt, and immediately monitored the resulting build deployment logs on the Render Dashboard").
    4. Provide a closing "Summary of Focus Areas" highlighting the exact technologies handled.
    
    Format your response beautifully using clean markdown headings and bullet points.
    """

    try:
        # ⚡ Call Groq's high-speed Llama model instead of Gemini
        response = ai_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
        )
        return {"summary": response.choices[0].message.content}
    except Exception as e:
        return {"summary": f"API Error: Make sure your Groq API key is correct! Details: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)