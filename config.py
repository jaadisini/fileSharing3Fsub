#(©)CodeXBotz
#By @Codeflix_Bots

import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
load_dotenv()
print("DEBUG TG_BOT_TOKEN:")





# Bot token from @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7736892583:AAHPSAILxq5dt6rApsCdkaq5TieGf__Ykr8")

# Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", "24773720"))

# Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "b8158aa3d0e6deabfb14c92ccf95ff8d")

# Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002654026135"))

# OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "7688387817"))

# Port
PORT = os.environ.get("PORT", "8080")

# Database 
DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://erkbwrs084:909090@cluster0.qdrfgmb.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DATABASE_NAME", "filesharexbot")

# Force sub channel id, if you want enable force sub
FORCESUB_CHANNEL = int(os.environ.get("FORCESUB_CHANNEL", "-1002282577591"))
FORCESUB_CHANNEL2 = int(os.environ.get("FORCESUB_CHANNEL2", "-1002350008026"))
FORCESUB_CHANNEL3 = int(os.environ.get("FORCESUB_CHANNEL3", "-1002406379151"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# Start message
START_MSG = os.environ.get("START_MESSAGE", 
    "<b>👋 Hello {mention}!</b>\n\n"
    "<b>I can store private files in a specified channel, and other users can access them from a special link! 🔐📁</b>\n\n"
    "<b>I'm fast like a cheetah 🐆💨</b>"
)

# ADMINS list
ADMINS = []
try:
    for x in os.environ.get("ADMINS", "7688387817").split():
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", 
    "<b>Hello {first},</b>\n\n"
    "<b>🛎 You need to join the channels to use me</b> (ሰላም፣ ፋይሉን ለማግኘት ቻናሎቹን Join ማረግ አለብዎት)\n\n"
    "<b>📭 Please join the channels first and click 'Try Again'</b> (ቻናሎቹን Join ከረጉ በኋላ ከታች 'Try again' የሚለውን ይጫኑ)"
)

# Custom caption - Keep None for disabling
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

# Set True if you want to prevent users from forwarding files from the bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Set true if you want to disable your Channel Posts' Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

# Bot stats text
BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"

# User reply text
USER_REPLY_TEXT = "❌ Don't send me messages directly, I'm only a File Share bot!"

# Adding OWNER_ID to ADMINS
ADMINS.append(OWNER_ID)

# Log file name
LOG_FILE_NAME = "codeflixbots.txt"

# Logging configuration
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
