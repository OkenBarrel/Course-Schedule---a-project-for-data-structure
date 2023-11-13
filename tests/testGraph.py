import unittest
from context import utils
from context import models

from utils import DB

class testGraph(unittest.TestCase):
    def test_building_cs_courses_graph_from_DB(self):
        l=[]
        g = models.lnkGraph.lnkGraph()

        db, cur = utils.DB.connect_db("../models/coursesInfo.db")
        cursor = cur.execute("select * from courses")
        for row in cursor:
            # print("num: {} name:{}".format(row[0],row[1]))
            # print(row)
            c = models.course.course(row[1], row[2], row[3], row[4], row[5], row[6])
            # print(c)
            l.append(c)
            g.append_ver(c)

        cursor = cur.execute("select * from prerequisites")

        for row in cursor:
            preID = row[0]
            afterID = row[1]
            # print(row[0]+" "+row[1])
            pre = g.find_ver_by_ID(preID)
            after = g.find_ver_by_ID(afterID)
            if pre and after:  # out degree (after course) in link
                g.graph[pre].append(after)

        g.show_ver()