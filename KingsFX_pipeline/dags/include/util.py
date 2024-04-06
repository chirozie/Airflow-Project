from dotenv import load_dotenv
import os
from sqlalchemy import create_engine


def get_api_key():
    '''
    This functions returns the exchange rate API key stored in the environment 
    variable (.env)
    Parameter: Does not accept a parameter
    Retrun value: 
    - API key
    - API ID
    Return type: Tuple
    '''
    load_dotenv()
    api_key = os.getenv('API_KEY')
    api_id = os.getenv('API_ID')
    
    return (api_id, api_key)


def get_database_conn():
    '''
    This function retrieve database credentials from environment variable file (.env)
    and create a connection object used for establishing connection to a postgresql
    database instance.
    Parameter: Does not accept a parameter
    Return value: return a postgresql database connection object
    Return type: database obeject
    '''
    # Get database credentials from environment variable
    load_dotenv()
    db_user_name = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')
    port = os.getenv('DB_PORT')
    host = os.getenv('DB_HOST')
    # Create and return a postgresql database connection object
    return create_engine(f'postgresql+psycopg2://{db_user_name}:{db_password}@{host}:{port}/{db_name}')