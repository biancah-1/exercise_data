import pandas as pd

# putting date into date obj
def date_clean(x):
    obj = pd.to_datetime(x)
    return(obj)

# function to create clean dataframe containing desired info from raw csvs 
def clean_data(path,og_names,new_names):
    data = pd.read_csv(path,header=0)
    df = pd.DataFrame()

    if len(og_names)==len(new_names):
        for i in range(len(og_names)):
            # copy over desired columns into df 
            df.loc[:,new_names[i]] = data.loc[:,og_names[i]]
        if 'TIMESTAMP' in og_names:
            new_name_date = new_names[og_names.index('TIMESTAMP')] # look for name used for timestamp in list
            df[new_name_date] = df[new_name_date].apply(date_clean) 
            df.sort_values(by=new_name_date) # sort df ascending by date
        return df
    else:
        print('Must have same number of new column names and old column names')