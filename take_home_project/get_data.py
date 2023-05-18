import psycopg2
import pandas as pd


def get_data():
    #connecting to DB
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        database="brx1",
        user="process_trending",
        password="abc123"
    )

    # create a dictionary to store the dataframes
    dataframes = {}

    # fetch data from each table and store it in a separate dataframe
    tables = [("temperature",'"CM_HAM_DO_AI1/Temp_value"'), ("pH",'"CM_HAM_PH_AI1/pH_value"'), ("distilled_O2",'"CM_PID_DO/Process_DO"'), ("pressure",'"CM_PRESSURE/Output"')]

    # open a cursor to perform Database operations    
    cur = conn.cursor()

    for name,table in tables:
        cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        df = pd.DataFrame(rows, columns=columns)
        dataframes[name] = df
    

    # close the connection
    cur.close()
    conn.close()
    
    return dataframes["temperature"], dataframes["pH"], dataframes["distilled_O2"], dataframes["pressure"]