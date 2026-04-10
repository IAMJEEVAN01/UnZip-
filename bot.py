import os
import patoolib
from pyrogram import Client, filters
from flask import Flask
from threading import Thread

# --- CONFIGURATION ---
API_ID = 37517668
API_HASH = "2416d55a1946a4fb155e1013c19337c0"
BOT_TOKEN = "8609850670:AAF3Vf1Aft18_TOoyFXI1zGmQu9QcYeNbL4"

app = Client("UnzipBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Render 24/7 rehne ke liye dummy server
server = Flask('')
@server.route('/')
def home(): return "THE PARAMOUNT IS ALIVE!"
def run(): server.run(host='0.0.0.0', port=8080)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply_text("**THE PARAMOUNT UNZIPPER** active hai! 😈\nKoi bhi Zip/Rar file bhejo, main use chir-phaad ke rakh dunga.")

@app.on_message(filters.document & filters.private)
async def handle_zip(client, message):
    file_ext = message.document.file_name.split('.')[-1].lower()
    if file_ext in ['zip', 'rar', '7z']:
        status = await message.reply_text("📥 Downloading and Extracting... Sabr rakho Maharaj.")
        
        # Download
        file_path = await message.download()
        extract_dir = "extracted_files"
        if not os.path.exists(extract_dir): os.makedirs(extract_dir)
        
        try:
            # Extract
            patoolib.extract_archive(file_path, outdir=extract_dir)
            
            # Upload extracted files
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    await client.send_document(message.chat.id, os.path.join(root, file))
            
            await status.edit("✅ Mission Success! Saari files bhej di gayi hain.")
        except Exception as e:
            await status.edit(f"⚠️ Error: {str(e)}")
        
        # Cleanup
        if os.path.exists(file_path): os.remove(file_path)
    else:
        await message.reply_text("❌ Ye Zip ya Rar file nahi hai Maharaj!")

if __name__ == "__main__":
    Thread(target=run).start() # Server starts here
    print("🔥 THE PARAMOUNT UNZIPPER IS RUNNING... 🔥")
    app.run()
      
