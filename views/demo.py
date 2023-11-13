import os,sys
from PyQt5.QtGui import QIcon,QFontMetricsF
from PyQt5.QtCore import pyqtSignal,Qt,QCoreApplication
from PyQt5.QtWidgets import QGridLayout,QSizePolicy,QFrame,QLabel,QDialog,QScrollArea,QCheckBox,QWidget,QVBoxLayout,QGroupBox,QLineEdit,QInputDialog,QMessageBox,QTabWidget,QComboBox,QAction,QPushButton,QMainWindow,QHBoxLayout,QDockWidget
from utils import formatting
from functools import partial

if getattr(sys, 'frozen', False):
    working_dir = os.path.dirname(sys.executable)
elif __file__:
    working_dir = os.path.split(os.path.dirname(__file__))[0]


# TODO views: change the color scheme
class Ui_MainWindow(QMainWindow):
    checkbox_state_change=pyqtSignal(dict)
    def setupUI(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200,800)
        # MainWindow.setFixedSize(1200,800)

        self.yes_butt=QPushButton("yes")
        self.no_butt = QPushButton("no")
        # self.major_lable=QLabel('none yet')

        self.dock=QDockWidget("settings")
        wgt=QWidget()
        dock_layout=QVBoxLayout()
        dock_layout.addWidget(self.yes_butt)
        dock_layout.addWidget(self.no_butt)
        wgt.setStyleSheet("""
            .QWidget {background:#545d64;}    
        """)
        wgt.setLayout(dock_layout)
        self.dock.setWidget(wgt)

        self.tabArea=QTabWidget()
        print('tabArea h = '+str(self.tabArea.size().height())+'  w = '+str(self.tabArea.size().width()))

        self.tabArea.setTabsClosable(True)

        self.setCentralWidget(self.tabArea)
        # self.dock.resize(600, self.height())
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock)

        self.toolbar=self.addToolBar("Toolbar")
        print('working dir in views: '+working_dir)
        new = QAction(QIcon(working_dir+"/views/v.png"), '导入课程', self)
        self.toolbar.addAction(new)
        open=QAction(QIcon(working_dir+"/views/sina.xpm"),'open',self)
        self.toolbar.addAction(open)
        delete_plan=QAction('delete plan',self)
        self.toolbar.addAction(delete_plan)
        self.toolbar.addWidget(QComboBox())

        self.translateUI(MainWindow)

    def translateUI(self,MainWindow):
        _translate=QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow","大学生辅助教学计划编排系统"))

    def msg_popup(self,title,text,type):
        msg = QMessageBox()
        if type=='warning':
            reply = msg.warning(self, title, text, QMessageBox.Yes | QMessageBox.Close, QMessageBox.Yes)
        elif type=='information':
            # no need to confirm anything, just simply providing information
            reply=msg.information(self, title, text)
        elif type=='question':
            reply = msg.question(title, text, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        return reply

    def warning_popup(self,title,text):
        return self.msg_popup(title,text,'warning')

    def info_popup(self,title,text):
        return self.msg_popup(title,text,'information')

    def question_popup(self,title,text):
        return self.msg_popup(title,text,'question')

    def input_popup(self, title, prompt, default, type):
        inp = QInputDialog()
        if type== 'item':
            res,ok=inp.getItem(self,title,prompt,default,0,False)
            if ok and res:
                print(res)
        elif type=='text':
            res, ok = inp.getText(self, title, prompt, QLineEdit.Normal, default)
        return ok,res

    def get_text_input(self,title,prompt,default):
        return self.input_popup(title,prompt,default,'text')

    def get_item_input(self,title,prompt,item_list):
        return self.input_popup(title,prompt,item_list,'item')

    # TODO display_plan: compulsory courses should be in better style
    def display_plan(self,plan:list,tab_name:str,chosen=False):
        new_tab=QScrollArea()
        self.tabArea.addTab(new_tab,tab_name)
        self.tabArea.setCurrentWidget(new_tab)
        wgt=QWidget()
        cnt_term=1
        wgt_layout=QHBoxLayout()
        for ele in plan:
            gb=QGroupBox('term'+str(cnt_term))
            gb_layout=QVBoxLayout()
            gb_layout=QGridLayout()
            # show_credit=QGroupBox('已选学分')
            show_credit=QLabel()
            show_credit.setFrameStyle(QFrame.Panel|QFrame.Sunken)
            show_credit.setFixedHeight(30)
            # show_credit.setGeometry(0,0,show_credit.size().width(),show_credit.size().height())
            gb_layout.addWidget(show_credit)
            # gb_layout.setStretchFactor(show_credit,1)
            cnt_term+=1
            credits=0
            gb.setFixedSize(220, 680)
            # show_credit.setFixedSize(220,50)
            for el in ele:
                check=QCheckBox(parent=gb)
                if chosen:
                    course = el[0]
                    wrapped_word=formatting.word_wrap(course.credit+' '+course.name,gb.size().width(),QFontMetricsF(check.font()).width("新"))
                else:
                    if el.name=='高级语言程序设计':
                        print('what')
                    wrapped_word=formatting.word_wrap(el.credit+' '+el.name,gb.size().width(),QFontMetricsF(check.font()).width("新"))
                check.setText(wrapped_word)
                if chosen:
                    is_chosen=el[1]
                    if course.compulsory:
                        check.setStyleSheet('''QCheckBox{color:red;}''')
                        check.setEnabled(False)
                    if is_chosen:
                        check.setChecked(True)
                        credits+=float(course.credit)
                else:
                    if el.compulsory:
                        check.setStyleSheet('''QCheckBox{color:red;}''')
                        check.setChecked(True)
                        check.setEnabled(False)
                        credits+=float(el.credit)
                # check.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
                check.stateChanged.connect(partial(self.check_change,check.text().replace('\n',''),cnt_term-1))
                gb_layout.addWidget(check)
                # print(check.geometry().width())
                # gb_layout.setSpacing(0)
                # print(gb_layout.spacing())
                # gb_layout.setStretchFactor(check,10)
            show_credit.setText('已选学分 '+str(credits))
            # gb_layout.setSpacing(-50)
            gb.setLayout(gb_layout)
            wgt_layout.addWidget(gb)
        wgt.setLayout(wgt_layout)
        self.tabArea.currentWidget().setWidget(wgt)
        print("done")
        return

    def check_change(self,course_name,term,state):
        pass


class Ui_popup(QDialog):
    def setUI(self,popup,title,option):
        popup.setObjectName("pop_up")
        # QDialog().setWindowTitle()
        popup.setWindowTitle(title)
        popup.resize(400,500)
        self.group=QGroupBox('请选择')
        layout=QVBoxLayout()
        self.yes=QPushButton('yes')
        layout.addWidget(self.group)
        layout.addWidget(self.yes)
        popup.setLayout(layout)
        self.display_choice(option)

    def display_choice(self,option):
        gb_layout=QVBoxLayout()
        for e in option:
            c=QCheckBox(str(e))
            gb_layout.addWidget(c)

            if gb_layout.setStretchFactor(c,0):
                print('set 0 stretch: '+c.text())
        self.group.setLayout(gb_layout)
