import pandas as pd
from .pdf2db import df2db


def handin2list(df1):
    for col in ['pre']:
        df1[col]=df1[col].str.split(",")
    print(df1.columns)

def pre2db(pre_table_name,pre_path,db):
    df1 = pd.read_excel(pre_path,index_col=False)
    # print(df1)

    handin2list(df1)

    filter_df1=df1[df1['pre'].notna()]
    df1['courseID']=df1['courseID'].apply(lambda x: f'{x:05d}')

    pre=pd.DataFrame()
    pre['courseID']=[]
    pre['pre']=[]

    df1['pre'] = df1['pre'].apply(lambda x: x if isinstance(x, list) else [x])
    
    # print(df1)

    for _, i in filter_df1.iterrows():
        li=i['pre']
        # print(li)
        for e in li:
            # print(i['courseID'],e)
            pre.loc[len(pre.index)]=[i['courseID'],e]
            
    # print(pre)
    df2db(pre,pre_table_name,db)

