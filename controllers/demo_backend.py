import os.path
from context import models
from PyQt5.QtWidgets import QMessageBox,QFileDialog,QAction,QMainWindow,QApplication
from views import demo
from PyQt5.QtCore import QEvent
from utils import files,DB,files2db
from models import course,lnkGraph
from .topoSort import topoSort
# import numpy as np

db_name='test.db'

class MainWindow(demo.Ui_MainWindow,QMainWindow):
    major_list=[]
    plan_list=[]
    db=None
    cur=None
    current_course_graph=None

    def __init__(self):
        super(QMainWindow,self).__init__()
        self.setupUI(self)
        self.show()
        self.connect_sigs()
        self._eventFilter()
        db_path = '../models/' + db_name
        self.db, self.cur = DB.connect_db(db_path)

    def _eventFilter(self):
        self.yes_butt.installEventFilter(self)

    def eventFilter(self,watched,event):
        if watched==self.yes_butt:
            if event.type()==QEvent.MouseButtonPress:
                print("yes!!")
                return True

        return False
    # without 'return False' the app will simply freeze

    def connect_sigs(self):
        # self.yes_butt.clicked.connect(self.yes_butt_clicked)
        self.toolbar.actionTriggered[QAction].connect(self.toolbar_triggered)

    def toolbar_triggered(self,a):
        print("toolbar triggered")
        if a.text()=="导入课程":
            print("importing courses")
            open_file=QFileDialog.getOpenFileName(self,'选择对应教学计划pdf文件','','PDFs (*.pdf)')
            if not open_file[0]:
                return
            pdf_path = open_file[0]
            self.import_courses(pdf_path)
        elif a.text()=='open':
            if len(self.major_list)==0:
                # print("zero")
                msg3_title='警告'
                msg3_text='请先导入专业课程信息'
                self.info_popup(msg3_title,msg3_text)
                return
            print("open")
            self.create_plan()
        return

    def import_courses(self,pdf_path):

        pdf_dir = pdf_path.rsplit('/', 1)[0]
        pdf_name = pdf_path.rsplit('/', 1)[1]
        input_ok, major_name = self.get_text_input('请输入专业名称', '专业：', pdf_name.split('.', 1)[0])
        if not input_ok or not major_name:
            return
        excel_name = major_name.split('.')[0] + '_prerequisites.xlsx'

        pdf_df = files2db.pdf2df(pdf_path)

        # putting courses into database
        files2db.df2db(pdf_df, major_name, self.db)

        # creating empty excel for user
        files2db.create_user_excel(pdf_df, excel_name)

        msg_title = "警告"
        msg_text = "请确认在 models文件夹 " + excel_name + "文件中已经填写了正确先修课信息"
        msg_reply = self.warning_popup(msg_title, msg_text)

        if msg_reply == QMessageBox.Close:
            print("CLOSE")
            return
        # putting prerequisites info into database
        table_name = major_name + '_prerequisites'
        files2db.pre2db(table_name, "../models/" + excel_name, self.db)
        if DB.check_table_empty(self.cur, table_name) or DB.check_table_exist(self.cur, table_name) is False:
            msg2_title = '警告'
            msg2_text = '导入信息为空，请正确导入先修课信息'
            self.info_popup(msg2_title, msg2_text)
            return
        msg3_title = '提示'
        msg3_text = '导入成功，\n可以开始创建教学计划啦！'
        self.info_popup(msg3_title, msg3_text)
        self.major_list.append(major_name)
        # DB.close_db(db, cur)
        return

    # TODO create_plan: merge 2 pop-up window
    def create_plan(self):
        input_title = '请选择'
        input_prompt = '建立教学计划的专业：'
        input2_ok, item = self.get_item_input(input_title, input_prompt, self.major_list)
        if not input2_ok or not item:
            return
        input3_title='请输入'
        input3_prompt='计划名称：'
        input3_ok,plan_name=self.get_text_input(input3_title,input3_prompt,'default')
        if not input3_ok:
            return
        self.build_courses_graph(item)
        res=topoSort(self.current_course_graph)
        # self.current_course_graph.show_ver()
        self.display_plan(res,plan_name)



    def build_courses_graph(self, major_name):
        g=lnkGraph.lnkGraph()
        cursor=self.cur.execute("select * from "+major_name)
        for row in cursor:
            # print(row)
            c=course.course(row[0],row[1],row[2],row[3],row[4],row[5])
            g.append_ver(c)
        # g.show_ver()
        cursor=self.cur.execute("select * from "+major_name+"_prerequisites")
        for row in cursor:
            preID = row[0]
            afterID = row[1]
            # print(row[0]+" "+row[1])
            pre = g.find_ver_by_ID(preID)
            after = g.find_ver_by_ID(afterID)
            if pre and after:  # out degree (after course) in link
                g.graph[pre].append(after)
            # print(row)
        # g.show_ver()
        self.current_course_graph=g

    def yes_butt_clicked(self):
        print("yes!")


# if __name__=='__main__':
#
#     app=QApplication([])
#     w=MainWindow()
#     app.exec_()

