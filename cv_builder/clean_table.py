import re
from my_projects.cv_builder.html_table import *


def remove_brackets(data=df_index_table):

    """
    :param data: data frame to perform regex on
    :return: City/states with brackets removed.
    """

    pattern = r'\([^\)]*\)'

    data['new_city'] = data['city'].apply(lambda x: re.sub(pattern, '', x))
    data = data.drop(['city'], axis=1)
    data = data.rename(index=str, columns={'new_city': 'city'})

    return data


df_index_table = remove_brackets()


def split_city_name(data=df_index_table):

    """
    :param data: data frame to perform regex on
    :return: City/State split from Country and saved in a list.
    """

    data['new_city'] = data['city'].apply(lambda x: x.split(', '))

    data['state'] = data['new_city'].apply(lambda x: x[1])
    data['city_name'] = data['new_city'].apply(lambda x: x[0])
    data['country'] = data['new_city'].apply(lambda x: x[-1])

    data = data.drop(['new_city', 'city'], axis=1)
    data = data.rename(index=str, columns={'city_name': 'city'})

    data = data[['city', 'state', 'country', 'cost_of_living', 'rent', 'cost_of_living_plus_rent', 'groceries',
                 'restaurant_price', 'local_purchasing_power']]

    return data


df_index_table = split_city_name()
