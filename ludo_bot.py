import os
import logging
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
from dotenv import load_dotenv
from ludo_personality import get_ludo_ai_response

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Chat histories to maintain memory per user/group
chat_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🎲 **Ludo Win Zone Official AI Bot** সক্রিয়!

"
        "আরে সবাই শোন! আমি এই গ্রুপের সবচেয়ে স্মার্ট, ফানি এবং ডেঞ্জারাস বট। "
        "লুডু টুর্নামেন্টে কে জিতল, কে ছয় মারতে পারল না—সব খবর রাখি। "
        "কারো সাথে দুষ্টুমি করব, কাউকে টোল করব, আবার কারো মন খারাপ থাকলে ভালোবাসাও দেবো! 😎❤️

"
        "আমার সাথে চ্যাট শুরু করে দাও!"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Ignore if message is empty
    if not update.message or not update.message.text:
        return

    chat_id = update.effective_chat.id
    user = update.effective_user
    user_name = user.first_name if user else "প্লেয়ার"
    user_text = update.message.text
    
    # Initialize history for this chat
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []
    
    # Format message with user name for group context awareness
    formatted_msg = f"{user_name}: {user_text}"
    chat_histories[chat_id].append({"role": "user", "content": formatted_msg})
    
    # Keep only last 15 messages for context window
    if len(chat_histories[chat_id]) > 15:
        chat_histories[chat_id] = chat_histories[chat_id][-15:]

    # Check if bot is mentioned or replying in group, or if it should randomly jump in (15% chance to chat spontaneously)
    is_group = update.effective_chat.type in ["group", "supergroup"]
    bot_username = context.bot.username
    is_mentioned = bot_username and bot_username in user_text
    is_reply_to_bot = update.message.reply_to_message and update.message.reply_to_message.from_user.id == context.bot.id
    
    should_reply = not is_group or is_mentioned or is_reply_to_bot or (random.random() < 0.25)

    if not should_reply:
        return

    # Show typing indicator
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    # Generate response
    reply = get_ludo_ai_response(chat_histories[chat_id])
    
    chat_histories[chat_id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN missing in .env!")
        exit(1)
        
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🎲 Ludo Win Zone Telegram Bot is live and kicking!")
    app.run_polling()
