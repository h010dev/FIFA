from my_projects.cv_builder.clean_table import df_index_table
from my_projects.cv_builder.exchange_rates import exchange_to
from my_projects.cv_builder.secret_vars import *


def add_expense(budget, unique_expense, base_loc=current_loc, a=c_from, b=c_to, data=df_index_table):

    """
    :param budget: current monthly expenses
    :param unique_expense: unique expenses that won't be affected by the cost of living index
    :param base_loc: current location
    :param a: currency to exchange from
    :param b: currency to exchange to
    :param data: data frame to apply estimated expenses to
    :return: New column in listed data frame with estimated expenses for each city based on current living expenses and
    specified exchange rate.
    """

    budget_converted = budget * exchange_to(a, b)
    unique_expense_converted = unique_expense * exchange_to(a, b)
    base_index = data[data['city'] == base_loc]['cost_of_living_plus_rent'].astype(float)

    data['base_index_ratio'] = data['cost_of_living_plus_rent'].apply(lambda x: float(x) / base_index)

    data['min_monthly_budget_' + b] = \
        data['base_index_ratio'].apply(lambda x: x * budget_converted + unique_expense_converted)

    data['min_annual_budget_' + b] = data['base_index_ratio'].apply(
        lambda x: 12 * (x * budget_converted + unique_expense_converted))

    return data


df_index_table = add_expense(my_budget, my_unique_expense)
