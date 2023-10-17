import pandas as pd


def handin2list(df1):
    for col in ['pre']:
        df1[col]=df1[col].str.split(",")
    print(df1.columns)

if __name__=="__main__":
    df1 = pd.read_csv('final.csv',index_col=False)

    handin2list(df1)

    filter_df1=df1[df1['pre'].notna()]
    df1['courseID']=df1['courseID'].apply(lambda x: f'{x:05d}')

    pre=pd.DataFrame()
    pre['pre']=[]
    pre['after']=[]
    df1['pre'] = df1['pre'].apply(lambda x: x if isinstance(x, list) else [x])
    
    print(df1)

    for _, i in filter_df1.iterrows():
        li=i['pre']
        print(li)
        for e in li:
            print(i['courseID'],e)
            pre.loc[len(pre.index)]=[i['courseID'],e]
            
    print(pre)
    pre.to_csv('prerequisites.csv')