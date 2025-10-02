# -*- coding: UTF-8 -*-

import sys
from PySide6.QtCore import QModelIndex, Qt, QAbstractTableModel
from PySide6.QtWidgets import QApplication, QTableView, QMainWindow, QAbstractItemView

from str import *

#---------------------------------------------------------------------------------------------------------
class pyqtTableModel(QAbstractTableModel):

    #---------------------------------------------------------------------------------------------------------
    def __init__(self, data, headers):
        super().__init__()
        self._data = data
        self._headers = headers

    #---------------------------------------------------------------------------------------------------------
    def rowCount(self, parent=None):
        return len(self._data)

    #---------------------------------------------------------------------------------------------------------
    def columnCount(self, parent=None):
        return len(self._headers)

    #---------------------------------------------------------------------------------------------------------
    def getData(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
           return None
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        
        return None

    #---------------------------------------------------------------------------------------------------------
    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            elif orientation == Qt.Orientation.Vertical:
                return str(section + 1) # Row numbers
        return None
    
    #---------------------------------------------------------------------------------------------------------
    def addRow(self, new_row_data):

        print("addRow - new_row_data = " + str(new_row_data))

        if new_row_data and len(new_row_data) > 0:

           row_count = self.rowCount()
           print("addRow - row_count = " + str(row_count))

           self.beginInsertRows(QModelIndex(), row_count, row_count)
           self._data.append(new_row_data) # Modify your internal data
           #self._data.insert(row_count, new_row_data) # Modify your internal data
           self.endInsertRows()
           #self.layoutChanged.emit()

        return self.rowCount()

    #---------------------------------------------------------------------------------------------------------
    def delRow(self, modelData, lstData, row_index=0):

        nMax = self.rowCount()

        if row_index==0:
           row_index = self.getRowIndex(modelData, lstData)

        if (row_index >= 0 and row_index < nMax):
            self.beginRemoveRows(QModelIndex(), row_index, row_index)
            del self._data[row_index] # Modify your internal data
            self.endRemoveRows()
            self.layoutChanged.emit()

        return self.rowCount()

    #---------------------------------------------------------------------------------------------------------
    def getRowIndex(self, modelData, lstData):

        nMax = self.rowCount()

        n = 0
        while n < nMax:
              tData = self.getData(n)
              if tData == lstData:
                 return n
              n = n + 1

        return -1

    #---------------------------------------------------------------------------------------------------------
    def setDataCell(self, index, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:
            # Modify your internal data structure
            self._data[index.row()][index.column()] = value
            # Emit dataChanged for the specific cell
            self.dataChanged.emit(index, index, [role])
            self.layoutChanged.emit()
            return True
        return False

    #---------------------------------------------------------------------------------------------------------
    def update_single_cell(self, row, column, new_value):
        # Example of updating data and emitting signal
        index = self.index(row, column)
        return self.setDataCell(index, new_value, Qt.ItemDataRole.EditRole)

    #---------------------------------------------------------------------------------------------------------
    def setGridSelectionSingle(self, tvGrid):
        tvGrid.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        return 

    #---------------------------------------------------------------------------------------------------------
    def setGridSelectionExtended(self, tvGrid):
        tvGrid.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        return 

    #---------------------------------------------------------------------------------------------------------
    def setGridSelectionMultiSelection(self, tvGrid):
        tvGrid.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
        return 

    #---------------------------------------------------------------------------------------------------------
    def setGridSelectionNoSelection(self, tvGrid):
        tvGrid.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        return 

#---------------------------------------------------------------------------------------------------------
def pyqt_tv_setColumnWidth(tvGrid, nCol, nLen):
    tvGrid.setColumnWidth(nCol, nLen) 

#---------------------------------------------------------------------------------------------------------
