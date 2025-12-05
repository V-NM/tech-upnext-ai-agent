# tech-upnext-ai-agent
Tech-UpNext AI is an agentic AI-powered news aggregation and newsletter platform built with FastAPI, Groq LLM, and React. It autonomously fetches tech news from multiple RSS sources, summarizes content using AI, classifies categories, stores results in a database, and delivers daily newsletters via SendGrid.

# 🚀 Tech-UpNext AI — Autonomous Tech News Agent & Newsletter Platform

Tech-UpNext AI is a fully agentic, AI-powered news aggregation and newsletter system. It automatically fetches the latest tech news from trusted RSS sources, summarizes it using Groq LLM, classifies the content into categories, stores it in a database, and sends clean HTML newsletters to subscribers — all without manual effort.

This project demonstrates a complete **Perception → Decision → Action** autonomous AI workflow.

---

## 🧠 Key Features

- ✅ Autonomous RSS news ingestion  
- ✅ AI-powered 2-line summarization using **Groq (llama-3.1-8b-instant)**  
- ✅ Automatic category classification  
- ✅ Beginner-friendly AI explainer generation  
- ✅ Clean premium HTML newsletters  
- ✅ Automated email delivery with **SendGrid**  
- ✅ Subscriber management system  
- ✅ React-based frontend dashboard  
- ✅ One-click AI agent execution (`/run` endpoint)  
- ✅ Persistent SQLite database  
- ✅ CORS-enabled API for frontend integration  
- ✅ Graceful fallback handling for AI & email failures  

---

## 🤖 Agentic AI Workflow

1. **Perception** → Reads live RSS feeds  
2. **Decision** → AI:
   - Summarizes content
   - Determines if it is tech-related
   - Assigns the correct category  
3. **Action** → Saves to DB & sends newsletters  
4. **Loop** → Repeats on each agent execution  

This makes Tech-UpNext AI a **true autonomous AI agent system**.

---

## 🧰 Tech Stack

### 🔧 Backend
- **FastAPI** — API Framework  
- **SQLite** — Lightweight database  
- **Feedparser** — RSS parsing  
- **Newspaper3k** — Article extraction  
- **Groq LLM Client** — AI summarization  
- **SendGrid API** — Email delivery  
- **dotenv** — Secure environment config  
- **CORS Middleware**

### 🎨 Frontend
- **React.js**
- **CSS for responsive UI**
- Live news feed display  
- Subscription form  
- Agent execution button  

---

## 🗄️ Database Schema

### ✅ `news` Table
- `id`
- `title`
- `link`
- `summary`
- `explainer`
- `category`

### ✅ `subscribers` Table
- `id`
- `email` (unique)

---

## 📩 Newsletter Features

- AI-generated 2-line summaries  
- Categorized news sections  
- Premium clean email UI  
- Direct "Read More" links  
- Scales to large audiences using SendGrid  
- Automated dispatch after agent runs  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/tech-upnext-ai.git
cd tech-upnext

2️⃣ Setup Python Environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt

3️⃣ Setup .env File
GROQ_API_KEY=your_groq_api_key
SENDGRID_API_KEY=your_sendgrid_api_key
SENDGRID_FROM_EMAIL=your_verified_sendgrid_email

4️⃣ Run Backend
uvicorn backend:app --reload

Backend will start at:
http://127.0.0.1:8000

5️⃣ Run Frontend (React)
cd frontend
npm install
npm start

📡 API Endpoints
Method	Endpoint	Description
POST	/subscribe	Subscribe to newsletter
GET	/run	Run the AI agent manually
GET	/news	Fetch stored news
GET	/categories	Get all available categories

🎯 Use Cases
✅ Hackathons
✅ AI product demos
✅ Resume & portfolio projects
✅ Startup MVP
✅ Newsletter automation
✅ Learning agentic AI systems

🔮 Future Enhancements
Scheduled automatic agent runs (cron jobs)
User-specific category subscriptions
Personalized recommendations
Click-based learning system
Admin analytics dashboard
Mobile app integration

Why This Project Stands Out
✅ Real-world AI integration
✅ End-to-end backend + frontend + AI + email automation
✅ Demonstrates true agentic behavior
✅ Production-style architecture
✅ Clean, scalable design

🧑‍💻 Author
Vishnu Namboothiri Manukumar
Java Backend Developer | AI & Full-Stack Enthusiast

⭐ Star the Repo
If you find this project useful, give it a ⭐ to support the work!
