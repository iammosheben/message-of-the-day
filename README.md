# 📬 Message of the Day (MotD) - WhatsApp and Telegram Bot Integration

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Telegram](https://img.shields.io/badge/Telegram-Bot-green)
![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-red)
![JSON](https://img.shields.io/badge/JSON-Data-yellow)

## 🌟 Project Overview

**Message of the Day** is a subscription service that delivers a daily "message of the day" (MotD) to WhatsApp subscribers and provides a Telegram bot for subscription management.

### 🌈 Features
- **WhatsApp Message of the Day** 📲
  - Uses the Twilio API to send daily motivational messages to WhatsApp subscribers.
- **Telegram Bot Subscription Management** 🤖
  - Allows subscribing and unsubscribing to the daily messages via a Telegram bot.

### 📂 Directory Structure
```plaintext
message-of-the-day/
│
├── messageoftheday.py         # Sends WhatsApp messages via Twilio API
├── subscribers.json           # Stores subscriber data
├── subscription.py            # Telegram bot for subscription management
└── README.md                  # Project documentation (this file)
```
💻 Technologies
Programming Language: Python 3.9+
APIs and Libraries:
python-telegram-bot: Telegram Bot API client
twilio: WhatsApp messaging via Twilio API
nest-asyncio: Allow event loop reuse in asynchronous environments
json: Data storage in JSON format

⚙️ Installation
Clone the Repository

```plaintext
git clone https://github.com/iammosheben/message-of-the-day.git
cd message-of-the-day
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.tx
```
🔧 Configuration
Twilio Account Setup
Sign up for a Twilio Account.
Create a WhatsApp sender number.
Note down the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN.
Telegram Bot Setup
Create a Telegram bot via BotFather.
Note down the TELEGRAM_BOT_TOKEN.
Environment Variables
Create a .env file in the project directory and add the following:
```plaintext
ini

TWILIO_ACCOUNT_SID=<your_twilio_account_sid>
TWILIO_AUTH_TOKEN=<your_twilio_auth_token>
TWILIO_PHONE_NUMBER=<your_twilio_phone_number>

TELEGRAM_BOT_TOKEN=<your_telegram_bot_token>
```

🚀 Usage
Start the Message of the Day Service
This script will send daily WhatsApp messages to all subscribers listed in subscribers.json.
```plaintext
python messageoftheday.py
Start the Telegram Subscription Bot
This bot allows users to manage their subscription status via Telegram.
python subscription.py
```
📋 Example Subscribers JSON Structure
The subscriber data is stored in subscribers.json in the following format:

```json

{
  "_default": {
    "10": {
      "phone_number": "whatsapp:+1000000000",
      "name": "user name",
      "language": "iw"
    },
    "20": {
      "phone_number": "whatsapp:+10000000000",
      "name": "user name",
      "language": "en"
    },
    "30": {
      "phone_number": "whatsapp:+1000000000",
      "name": "user name",
      "language": "iw"
    }
  }
}
```
✉️ Preview of Message of the Day
Here's an example of the daily message sent to WhatsApp subscribers:

```sql

Hello username! Here's your Message of the Day:
<--picture of the day file> 
🖼 Picture of the Day:
Where is this rocky ridge?
Description: The Roaches, Peak District, England (© George W Johnson/Getty Images)

💡 Interesting Facts:
Tiger Woods is the first athlete to has been named "Sportsman of the Year" by magazine Sports Illustrated two times

📜 Today in History:
1594 – The Dutch city of Coevorden held by the Spanish, falls to a Dutch and English force.[2]
1541 – King Henry VIII orders English-language Bibles be placed in every church. In 1539 the Great Bible would be provided for this purpose.

🐾 Animal Facts:
Dog: All puppies are born deaf.

📖 Random Wikipedia Summary:
Coucy-lès-Eppes station
Coucy-lès-Eppes station (French: Gare de Coucy-lès-Eppes) is a railway station located in the commune of Coucy-lès-Eppes, in the department of Aisne, northern France. It is situated at kilometric point (KP) 41.022  on the Reims-Laon railway.

😂 Joke of the Day:
Why did the chicken cross the road, roll in the mud and cross the road again?
He was a dirty double-crosser!

Enjoy your day and keep learning!
```
---------------------------------------------------------------

🗓️ Date: 2024-05-07
📑 License
This project is licensed under the MIT License.

👤 Author
Moshe Ben 
