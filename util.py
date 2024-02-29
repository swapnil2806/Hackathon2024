import pandas as pd
import numpy as np
import datetime
import random

unique_currency_path = "C:\\Users\\Renu Gaindar\\Mtech\\ChatBot\\datasets\\port_country_unique_values.csv"

try:
    currency_df = pd.read_csv(unique_currency_path, header=None, names=['CountryCode']).drop_duplicates()
    currency_list = [str(value).lower() for value in currency_df['CountryCode'].tolist()]
except FileNotFoundError:
    print("CSV file not found at the specified path.")
    currency_list = []

def country_search(input_list):
    """
    Finds matching country codes from a given input list.
    
    :param input_list: List of country codes to match
    :return: List of matching country codes found in both the input list and the CSV file
    """
    if not currency_list:  # Check if currency_list is empty, indicating CSV load failure
        return []

    input_list_lower = [str(item).lower() for item in input_list]
    matching_items = list(set(input_list_lower) & set(currency_list))
    
    return matching_items