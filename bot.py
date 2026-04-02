from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
import os

# 🔐 Use ENV (Render) OR fallback (local)
TOKEN = os.getenv("TOKEN") or "8145649130:AAEDGyAcELtEd7So2fbkyC-wJyPIQev5gWE"
API_KEY = os.getenv("API_KEY") or "46111cc1"

cache = {}

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 Welcome to Movie Bot 🤖\n\nSend any movie name 😊"
    )

# MOVIE FETCH
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

# SEND MOVIE
async def send_movie(update: Update, movie_name):
    await update.message.chat.send_action("typing")

    msg = await update.message.reply_text("🔍 Searching...")

    data = get_movie(movie_name)

    if not data:
        await msg.edit_text("⚠️ Server error, try again later")
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

        # 🎬 Trailer button
        trailer_url = f"https://www.youtube.com/results?search_query={title}+trailer"
        keyboard = [[InlineKeyboardButton("▶️ Watch Trailer", url=trailer_url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            if poster and poster != "N/A":
                await update.message.reply_photo(
                    photo=poster,
                    caption=caption,
                    reply_markup=reply_markup
                )
            else:
                await update.message.reply_text(
                    caption,
                    reply_markup=reply_markup
                )
        except Exception as e:
            print("Send error:", e)
            await update.message.reply_text(caption)

    else:
        await msg.edit_text("❌ Movie not found")

# /movie command
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = " ".join(context.args)

    if not movie_name:
        await update.message.reply_text("Type movie name 😊")
        return

    await send_movie(update, movie_name)

# DIRECT TEXT
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = update.message.text.strip()

    if len(movie_name) < 2:
        return

    await send_movie(update, movie_name)

# APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("movie", movie))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running 🚀")

app.run_polling()