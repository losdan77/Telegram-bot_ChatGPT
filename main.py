import time
import g4f
import telebot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f"<b>{message.json['from']['first_name']}</b>, я бот ChatGPT, напишите свой вопрос:",
                     parse_mode='html')


@bot.message_handler(content_types=['text'])
def chat_gpt(message):
    bot.send_message(message.chat.id,
                     'Секундочку...')

    content = message.text

    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo',
                                         provider=g4f.Provider.FreeGpt,
                                         messages=[{'role': 'user', 'content': content}],
                                         stream=True)

    bot.reply_to(message,
                 f"{''.join(list(response))}"
                 )
    time.sleep(2)

    bot.register_next_step_handler(message,
                                   chat_gpt)


bot.infinity_polling(none_stop=True)