# from PyPDF2 import PdfReader
import pdfplumber
import pandas as pd


def format_change(x):
    return f'{x:05d}'
def pdf2df(pdf):
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

    df.reset_index(drop=True, inplace=True)
    return df
def pdf2db(path):
    with pdfplumber.open(path) as pdf:

        df=pdf2df(pdf)

        # print(df)
        df_user=pd.DataFrame()
        df_user['courseID']=df['courseID']
        df_user['name'] = df['name']
        print(df_user)
        df_user.to_csv("prerequisites.csv",encoding="utf_8_sig")
        dff=pd.read_csv("prerequisites.csv",encoding="utf-8")
        print(dff)
        # df.to_excel(excel_writer='courses.xlsx',sheet_name='courses')