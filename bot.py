import telebot


from config import TOKEN, keys
from extensions import APIException, CurrencyConvector

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message: telebot.types.Message):

    bot.send_message(message.chat.id, f'Привет, {message.chat.username}.\
  Я Бот для конвертации валют.\n Для конвертации введите: <название конвертируемой валюты>\
  <название валюты в которой нужно конвертировать>\
  <количество конвертируемой валюты>\n Список доступных валют: /values\n Нужна помощь /help')


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Для конвертации введите: <название конвертируемой валюты>\
 <название валюты в которой нужно конвертировать>\
 <количество конвертируемой валюты>\n Список доступных валют: /values')


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты для конвертации:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message, ):
    try:
        val = message.text.split(' ')

        if len(val) < 3:
            raise APIException('Ошибка при вводе параметров. Слишком мало параметров. /help')
        if len(val) > 3:
            raise APIException('Ошибка при вводе параметров. Слишком много параметров. /help')

        base, quota, amount = val

        total_sum = CurrencyConvector.get_price(base, quota, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Сумма конвертации {amount} {base} в {quota} составляет {total_sum}'
        bot.send_message(message.chat.id, text)


bot.polling()
