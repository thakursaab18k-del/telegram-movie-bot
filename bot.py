from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os
import threading
from flask import Flask


# 🔐 ENV ONLY (no fallback token)
TOKEN = os.getenv("TOKEN")
API_KEY = os.getenv("API_KEY") or "46111cc1"

cache = {}

# ================== 🌐 DUMMY WEB SERVER ==================
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ================== 🤖 BOT CODE ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to Movie Bot 🤖\n\nSend any movie name 😊")

def get_movie(movie_name):
    movie_name = movie_name.lower()

    if movie_name in cache:
        return cache[movie_name]

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        cache[movie_name] = data
        return data
    except Exception as e:
        print("Error:", e)
        return None

def get_watch_links(title):
    query = title.replace(" ", "+")

    return [
        [InlineKeyboardButton("🔍 Netflix", url=f"https://www.netflix.com/search?q={query}")],
        [InlineKeyboardButton("🔍 Prime Video", url=f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={query}")],
        [InlineKeyboardButton("🔍 Hotstar", url=f"https://www.hotstar.com/in/search?q={query}")]
    ]

async def send_movie(update: Update, movie_name):
    await update.message.chat.send_action("typing")
    msg = await update.message.reply_text("🔍 Searching...")

    data = get_movie(movie_name)

    if not data:
        await msg.edit_text("⚠️ Server error")
        return

    if data.get("Response") == "True":
        title = data.get("Title", "N/A")
        rating = data.get("imdbRating", "N/A")
        year = data.get("Year", "N/A")
        genre = data.get("Genre", "N/A")
        plot = data.get("Plot", "No description")
        poster = data.get("Poster")

        caption = f"""🎬 {title}
⭐ Rating: {rating}
📅 Year: {year}
🎭 Genre: {genre}

📝 {plot}"""

        trailer_url = f"https://www.youtube.com/results?search_query={title}+trailer"

        keyboard = [
            [InlineKeyboardButton("▶️ Trailer", url=trailer_url)],
            *get_watch_links(title)
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        if poster and poster != "N/A":
            await update.message.reply_photo(photo=poster, caption=caption, reply_markup=reply_markup)
        else:
            await update.message.reply_text(caption, reply_markup=reply_markup)

    else:
        await msg.edit_text("❌ Movie not found")

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = " ".join(context.args)

    if not movie_name:
        await update.message.reply_text("Type movie name 😊")
        return

    await send_movie(update, movie_name)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text.strip()
    if len(movie_name) < 2:
        return
    await send_movie(update, movie_name)

# ================== 🚀 RUN BOT ==================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movie", movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running 🚀")

app.run_polling()
API_KEY = os.getenv("API_KEY") or "46111cc1"

cache = {}

# ================== 🌐 DUMMY WEB SERVER ==================
web_app = Flask(name)

@web_app.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ================== 🤖 BOT CODE ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to Movie Bot 🤖\n\nSend any movie name 😊")

def get_movie(movie_name):
    movie_name = movie_name.lower()

    if movie_name in cache:
        return cache[movie_name]

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        cache[movie_name] = data
        return data
    except Exception as e:
        print("Error:", e)
        return None

def get_watch_links(title):
    query = title.replace(" ", "+")

    return [
        [InlineKeyboardButton("🔍 Netflix", url=f"https://www.netflix.com/search?q={query}")],
        [InlineKeyboardButton("🔍 Prime Video", url=f"https://www.primevideo.com/search/ref=atv_nb_sr?phrase={query}")],
        [InlineKeyboardButton("🔍 Hotstar", url=f"https://www.hotstar.com/in/search?q={query}")]
    ]

async def send_movie(update: Update, movie_name):
    await update.message.chat.send_action("typing")
    msg = await update.message.reply_text("🔍 Searching...")

    data = get_movie(movie_name)

    if not data:
        await msg.edit_text("⚠️ Server error")
        return

    if data.get("Response") == "True":
        title = data.get("Title", "N/A")
        rating = data.get("imdbRating", "N/A")
        year = data.get("Year", "N/A")
        genre = data.get("Genre", "N/A")
        plot = data.get("Plot", "No description")
        poster = data.get("Poster")

        caption = f"""🎬 {title}
⭐ Rating: {rating}
📅 Year: {year}
🎭 Genre: {genre}

📝 {plot}"""

        trailer_url = f"https://www.youtube.com/results?search_query={title}+trailer"

        keyboard = [
            [InlineKeyboardButton("▶️ Trailer", url=trailer_url)],
            *get_watch_links(title)
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        if poster and poster != "N/A":
            await update.message.reply_photo(photo=poster, caption=caption, reply_markup=reply_markup)
        else:
            await update.message.reply_text(caption, reply_markup=reply_markup)

    else:
        await msg.edit_text("❌ Movie not found")

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = " ".join(context.args)

    if not movie_name:
        await update.message.reply_text("Type movie name 😊")
        return

    await send_movie(update, movie_name)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text.strip()
    if len(movie_name) < 2:
        return
    await send_movie(update, movie_name)

# ================== 🚀 RUN BOT ==================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movie", movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running 🚀")

app.run_polling()
