import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters
import yt_dlp

TOKEN = "8412613896:AAFN1KfclmzBhHy8nPpqkRlejxcJuQlCtRw"  # BotFather se mila token

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 Namaste! Song ka naam bhejo: /song <name>")

async def song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Usage: /song <song name>")
        return

    await update.message.reply_text(f"🔍 Searching: {query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/tmp/song.%(ext)s',  # Temp folder for Render
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            file_path = ydl.prepare_filename(info['entries'][0])

            # Rename to .mp3 if not already
            if not file_path.endswith(".mp3"):
                new_file_path = os.path.splitext(file_path)[0] + ".mp3"
                if os.path.exists(new_file_path):
                    file_path = new_file_path

        await update.message.reply_audio(audio=open(file_path, 'rb'))
        os.remove(file_path)

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start, filters.ChatType.PRIVATE | filters.ChatType.GROUPS))
    app.add_handler(CommandHandler("song", song, filters.ChatType.PRIVATE | filters.ChatType.GROUPS))
    print("Bot chal raha hai...")
    app.run_polling()
