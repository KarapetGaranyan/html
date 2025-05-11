import requests
import json


def github_api_request():
    """
    Отправляет GET-запрос к API GitHub для поиска репозиториев с HTML кодом.
    Печатает статус-код и содержимое ответа в формате JSON.
    """
    # URL для поиска репозиториев на GitHub с HTML кодом
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "language:html",
        "sort": "stars",
        "order": "desc",
        "per_page": 5  # Ограничим результаты для лучшей читаемости
    }

    # Отправляем GET-запрос
    response = requests.get(url, params=params)

    # Печатаем статус-код ответа
    print(f"Статус-код ответа: {response.status_code}")

    # Печатаем содержимое ответа в JSON формате
    print("\nСодержимое ответа в формате JSON:")
    json_response = response.json()
    print(json.dumps(json_response, indent=2, ensure_ascii=False))

    return response.status_code, json_response


if __name__ == "__main__":
    github_api_request()