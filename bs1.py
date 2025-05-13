import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# Создаём переводчик
translator = Translator()


# Создаём функцию, которая будет получать информацию и переводить на русский
def get_russian_words():
    url = "https://randomword.com/"
    try:
        response = requests.get(url)

        # Создаём объект Soup
        soup = BeautifulSoup(response.content, "html.parser")
        # Получаем слово и удаляем пробелы
        english_word = soup.find("div", id="random_word").text.strip()
        # Получаем описание слова
        english_definition = soup.find("div", id="random_word_definition").text.strip()

        # Переводим слово и определение на русский
        russian_word = translator.translate(english_word, dest="ru").text
        russian_definition = translator.translate(english_definition, dest="ru").text

        # Возвращаем словарь с русскими словами и определениями
        return {
            "word": russian_word,
            "definition": russian_definition,
            "original_word": english_word  # Сохраняем оригинальное слово для проверки
        }
    # Функция, которая сообщит об ошибке, но не остановит программу
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return None


# Создаём функцию, которая будет делать саму игру
def word_game():
    print("Добро пожаловать в игру со словами на русском языке!")
    while True:
        # Получаем русское слово и определение
        word_dict = get_russian_words()

        if not word_dict:
            print("Не удалось получить слово. Попробуем еще раз.")
            continue

        word = word_dict.get("word")
        definition = word_dict.get("definition")

        # Начинаем игру
        print(f"Значение слова - {definition}")
        user_answer = input("Что это за слово? ")

        # Проверяем ответ (не учитываем регистр)
        if user_answer.lower() == word.lower():
            print("Все верно!")
        else:
            print(f"Ответ неверный, было загадано это слово - {word}")

        # Создаём возможность закончить игру
        play_again = input("Хотите сыграть еще раз? (y/n): ")
        if play_again.lower() != "y":
            print("Спасибо за игру!")
            break


if __name__ == "__main__":
    word_game()