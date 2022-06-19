import pandas as pd

#Function to read the data
def read_data(file_path, **kwargs):
    try:
        raw_data=pd.read_excel(file_path  ,**kwargs)
    except Exception as e:
        print(e)
    else:
        return raw_data

