# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from controllers.demo_backend import MainWindow
import views
import utils
import models
from PyQt5.QtWidgets import QApplication

if __name__=='__main__':
    app=QApplication([])
    w=MainWindow()
    app.exec_()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
