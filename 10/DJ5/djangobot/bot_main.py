import telebot
from telebot.types import Message
import requests

API_URL = "http://127.0.0.1:8000/api"

BOT_TOKEN = "7575779990:AAFoDQB-YO3EnkKjf-bSazm7IAENv5YG3X8"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    data = {
        'user_id': message.from_user.id,
        'username': message.from_user.username
    }

    print(f"Отправляю данные: {data}")
    print(f"URL: {API_URL}/register/")

    try:
        response = requests.post(API_URL + "/register/", json=data)
        print(f"Статус код: {response.status_code}")
        print(f"Ответ сервера: {response.text}")

        if response.status_code != 200:  # Исправлено здесь
            bot.send_message(message.chat.id, "Произошла ошибка при регистрации!")
            print(response.json())
            print(response.status_code)
            print(response.text)
        else:
            if response.json().get('message'):
                bot.send_message(message.chat.id, "Вы уже были зарегистрированы ранее!")
            else:
                bot.send_message(message.chat.id,
                                 f"Вы успешно зарегистрированы! Ваш уникальный номер: {response.json()['id']}")

    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        bot.send_message(message.chat.id, f"❌ Ошибка: {str(e)}")


@bot.message_handler(commands=['myinfo'])
def user_info(message):
    response = requests.get(f"{API_URL}/user/{message.from_user.id}/")

    if response.status_code == 200:
        bot.reply_to(message, f"Ваша регистрация:\n\n{response.json()}")
    elif response.status_code == 404:
        bot.send_message(message.chat.id, "Вы не зарегистрированы!")
    else:
        bot.send_message(message.chat.id, "Непредвиденная ошибка!")


if __name__ == "__main__":
    bot.polling(none_stop=True)

