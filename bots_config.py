from consts import RunningEnviroments
import telebot
from telebot import TeleBot

def get_bot(env):
    if env == RunningEnviroments.PRODUCTION:
        API_TOKEN = 'add token here' # main bot token
        return TeleBot(API_TOKEN, threaded=False)
    elif env == RunningEnviroments.DEVELOPMENT :
        API_TOKEN = 'add token here' # test bot token
        return TeleBot(API_TOKEN, threaded=False)
    