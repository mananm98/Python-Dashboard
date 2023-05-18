import pandas as pd

def create_marker(df):
    '''
    Takes in a DataFrame and returns a dictionary of mappings of row_index_number and corresponding Timestamp
    '''
    marks = {}

    # Add a new column 'hours' in the DataFrame by converting the timestamp to '%I %p' format
    df['hours'] = df['time'].apply(lambda x : x.strftime('%I %p'))

    curr_numdate = 0
    
    # Group the DataFrame by 'hours' column and count the Timestamps in each hour
    hours = df["hours"].unique()
    datapoints_in_each_hour = df.groupby("hours").count()['time']

    # iterate through each hour, to create range-slider intervals
    for time,count in zip(hours,datapoints_in_each_hour):
        marks[curr_numdate] = time
        curr_numdate += count
    
    marks[curr_numdate] = "end_of_last_hr"
    return marks