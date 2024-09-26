import requests
from bs4 import BeautifulSoup
import urllib.parse

# Функция для краулинга одной страницы
URL_TEST_SITE = 'https://books.toscrape.com/'


def crawl(url, visited):
    # Проверяем, был ли этот URL уже посещен
    if url in visited:
        return
    visited.add(url)

    # Отправляем HTTP-запрос к указанному URL
    try:
        response = requests.get(url)
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return

    # Проверяем успешность запроса (200 - это успешный ответ)
    if response.status_code == 200:
        # Создаем объект BeautifulSoup для парсинга HTML
        root = BeautifulSoup(response.text, 'html.parser')
        # print("root name", root.name)

        # Например, извлечем все заголовки <h2> на странице
        titles = root.find_all(['h1', 'h2', 'h3', 'h4'])
        # Открываем файл для записи
        with open('output.txt', 'a', encoding='utf-8') as file:
            # Пишем результаты в файл
            file.write(f"Заголовки с {url}:\n")
            for idx, title in enumerate(titles, start=1):
                # Выводим заголовки в консоль и записываем в файл
                # print(f"{idx}. {title.get_text()}")
                file.write(f"{idx}. {title.get_text()}\n")

        # Извлекаем все ссылки на странице
        links = root.find_all('a', href=True)
        with open('links.txt', 'a', encoding='utf-8') as link_file:
            link_file.write(f"Ссылки с {url}:\n")
            for link in links:
                href = link['href']

                # Обрабатываем относительные ссылки
                full_url = urllib.parse.urljoin(url, href)

                # Записываем ссылку в файл и выводим в консоль
                print(f"Найдена ссылка: {full_url}")
                link_file.write(f"{full_url}\n")

                # Рекурсивно обходим по ссылкам (но избегаем бесконечных циклов)
                if full_url.startswith('http') and full_url not in visited:
                    crawl(full_url, visited)

        print("\nРезультаты записаны в файл output.txt")
    else:
        print(f"Ошибка {response.status_code}: Не удалось получить страницу")


# Основная функция для запуска краулера
def main():
    # Множество для отслеживания посещенных ссылок
    visited_urls = set()

    # Запускаем краулер с начальной страницы
    crawl(URL_TEST_SITE, visited_urls)


# Запуск программы
if __name__ == "__main__":
    main()
