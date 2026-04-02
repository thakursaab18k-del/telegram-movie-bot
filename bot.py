from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

# 🔑 YOUR TOKENS (already added)
TOKEN = "8145649130:AAHbbhcOkkJ2C3C-eYT4H7TJuZq3JiUHflg"
API_KEY = "46111cc1"

# ⚡ Cache for fast response
cache = {}

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am your movie bot 🤖🎬\nUse /movie <name>")

# HELP COMMAND
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /movie <movie name>\nExample: /movie avatar")

# GET MOVIE DATA
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

# MOVIE COMMAND
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie_name = " ".join(context.args)

    if not movie_name:
        await update.message.reply_text("Please type movie name 😊")
        return

    # ⚡ typing animation
    await update.message.chat.send_action("typing")

    # ⚡ quick feedback
    await update.message.reply_text("Searching... 🎬")

    data = get_movie(movie_name)

    if not data:
        await update.message.reply_text("Server error 😕")
        return

    if data.get("Response") == "True":
        title = data.get("Title", "N/A")
        rating = data.get("imdbRating", "N/A")
        year = data.get("Year", "N/A")
        plot = data.get("Plot", "No description available")
        poster = data.get("Poster")

        caption = f"""🎬 {title}
⭐ Rating: {rating}
📅 Year: {year}

📝 {plot}"""

        # 🖼️ send poster
        if poster and poster != "N/A":
            await update.message.reply_photo(photo=poster, caption=caption)
        else:
            await update.message.reply_text(caption)

    else:
        await update.message.reply_text("Movie not found ❌")

# MAIN APP
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("movie", movie))

print("Bot is running... 🚀")

app.run_polling()