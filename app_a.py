import telebot
from config import keys, TOKEH
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEH)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Здравствуйте! Я могу дать вам информацию о конвертации некоторых валют.\ ' \
           'Для этого введите комманду в следующем формате:\n<имя валюты> \
<в какую валюту перевсти> \
<единица переводимой валюты> \n <Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException('Не соответствует трём параметрам.')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
        if amount != '1':
            raise ConvertionException('Количество превышает единицу валюты')
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
