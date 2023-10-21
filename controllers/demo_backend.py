from PyQt5.QtWidgets import QMainWindow,QApplication
# from context import views
from views import demo
from PyQt5.QtCore import QEvent


class MainWindow(demo.Ui_MainWindow,QMainWindow):

    def __init__(self):
        super(QMainWindow,self).__init__()
        self.setupUI(self)
        self.show()
        # self.connect_sigs()
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

    # def connect_sigs(self):
    #     self.yes_butt.clicked.connect(self.yes_butt_clicked)
    #
    # def yes_butt_clicked(self):
    #     print("yes!")



if __name__=='__main__':

    app=QApplication([])
    w=MainWindow()
    # w.show()
    app.exec_()

