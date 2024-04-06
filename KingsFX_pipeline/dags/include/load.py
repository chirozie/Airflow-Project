import pandas as pd



def load_data(engine, table):
    '''
    This function loads the transformed data to a postgres database table

    Parameters: Engine - A sqlalchemy engine. df - a dataframe, table - Database table
    Return Value: None
    Return Type: None
    '''
    df = pd.read_csv('./opt/airflow/raw/data.csv')
    df.to_sql(table, engine, if_exists='append', index=False)