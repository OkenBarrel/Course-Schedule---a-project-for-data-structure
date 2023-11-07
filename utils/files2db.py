# from PyPDF2 import PdfReader
import pdfplumber
import pandas as pd
# from .files import check_dir
import os


# def format_change(x):
#     return f'{x:05d}'
def pdf2df(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        for p in range(2):
            # print(p)
            page=pdf.pages[p]
            table=page.extract_table()
            del table[1:3]
            for e in table:
                del e[4:24]

            ta2=table[:]
            length=len(table)

            for e in range(1,length):
                try:
                    int(table[e][0])
                except (ValueError, TypeError):
                    ta2.remove(table[e])
            if p!=0:
                ta2[0]=['courseID','name','final','credit','department']
                # print(ta2)
                df2=pd.DataFrame(ta2[1:],columns=ta2[0])
                df2.insert(df2.shape[1],"compulsory",0)
            else:
                df=pd.DataFrame(ta2[1:],columns=ta2[0])

            if p!=0:
                df=pd.concat([df,df2])
            else:
                df.columns=df.columns.str.replace("\n","")
                df.rename(columns={"课程编码":"courseID","课程名称":"name","学分":"credit","开课单位":"department","考试":"final"},inplace=True)
                df.insert(df.shape[1],"compulsory",1)

            for column in ["name","department"]:
                df[column]=df[column].str.replace("\n","")
        s=len(df)
        for e in range(s-3,s):
            df.iloc[e,5]=1
            # df.to_sql()
        df.reset_index(drop=True, inplace=True)
        return df


def df2db(df,table_name,con):
    df.to_sql(name=table_name,con=con,if_exists='replace',index=False)


def create_user_excel(df,excel_name):

    df_user=pd.DataFrame()

    df_user['courseID']=str(df['courseID'])
    df_user['name'] = df['name']
    df_user['pre']=None
    # print(df_user)
    if os.path.exists("../models/"+excel_name) is False:
    # if check_dir("../models",excel_name) is False:
        df_user.to_excel("../models/"+excel_name,index=False)
    else:
        print('prerequisites already exist')

def handin2list(df1):
    for col in ['pre']:
        df1[col] = df1[col].str.split(",")
    print(df1.columns)


def pre2db(pre_table_name, pre_path, db):
    df1 = pd.read_excel(pre_path, index_col=False,dtype=str)
    # print(df1)

    handin2list(df1)

    filter_df1 = df1[df1['pre'].notna()]

    pre = pd.DataFrame()
    pre['courseID'] = []
    pre['pre'] = []

    df1['pre'] = df1['pre'].apply(lambda x: x if isinstance(x, list) else [x])

    for _, i in filter_df1.iterrows():
        li = i['pre']
        for e in li:
            pre.loc[len(pre.index)] = [i['courseID'], e]

    df2db(pre, pre_table_name, db)

