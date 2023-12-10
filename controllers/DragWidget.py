from PyQt5.QtGui import QDropEvent,QDrag,QDragEnterEvent
from PyQt5.QtCore import QMimeData,Qt,pyqtSignal
from PyQt5.QtWidgets import QWidget,QVBoxLayout


class DragWidget(QWidget):
    drop=pyqtSignal(dict)
    def __init__(self ,parent=None):
        super(DragWidget ,self).__init__(parent)
        self.setAcceptDrops(True)
        self.layout =QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(""".QWidget{border:2px solid green;}""")

    def addWidget(self ,widget):
        self.layout.addWidget(widget)
        return

    def insertWidget(self,index,item):
        self.layout.insertWidget(index, item)
        return

    def takeAt(self,index):
        wgt=self.layout.takeAt(index)
        return wgt

    def getSize(self):
        return self.size

    def mousePressEvent(self ,e):
        print(e)
        item = self.childAt(e.pos()).parent()
        if item == None:
            return
        index = self.layout.indexOf(item)

        self.drag = QDrag(item)
        mime = QMimeData()
        mime.setText(str(index))
        self.drag.setMimeData(mime)
        # print('end' + str(item))
        self.drag.exec_(Qt.MoveAction)
        # print('end' + str(item))

    def dropEvent(self, e: QDropEvent) -> None:
        source_drag_widget = e.source()
        while type(source_drag_widget )!=DragWidget:
            source_drag_widget =source_drag_widget.parent()
        if source_drag_widget==self:
            return
        credits_label=self.parent().layout().itemAt(0).widget()
        big= self.parent().parent()
        term_cnt=big.layout().count()
        source_index =int(source_drag_widget.drag.mimeData().text())
        source_term=int(source_drag_widget.parent().title()[4:])
        target_term=int(self.parent().title()[4:])
        print('from '+str(source_term)+" to "+str(target_term))
        if (source_term!=0 or source_term!=term_cnt-1) and source_term<target_term and source_drag_widget.layout.count()==1:
            self.drop.emit({'no':1})
            return

        cre=float(credits_label.text()[5:])
        if cre>=17.5:
            return
        target_pos =e.pos()
        target_item =self.childAt(target_pos)
        while type(target_item )!=QWidget:
            target_item= target_item.parent()
        old_item = source_drag_widget.takeAt(source_index).widget()
        while type(old_item)!=QWidget:
            old_item =old_item.parent()
        check=old_item.layout().itemAt(0).widget()
        name=old_item.layout().itemAt(2).widget().text()
        name=name.replace("\n",'')
        credit=check.checkState()==2 and float(old_item.layout().itemAt(1).widget().text()) or 0
        target_index =self.layout.indexOf(target_item)
        self.insertWidget(target_index ,old_item)
        sig={"credit":credit,"source_term":source_drag_widget.parent().title()[4:],'name':name}
        self.drop.emit(sig)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        e.setDropAction(Qt.MoveAction)
        e.accept()
        return