import os.path
from PyQt5.QtWidgets import QGridLayout,QWidget,QLabel,QDialog,QComboBox,QCheckBox,QGroupBox,QMessageBox,QFileDialog,QAction,QMainWindow
from views import demo
from PyQt5.QtCore import QMimeData,QEvent,pyqtSignal
from PyQt5.QtGui import QDragEnterEvent,QDrag,QMouseEvent
from utils import DB,files2db
from models import course,lnkGraph
from .topoSort import topoSort
from .DragWidget import DragWidget
import json,os,sys,copy



db_name='test.db'
if getattr(sys, 'frozen', False):
    working_dir = os.path.dirname(sys.executable)
elif __file__:
    working_dir = os.path.split(os.path.dirname(__file__))[0]


class MainWindow(demo.Ui_MainWindow,QMainWindow):
    db=None
    cur=None
    unsaved_plan={}
    current_course_graph=None
    working_major=None
    working_dir=None
    config={}
    db_path=''
    open_combo=pyqtSignal(int)

    # TODO 增加更新前置信息的tool？
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.setupUI(self)
        self.show()
        self._connect_sigs()
        self._eventFilter()
        self.create_config()
        self.db_path = working_dir+'/models/' + db_name
        print(self.db_path)
        self.db, self.cur = DB.connect_db(self.db_path)

    def _eventFilter(self):
        self.yes_butt.installEventFilter(self)

    def get_plan_from_widget(self,widget:QWidget,major_name):
        plan=[]

        for child in widget.findChildren(QGroupBox):
            temp=[]
            drag_widget=child.findChild(DragWidget)
            cnt=drag_widget.layout.count()
            for w in range(cnt):
                wgt=drag_widget.layout.itemAt(w).widget()
                wgt_layout=wgt.layout()
                check=wgt_layout.itemAt(0).widget()
                credit_label = wgt_layout.itemAt(1).widget()
                name_label=wgt_layout.itemAt(2).widget()
                name=name_label.text().replace('\n','')
                id = DB.get_courseID(name, self.cur, major_name)
                temp.append((id,check.checkState()))
            # layout = child.layout().itemAt(1)
            # row = layout.rowCount()
            # for r in range(row):
            #     check = layout.itemAtPosition(r, 0)
            #     name_label = layout.itemAtPosition(r,2).widget()
            #     print(type(name_label))
            #     name=name_label.text().replace('\n','')
            #     id = DB.get_courseID(name, self.cur, major_name)
            #     temp.append((id,check.widget().checkState()))
            # for grand in child.findChildren(QCheckBox):
            #     name=grand.text().replace('\n','')
            #     print(name)
            #     id=DB.get_courseID(name.split(' ')[1],self.cur,major_name)
            #     temp.append((id,grand.checkState()))
            plan.append(temp)
        return plan

    def eventFilter(self,watched,event):
        if watched==self.yes_butt:
            if event.type()==QEvent.MouseButtonPress and self.tabArea.isTabEnabled(self.tabArea.currentIndex()):
                print("yes!!")
                wgt=self.tabArea.currentWidget().widget()
                tab=self.tabArea
                plan_name=tab.tabText(tab.currentIndex())
                print(plan_name)
                combo = self.toolbar.findChild(QComboBox)
                print('guess if im in'+str(combo.findText(plan_name)))
                if combo.findText(plan_name)==-1:
                    combo.addItem(plan_name)
                plans_in_config=[p['name'] for p in self.config['plans']]
                if plan_name not in plans_in_config:
                    plan_id = self.config['global_id'] + 1
                    self.config['global_id'] += 1
                    self.config['plans'].append({
                        'id': plan_id,
                        'name': plan_name,
                        'major':self.unsaved_plan[plan_name]
                    })
                    major_name=self.unsaved_plan[plan_name]

                for p in self.config['plans']:
                    if p['name']==plan_name:
                        plan_id=p['id']
                        major_name=p['major']
                plan = self.get_plan_from_widget(wgt,major_name)
                if DB.plan2DB(plan,self.db,self.cur,plan_id):
                    print(self.unsaved_plan)
                    # del self.unsaved_plan[plan_name]
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
        self.open_combo.connect(self.combo_activated_triggered)
        self.tabArea.tabCloseRequested.connect(self.tab_close_triggered)
        self.tabArea.currentChanged.connect(self.tab_changing)

        # self.mng.triggered[QAction].connect(self.menu_triggered)
        # self.mng_plan.triggered[QAction].connect(self.menu_triggered)

    # def combo_triggered(self,index):
    #     print('combo '+str(index))
    def tab_changing(self,index):
        print('changing now!!!'+str(index))
        if len(self.config['majors'])<=1:
            return
        for p in self.config['plans']:
            if self.tabArea.tabText(index)==p['name'] and self.working_major!=p['major']:
                self.current_course_graph=self.build_courses_graph(p['major'])
                self.working_major=p['major']
                return

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
        self.current_course_graph=self.build_courses_graph(major_name)
        self.display_plan(plan,plan_name,True)
        return

    def check_change(self,course_name,term,credit,state):
        print(course_name + ' at ' + str(term) + ' is now ' + str(state))
        self.tabArea.currentIndex()
        wgt=self.tabArea.currentWidget().widget()
        print(type(wgt))
        for gb in wgt.findChildren(QGroupBox):
            if gb.title()=='term'+str(term):
                show_credit=gb.findChild(QLabel)
                cre = float(show_credit.text()[5:])
                if state:
                    cre+=float(credit)
                else:
                    cre-=float(credit)
                show_credit.setText('已选学分 '+str(cre))
                print(cre)

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
        elif tool.text()=='delete plan':
            new=Pop_up('testing',[p['name'] for p in self.config['plans']])
            new.results.connect(self.delete_plan)
            res=new.exec_()
            print(res)
        return

    def delete_plan(self,results):
        combo = self.toolbar.findChild(QComboBox)
        copied=copy.deepcopy(self.config)
        sql='delete from plans where plan_id='
        for p in copied['plans']:
            # print(p)
            if p['name'] in results:
                self.cur.execute(sql+str(p['id']))
                self.db.commit()
                print('removing '+p['name'])
                combo.removeItem(combo.findText(p['name']))
                self.config['plans'].remove(p)
        return

    def drop(self,target_term,sig):
        '''
        if sig['credit']==0 it means that changed course is not chosen
        '''
        print(str(sig['credit'])+' '+sig['name']+ 'from term' + sig['source_term']+' to term'+str(target_term))
        from_index=int(sig['source_term'])-1
        to_index=target_term-1
        course_name=sig['name']
        wgt = self.tabArea.currentWidget().widget()
        from_gb=wgt.layout().itemAt(from_index).widget()
        to_gb=wgt.layout().itemAt(to_index).widget()
        course_node_num=self.current_course_graph.find_ver_num_by_name(course_name)
        if self.current_course_graph.indegree[course_node_num]!=0:
            print("topo again")
            wgt = self.tabArea.currentWidget().widget()
            plan=self.get_plan_from_widget(wgt,self.working_major)
            afters_num=[course_node_num]
            afters_num+=self.current_course_graph.find_all_after(course_node_num)
            afters_id=[self.current_course_graph.graph[n].head.ele.courseID for n in afters_num]


            # n=lnkGraph.lnkGraph()
            # afters=[course_node_num]
            # checkout=[]
            # afters+=self.current_course_graph.find_all_after(course_node_num)
            # for num in afters:
            #     n.append_ver(self.current_course_graph.graph[num].head.ele)
            # cursor = self.cur.execute('select * from 计算机_prerequisites;')
            # for row in cursor:
            #     courseID = row[0]
            #     preID = row[1]
            #     # print(row[0]+" "+row[1])
            #     after_index = n.find_ver_by_ID(courseID)
            #     pre_index = n.find_ver_by_ID(preID)
            #     if pre_index!=-1 and after_index!=-1:  # out degree (pre_index course) in link
            #         # g.graph[pre_index].append(after_index)
            #         if courseID not in checkout:
            #             checkout.append(checkout)
            #         if preID not in checkout:
            #             checkout.append(preID)
            #         n.add_edge(pre_index, after_index)
            # n.show_ver()
            # rest_graph=self.build_courses_graph(self.working_major,checkout)
            # plan=topoSort(n)
            # final_plan=topoSort(rest_graph,plan)

            return
        if sig['credit']!=0:
            from_credit_label=from_gb.layout().itemAt(0).widget()
            to_credit_label=to_gb.layout().itemAt(0).widget()
            print(from_credit_label.text()[5:])
            print(to_credit_label.text()[5:])
            from_credit=float(from_credit_label.text()[5:])-sig['credit']
            to_credit=float(to_credit_label.text()[5:])+sig['credit']
            from_credit_label.setText('已选学分 '+str(from_credit))
            to_credit_label.setText('已选学分 '+str(to_credit))

        # wgt.layout().item

    def import_courses(self,pdf_path):

        # pdf_dir = pdf_path.rsplit('/', 1)[0]
        pdf_name = pdf_path.rsplit('/', 1)[1]
        input_ok, major_name = self.get_text_input('请输入专业名称', '专业：', pdf_name.split('.', 1)[0])
        if not input_ok or not major_name:
            return
        excel_name = major_name.split('.')[0] + '_prerequisites.xlsx'
        excel_path=working_dir+'/models/'+major_name.split('.')[0] + '_prerequisites.xlsx'

        pdf_df = files2db.pdf2df(pdf_path)

        # putting courses into database
        files2db.df2db(pdf_df, major_name, self.db)

        # creating empty excel for user
        files2db.create_user_excel(pdf_df, excel_path)

        msg_title = "警告"
        msg_text = "请确认在 models文件夹 " + excel_name + "文件中已经填写了正确先修课信息"
        msg_reply = self.warning_popup(msg_title, msg_text)

        if msg_reply == QMessageBox.Close:
            print("CLOSE")
            return
        # putting prerequisites info into database
        table_name = major_name + '_prerequisites'
        files2db.pre2db(table_name, working_dir+"/models/" + excel_name, self.db)
        if DB.check_table_empty(self.cur, table_name) or DB.check_table_exist(self.cur, table_name) is False:
            msg2_title = '警告'
            msg2_text = '导入信息为空，请正确导入先修课信息'
            self.info_popup(msg2_title, msg2_text)
            return
        msg3_title = '提示'
        msg3_text = '导入成功！'
        self.info_popup(msg3_title, msg3_text)
        if major_name not in self.config['majors']:
            self.config['majors'].append(major_name)
        # DB.close_db(db, cur)
        return

    # TODO create_plan: maybe merge 2 pop-up window
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
        tab_num = self.tabArea.count()
        combo=self.toolbar.findChild(QComboBox)

        opened_tabs=[self.tabArea.tabText(tab_index) for tab_index in range(tab_num)]

        if plan_name in opened_tabs:
            for index in range(tab_num):
                if self.tabArea.tabText(index)==plan_name:
                    self.tabArea.setCurrentIndex(index)
                    return
        combo_index=combo.findText(plan_name)
        if combo_index!=-1:
            self.open_combo.emit(combo_index)
            return
        self.current_course_graph=self.build_courses_graph(major_name)
        plan=topoSort(self.current_course_graph)
        self.unsaved_plan[plan_name]=major_name
        self.display_plan(plan,plan_name)

    def build_courses_graph(self, major_name,checkout=[]):
        g=lnkGraph.lnkGraph()
        cursor = self.cur.execute('''select * from 计算机 as c
                                        where not exists (select p.courseID from  计算机_prerequisites as p 
                                        where c.courseId=p.courseID 
                                        group by p.courseID);''')
        for row in cursor:
            # print(row)
            if row[0] in checkout:
                continue
            c = course.course(row[0], row[1], row[2], row[3], row[4], row[5])
            g.append_ver(c)
        cursor = self.cur.execute('''select p.courseID,count(*) as num,c.name,c.final,c.credit,c.department,c.compulsory 
                                    from 计算机_prerequisites as p,计算机 as c 
                                    where c.courseId=p.courseID 
                                    group by p.courseID 
                                    order by num;''')
        # print('again!!!')
        for row2 in cursor:
            # print(row2)
            if row2[0] in checkout:
                continue
            c = course.course(row2[0], row2[2], row2[3], row2[4], row2[5], row2[6])
            g.append_ver(c)
        # g.show_ver()
        cursor = self.cur.execute('select * from 计算机_prerequisites;')
        for row in cursor:
            courseID = row[0]
            preID = row[1]
            # print(row[0]+" "+row[1])
            after_index = g.find_ver_by_ID(courseID)
            pre_index = g.find_ver_by_ID(preID)

            if pre_index!=-1 and after_index!=-1:  # out degree (pre_index course) in link
                # g.graph[pre_index].append(after_index)
                g.add_edge(pre_index, after_index)
        return g

    def create_config(self):
        if not os.path.exists(working_dir+'/models/config.json'):
            self.config={
                'global_id':0,
                'majors':[],
                'plans':[]
            }
            with open(working_dir+'/models/config.json','w',encoding='utf-8') as config:
                json.dump(self.config,config)
        else:
            self.load_config()

    def load_config(self):
        cf=open(working_dir+'/models/config.json',encoding='utf-8')
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
        with open(working_dir+'/models/config.json','w',encoding='utf-8') as config:
            json.dump(self.config,config)

    # TODO tab_close_triggered: put plan into database when closing
    def tab_close_triggered(self, index):
        self.tabArea.removeTab(index)

    # def yes_butt_clicked(self):
    #     print("yes!")


class Pop_up(demo.Ui_popup,QDialog):
    results=pyqtSignal(dict)
    def __init__(self,title,option):
        super(QDialog,self).__init__()
        self.setUI(self,title,option)
        # self.show()
        self._connect()

    def _connect(self):
        self.yes.clicked.connect(self.yes_btn)
        # self.results.connect(self.yes_btn)

    def yes_btn(self):
        print('yes')
        deleted_plan={}
        for check in self.group.findChildren(QCheckBox):
            if check.checkState():
                deleted_plan[check.text()]=check.checkState()
        print(deleted_plan)
        self.results.emit(deleted_plan)
        self.accept()


