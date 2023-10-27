import os.path

from PyQt5.QtWidgets import QFileDialog,QAction,QMainWindow,QApplication

from views import demo
from PyQt5.QtCore import QEvent
from utils import files,DB,files2db,pre2db
# import numpy as np

db_name='test.db'

class MainWindow(demo.Ui_MainWindow,QMainWindow):

    def __init__(self):
        super(QMainWindow,self).__init__()
        self.setupUI(self)
        self.show()
        self.connect_sigs()
        self._eventFilter()

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
        print("toolbar")
        if a.text()=="新建教学计划":
            print("new")
            open_file=QFileDialog.getOpenFileName(self,'选择对应教学计划pdf文件','','PDFs (*.pdf)')
            if open_file!=('',''):
                pdf_path=open_file[0]
                splited_path = pdf_path.rsplit('/', 1)

                pdf_dir=splited_path[0]
                pdf_name=splited_path[1]
                excel_name = pdf_name.split('.')[0] + '_prerequisites.xlsx'

                db_path = '../models/' + db_name
                db, cur = DB.connect_db(db_path)
                pdf_df = files2db.pdf2df(pdf_path)

                files2db.df2db(pdf_df, pdf_name.split('.', 1)[0], db)
                files2db.create_user_excel(pdf_df,excel_name)
                files2db.pre2db(pdf_name.split('.', 1)[0]+'_pre',"../models/"+excel_name,db)

                DB.close_db(db, cur)
        elif a.text()=='open':
            print("open")

    def yes_butt_clicked(self):
        print("yes!")



if __name__=='__main__':

    app=QApplication([])
    w=MainWindow()
    # w.show()
    app.exec_()

