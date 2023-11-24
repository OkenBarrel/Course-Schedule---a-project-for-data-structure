import os,sys
from PyQt5.QtGui import QIcon,QFontMetricsF
from PyQt5.QtCore import pyqtSignal,Qt,QCoreApplication
from PyQt5.QtWidgets import QFormLayout,QFrame,QLabel,QDialog,QScrollArea,QCheckBox,QWidget,QVBoxLayout,\
                            QGroupBox,QLineEdit,QInputDialog,QMessageBox,QTabWidget,QComboBox,QAction,QPushButton,\
                            QMainWindow,QHBoxLayout,QDockWidget
from utils import formatting
from functools import partial
from controllers.DragWidget import DragWidget
# from controllers.demo_backend import DragWidget


if getattr(sys, 'frozen', False):
    working_dir = os.path.dirname(sys.executable)
elif __file__:
    working_dir = os.path.split(os.path.dirname(__file__))[0]


# TODO views: change the color scheme
class Ui_MainWindow(QMainWindow):
    checkbox_state_change=pyqtSignal(dict)
    drag_drop=pyqtSignal(int)
    def setupUI(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200,800)
        # MainWindow.setFixedSize(1200,800)

        self.yes_butt=QPushButton("保存计划")
        self.credit_limit=QLineEdit()
        self.credit_limit.setFixedWidth(120)
        self.credit_limit.setPlaceholderText('default: 17.5')
        self.no_butt = QPushButton("再次排序")

        self.dock=QDockWidget("settings")
        form=QFormLayout()
        # TODO !!
        form.addRow("学期最大\n修读学分",self.credit_limit)
        wgt=QWidget()
        dock_layout=QVBoxLayout()
        dock_layout.addWidget(self.yes_butt)
        dock_layout.addWidget(self.no_butt)
        dock_layout.addLayout(form)

        wgt.setStyleSheet("""
            .QWidget {background:#545d64;}
            .QPushButton {background:#545d64;}
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
    def display_plan(self,plan:list,tab_name:str,chosen=False,repaint=False,chosen_list=[]):
        if not repaint:
            new_tab=QScrollArea()
            self.tabArea.addTab(new_tab,tab_name)
            self.tabArea.setCurrentWidget(new_tab)
        wgt=QWidget()
        cnt_term=1
        wgt_layout=QHBoxLayout()
        for ele in plan:
            gb=QGroupBox('term'+str(cnt_term),parent=wgt)
            gb_layout_out=QVBoxLayout()
            drag_widget=DragWidget()
            drag_widget.setFixedSize(240,630)
            show_credit=QLabel()
            show_credit.setFrameStyle(QFrame.Panel|QFrame.Sunken)
            show_credit.setFixedHeight(30)

            gb_layout_out.addWidget(show_credit)
            cnt_term+=1
            credits=0
            gb.setFixedSize(240, 680)
            for cnt_course,el in enumerate(ele):
                inner_wgt=QWidget()
                inner_layout=QHBoxLayout()

                check=QCheckBox(parent=inner_wgt)
                if el.name in chosen_list:
                    check.setChecked(True)
                inner_layout.addWidget(check)
                credit_label = QLabel(parent=inner_wgt)
                name_label = QLabel(parent=inner_wgt)
                # if chosen:
                #     course = el[0]
                #     wrapped_word=formatting.word_wrap(course.name,195,QFontMetricsF(check.font()).width("新"))
                #     credit_text=course.credit
                #     is_chosen = el[1]
                #     if course.compulsory:
                #         inner_wgt.setStyleSheet('''.QLabel{color:red;}''')
                #         check.setEnabled(False)
                #     if is_chosen:
                #         check.setChecked(True)
                #         credits += float(course.credit)
                # else:
                wrapped_word=formatting.word_wrap(el.name,195,QFontMetricsF(check.font()).width("新"))
                credit_text=el.credit
                if el.compulsory:
                    inner_wgt.setStyleSheet('''.QLabel{color:red;}''')
                    # check.setChecked(True)
                    check.setEnabled(False)
                    credits += float(el.credit)
                credit_label.setText(credit_text)
                credit_label.setEnabled(False)
                name_label.setText(wrapped_word)
                name_label.setEnabled(False)
                inner_layout.addWidget(credit_label)
                inner_layout.addWidget(name_label)
                inner_wgt.setLayout(inner_layout)
                drag_widget.addWidget(inner_wgt)
                check.stateChanged.connect(partial(self.checkbox_change, wrapped_word.replace('\n', ''), cnt_term - 1, credit_text))
            drag_widget.drop.connect(partial(self.drop, cnt_term - 1))
            show_credit.setText('已选学分 '+str(credits))
            gb_layout_out.addWidget(drag_widget)
            gb_layout_out.setStretch(0,1)
            gb_layout_out.setStretch(1,10)
            gb.setLayout(gb_layout_out)
            wgt_layout.addWidget(gb)
        wgt.setLayout(wgt_layout)
        self.tabArea.currentWidget().setWidget(wgt)
        print("done")
        return

    def checkbox_change(self, course_name, term, credit, state):
        pass

    def drop(self,target_term,credit):
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
