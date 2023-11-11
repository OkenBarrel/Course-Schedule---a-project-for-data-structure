import os,sys,json
import utils
from utils import files



path="E:/Files for Work/ds proj/courseSchedule/views"
print(os.path.split(os.path.abspath(os.path.join(__file__,'..')))[0])

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
li=[p['name'] for p in config['plans']]
print(li+['fuck'])