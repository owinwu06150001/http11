import discord
from discord.ext import commands
from flask import Flask, render_template
import sqlite3
import os
import threading

app = Flask(__name__)
# Render 提供 PORT 環境變數
PORT = int(os.environ.get("PORT", 5000))

# 資料庫路徑 (Render 的檔案系統僅暫存，重啟會消失，若要永久保存請連結 External Disk)
DB_PATH = 'data.db'

# ... [保留前面的資料庫 init_db 與路由邏輯] ...

# 調整機器人啟動邏輯
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author != bot.user:
        # 寫入邏輯...
        pass
    await bot.process_commands(message)

# 使用迴圈啟動機器人，不要直接用 bot.run() 阻塞主執行緒
def start_bot():
    bot.run(os.environ['DISCORD_TOKEN'])

if __name__ == '__main__':
    # 啟動機器人執行緒
    threading.Thread(target=start_bot, daemon=True).start()
    # 啟動 Flask
    app.run(host='0.0.0.0', port=PORT)
