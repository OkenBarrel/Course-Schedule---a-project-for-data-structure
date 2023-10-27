import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtWidgets import QInputDialog,QComboBox,QAction,QToolBar,QMenuBar,QTextEdit,QPushButton,QMainWindow,QHBoxLayout,QDockWidget
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
        self.setCentralWidget(QTextEdit())
        # self.dock.resize(600, self.height())
        self.addDockWidget(Qt.LeftDockWidgetArea,self.dock)

        # self.menuBar().addMenu("File")
        # self.setLayout(layout)

        self.toolbar=self.addToolBar("管理教学计划")
        new = QAction(QIcon("../views/v.png"), '新建教学计划', self)
        self.toolbar.addAction(new)
        open=QAction(QIcon("../views/sina.xpm"),'open',self)
        self.toolbar.addAction(open)
        self.toolbar.addWidget(QComboBox())


        self.translateUI(MainWindow)


    def translateUI(self,MainWindow):
        _translate=QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow","大学生辅助教学计划编排系统"))



    def translateUI(self,name_it_window):
        _translate=QCoreApplication.translate
        name_it_window.setWindowTitle(_translate('name_it_window','输入窗口'))

