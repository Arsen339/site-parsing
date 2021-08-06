# TODO
# Проверить, у какого сайта "тяжелее" главная страница
# Получить html
# Узнать, какие файлы CSS и JS нужны для отображения
# Посчитать общий размер файлов
# Вывести на консоль результат

# Библиотека для получения информации с сайта
import time
from urllib.parse import urljoin

import requests
from html.parser import HTMLParser

from html.entities import name2codepoint


def time_track(func):
    def surrogate(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        ended_at = time.time()
        elapsed = abs(round(ended_at - started_at, 6))
        print(f"Функция {func.__name__} работала {elapsed} секунд")
        return result
    return surrogate








class LinkExtractor(HTMLParser):
    """Вытягивает ссылки из html-файла"""
    def __init__(self, base_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.links = []
        self.base_url = base_url

    def handle_starttag(self, tag, attrs):
        # найдем только тэги link
        if tag not in ('link, script'):
            return
        attrs = dict(attrs)
        print("Start tag:", tag)
        if tag == 'link':
            # распарсили css
            if 'rel' in attrs and attrs['rel'] == 'stylesheet':
                link = self._refine(attrs['href'])
                self.links.append(link)
        elif tag == 'script':
            # распарсили js
            if 'src' in attrs:
                link = self._refine(attrs['src'])
                self.links.append(link)

    def _refine(self, link):
        return urljoin(self.base_url, link)


class PageSizer:

    def __init__(self, url):
        self.url = url
        self.total_bytes = 0

    def run(self):
        self.total_bytes = 0
        html_data = self._get_html(url=self.url)
        if html_data is None:
            return
        self.total_bytes += len(html_data)
        extractor = LinkExtractor(base_url=self.url)
        extractor.feed(html_data)
        for link in extractor.links:
            extra_data = self._get_html(url=link)
            if extra_data is None:
                continue
            self.total_bytes += len(extra_data)

    def _get_html(self, url):
        print(f" go {url}")

        try:
            res = requests.get(url)

        except Exception as exc:
            print(exc)
        else:
            return res.text

@time_track
def main():
    sites = [
        'https://www.fl.ru',
        'https://www.weblancer.net/',
        'https://www.freelancejob.ru/'


    ]


    sizers = [PageSizer(url) for url in sites]

    for sizer in sizers:
        sizer.run()
    for sizer in sizers:
        print(f"\t for url {sizer.url} need download {sizer.total_bytes//1024} Kb")

if __name__ == '__main__':
    main()