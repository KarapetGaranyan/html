import scrapy
import json


class DivanLightingSpider(scrapy.Spider):
    name = "divan_lighting"
    allowed_domains = ["divan.ru"]

    # Начинаем с категории освещения
    start_urls = ["https://www.divan.ru/category/osveshhenie"]

    def parse(self, response):
        """
        Обрабатывает страницу категории освещения
        """
        # Сначала нужно проверить структуру страницы и селекторы для товаров
        # Получаем все товары на странице по CSS селектору
        lighting_items = response.css('div._Ud0k')

        # Если на странице есть товары, обрабатываем их
        for item in lighting_items:
            # Получаем название товара
            name = item.css('div.lsooF span::text').get()

            # Получаем цену товара
            price = item.css('div.pY3d2 span::text').get()

            # Получаем URL товара
            url = item.css('a').attrib['href']

            # Если это относительный URL, преобразуем его в абсолютный
            if url.startswith('/'):
                url = f"https://www.divan.ru{url}"

            # Создаем словарь с данными о товаре
            yield {
                'name': name,
                'price': price,
                'url': url,
                'category': 'Освещение'
            }

        # Ищем ссылку на следующую страницу для пагинации
        next_page = response.css('a[aria-label="Next page"]::attr(href)').get()
        if next_page:
            # Если есть следующая страница, переходим на нее
            if next_page.startswith('/'):
                next_page = f"https://www.divan.ru{next_page}"
            yield scrapy.Request(next_page, callback=self.parse)

        # Дополнительно можем проверить подкатегории освещения
        subcategories = response.css('a[href*="/category/osveshhenie/"]::attr(href)').getall()
        unique_subcategories = set()

        for subcategory in subcategories:
            # Проверяем, что это действительно подкатегория освещения
            if '/category/osveshhenie/' in subcategory and subcategory not in unique_subcategories:
                unique_subcategories.add(subcategory)
                # Если это относительный URL, преобразуем его в абсолютный
                if subcategory.startswith('/'):
                    subcategory = f"https://www.divan.ru{subcategory}"
                yield scrapy.Request(subcategory, callback=self.parse_subcategory)

    def parse_subcategory(self, response):
        """
        Обрабатывает страницу подкатегории освещения
        """
        # Определяем текущую подкатегорию из URL или хлебных крошек
        current_subcategory = response.url.split('/')[-1]

        # Получаем все товары на странице
        lighting_items = response.css('div._Ud0k')

        for item in lighting_items:
            name = item.css('div.lsooF span::text').get()
            price = item.css('div.pY3d2 span::text').get()
            url = item.css('a').attrib['href']

            # Если это относительный URL, преобразуем его в абсолютный
            if url.startswith('/'):
                url = f"https://www.divan.ru{url}"

            yield {
                'name': name,
                'price': price,
                'url': url,
                'category': 'Освещение',
                'subcategory': current_subcategory
            }

        # Проверяем пагинацию
        next_page = response.css('a[aria-label="Next page"]::attr(href)').get()
        if next_page:
            if next_page.startswith('/'):
                next_page = f"https://www.divan.ru{next_page}"
            yield scrapy.Request(next_page, callback=self.parse_subcategory)


# Для запуска паука и сохранения данных в JSON-файл:
# scrapy runspider divan_lighting_spider.py -o lighting_products.json


# Альтернативный вариант с использованием API (если на сайте есть API)
class DivanLightingApiSpider(scrapy.Spider):
    name = "divan_lighting_api"
    allowed_domains = ["divan.ru"]

    # API URL может отличаться, требуется изучение сетевых запросов на сайте
    api_url = "https://www.divan.ru/api/catalog"

    def start_requests(self):
        """
        Начинаем с API запроса для получения данных
        """
        # Параметры запроса к API
        params = {
            'category': 'osveshhenie',
            'page': 1,
            'limit': 48  # Количество товаров на странице
        }

        yield scrapy.Request(
            url=f"{self.api_url}?{self.urlencode(params)}",
            callback=self.parse_api
        )

    def urlencode(self, params):
        """
        Преобразует словарь параметров в URL-encoded строку
        """
        return "&".join(f"{k}={v}" for k, v in params.items())

    def parse_api(self, response):
        """
        Обрабатывает JSON-ответ от API
        """
        try:
            # Парсим JSON-ответ
            data = json.loads(response.body)

            # Извлекаем товары
            items = data.get('items', [])

            for item in items:
                yield {
                    'name': item.get('name'),
                    'price': item.get('price', {}).get('current'),
                    'url': f"https://www.divan.ru{item.get('url')}",
                    'category': 'Освещение',
                    'subcategory': item.get('subcategory', {}).get('name')
                }

            # Проверяем, есть ли следующая страница
            current_page = int(response.url.split('page=')[1].split('&')[0])
            total_pages = data.get('pagination', {}).get('total_pages', 1)

            if current_page < total_pages:
                # Формируем URL для следующей страницы
                next_url = response.url.replace(f'page={current_page}', f'page={current_page + 1}')
                yield scrapy.Request(next_url, callback=self.parse_api)

        except json.JSONDecodeError:
            self.logger.error(f"Не удалось распарсить JSON: {response.body[:100]}")