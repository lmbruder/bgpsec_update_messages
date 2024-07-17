import pandas as pd
import os

def add_data_to_df(file):
    df = pd.read_csv(file, index_col=None, header=0)
    list.append(df)

list = []
directory = '/path/to/folder/'
all_files = sorted(os.listdir(directory))
# go through all files with first seen timestamps and add all to a dataframe
for timestamps in all_files:
    print(timestamps)
    add_data_to_df(directory + timestamps)
    

frame = pd.concat(list, axis=0, ignore_index=True)
frame['timestamp'] = pd.to_datetime(frame['timestamp'], unit='ms') + pd.Timedelta(hours=2)
# gather occurences per for example 1 or 30 minutes ('min', '30min')
frame['time_block'] = frame['timestamp'].dt.floor('30min')
counts_per_block = frame.groupby('time_block').size().reset_index(name='count')
# write to csv
counts_per_block.to_csv('timestamps.csv', index=False)