# 🚀 tech-upnext-ai-agent  
Autonomous AI-Powered Tech News Aggregator & Newsletter Platform  

Tech-UpNext AI is a fully agentic, AI-powered news aggregation and newsletter system built using FastAPI, Groq LLM, and React. It autonomously fetches the latest tech news from multiple trusted RSS sources, summarizes the content using AI, intelligently classifies categories, stores results in a persistent database, and delivers premium HTML newsletters via SendGrid.

This project demonstrates a complete Perception → Decision → Action autonomous AI workflow.

---

🧠 Key Features

- Fully autonomous RSS news ingestion  
- AI-powered 2-line summarization using Groq (llama-3.1-8b-instant)  
- Automatic category detection and classification  
- Beginner-friendly AI explainer generation  
- Clean premium HTML newsletters  
- Automated bulk email delivery via SendGrid  
- Secure subscriber management system  
- Modern React.js dashboard  
- One-click AI Agent execution (/run endpoint)  
- Persistent SQLite database storage  
- CORS-enabled backend for seamless frontend integration  
- Graceful error handling and fallbacks for AI and email failures  

---

🤖 Agentic AI Workflow

1. Perception → Reads live RSS feeds  
2. Decision → AI:
   - Summarizes content  
   - Determines if it qualifies as tech news  
   - Assigns the most relevant category  
3. Action → Saves results to the database and sends newsletters  
4. Loop → Repeats on each agent execution  

Tech-UpNext AI is a true autonomous AI agent system.

---

🧰 Tech Stack

Backend
- FastAPI – High-performance API framework  
- SQLite – Lightweight relational database  
- Feedparser – RSS feed parsing  
- Newspaper3k – Full article extraction  
- Groq LLM Client – AI summarization & classification  
- SendGrid API – Scalable email delivery  
- dotenv – Secure secrets management  
- CORS Middleware – Frontend connectivity  

Frontend
- React.js  
- Responsive CSS Styling  
- Live AI news feed  
- Newsletter subscription  
- One-click AI Agent trigger  

---

🗄️ Database Schema

news Table
- id  
- title  
- link  
- summary  
- explainer  
- category  

subscribers Table
- id  
- email (unique)  

---

📩 Newsletter Features

- AI-generated 2-line summaries  
- Professionally categorized news sections  
- Premium clean email UI  
- Direct "Read More" article links  
- Scales easily for large audiences using SendGrid  
- Automatic dispatch after every agent run  

---

⚙️ Installation & Setup

1. Clone the Repository

git clone https://github.com/V-NM/tech-upnext-ai-agent 
cd tech-upnext 

---

2. Setup Python Environment

python -m venv venv  
source venv/bin/activate   (Mac/Linux)  
venv\Scripts\activate      (Windows)  
pip install -r requirements.txt  

---

3. Setup .env File

Create a .env file in the root directory and add:

GROQ_API_KEY=your_groq_api_key  
SENDGRID_API_KEY=your_sendgrid_api_key  
SENDGRID_FROM_EMAIL=your_verified_sendgrid_email  

---

4. Run Backend

uvicorn backend:app --reload  

Backend will start at:  
http://127.0.0.1:8000  

---

5. Run Frontend (React)

cd frontend  
npm install  
npm start  

---

📡 API Endpoints

POST /subscribe → Subscribe to newsletter  
GET /run → Run the AI Agent manually  
GET /news → Fetch stored news  
GET /categories → Get all available categories  

---

🎯 Use Cases

Hackathons  
AI product demos  
Resume and portfolio projects  
Startup MVPs  
Newsletter automation systems  
Learning real-world agentic AI systems  

---

🔮 Future Enhancements

Scheduled automatic agent runs (cron jobs)  
User-specific category subscriptions  
Personalized recommendations  
Click-based learning system  
Admin analytics dashboard  
Mobile app integration  

---

🏆 Why This Project Stands Out

Real-world AI implementation  
Complete end-to-end system (Backend + Frontend + AI + Email)  
True agentic automation architecture  
Production-style design and code structure  
Clean, scalable, and extensible platform  

---

🧑‍💻 Author

Vishnu Namboothiri Manukumar  
Java Backend Developer | AI & Full-Stack Enthusiast  

---

⭐ Support the Project

If you find this project helpful, please give it a star on GitHub — it motivates future improvements.
