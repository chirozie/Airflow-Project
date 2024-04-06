import json
import pandas as pd
from datetime import datetime


def transform_data():
    '''
    This function transforms the extracted json data of currencies exchange rates into a pandas dataframe and saves the 
    data to a csv file
    Parameters: Null
    Return Value: Null
    Return Type: Null
    '''
    # read the json file 
    with open('./opt/airflow/raw/extract.json', 'r') as json_file:
        response = json.load(json_file)
    
    rates = []
    timestamp = response['timestamp']

    for rate in response['to']:
        rates.append((timestamp, 'USD', rate['quotecurrency'], rate['mid']))

    data = pd.DataFrame(rates, columns=['timestamp', 'currency_from','currency_to', 'rate'])

    # clean the timestamp column
    data['timestamp'] = data['timestamp'].apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ'))

    # save to csv
    data.to_csv('./opt/airflow/raw/data.csv', index=False)