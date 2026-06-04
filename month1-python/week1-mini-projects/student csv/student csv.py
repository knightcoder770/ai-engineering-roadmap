import pandas as pd

def load_csv():
    try:
        data=pd.read_csv("F:\\ai engineer\\python fundamentals\\student csv\\student_data.csv")
        return data
    except FileNotFoundError:
        print("file is not found")
    except pd.errors.EmptyDataError:
        print("file is empty")
    except Exception as e:
        print("some other error:",e)

def explore_data(data):
    print('-'*100)
    print(f"the number of rows and columns in data is : {data.shape}")
    print('-'*100)
    print(f"the column elements are:{data.columns}")
    print('-'*100)

    print("the details of first 5 students are:")  
    print(data.iloc[0:5]) 
    print('-'*100)
    null_maths=data['math'].isnull().sum()
    null_science=data['science'].isnull().sum()
    null_english=data['english'].isnull().sum()
    print('-'*100)
    print(f"{null_maths} student maths marks are not available") 
    print(f"{null_science} student science marks are not available") 
    print(f"{null_english} student english marks are not available") 
    print('-'*100)

def clean_data(data):        
    
    data['math']=data['math'].fillna(data['math'].mean())
    data['science']=data['science'].fillna(data['science'].mean())
    data['english']=data['english'].fillna(data['science'].mean())
    data=data.drop_duplicates()
    data=data.round(2)
    return data

def analyse_data(data):
    data['total']=data['math']+data['science']+data['english']
    data['average']=data['total']/3
    
    data['grade'] = 'D'  
    data.loc[data['average'] > 60, 'grade'] = 'C'
    data.loc[data['average'] > 75, 'grade'] = 'B'
    data.loc[data['average'] > 90, 'grade'] = 'A'
    data.loc[(data['math'] < 40) | (data['english'] < 40) | (data['science'] < 40), 'grade'] = 'F'
    
    data['result']='PASS'
    data.loc[data['grade']=='F','result']='FAIL'
    
    data['rank'] = data['average'].rank(method='min', ascending=False).astype(int)
    
    data['attendance_status']='GOOD'
    data.loc[data['attendance']<75,'attendance_status']='BAD'
    
    data=data.round(2)
    return data
def display_details(data):
    print('-'*100)
    top_3=data.sort_values(by='rank')
    print(F"the top 3 students are:\n{top_3.head(3)}")
    print('-'*100)
    failed_students=data.loc[data['grade']=='F']
    print(f"failed students are:\n{failed_students}")
    print('-'*100)
    average_maths=data['math'].mean()
    average_science=data['science'].mean()
    average_english=data['english'].mean()
    print(f" average maths marks={average_maths}")
    print(f"average science marks={average_science}")
    print(f"average english marks={average_english}")
    print('-'*100)
    grade_counts = data['grade'].value_counts()
    print("Grade distribution:")
    print(grade_counts)
    print('-'*100)
    mask = (data['grade'] == 'F') | (data['attendance_status'] == 'BAD')
    at_risk = data.loc[mask]
    print("At-risk students:")
    print(at_risk)
    
    data=data.round(2)
    data.to_csv("F:\\ai engineer\\python fundamentals\\student csv\\student_data_cleaned.csv", index=False)
    
def main():
    data=load_csv() 
    explore_data(data)    
    data=clean_data(data)
    data=analyse_data(data)
    data=display_details(data)
   
if __name__== "__main__" :
    main()
