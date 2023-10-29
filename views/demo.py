import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtWidgets import QWidget,QTabBar,QVBoxLayout,QRadioButton,QGroupBox,QLineEdit,QInputDialog,QMessageBox,QTabWidget,QComboBox,QAction,QToolBar,QMenuBar,QTextEdit,QPushButton,QMainWindow,QHBoxLayout,QDockWidget
# from PyQt5.QtCore import *
# QHBoxLayout,QDockWidget,QMainWindow,QPushButton


class Ui_MainWindow(QMainWindow):
    def setupUI(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200,800)

        layout=QHBoxLayout()

        self.yes_butt=QPushButton("yes")

        self.dock=QDockWidget("settings")
        self.dock.setWidget(self.yes_butt)

        self.tabArea=QTabWidget()

        # self.tabArea.addTab(QWidget(),'testing')
        # tab=self.tabArea.currentWidget()
        # tab_layout=QHBoxLayout()
        # tab_layout.addWidget(QGroupBox('what'))
        # tab_layout.addWidget(QGroupBox('the'))
        # tab_layout.addWidget(QGroupBox('fuck'))
        # tab.setLayout(tab_layout)

        # gb=self.tabArea.currentWidget()
        # vbox=QVBoxLayout()
        #
        # for i in range(20):
        #     vbox.addWidget(QRadioButton("what"))
        # gb.setLayout(vbox)
        #
        # self.tabArea.addTab(QGroupBox('term2'), 'another')
        self.tabArea.setTabsClosable(True)

        self.setCentralWidget(self.tabArea)
        # self.dock.resize(600, self.height())
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock)

        # self.menuBar().addMenu("File")
        # self.setLayout(layout)

        self.toolbar=self.addToolBar("Toolbar")
        new = QAction(QIcon("../views/v.png"), '导入课程', self)
        self.toolbar.addAction(new)
        open=QAction(QIcon("../views/sina.xpm"),'open',self)
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
    def display_plan(self,plan,tab_name):
        self.tabArea.addTab(QWidget(),tab_name)
        cnt=1
        tab_layout=QHBoxLayout()
        for ele in plan:
            gb=QGroupBox('term'+str(cnt))
            gb_layout=QVBoxLayout()
            cnt+=1
            for el in ele:
                print(el)
                gb_layout.addWidget(QRadioButton(el.name))
            gb.setLayout(gb_layout)
            tab_layout.addWidget(gb)
        self.tabArea.currentWidget().setLayout(tab_layout)
        print("done")


