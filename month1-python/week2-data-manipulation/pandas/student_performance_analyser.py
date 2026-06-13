import pandas as pd

def load_csv():
    df=pd.read_csv(r"F:\ai-engineering-roadmap\month1-python\week2-data-manipulation\pandas\Student_Performance.csv")
    return df

def explore(df):
    print(df.info())
    
def find_missing(df):
    total_missing = df.isnull().sum().sum()
    print(f"total missing values is : {total_missing}")
        
def find_outliers(df):
    df_num=df.select_dtypes(include=['number'])
    q25=df_num.quantile(0.25)
    q75=df_num.quantile(0.75)
    iqr=q75-q25
    lower_bound=q25-(1.5*iqr)
    upper_bound=q75+(1.5*iqr)
    outliers = (df_num < lower_bound) | (df_num > upper_bound)
    return df_num,outliers

def remove_outliers(df):
    df_num,outliers=find_outliers(df)
    df[df_num.columns]=df_num.mask(outliers,df_num.mask(outliers).mean(),axis=1)
    return df

def fill_missing(df):
    column_means = df.mean(numeric_only=True)
    df = df.fillna(column_means)
    return df
def dependent_factors(df):
    print('-'*50+'-'*50)
    print(df.corr(numeric_only=True))
    print('-'*50+'-'*50)
    
def average_performance(df):
    print(df.mean(numeric_only=True))

def analyse_extracurricular_impact(df):    
    print('-'*50+'-'*50)
    print("\n--- Extracurricular Activities Impact Analysis ---")
    impact = df.groupby('Extracurricular Activities').mean(numeric_only=True)
    print(impact) 
    print("\n--- Summary of Key Differences ---")
    yes_perf = impact.loc['Yes', 'Performance Index']
    no_perf = impact.loc['No', 'Performance Index']
    diff = yes_perf - no_perf
    print(f"Average Performance Index for 'Yes': {yes_perf:.2f}")
    print(f"Average Performance Index for 'No': {no_perf:.2f}")
    print(f"Students in extracurriculars scored {abs(diff):.2f} points {'higher' if diff > 0 else 'lower'} on average.")
    print('-'*50+'-'*50)
    
def main():
    df=load_csv()
    explore(df)
    find_missing(df)
    df=remove_outliers(df)
    df=fill_missing(df)
    dependent_factors(df)
    average_performance(df)
    analyse_extracurricular_impact(df)
    
if __name__=="__main__":
    main()