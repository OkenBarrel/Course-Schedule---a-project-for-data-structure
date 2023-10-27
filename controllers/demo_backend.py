import os.path

from PyQt5.QtWidgets import QLineEdit,QInputDialog,QFileDialog,QAction,QMainWindow,QApplication
from PyQt5.QtCore import QDir
from views import demo
from PyQt5.QtCore import QEvent
from utils import files,DB,files2db
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
                # ok,text=self.get_major_popup()
                # if ok and text:
                #     print(text)
                return True

        return False
    # without 'return False' the app will simply freeze

    def set_major_popup(self):
        inp = QInputDialog()
        # inp.setMinimumSize(800,200)
        # inp.resize(800,200
        # inp.setFixedSize(400, 200)

        text, ok = inp.getText(self, "输入专业名称", "专业", QLineEdit.Normal, "ex: computer Science")
        return ok,text
        # if ok and text:
        #     print('OKKK')
        #     print(text)


    def connect_sigs(self):
        # self.yes_butt.clicked.connect(self.yes_butt_clicked)
        self.toolbar.actionTriggered[QAction].connect(self.toolbar_triggered)

    def toolbar_triggered(self,a):
        print("toolbar")
        if a.text()=="新建教学计划":
            print("new")
            open_file=QFileDialog.getOpenFileName(self,'选择对应教学计划pdf文件','','PDFs (*.pdf)')
            ok, major_name = self.set_major_popup()
            if ok and open_file!=('',''):
                # There should be a pop-up window for user to input their major
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
    app.exec_()

