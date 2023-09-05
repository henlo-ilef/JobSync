# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 17:25:59 2023

@author: henloIlef
"""

import pandas as pd

#salary parsing 
def salary_parsing(df):
    df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)

    df = df[df['Salary Estimate'] != '-1']

    salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])

    minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

    minus_ph= minus_Kd.apply(lambda x: x.replace('Per Hour',''))

    df['min_salary'] = minus_ph.apply(lambda x: float(x.split('-')[0]) if '.' in x.split('-')[0] else int(x.split('-')[0]) )

    df['max_salary'] = minus_ph.apply(lambda x: float(x.split('-')[1]) if '.' in x.split('-')[1] else int(x.split('-')[1]) )

    df['avg_salary'] = (df['min_salary']+df['max_salary'])/2
    return df
#Company name text only
def company_name_parsing(df):
    df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else str(x['Company Name'])[:-3],axis = 1)
    return df
#state field
def state_field(df):
    df['job_state'] = df['Location'].apply(lambda x: str(x).split(',')[-1])
    return df
#age of company
def company_age(df):
    df['age'] = df.Founded.apply(lambda x: x if x<1 else 2023-x)
    return df
#parsing of job description (python, etc.)
def job_description_parsing(df,skills):
    for s in skills:
        df[f'{s}_yn'] = df['Job Description'].apply(lambda x: 1 if s in str(x).lower() else 0)
        print(df[f'{s}_yn'].value_counts())
    return df


def main():
    df = pd.read_csv('glassdoor_jobs.csv')
    skills = ['git', 'python', 'aws', 'unix', 'sql', 'javascript', 'html5', 'css', 'java', 'docker', 'design', 'software', 'cloud']
    df = salary_parsing(df)
    df = company_name_parsing(df)
    df = state_field(df)
    df = company_age(df)
    df = job_description_parsing(df,skills)
    df.to_csv('ads_data_cleaned.csv',index=False)
if __name__ == '__main__':
    main()
