from requests_html import HTMLSession
import pandas as pd


def get_states():

    """
    :return: Data frame containing a list of US states and their abbreviations.
    """

    session = HTMLSession()

    link = 'https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States'

    s = session.get(link)

    table = s.html.find('tbody')

    state_abrvs = list()

    row_1 = table[0].find('tr')

    for i in range(2, len(row_1)):

        d = dict()

        d['State'] = str(row_1[i].find('a')[0].text)
        d['Abbreviation'] = str(row_1[i].find('td')[0].text)

        state_abrvs.append(d)

    row_2 = table[1].find('tr')

    for i in range(2, len(row_2)):

        d = dict()

        d['State'] = str(row_2[i].find('a')[0].text)
        d['Abbreviation'] = str(row_2[i].find('td')[0].text)

        state_abrvs.append(d)

    row_3 = table[2].find('tr')

    for i in range(2, len(row_3)):

        d = dict()

        d['State'] = str(row_3[i].find('a')[0].text)
        d['Abbreviation'] = str(row_3[i].find('td')[0].text)

        state_abrvs.append(d)

    df = pd.DataFrame(state_abrvs, columns=['State', 'Abbreviation'])

    return df


states = get_states()
