# Собственный телеграм бот с бесплатным ChatGPT
### Вашему вниманию представляется простой пример кода на языке Python для создания Телеграм бота, с бесплатным ChatGPT. Итоговый код бота будет представден в конце статьи. 
### Для создания бота будут использоваться библиотеки: [telebot](https://pypi.org/project/pyTelegramBotAPI/) и [g4f](https://pypi.org/project/g4f/)
Рекомендуемая версии Python:
```
Python 3.10
```
В первую очередь необходимо установить все необходимые зависимости:
```
pip install -U g4f[all]
pip install pyTelegramBotAPI
pip install python-dotenv
```

Для корректного хранения ```API_token``` бота в дериктории нашего проекта создаем файл ```.env``` и записываем туда токен бота:
```
TOKEN = 'api токен бота'
```
Теперь непосредственно переходим к написаю бота. В этой же директории создаем файл ```main.py``` и импортируем необходимые библиотеки:
```
import time
import g4f
import telebot
import os
from dotenv import load_dotenv
```
Импортируем api токен бота из файла ```.env```:
```
load_dotenv()
TOKEN = os.getenv('TOKEN')
```
Создаем бота с его api токеном:
```
bot = telebot.TeleBot(TOKEN)
```
Прописываем функцию обработки начала работы с ботом (по команде ```/start```)
```
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     f"<b>{message.json['from']['first_name']}</b>, я бот ChatGPT, напишите свой вопрос:",
                     parse_mode='html')
```
При вводе пользователем команды ```/start```, бот отправит сообщение: ```"Ваше имя", я бот ChatGPT, напишите свой вопрос:"```, затем пользователем вводится запрос к чату и в работу вступает второй хендлер со своей функцией:
```
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
```
Текст запроса пользователя заносится в переменную ```content```, далее создется чат в указанной модели нейронной сети, у нас это ```gpt-3.5-turbo```, с указанным провайдером, в примере используется ```g4f.Provider.FreeGpt``` (список доступных моделей и провайдеров можно посмотреть на [официальном сайте библиотеки](https://pypi.org/project/g4f/)), в переменную ```message``` заноситься запрос пользователя из переменной ```content```, если позволяет провайдер, можно указать значение аргумента ```stream``` в True. Полученный ответ от нейронной сети, записанный в переменную ```response```, отправляется ботом в ответ на запрос пользователя с помощью метода ```bot.reply_to()```, далее выполняется обращение к той же функции с помощью строки ```bot.register_next_step_handler(message, chat_gpt)```, чтобы чат с нейронкой зациклился, для того чтобы можно было реализовать еще какие-либо функции.

Ну и в завершении, обязательно добавить данные строки для работы нашего бота:
```
if __name__ == '__main__':
    bot.infinity_polling(none_stop=True)
```

### Итоговый код:
```
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
```
### Вот так довольно просто можно реальзовать своего бота с функционалом ChatGPT.





