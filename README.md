
# 🏝️ IslandWhiz – Sri Lanka Tourism Chatbot

**IslandWhiz** is an AI-powered tourism chatbot designed to help travelers explore Sri Lanka. It provides information about destinations, the best time to visit, travel tips, and live status — all through a conversational web interface. The system uses **Rasa** for natural language understanding (NLP), **Flask** for backend APIs, **MySQL** for dynamic data, and a custom-built **HTML/CSS/JS** frontend.

---

## 🚀 Features

- 💬 Natural language conversation with tourists
- 📍 Recommends Sri Lankan destinations (e.g., Ella, Sigiriya, Mirissa)
- 📅 Provides the best visiting time for each place
- 🌐 Shares live travel info and cultural advice
- ⚙️ Modular structure using Rasa, Flask, and MySQL

---

## 🛠️ Technologies Used

| Component     | Technology              |
|---------------|--------------------------|
| NLP Engine    | [Rasa](https://rasa.com) |
| Backend       | Flask (Python 3.10)      |
| Database      | MySQL 8.0 (via Workbench)|
| Frontend      | HTML5, CSS3, JavaScript  |
| Libraries     | flask, flask-cors, mysql-connector-python, requests |
| Tools         | VS Code, Postman, MySQL Workbench |

---

## 📦 Project Structure

```
islandwhiz/
│
├── backend/
│   ├── app.py                # Flask server
│   ├── actions.py            # Rasa custom actions (DB access)
│
├── rasa/
│   ├── nlu.yml               # Training data for intents
│   ├── domain.yml            # Intents, entities, responses
│   ├── stories.yml           # Conversation flows
│   ├── rules.yml             # Rule-based flows
│
├── frontend/
│   ├── templates/index.html
│   ├── static/styles.css
│   ├── static/app.js
│
├── database/
│   ├── travel_bot.sql        # SQL schema and sample data
│
└── README.md
```

---

## ⚙️ Installation and Setup

### 1. Clone the Repository and install rasa

```bash
git clone https://github.com/supunakalanka76/islandwhiz.git
cd islandwhiz
```

```bash
pip install rasa
```

### 2. Set Up Python Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate      # Mac/Linux
pip install -r backend/requirements.txt
```

### 3. Set Up MySQL

- Open MySQL Workbench.
- Create a database named `travel_bot`.
- Run `travel_bot.sql` in `/database` folder to create and populate tables.
- Update DB credentials in `actions.py` if needed.

### 4. Train the Rasa Model

```bash
cd backend
rasa train
```

### 5. Run the Servers

In 3 separate terminals:

```bash
# Terminal 1 – Rasa action server
rasa run actions

# Terminal 2 – Rasa chatbot server
rasa run --enable-api

# Terminal 3 – Flask backend server
python app.py
```

### 6. Open the Chat UI

Go to `http://localhost:5000` in your browser to interact with the chatbot.

---

## 💬 Sample Queries

- “Tell me about Ella”
- “What’s the best time to visit Mirissa?”
- “Give me some travel tips”
- “Thanks!”

---

## 📈 Future Improvements

- 🎙️ Voice input and output
- 🌐 Sinhala and Tamil language support
- 📡 Real-time API integration (weather, transport)
- 📱 Progressive Web App (PWA) or mobile app version
- 🧠 Context-aware multi-turn conversations

---

## 🙋‍♂️ Authors

**M.W.H.G. Supun Akalanka**  
📚 BEng (Hons) Software Engineering – London Metropolitan University  
🎓 AI Module – Coursework 2  
📅 April 2025

**R. D. Sahan Lakmal Senavirathna**  
📚 BEng (Hons) Software Engineering – London Metropolitan University  
🎓 AI Module – Coursework 2  
📅 April 2025

---

## 📄 License

This project is developed for educational purposes only. All code is open-source for academic use.
