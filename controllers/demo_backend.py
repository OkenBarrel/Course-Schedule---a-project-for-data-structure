import os.path

from PyQt5.QtWidgets import QComboBox,QMessageBox,QLineEdit,QInputDialog,QFileDialog,QAction,QMainWindow,QApplication
from views import demo
from PyQt5.QtCore import QEvent,QSize
from utils import files,DB,files2db
# import numpy as np

db_name='test.db'

class MainWindow(demo.Ui_MainWindow,QMainWindow):
    major_list=[]


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




    def connect_sigs(self):
        # self.yes_butt.clicked.connect(self.yes_butt_clicked)
        self.toolbar.actionTriggered[QAction].connect(self.toolbar_triggered)

    def toolbar_triggered(self,a):
        print("toolbar")
        if a.text()=="导入课程":
            print("new")
            open_file=QFileDialog.getOpenFileName(self,'选择对应教学计划pdf文件','','PDFs (*.pdf)')
            if not open_file[0]:
                return

            pdf_path = open_file[0]
            splited_path = pdf_path.rsplit('/', 1)

            pdf_dir = splited_path[0]
            pdf_name = splited_path[1]
            input_ok, major_name = self.input_popup('请输入专业名称','专业：',pdf_name.split('.',1)[0])
            if not input_ok:
                return
            # There should be a pop-up window for user to input their major
            excel_name = major_name.split('.')[0] + '_prerequisites.xlsx'

            db_path = '../models/' + db_name
            db, cur = DB.connect_db(db_path)
            pdf_df = files2db.pdf2df(pdf_path)

            # putting courses into database
            files2db.df2db(pdf_df, major_name, db)

            # creating empty excel for user
            files2db.create_user_excel(pdf_df,excel_name)

            msg_title = "警告"
            msg_text = "请确认在 models文件夹 " + excel_name + "文件中已经填写了正确先修课信息"
            msg_reply=self.warning_popup(msg_title,msg_text)
            if msg_reply==QMessageBox.Close:
                print("CLOSE")
                return
            # putting prerequisites info into database
            table_name=major_name + '_prerequisites'
            files2db.pre2db(table_name, "../models/" + excel_name, db)
            if DB.check_table_empty(cur,table_name) or DB.check_table_exist(cur, table_name) is False:
                msg2_title = '警告'
                msg2_text = '导入信息为空，请正确导入先修课信息'
                self.warning_popup(msg2_title, msg2_text)
                return
            else:
                msg3_title = '提示'
                msg3_text = '先修课信息导入成功，可以开始创建教学计划啦！'
                self.info_popup(msg3_title, msg3_text)
                self.major_list.append(major_name)
            DB.close_db(db, cur)
        elif a.text()=='open':
            if len(self.major_list)==0:
                # print("zero")
                msg3_title='警告'
                msg3_text='请先导入专业课程信息'
                self.info_popup(msg3_title,msg3_text)
                return

            input_title='请选择'
            input_prompt='建立教学计划的专业：'
            input2_ok,item=self.input_popup(input_title,input_prompt,self.major_list,'item')
            # if input2_ok and item:


            print("open")
        return

    def yes_butt_clicked(self):
        print("yes!")


if __name__=='__main__':

    app=QApplication([])
    w=MainWindow()
    app.exec_()

