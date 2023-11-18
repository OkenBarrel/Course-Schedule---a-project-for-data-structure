from PyQt5.QtGui import QDropEvent,QDrag,QDragEnterEvent
from PyQt5.QtCore import QMimeData,Qt
from PyQt5.QtWidgets import QLabel,QWidget,QVBoxLayout

class DragWidget(QWidget):
    def __init__(self ,parent=None):
        super(DragWidget ,self).__init__(parent)
        self.setAcceptDrops(True)
        self.layout =QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet("""QWidget{background:aqua;}""")

    def addWidget(self ,widget):
        print("into add")
        self.layout.addWidget(widget)

    def mousePressEvent(self ,e):
        print(e)
        print("mouse press")
        item =self.childAt(e.pos()).parent()
        if item==None:
            return
        index =self.layout.indexOf(item)

        self.drag =QDrag(item)
        mime =QMimeData()
        mime.setText(str(index))
        self.drag.setMimeData(mime)
        self.drag.setHotSpot(e.pos( ) -item.pos())
        print('end' + str(item))
        self.drag.exec_(Qt.MoveAction)
        print('end' + str(item))

    def dropEvent(self, e: QDropEvent) -> None:
        source_drag_widget = e.source()
        while type(source_drag_widget )!=DragWidget:
            source_drag_widget =source_drag_widget.parent()
        if source_drag_widget==self:
            return

        target_pos =e.pos()
        target_item =self.childAt(target_pos)
        print("target item " +str(target_item))
        while type(target_item )!=QWidget:
            target_item= target_item.parent()
        for e in target_item.findChildren(QLabel):
            print(e.text())

        source_index =int(source_drag_widget.drag.mimeData().text())
        print(source_index)
        old_item =source_drag_widget.layout.takeAt(source_index).widget()
        while type(old_item)!=QWidget:
            old_item =old_item.parent()
        for e in old_item.findChildren(QLabel):
            print(e.text())
        target_index =self.layout.indexOf(target_item)
        self.layout.insertWidget(target_index ,old_item)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        e.setDropAction(Qt.MoveAction)
        e.accept()
        return

