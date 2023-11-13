import os,sys,json
import utils
from utils import files



path="E:/Files for Work/ds proj/courseSchedule/views"
print(os.path.split(os.path.abspath(os.path.join(__file__,'..')))[0])
def func(li):
    li.append('111')

config={
    "majors":[],
    'plans':[{
        'id':1,
        'name':'what'
    },{
        'id':2,
        'name':'fuck'
    }
    ]
}
di={'what':2,'the':2,'fuck':2}
# print('what' in di)
s='012345678'
print(s[3:5])
# print(li)