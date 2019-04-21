import re


page_list = list()


def page_counter(url):

    """
    :param url: response.url item
    :return: number of pages spider has scraped
    """

    global page_list

    try:
        offset = re.findall(r'[0-9]+', url)[0]
        page = int(eval(offset) / 60)
        page_list.append(page)

    except IndexError:
        page = 0
        page_list.append(page)

    pages_visited = max(page_list) - min(page_list) + 1

    return pages_visited
