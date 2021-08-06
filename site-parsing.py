# TODO
# Проверить, у какого сайта "тяжелее" главная страница
# Получить html
# Узнать, какие файлы CSS и JS нужны для отображения
# Посчитать общий размер файлов
# Вывести на консоль результат

# Библиотека для получения информации с сайта
from urllib.request import urlopen
from html.parser import HTMLParser
from html.entities import name2codepoint


class LinkExtractor(HTMLParser):
    """Вытягивает ссылки из html-файла"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.links = []

    def handle_starttag(self, tag, attrs):
        # найдем только тэги link
        if tag not in ('link, script'):
            return
        attrs = dict(attrs)
        print("Start tag:", tag)
        if tag == 'link':
            # распарсили css
            if 'rel' in attrs and attrs['rel'] == 'stylesheet':
                self.links.append(attrs['href'])
        elif tag == 'script':
            # распарсили js
            if 'src' in attrs:
                self.links.append(attrs['src'])



sites = [
    'https://www.fl.ru',
    # 'https://www.weblancer.net/',
    # 'https://www.freelancejob.ru/'


]

for url in sites:
    print(f" go {url}")
    res = urlopen(url)
    html_data  = res.read()

    html_data = html_data.decode("utf8")  # перекодируем поток байт в utf8
    total_bytes = len(html_data)    # вычислим размер
    # распарсим сайт
    extractor = LinkExtractor()
    extractor.feed(html_data)
    print(extractor.links)
    for link in extractor.links:
        print(f"\tGo {link}")
        try:
            res = urlopen(link)
        except Exception as exc:
            print(exc)

        extra_data = res.read()
        total_bytes += len(extra_data)  # вычислим размер
    print(f"\t for url {url} need download {total_bytes//1024} Kb")




