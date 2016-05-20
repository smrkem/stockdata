import requests


def get_items():
    url = 'http://localhost:5000/api/v1/cases/'
    r = requests.get(url)
    items = r.json()
    return items['cases']
