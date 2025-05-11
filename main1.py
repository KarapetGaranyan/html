import requests
import json


def get_posts_by_user_id(user_id):
    """
    Отправляет GET-запрос к JSONPlaceholder API для получения постов с определенным userId.

    Args:
        user_id (int): ID пользователя, посты которого нужно получить

    Returns:
        tuple: (код ответа, данные ответа)
    """
    # URL API с параметром фильтрации
    url = f"https://jsonplaceholder.typicode.com/posts"
    params = {"userId": user_id}

    # Отправляем GET-запрос
    response = requests.get(url, params=params)

    # Выводим информацию о запросе
    print(f"URL запроса: {response.url}")
    print(f"Статус-код ответа: {response.status_code}")

    # Получаем данные в формате JSON
    data = response.json()

    # Выводим количество полученных записей
    print(f"Количество полученных записей: {len(data)}")

    # Выводим полученные записи
    print("\nПолученные записи:")
    print(json.dumps(data, indent=2))

    return response.status_code, data


if __name__ == "__main__":
    # Получаем посты пользователя с ID = 1
    get_posts_by_user_id(1)