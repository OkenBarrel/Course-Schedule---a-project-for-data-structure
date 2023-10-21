import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QCoreApplication
from PyQt5.QtWidgets import QAction,QToolBar,QMenuBar,QTextEdit,QPushButton,QMainWindow,QHBoxLayout,QDockWidget
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

        toolbar=self.addToolBar("管理教学计划")
        new = QAction(QIcon('views\\tb.png'), '管理教学计划', self)
        toolbar.addAction(new)

        self.translateUI(MainWindow)


    def translateUI(self,MainWindow):
        _translate=QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow","大学生辅助教学计划编排系统"))

