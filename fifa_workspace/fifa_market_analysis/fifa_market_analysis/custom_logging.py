import re


def current_page(url):

    """
    :param url: response.url item
    :return: current page spider is on
    """

    try:
        offset = re.findall(r'[0-9]+', url)[0]
        page = int(eval(offset) / 60) + 1
        return page

    except IndexError:
        page = 1
        return page
