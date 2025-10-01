# -*- coding: UTF-8 -*-

import sys
from PySide6.QtCore import Qt, QAbstractTableModel
from PySide6.QtWidgets import QApplication, QTableView, QMainWindow

from str import *

#---------------------------------------------------------------------------------------------------------
class MyTableModel(QAbstractTableModel):
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1) # Row numbers
        return None
        
#---------------------------------------------------------------------------------------------------------
