import requests
import json


def create_post():
    """
    Отправляет POST-запрос к JSONPlaceholder API для создания новой записи.
    Распечатывает статус-код и содержимое ответа.
    """
    # URL API для создания новых записей
    url = "https://jsonplaceholder.typicode.com/posts"

    # Данные для отправки
    data = {
        'title': 'foo',
        'body': 'bar',
        'userId': 1
    }

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Отправляем POST-запрос
    print(f"Отправка POST-запроса к {url}")
    print(f"Отправляемые данные: {json.dumps(data, indent=2)}")

    response = requests.post(url, json=data, headers=headers)

    # Выводим статус-код ответа
    print(f"\nСтатус-код ответа: {response.status_code}")

    # Проверяем успешность запроса
    if response.status_code >= 200 and response.status_code < 300:
        print("Запрос успешно выполнен!")
    else:
        print(f"Ошибка при выполнении запроса. Код: {response.status_code}")

    # Выводим содержимое ответа
    try:
        json_response = response.json()
        print("\nСодержимое ответа в формате JSON:")
        print(json.dumps(json_response, indent=2))

        # Выводим полученный ID (JSONPlaceholder обычно возвращает ID)
        if 'id' in json_response:
            print(f"\nСоздана запись с ID: {json_response['id']}")

        return response.status_code, json_response
    except json.JSONDecodeError:
        print("\nНевозможно декодировать ответ как JSON:")
        print(response.text)
        return response.status_code, response.text


if __name__ == "__main__":
    create_post()