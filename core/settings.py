# encoding=utf-8
import os
from distutils.log import info

from dotenv import load_dotenv

from .utils import change_to_level

# Carregar Variáveis de ambiente -> .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

DEFAULT_LVL = 20  # INFO

LOG_LVL = change_to_level(os.getenv("LOG_LVL"), DEFAULT_LVL)
