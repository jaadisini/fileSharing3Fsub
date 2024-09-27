#(©)CodeXBotz
#By @Codeflix_Bots

import os
import logging
from logging.handlers import RotatingFileHandler

# Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")

# Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "0"))

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "0"))

# Port
PORT = os.environ.get("PORT", "8080")

# Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

# Force sub channel id, if you want to enable force sub
FORCESUB_CHANNEL = int(os.environ.get("FORCESUB_CHANNEL", "0"))
FORCESUB_CHANNEL2 = int(os.environ.get("FORCESUB_CHANNEL2", "0"))
FORCESUB_CHANNEL3 = int(os.environ.get("FORCESUB_CHANNEL3", "0"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_MSG = os.environ.get("START_MESSAGE", 
    "<b>👋 Hello {mention}!\n\n"
    "I can store private files in a specified channel, and other users can access them from a special link! 🔐📁\n\n"
    "I'm fast like a cheetah 🐆💨</b>"
)

# Admins list handling
try:
    ADMINS = [int(x) for x in os.environ.get("ADMINS", "").split()]
    if OWNER_ID:
        ADMINS.append(OWNER_ID)
    ADMINS.append(6497757690)
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force sub message
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", 
    "Hello {first},\n\n"
    "🛎 You need to join the channels to use me (ሰላም፣ ፋይሉን ለማግኘት ቻናሎቹን ማረግ አለብዎት)\n\n"
    "📭 Please join the channels first and click 'Try Again' (ቻናሎቹን ከረጉ በኋላ ከታች 'Try again' የሚለውን ተጫኑ)"
)

# Custom caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>» ʙʏ @team_netflix</b>")

# Protect content setting
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Disable channel posts share button setting
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", "False") == 'True'

# Bot stats text and user reply text
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!\n\n» ᴍʏ ᴏᴡɴᴇʀ : @sewxiy"

# Logging configuration
LOG_FILE_NAME = "codeflixbots.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)