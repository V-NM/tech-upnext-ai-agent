from fastapi import FastAPI, Request, Query
import feedparser
import sqlite3
import os
import time
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from groq import Client
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from newspaper import Article
import json

# -------------------- CONFIG --------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDGRID_FROM_EMAIL = os.getenv("SENDGRID_FROM_EMAIL")

if not GROQ_API_KEY or not SENDGRID_API_KEY or not SENDGRID_FROM_EMAIL:
    raise ValueError("Please set all keys in .env")

client = Client(api_key=GROQ_API_KEY)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- DATABASE --------------------
conn = sqlite3.connect("news.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    link TEXT,
    summary TEXT,
    explainer TEXT,
    category TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS subscribers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE
)
""")

conn.commit()

# -------------------- RSS FEEDS --------------------
FEEDS = [
    "https://www.theverge.com/rss/index.xml",
    "https://www.cnet.com/rss/news/",
    "https://arstechnica.com/feed/",
    "https://www.zdnet.com/news/rss.xml",
    "https://www.engadget.com/rss.xml",
    "https://www.techradar.com/rss",
]

# -------------------- AI FUNCTIONS --------------------
def summarize_and_classify(text: str):
    """
    Returns summary (2 sentences) and category as plain text.
    No JSON parsing.
    """
    try:
        prompt = f"""
        Summarize this article in 2 short sentences.
        Also suggest a single category it belongs to from: technology, AI, startups, cybersecurity.
        Output format: 
        Summary: ...
        Category: ...
        Article: {text}
        """
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        time.sleep(4)
        content = response.choices[0].message.content.strip()

        # Extract summary and category heuristically
        summary = ""
        category = "technology"
        for line in content.splitlines():
            if line.lower().startswith("summary:"):
                summary = line.split(":", 1)[1].strip()
            elif line.lower().startswith("category:"):
                category = line.split(":", 1)[1].strip()

        if not summary:
            summary = text[:180]

        return summary, category

    except Exception as e:
        print("Groq Error:", e)
        return text[:180], "technology"


def generate_explainer(text: str):
    """
    Returns explainer text directly from AI.
    """
    try:
        prompt = f"Explain this topic simply for a beginner:\n{text}"
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        time.sleep(4)
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Groq Error:", e)
        return text[:180]


# -------------------- AGENT RUN LOCK --------------------
agent_running = False

# -------------------- SENDGRID --------------------
def send_newsletter():
    local_cursor = conn.cursor()
    subs = local_cursor.execute("SELECT email FROM subscribers").fetchall()

    # Fetch categories in a consistent, lowercase manner to avoid duplicates
    categories = local_cursor.execute("SELECT DISTINCT LOWER(category) FROM news").fetchall()

    if not subs or not categories:
        print("No subscribers or no news")
        return

    for s in subs:
        email = s[0]
        html = f"""
        <html>
        <head>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                background-color: #f9f9f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 90%;
                max-width: 650px;
                margin: 30px auto;
                background-color: #ffffff;
                padding: 25px 30px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            h2 {{
                text-align: center;
                color: #1a1a1a;
                font-weight: 600;
            }}
            h3 {{
                border-bottom: 1px solid #e0e0e0;
                padding-bottom: 5px;
                color: #555;
                margin-top: 25px;
                font-weight: 500;
            }}
            h4 {{
                color: #222;
                margin-bottom: 5px;
                font-weight: 500;
            }}
            p {{
                line-height: 1.5;
                color: #555;
                margin-top: 0;
            }}
            a {{
                color: #1a73e8;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            .news-item {{
                margin-bottom: 20px;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #999;
                margin-top: 25px;
            }}
        </style>
        </head>
        <body>
        <div class="container">
            <h2>Tech-UpNext 📰 Daily Digest</h2>
        """

        for c in categories:
            category = c[0]
            html += f"<h3>{category.title()}</h3>"
            news_list = local_cursor.execute(
                "SELECT title, link, summary FROM news WHERE LOWER(category)=?",
                (category,)
            ).fetchall()

            for n in news_list:
                html += f"""
                <div class="news-item">
                    <h4>{n[0]}</h4>
                    <p>{n[2]}</p>
                    <a href="{n[1]}">Read More</a>
                </div>
                """

        html += """
            <div class="footer">
                You are receiving this email because you subscribed to Tech-UpNext.<br>
                &copy; 2025 Tech-UpNext. All rights reserved.
            </div>
        </div>
        </body>
        </html>
        """

        msg = Mail(
            from_email=SENDGRID_FROM_EMAIL,
            to_emails=email,
            subject="Your Tech-UpNext Digest 📰",
            html_content=html
        )

        try:
            sg = SendGridAPIClient(SENDGRID_API_KEY)
            sg.send(msg)
            print("✅ Email sent to:", email)
        except Exception as e:
            print("❌ SendGrid Error:", e)


# -------------------- SUBSCRIBE --------------------
@app.post("/subscribe")
async def subscribe(req: Request):
    data = await req.json()
    email = data.get("email")
    if not email:
        return {"status": "error", "message": "Email required"}

    cursor.execute(
        "INSERT OR IGNORE INTO subscribers (email) VALUES (?)",
        (email,)
    )
    conn.commit()
    return {"status": "Subscribed"}

# -------------------- RUN AGENT --------------------
@app.get("/run")
def run_agent(send_mail: bool = True):
    global agent_running
    if agent_running:
        return {"status": "Agent already running ⏳"}

    agent_running = True
    cursor.execute("DELETE FROM news")

    for feed in FEEDS:
        data = feedparser.parse(feed)
        for item in data.entries[:1]:
            try:
                article = Article(item.link)
                article.download()
                article.parse()
                text = article.text
            except:
                text = item.title

            summary, category = summarize_and_classify(text)
            explainer = generate_explainer(text)

            cursor.execute(
                "INSERT INTO news (title, link, summary, explainer, category) VALUES (?, ?, ?, ?, ?)",
                (item.title, item.link, summary, explainer, category)
            )

    conn.commit()

    if send_mail:
        send_newsletter()

    agent_running = False
    return {"status": "Agent executed successfully ✅"}

# -------------------- GET NEWS --------------------
@app.get("/news")
def get_news(categories: str = Query("all"), explainer: bool = Query(False)):
    """
    categories: comma separated string e.g. "AI,technology"
    explainer: True/False
    Case-insensitive filtering
    """
    local_cursor = conn.cursor()
    if categories.lower() == "all":
        rows = local_cursor.execute(
            "SELECT title, link, summary, explainer, category FROM news"
        ).fetchall()
    else:
        selected = [c.strip().lower() for c in categories.split(",")]
        placeholders = ",".join("?"*len(selected))
        rows = local_cursor.execute(
            f"SELECT title, link, summary, explainer, category FROM news "
            f"WHERE LOWER(category) IN ({placeholders})",
            selected
        ).fetchall()

    return [
        {
            "title": r[0],
            "link": r[1],
            "summary": r[2],
            "explainer": r[3],
            "category": r[4],
        } for r in rows
    ]

# -------------------- GET ALL CATEGORIES --------------------
@app.get("/categories")
def get_categories():
    """
    Returns list of all categories in lowercase to ensure case-insensitive filtering
    """
    local_cursor = conn.cursor()
    rows = local_cursor.execute("SELECT DISTINCT LOWER(category) FROM news").fetchall()
    return [r[0] for r in rows]

