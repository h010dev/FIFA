from requests_html import HTMLSession
import pandas as pd


pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)

session = HTMLSession()


def read_table(r=session.get('https://www.numbeo.com/cost-of-living/rankings.jsp')):

    """
    :param r: url to start session on.
    :return: Data frame with various living indexes listed by city/state and country.
    """

    table_list = list()

    table = r.html.find('table.stripe', first=True)
    body = table.find('tbody')
    row = body[0].find('tr')

    for i in range(len(row)):

        row_dictionary = dict()

        row_dictionary['city'] = row[i].find('td')[1].text
        row_dictionary['cost_of_living'] = row[i].find('td')[2].text
        row_dictionary['rent'] = row[i].find('td')[3].text
        row_dictionary['cost_of_living_plus_rent'] = row[i].find('td')[4].text
        row_dictionary['groceries'] = row[i].find('td')[5].text
        row_dictionary['restaurant_price'] = row[i].find('td')[6].text
        row_dictionary['local_purchasing_power'] = row[i].find('td')[7].text

        table_list.append(row_dictionary)

    df = pd.DataFrame(table_list, columns=['city', 'cost_of_living', 'rent', 'cost_of_living_plus_rent',
                                           'groceries', 'restaurant_price', 'local_purchasing_power'])
    return df


df_index_table = read_table()
