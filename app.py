import telebot

from config import My_keys, TOKEN
from extensions import Exceptions, Converters

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def _help(message: telebot.types.Message):
    text = 'Я бот который переводит одну валюту в другую! \n' \
           'Чтобы я мог это сделать, Вы должны мне помочь. \n' \
           'Для этого напишите мне сообщение в формате: \n' \
           '<название валюты>  <в какую валюту нужно перевести>  <количество переводимой валюты>\n' \
           '\n' \
           'Названия валют нужно указывать в именительном падеже!\n' \
           'Список всех валют можно увидеть введя: /values\n'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def _values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in My_keys.keys():
        text = '\n'.join((text, key,))

    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def _convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) < 3:
            raise Exceptions('Мало параметров!')

        if len(values) > 3:
            raise Exceptions('Много параметров!')

        quote, base, amount = values
        total_base = Converters._convert(quote, base, amount)
    except Converters as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду!\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
