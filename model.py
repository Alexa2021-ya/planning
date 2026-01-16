from datetime import datetime, timedelta
import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QTableView, QVBoxLayout)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex
from db import DB

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, w):
        super().__init__()
        self.a = w
        self.db = DB()
        d1 = w.calculate_week()[0]
        d2 = w.calculate_week()[1]
        self.data_ = self.db.get_data(d1, d2)

    def rowCount(self, parent=QtCore.QModelIndex()):
        return 24

    def columnCount(self, parent=QtCore.QModelIndex()):
        return 7
    
    def data(self, index, role):
        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            try:
                for i in range(len(self.data_[0]) - 1):
                    self.index_column = datetime.datetime.strptime(self.data_[i][0], '%Y-%m-%d').weekday()
                    if self.index_column == index.column():
                        for j in range(1, len(self.data_[i])):
                            if index.row() == j - 1:
                                return self.data_[i][j]
            except IndexError:
                return ''
            
    def setData(self, index, value, role):
        if (role == QtCore.Qt.EditRole):
            #Определение колонки
            col = '_' + str(index.row())
            #Определение id
            #Вычисление начала недели
            d = datetime.datetime.strptime(self.a.calculate_week()[0], "%Y-%m-%d").date()
            d = d - timedelta(d.weekday())
            #Определение даты=id
            d = d + timedelta(index.column())
            if (not value or value.isspace()):
                if (self.db.is_data(d)):
                    self.db.delete_data(col, d) 
            elif (self.db.is_data(d)):
                self.db.edit_data(col, value, d) 
            else:
                self.db.add_data(col, d, value) 
            #Обновление таблицы
            self.beginResetModel()
            d1 = self.a.calculate_week()[0]
            d2 = self.a.calculate_week()[1]
            self.data_ = self.db.get_data(d1, d2)
            self.endResetModel()
            self.a.table_week.resizeRowsToContents()
            return True
        return False

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return ['Понедельник', 'Вторник', 'Среда', 'Четверг',
                        'Пятница', 'Суббота', 'Воскресенье'][section]
            if orientation == QtCore.Qt.Vertical:
                return ['00:00', '1:00', '2:00', '3:00', '4:00', '5:00',
                        '6:00', '7:00', '8:00', '9:00', '10:00', '11:00',
                        '12:00', '13:00', '14:00', '15:00', '16:00',
                        '17:00', '18:00', '19:00', '20:00', '21:00',
                        '22:00', '23:00'][section]
