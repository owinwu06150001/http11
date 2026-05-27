import discord
from discord.ext import commands
from flask import Flask, render_template
import sqlite3
import os
import threading

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 5000))
DB_PATH = 'data.db'

# --- 資料庫初始化 ---
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (content TEXT, author TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- Flask 路由 ---
@app.route('/')
def index():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 讀取最後 50 筆訊息
    c.execute('SELECT * FROM logs ORDER BY rowid DESC LIMIT 50')
    messages = c.fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

# --- Discord 機器人 ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_message(message):
    if message.author != bot.user:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO logs VALUES (?, ?)', (message.content, str(message.author)))
        conn.commit()
        conn.close()
    await bot.process_commands(message)

def start_bot():
    bot.run(os.environ['DISCORD_TOKEN'])

# --- 啟動 ---
if __name__ == '__main__':
    # 在背景啟動機器人
    threading.Thread(target=start_bot, daemon=True).start()
    # 啟動 Flask Web 服務
    app.run(host='0.0.0.0', port=PORT)
