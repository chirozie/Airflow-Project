import requests
import json
import os

def extract_data(api_id, api_key):
    print(api_id, api_key)
    currencies = ['NGN', 'GHS', 'KES', 'UGX', 'MAD', 'XOF', 'EGP']
    to_curr = ",".join(currencies)
    url = f'https://xecdapi.xe.com/v1/convert_from.json?from=USD&to={to_curr}'

    response = requests.get(url, auth=(api_id, api_key)).json()
    print(response)

    if not os.path.exists('./opt/airflow/raw'):
        os.makedirs('./opt/airflow/raw')

    with open('./opt/airflow/raw/extract.json', 'w') as json_file:
        json.dump(response, json_file)