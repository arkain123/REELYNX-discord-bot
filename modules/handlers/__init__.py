import os
from dotenv import load_dotenv
from .command_handler import CommandHandler

load_dotenv()
handler = CommandHandler(prefix=os.getenv("PREFIX"))

__all__ = ['handler']