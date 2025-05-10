import os
import sys
sys.path += [os.path.dirname(os.path.dirname(os.path.dirname(__file__)))]
from flowerweb.config.init_config import Config
from telebot import TeleBot
from commands import Handler


config_section = Config().setup().get('notificator')
token = config_section.get('telebot')
admins = config_section.get('recipient')

bot = TeleBot(token=token)

@bot.message_handler(content_types=['text'])
def handler(message):
    Handler.run(message, admins, bot)


if __name__ == '__main__':
    bot.polling()