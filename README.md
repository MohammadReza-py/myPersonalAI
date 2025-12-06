# 🌟 Persona Agent – Python AI Character with Memory & Mood

A lightweight, extensible persona-based AI agent built in Python.
This project creates an AI character that maintains long-term memory, short-term conversation history, emotional understanding, and a dynamic mood system, powered by an OpenAI-compatible API.

# ✨ Features

# 🧠 Memory System

Long-term factual memory

Short-term sliding message history (last 12 messages)

# 🎭 Persona Engine
Customizable personality, background, and speaking style.

# 😊 Emotion Detection
Simple positive/negative/neutral sentiment classifier.

# 🌦️ Mood Tracking
Character mood updates automatically based on model output.

# 💬 Structured JSON Response
Ensures consistent output with keys:
reply, emotion_of_user, character_mood, next_action

# 🌐 Optional URL Content Fetching
Automatically downloads and injects webpage content if the prompt contains URLs.

# 🔌 Flexible API Backend
Uses an OpenAI-compatible endpoint (api.metisai.ir) but supports any compatible service.

# 📂 Project Structure
├── main.py        # AI agent logic, memory, persona, mood system

├── core.py        # API wrapper & URL processing

└── README.md

# 🛠 Installation
1. Clone the repo
git clone https://github.com/yourusername/persona-agent
cd persona-agent

2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt


(If you don’t have a requirements.txt file yet, ask me and I’ll generate one.)

# 🔧 Configuration
Environment Variables (recommended)

Create a .env file:

API_KEY=your_api_key_here
MODEL=gpt-4.1-mini
BASE_URL=https://api.metisai.ir/openai/v1


Then load them using python-dotenv.

# 🚀 Usage

Run the agent:

python main.py


You’ll be asked:

hello, what's up? how can I help you?


Then the agent returns a JSON output like:

{
  "reply": "سلام! امروز چطور می‌تونم کمکت کنم؟",
  "emotion_of_user": "neutral",
  "character_mood": "calm",
  "next_action": "reply"
}

# 🧱 Code Overview
## CharacterAgent
<ul>
Handles:
<li>
Memory updates
</li>
<li>
Mood logic
</li>
<li>
Building prompts
</li>
<li>
Sending API calls
</li>
<li>
Parsing model responses
</li>
</ul>
## AgentCore
<ul>
Handles:
<li>Sending messages to model</li>
<li>Replacing URLs with HTML content</li>
<li>Extracting text from responses</li>
</ul>

# 🐛 Troubleshooting
| Problem         | Cause                       | Fix                        |
| --------------- | --------------------------- | -------------------------- |
| API error       | Wrong API key or base URL   | Check `.env` values        |
| JSONDecodeError | Model returned invalid JSON | Add a schema validator     |
| Slow requests   | URL contains large webpage  | Disable URL-fetching logic |


<hr>

# 📌 TODO / Future Improvements:
<ul>
<li>
Persistent long-term memory via JSON/SQLite
</li>
<li>
Better emotion detection via ML model
</li>
<li>
Unit tests
</li>
<li>
Improved retry & error handling
</li>
<li>
Support for multiple LLM backends
</li>
<li>
Full logging system
</li>
</ul>

# 👥 Contributors

MohammadReza Bidar — Creator

(Open a PR to contribute!)

📄 License

MIT License. Free for personal and commercial use.
