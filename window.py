from datetime import datetime, timedelta
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QTableView, QVBoxLayout)
from PyQt5.QtCore import Qt
from db import DB
from model import TableModel

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.db = DB()
        self.initUi()
        self.data_ = ""
        self.get_date()
        
    def initUi(self):
        self.setObjectName("Планинг")
        self.resize(929, 600)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")

        self.horizontal_layot = QtWidgets.QHBoxLayout()
        self.horizontal_layot.setObjectName("horizontal_layot")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setEnabled(True)
        self.groupBox.setMaximumSize(QtCore.QSize(378, 16777215))
        self.groupBox.setStyleSheet("background-color: rgb(234, 234, 234);")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setObjectName("grid_layout")
        
        self.calendar = QtWidgets.QCalendarWidget(self.groupBox)
        self.calendar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.calendar.setStyleSheet("background-color: rgb(234, 234, 234); alternate-background-color: rgb(234, 234, 234); selection-background-color: rgb(234, 234, 234);")
        self.calendar.setObjectName("calendar")
        self.calendar.clicked.connect(self.get_date)
        self.grid_layout.addWidget(self.calendar, 0, 0, 1, 1)

        self.label_notes = QtWidgets.QLabel(self.groupBox)
        self.label_notes.setObjectName("label_notes")
        self.grid_layout.addWidget(self.label_notes, 1, 0, 1, 1)

        self.notes = QtWidgets.QPlainTextEdit(self.groupBox)
        self.notes.setObjectName("notes")
        self.grid_layout.addWidget(self.notes, 2, 0, 1, 1)

        self.add_note = QtWidgets.QPushButton(self.groupBox)
        self.grid_layout.addWidget(self.add_note, 3, 0, 1, 1)
        self.add_note.setObjectName("add_note")
        self.add_note.clicked.connect(self.edit_note)

        self.horizontalLayout.addLayout(self.grid_layout)
        self.horizontal_layot.addWidget(self.groupBox)
        
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.week = QtWidgets.QLabel(self.groupBox_2)
        self.week.setText("")
        self.week.setAlignment(Qt.AlignCenter) 
        self.week.setObjectName("week")
        self.gridLayout_3.addWidget(self.week, 0, 0, 1, 1)
        self.grid_layout2 = QtWidgets.QGridLayout()
        self.grid_layout2.setObjectName("grid_layout2")
        
        self.next_week = QtWidgets.QPushButton(self.groupBox_2)
        self.next_week.clicked.connect(self.get_next_week)
        self.next_week.setObjectName("next_week")
        self.grid_layout2.addWidget(self.next_week, 1, 1, 1, 1)
        self.last_week = QtWidgets.QPushButton(self.groupBox_2)
        self.last_week.clicked.connect(self.get_last_week)
        self.last_week.setObjectName("last_week")
        
        self.grid_layout2.addWidget(self.last_week, 1, 0, 1, 1)
        self.gridLayout_3.addLayout(self.grid_layout2, 2, 0, 1, 2)
        self.table_week = QtWidgets.QTableView(self.groupBox_2)
        self.table_week.setObjectName("table_week")
        self.gridLayout_3.addWidget(self.table_week, 1, 0, 1, 1)
        self.horizontal_layot.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.horizontal_layot)
        self.setCentralWidget(self.centralwidget)

        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("planning.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setWindowIcon(self.icon)
        
        QtCore.QMetaObject.connectSlotsByName(self)
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Планинг"))
        self.label_notes.setText(_translate("MainWindow", "Заметки"))
        self.add_note.setText(_translate("MainWindow", "Сохранить"))
        self.last_week.setText(_translate("MainWindow", "<"))
        self.next_week.setText(_translate("MainWindow", ">"))
        self.table_week.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.table_week.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Interactive)
        self.table_week.horizontalHeader().setStretchLastSection(1)
        self.show()

    def get_date(self):
        d1 = self.calculate_week()[0]
        self.get_note(d1)
        model = TableModel(self)
        self.table_week.setModel(model)
        
    def calculate_week(self):
        self.date_week = self.calendar.selectedDate()

        #дата понедельника
        monday =  self.date_week.addDays(1 - self.date_week.dayOfWeek())
        monday = monday.toString(format = Qt.ISODate)
        
        #дата воскресенья
        sunday = self.date_week.addDays(7 - self.date_week.dayOfWeek())
        sunday = sunday.toString(format = Qt.ISODate)
        #поменять формат
        self.week.setText(monday + "  -  " + sunday)
        
        return [monday, sunday]

    def get_note(self, d):
        self.notes.clear()
        if (self.db.is_note(d)):
            self.notes.appendPlainText(self.db.get_note(d))
    
    def edit_note(self):
        value = self.notes.toPlainText()
        d = self.calculate_week()[0]

        if (not value or value.isspace()):
            self.db.delete_note(d)
        else:
            if (self.db.is_note(d)):
                self.db.edit_note(value, d)
            else:
                self.db.add_note(value, d)

    def get_next_week(self):
        d = datetime.datetime.strptime(self.calculate_week()[1], "%Y-%m-%d").date() + timedelta(days=1)
        self.calendar.setSelectedDate(d)
        self.get_date()
        
    def get_last_week(self):
        d = datetime.datetime.strptime(self.calculate_week()[0], "%Y-%m-%d").date() - timedelta(days=1)
        self.calendar.setSelectedDate(d)
        self.get_date()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = Window()
    sys.exit(app.exec_())

