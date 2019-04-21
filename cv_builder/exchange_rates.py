from requests_html import HTMLSession
from my_projects.cv_builder.secret_vars import *


def exchange_to(a, b):

    """
    :param a: currency rate to exchange from
    :param b: currency rate to exchange to
    :return: Exchange rate between currency a and currency b.
    """

    session = HTMLSession()

    link = 'https://www.google.com/search?gl=us&hl=en&pws=0&source=hp&ei=pUaHXNOeEcrWvgTuwZfoBA&q=' + \
           f'{a}+to+{b}&btnK=Google+Search&oq={a}+to+{b}'

    s = session.get(link)

    exchange_header = s.html.find('#knowledge-currency__v2-header')
    print(exchange_header[0].text, '\n')

    rate = float(s.html.xpath('//span[@class="DFlfde"]/text()')[1])

    session.close()

    return rate


exchange_rate = exchange_to(c_from, c_to)
