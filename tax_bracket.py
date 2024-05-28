import json

def fetch_latest_tax_brackets(filename='config.json'):
    """
    Fetches the latest tax brackets from a JSON configuration file.
    
    :param filename: The path to the configuration file.
    :return: A dictionary of tax brackets.
    """
    try:
        with open(filename, 'r') as file:
            tax_brackets = json.load(file)['tax_brackets']
            # Convert "inf" strings to float('inf')
            for bracket in tax_brackets:
                if bracket['max'] == "inf":
                    bracket['max'] = float('inf')
            return tax_brackets
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")

def get_tax_bracket(income, tax_brackets):
    """
    Determines the tax bracket based on the user's income using the provided tax brackets.
    
    :param income: The user's annual income.
    :param tax_brackets: A list of tax brackets.
    :return: The tax bracket rate as a percentage.
    """
    for bracket in tax_brackets:
        if bracket['min'] <= income <= bracket['max']:
            return bracket['rate']
    
    return None