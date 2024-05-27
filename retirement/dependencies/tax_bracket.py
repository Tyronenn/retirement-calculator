import requests

def fetch_latest_tax_brackets():
    """
    Mock function to simulate fetching the latest tax brackets from an API.
    Replace this function with actual API calls in a real scenario.
    """
    # Simulated response from an API (replace with actual API call)
    return {
        'brackets': [
            {'min': 0, 'max': 9950, 'rate': 10},
            {'min': 9951, 'max': 40525, 'rate': 12},
            {'min': 40526, 'max': 86375, 'rate': 22},
            {'min': 86376, 'max': 164925, 'rate': 24},
            {'min': 164926, 'max': 209425, 'rate': 32},
            {'min': 209426, 'max': 523600, 'rate': 35},
            {'min': 523601, 'max': float('inf'), 'rate': 37}
        ]
    }

def get_tax_bracket(income):
    """
    Determines the tax bracket based on the user's income using the latest tax brackets.
    
    :param income: The user's annual income.
    :return: The tax bracket as a percentage.
    """
    tax_brackets = fetch_latest_tax_brackets()['brackets']
    
    for bracket in tax_brackets:
        if bracket['min'] <= income <= bracket['max']:
            return bracket['rate']
    
    return None