from pyrogram import Client, filters
import psutil, shutil
from pymongo import MongoClient
from config import MONGO_DB_URI  

# MongoDB connect
clientdb = MongoClient(MONGO_DB_URI)
db = clientdb["XURLUploader"]   # apna DB name
users_col = db["users"]         # apna collection name

@Client.on_message(filters.command("status"))
async def status_cmd(client, message):
    # System Info
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    total, used, free = shutil.disk_usage("/")
    disk = int(used / total * 100)

    # Users count
    total_users = users_col.count_documents({})

    text = (
        f"**✅ Bot Status**\n\n"
        f"• CPU: {cpu}%\n"
        f"• RAM: {ram}%\n"
        f"• Disk: {disk}%\n"
        f"• Total Users: {total_users}"
    )

    await message.reply_text(text)
