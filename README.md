# Tarot Chatbot 🤖🔮

A Telegram chatbot that provides **one tarot card per day** and allows free conversations after that. Built with **Python, OpenAI GPT-4o, and Telegram Bot API**.

## 🚀 Features
- ✅ One Tarot Card Per Day - Users can draw **only one tarot card daily**.
- ✅ Smart Chat - Users can continue chatting **without getting additional cards**.
- ✅ Meme Generation - The bot can also respond with **fun memes**.
- ✅ Conversational AI - Uses **OpenAI GPT-4o** for natural conversations.
- ✅ Inline Confirmation - If users try to get another card, they receive a **confirmation prompt**.

## 🛠️ Installation
### 1️⃣ Clone the Repository
```
git clone https://github.com/btttttong/M6_2024_Phychologyps.git
```

### 2️⃣ Create a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate    # Windows
```

### 3️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file and add your API keys:
```
BOT_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

## 🎮 Usage
### Run the Bot
```
python app2.py
```
### Telegram Commands
| Command   | Description |
|-----------|-------------|
| `/start`  | Start the bot and see welcome message |
| `/card`   | Get your **daily tarot card** |
| `/aboutme`| Learn about the bot |
| 💬 **Chat** | Continue chatting after getting your card |


## 📌 How It Works
1️⃣ **User sends a message**  
2️⃣ **Bot analyzes sentiment** using OpenAI  
3️⃣ **If it's the first request of the day** → **Bot gives a tarot card**  
4️⃣ **If a card was already given** → **Bot switches to chit-chat**  
5️⃣ **User can chat freely after drawing the card** 🎤💬  

## 🔗 API & Tech Stack
- Python
- Telegram Bot API
- OpenAI GPT-4o
- Asyncio
- Prefect (Task Orchestration)
- Heroku (Deployment)
- Cloudinary (Image Hosting for Cards & Memes)

## 💡 Future Improvements
- ✅ Store chat history for better conversations
- ✅ Personalize tarot readings
- ✅ Support multiple languages

## 🤝 Contributing
1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature-name`)
3. **Commit your changes** (`git commit -m "Added new feature"`)
4. **Push to GitHub** (`git push origin feature-name`)
5. **Create a Pull Request** 🎉

## 💌 Contact
🔹 **Maintainer:** BT  
🌐 **GitHub:** [btttttong](https://github.com/btttttong)  

### 🔮 Ready to Reveal Your Future?
🌟 **[Try the bot now!](https://t.me/Phychologyps_bot)** 🌟
