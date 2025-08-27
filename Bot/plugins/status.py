from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from pymongo import MongoClient
from datetime import datetime

# MongoDB connection
mongo = MongoClient(Config.DATABASE_URL)
db = mongo["BotDB"]          # Apna DB naam yahan change kar sakte ho
users_col = db["users"]      # Users collection
tasks_col = db["tasks"]      # Tasks collection


# ✅ User register hone par (start par add ho jaye)
@Client.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    if not users_col.find_one({"user_id": user_id}):
        users_col.insert_one({"user_id": user_id, "joined": datetime.utcnow()})
    await message.reply_text("👋 Welcome! You are registered.")


# ✅ Status command (Owner/Admin ke liye)
@Client.on_message(filters.command("status"))
async def status_handler(client: Client, message: Message):
    if message.from_user.id != Config.OWNER_ID:
        return await message.reply_text("⛔ You are not authorized.")

    # Total Users
    total_users = users_col.count_documents({})

    # Daily tasks (aaj ki date se filter)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    daily_tasks = tasks_col.count_documents({"date": today})

    text = (
        f"📊 **Bot Status**\n\n"
        f"👤 Total Users: **{total_users}**\n"
        f"📝 Tasks Today: **{daily_tasks}**"
    )

    await message.reply_text(text)


# ✅ Example - Jab bhi user koi task kare (file upload etc.)
# Ye sirf samjhane ke liye hai, apne actual task wale code me insert karo
async def add_task(user_id: int, task_type: str):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    tasks_col.insert_one({
        "user_id": user_id,
        "task_type": task_type,
        "date": today,
        "time": datetime.utcnow()
    })
