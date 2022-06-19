import re

# Function to drop null values from dataframe
def drop_null(df):
    try:
        data = df.dropna().reset_index()
    except Exception as e:
        print(e)
    else:
        return data

# Function to combine two columns
def combine_col(df,col1,col2):
    try:
        df[col1]= df[col2] + ' ' +df[col1]
    except Exception as e:
        print(e)
    else:
        return df

# Function to drop duplicates from dataframes' column    
def drop_duplicates(df,col):
    try:
        data=df.drop_duplicates(subset=col, keep='first')
    except Exception as e:
        print(e)
    else:
        return data

# Function to convert words to lowercase
def convert_lower(df,col_to_conert,new_col):
    try:
        df[new_col] = df[col_to_conert].apply(lambda x: x.lower())  
    except Exception as e:
        print(e)
    else:
        return df

# Function to remove special characters from a column
def remove_spl_char(df,col):
    try:
        df[col] = df[col].apply(lambda x: re.sub(r'[^\w\s]', '', x)) 
    except Exception as e:
        print(e)
    else:
        return df

# Function to preprocess the data
def process_data(df,col1,col2):
    # Combining columns
    df=combine_col(df,col1,col2)

    # Dropping Duplicates and keeping first record
    unique_df=drop_duplicates(df,[col1])
    
    # Converting String to Lower Case
    unique_df=convert_lower(df,col1,'desc_lowered')
   
    # Remove Stop special Characters
    unique_df=remove_spl_char(df,'desc_lowered')
    unique_df= unique_df.reset_index(drop=True)
    
    # Coverting Description to List
    desc_list = list(unique_df['desc_lowered'])

    return  unique_df,desc_list   