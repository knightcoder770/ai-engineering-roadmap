import numpy as np

def load_data():
    pass

def generate_data():
    rng=np.random.default_rng(42)
    age=rng.integers(low=10,high=30,size=200,endpoint=True)
    study_hours=rng.integers(low=0,high=24,size=200,endpoint=True)
    sleep_hours=rng.integers(low=0,high=24,size=200,endpoint=True)
    test_score=rng.integers(low=0,high=200,size=200)/2
    data=np.column_stack((age,study_hours,sleep_hours,test_score))
    data=data.astype(float)
    num_rows=data.shape[0]
    num_col=data.shape[1]
    nans_per_column=20
    for i in range(0,num_col):
        random_row=rng.choice(num_rows,size=nans_per_column,replace=False)
        data[random_row,i]=np.nan
    for i in range (0,num_col):
        random_row=rng.choice(num_rows,size=10,replace=False)
        data[random_row,i]=rng.integers(500,1000)
    return data

def find_missing(data):
    missing=np.sum(np.isnan(data),axis=0)
    col_names = ["age", "study_hours", "sleep_hours", "test_score"]
    for name, count in zip(col_names, missing):
        print(f"{name}: {count}")

def get_bounds(data):
    percentile_25=np.nanpercentile(data,q=25,axis=0)
    percentile_75=np.nanpercentile(data,q=75,axis=0)
    iqr=percentile_75-percentile_25
    lower_bound=percentile_25-(1.5*iqr)
    upper_bound=percentile_75+(1.5*iqr)
    return lower_bound,upper_bound

def find_outliers(data):     
    lower_bound,upper_bound=get_bounds(data)   
    outlier_mask=(lower_bound>data)|(data>upper_bound)
    no=np.sum(outlier_mask,axis=0)
    print(f"total no of outliers is {no}")

def remove_outliers(data):
    lower, upper = get_bounds(data)
    outlier_mask=(data<lower)|(data>upper)
    data=data.copy()
    data[outlier_mask]=np.nan
    return data

def fill_missing(data):
    column_mean=np.nanmean(data,axis=0)
    nan_place=np.isnan(data)
    return np.where(nan_place, column_mean, data)

def normalize(data):
    min_=np.nanmin(data,axis=0)
    max_=np.nanmax(data,axis=0)
    normalize_data=(data-min_)/(max_-min_)
    return normalize_data

def standardize(data):
    mean = np.nanmean(data, axis=0)
    std = np.nanstd(data, axis=0)
    standardised_data = (data - mean) / std
    return standardised_data

def summary_stats(raw_data,cleaned_data):
    col_names = ["age", "study_hours", "sleep_hours", "test_score"]
    
    raw_mean = np.nanmean(raw_data, axis=0)
    raw_std = np.nanstd(raw_data, axis=0)
    raw_min = np.nanmin(raw_data, axis=0)
    raw_max = np.nanmax(raw_data, axis=0)
    
    clean_mean = np.nanmean(cleaned_data, axis=0)
    clean_std = np.nanstd(cleaned_data, axis=0)
    clean_min = np.nanmin(cleaned_data, axis=0)
    clean_max = np.nanmax(cleaned_data, axis=0)
    
    print(f"{'Column':<15} | {'Stat':<6} | {'Raw Data':<12} | {'Cleaned Data':<12}")
    print("-" * 55)
    for i, name in enumerate(col_names):
        print(f"{name:<15} | {'Mean':<6} | {raw_mean[i]:<12.2f} | {clean_mean[i]:<12.2f}")
        print(f"{'':<15} | {'Std':<6} | {raw_std[i]:<12.2f} | {clean_std[i]:<12.2f}")
        print(f"{'':<15} | {'Min':<6} | {raw_min[i]:<12.2f} | {clean_min[i]:<12.2f}")
        print(f"{'':<15} | {'Max':<6} | {raw_max[i]:<12.2f} | {clean_max[i]:<12.2f}")
        print("-" * 55)
    
def main():
    raw_data=generate_data()
    find_missing(raw_data)
    find_outliers(raw_data)
    data=remove_outliers(raw_data)
    data=fill_missing(data)
    clean_data = data.copy()
    data=normalize(data)
    data=standardize(data)
    summary_stats(raw_data,clean_data)
    
if __name__=="__main__":
    main()