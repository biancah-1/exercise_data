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

# calculations
def weight_calcs(x):
    logs = x.split(',')

    w_list = []
    v_list = []
    for i in range(len(logs)):
        log_i = logs[i].split('x')
        weight = float(log_i[0])
        reps = float(log_i[1])
        vol = weight*reps

        w_list.append(weight)
        v_list.append(vol)
    
    w_max = max(w_list)
    v_total = sum(v_list)
   
    return w_max, v_list, v_total

