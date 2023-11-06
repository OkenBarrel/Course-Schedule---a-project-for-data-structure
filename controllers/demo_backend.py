import os.path
from context import models
from PyQt5.QtWidgets import QComboBox,QCheckBox,QGroupBox,QMessageBox,QFileDialog,QAction,QMainWindow,QApplication
from views import demo
from PyQt5.QtCore import QEvent
from utils import files,DB,files2db,formatting
from models import course,lnkGraph
from .topoSort import topoSort
import json,os
# import numpy as np

db_name='test.db'

class MainWindow(demo.Ui_MainWindow,QMainWindow):
    db=None
    cur=None
    id_to_course={}
    course_to_id={}
    current_plan={}
    tabs=[]
    current_course_graph=None
    working_dir=None
    config={}

    def __init__(self):
        super(QMainWindow,self).__init__()
        self.setupUI(self)
        self.show()
        self._connect_sigs()
        self._eventFilter()
        self.working_dir = os.path.split(os.path.abspath(os.path.join(__file__, '..')))[0]
        self.create_config()
        db_path = '../models/' + db_name
        self.db, self.cur = DB.connect_db(db_path)

    def _eventFilter(self):
        self.yes_butt.installEventFilter(self)

    def get_plan_from_widget(self,widget):
        plan=[]
        for child in widget.findChildren(QGroupBox):
            temp=[]
            # print(child.title())
            for grand in child.findChildren(QCheckBox):
                temp.append((self.course_to_id[grand.text().replace('\n','')],grand.checkState()))
                # print(grand.text().replace('\n', '') + " " + str(grand.checkState()))
            plan.append(temp)
        return plan

    # TODO save_plan_to_database: NOT Done
    def eventFilter(self,watched,event):
        if watched==self.yes_butt:
            if event.type()==QEvent.MouseButtonPress and self.tabArea.isTabEnabled(self.tabArea.currentIndex()):
                print("yes!!")
                wgt=self.tabArea.currentWidget().widget()
                plan=self.get_plan_from_widget(wgt)
                tab=self.tabArea
                plan_name=tab.tabText(tab.currentIndex())
                print(plan_name)
                select_plan = self.toolbar.findChild(QComboBox)
                select_plan.addItem(plan_name)
                plan_in_config=False
                for p in self.config['plans']:
                    if p['name']==plan_name:
                        plan_in_config=True
                        break
                if not plan_in_config:
                    plan_id = self.config['global_id'] + 1
                    self.config['global_id'] += 1
                    self.config['plans'].append({
                        'id': plan_id,
                        'name': plan_name,
                        'major':self.current_plan[plan_name]
                    })
                    major_name=self.current_plan[plan_name]

                for p in self.config['plans']:
                    if p['name']==plan_name:
                        plan_id=p['id']
                        # major_name=p['major']
                if DB.plan2DB(plan,self.db,self.cur,plan_id):
                    # del self.current_plan[plan_name]
                    return True
                else:
                    return False

        return False
    # without 'return False' the app will simply freeze

    def _connect_sigs(self):
        # self.yes_butt.clicked.connect(self.yes_butt_clicked)
        self.toolbar.actionTriggered[QAction].connect(self.toolbar_triggered)
        # self.toolbar.findChild(QComboBox).currentIndexChanged.connect(self.combo_triggered)
        self.toolbar.findChild(QComboBox).activated.connect(self.combo_activated_triggered)
        self.tabArea.tabCloseRequested.connect(self.tab_close_triggered)
        self.tabArea.currentChanged.connect(self.set_major)
        # self.mng.triggered[QAction].connect(self.menu_triggered)
        # self.mng_plan.triggered[QAction].connect(self.menu_triggered)

    # def combo_triggered(self,index):
    #     print('combo '+str(index))
    def set_major(self,index):
        print('changing now!!!'+str(index))

    # TODO activated_triggered: select plan for viewing
    def combo_activated_triggered(self, index):
        combo=self.toolbar.findChild(QComboBox)
        plan_name=combo.itemText(index)
        print('activated '+str(index)+' '+plan_name)
        for p in self.config['plans']:
            if p['name']==plan_name:
                plan_id=p['id']
                major_name=p['major']
                break
        plan=DB.DB2plan(plan_id,self.db,major_name)
        self.tabs.append(plan_name)
        self.display_plan(plan,plan_name,True)
        return

    # def menu_triggered(self,q):
    #     if q.text()=='import_courses':
    #         print("导入课程")
    #         open_file = QFileDialog.getOpenFileName(self, '选择对应教学计划pdf文件', '', 'PDFs (*.pdf)')
    #         if not open_file[0]:
    #             return
    #         pdf_path = open_file[0]
    #         self.import_courses(pdf_path)
    #     elif q.text()=='delete_courses':
    #         print("删除课程")
    #     elif q.text()=='创建计划':
    #         print("creating plan")
    #         if len(self.major_list)==0:
    #             # print("zero")
    #             msg3_title='警告'
    #             msg3_text='请先导入专业课程信息'
    #             self.info_popup(msg3_title,msg3_text)
    #             return
    #         self.create_plan()
    #     elif q.text()=='删除计划':
    #         print("deleting plan")
    #
    #     return

    def toolbar_triggered(self, tool):
        print("toolbar triggered "+tool.text())
        for i in self.toolbar.findChildren(QComboBox):
            print(i)
        if tool.text()== "导入课程":
            print("importing courses")
            open_file=QFileDialog.getOpenFileName(self,'选择对应教学计划pdf文件','','PDFs (*.pdf)')
            if not open_file[0]:
                return
            pdf_path = open_file[0]
            self.import_courses(pdf_path)
        elif tool.text()== 'open':
            if len(self.config['majors'])==0:
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
        msg3_text = '导入成功！'
        self.info_popup(msg3_title, msg3_text)
        self.config['majors'].append(major_name)
        # DB.close_db(db, cur)
        return

    # TODO create_plan: maybe merge 2 pop-up window
    # FIXME create_plan: bug when create new plan that already exists
    def create_plan(self):
        input_title = '请选择'
        input_prompt = '建立教学计划的专业：'
        input2_ok, major_name = self.get_item_input(input_title, input_prompt, self.config['majors'])
        if not input2_ok or not major_name:
            return
        input3_title='请输入'
        input3_prompt='计划名称：'
        input3_ok,plan_name=self.get_text_input(input3_title,input3_prompt,'default')
        if not input3_ok:
            return
        if plan_name in self.tabs:
            num=self.tabArea.count()
            for index in range(num):
                if self.tabArea.tabText(index)==plan_name:
                    self.tabArea.setCurrentIndex(index)
                    return
        self.build_courses_graph(major_name)
        plan=topoSort(self.current_course_graph)
        combo=self.toolbar.findChild(QComboBox)
        combo.addItem(plan_name)
        # print('in creating plan:'+plan_name)
        self.current_plan[plan_name]=major_name
        self.tabs.append(plan_name)
        self.display_plan(plan,plan_name)

        # put all course into database
        # DB.plan2DB(plan,self.db,self.cur,plan_id)

    def build_courses_graph(self, major_name):
        g=lnkGraph.lnkGraph()
        cursor=self.cur.execute("select * from "+major_name)
        for row in cursor:
            # print(row)
            c=course.course(row[0],row[1],row[2],row[3],row[4],row[5])
            self.course_to_id[row[1]]=row[0]
            self.id_to_course[row[0]]=row[1]
            g.append_ver(c)
        # g.show_ver()
        cursor=self.cur.execute("select * from "+major_name+"_prerequisites")
        for row in cursor:
            preID = row[0]
            afterID = row[1]
            pre = g.find_ver_by_ID(preID)
            after = g.find_ver_by_ID(afterID)
            if pre and after:  # out degree (after course) in link
                g.graph[pre].append(after)
        self.current_course_graph=g

    def create_config(self):
        if not os.path.exists(self.working_dir+'/models/config.json'):
            self.config={
                'global_id':0,
                'majors':[],
                'plans':[]
            }
            # print(self.working_dir+'/models/config.json')
            with open(self.working_dir+'/models/config.json','w',encoding='utf-8') as config:
                json.dump(self.config,config)
        else:
            self.load_config()

    def load_config(self):
        cf=open(self.working_dir+'/models/config.json',encoding='utf-8')
        self.config=json.load(cf)
        combo=self.toolbar.findChild(QComboBox)
        plans=[]
        for p in self.config['plans']:
            plans.append(p['name'])
        combo.addItems(plans)
        cf.close()

    def closeEvent(self, event):
        print('we are closing!!!')
        self.update_config()
        DB.close_db(self.db,self.cur)
        event.accept()

    def update_config(self):
        with open(self.working_dir+'/models/config.json','w',encoding='utf-8') as config:
            json.dump(self.config,config)

    # TODO tab_close_triggered: put plan into database when closing
    def tab_close_triggered(self, index):
        self.tabArea.removeTab(index)

    # def yes_butt_clicked(self):
    #     print("yes!")


# if __name__=='__main__':
#
#     app=QApplication([])
#     w=MainWindow()
#     app.exec_()

