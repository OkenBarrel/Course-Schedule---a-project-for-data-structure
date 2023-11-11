import os,sys
from PyQt5.QtGui import QIcon,QFontMetricsF
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtWidgets import QLabel,QScrollArea,QCheckBox,QWidget,QVBoxLayout,QRadioButton,QGroupBox,QLineEdit,QInputDialog,QMessageBox,QTabWidget,QComboBox,QAction,QToolBar,QMenuBar,QTextEdit,QPushButton,QMainWindow,QHBoxLayout,QDockWidget
from utils import formatting

if getattr(sys, 'frozen', False):
    working_dir = os.path.dirname(sys.executable)
elif __file__:
    working_dir = os.path.split(os.path.dirname(__file__))[0]

# TODO views: change the color scheme
class Ui_MainWindow(QMainWindow):
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
        # dock_layout.addWidget(self.major_lable)
        # self.dock.setWidget(self.yes_butt)
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
    def display_plan(self,plan,tab_name,chosen=False):
        new_tab=QScrollArea()
        self.tabArea.addTab(new_tab,tab_name)
        self.tabArea.setCurrentWidget(new_tab)
        wgt=QWidget()
        cnt=1
        wgt_layout=QHBoxLayout()
        for ele in plan:
            gb=QGroupBox('term'+str(cnt))
            gb_layout=QVBoxLayout()
            cnt+=1
            gb.setFixedSize(220, 680)
            for el in ele:
                check=QCheckBox()
                if chosen:
                    wrapped_word=formatting.word_wrap(el[0].name,gb.size().width(),QFontMetricsF(check.font()).width("新"))
                else:
                    wrapped_word=formatting.word_wrap(el.name,gb.size().width(),QFontMetricsF(check.font()).width("新"))
                check.setText(wrapped_word)
                if chosen:
                    if el[0].compulsory:
                        check.setStyleSheet('''QCheckBox{color:red;}''')
                    if el[1]:
                        check.setChecked(True)
                else:
                    if el.compulsory:
                        check.setStyleSheet('''QCheckBox{color:red;}''')
                        check.setChecked(True)
                gb_layout.addWidget(check)
            gb.setLayout(gb_layout)
            wgt_layout.addWidget(gb)

        wgt.setLayout(wgt_layout)

        self.tabArea.currentWidget().setWidget(wgt)
        print("done")


