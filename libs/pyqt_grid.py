# -*- coding: UTF-8 -*-

import sys
#from PySide6.QtCore import QModelIndex, Qt, QAbstractTableModel
#from PySide6.QtWidgets import QApplication, QTableView, QMainWindow, QAbstractItemView

#from PyQt5.QtGui import QIcon
#from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QTableView, QHeaderView, QMessageBox, QProgressBar,QLineEdit
#from PyQt5.uic import loadUi
#from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QThread, QPropertyAnimation, QAbstractTableModel

from PyQt5.QtCore import QModelIndex, Qt, QAbstractTableModel
from PyQt5.QtWidgets import QApplication, QTableView, QMainWindow, QAbstractItemView


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
    def getDataByRowCol(self, row, col, role=Qt.ItemDataRole.DisplayRole):

        if self.validateRowCol(row, col):
           return self._data[row][col]
        #if not index.isValid():
        #   return None
        #if role == Qt.ItemDataRole.DisplayRole:
        #    return self._data[index.row()][index.column()]
        
        return ""
    #---------------------------------------------------------------------------------------------------------
    def getDataByIndex(self, index, role=Qt.ItemDataRole.DisplayRole):

        if not index.isValid():
           return ""
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[index.row()][index.column()]
        
        return ""

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

        row_count = self.rowCount()
        print("addRow - row_count = " + str(row_count))

        #self.beginResetModel()  # refresh data
        #if new_row_data and len(new_row_data) > 0:
        #   self._data.append(new_row_data) # Modify your internal data
        #self.endResetModel()

        row_position = len(self._data)
        self.beginInsertRows(QModelIndex(), row_position, row_position)
        self._data.append(new_row_data)
        self.endInsertRows()

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
    def validateRowCol(self, row, col):
        print("validateRowCol - row = " + str(row) + " - col = " + str(col))
        if row >= 0 and row < self.rowCount() and col >= 0 and col < self.columnCount():
            return True
        else:
            return False

    #---------------------------------------------------------------------------------------------------------
    def setDataCell(self, row, col, value, role=Qt.ItemDataRole.EditRole):
        if role == Qt.ItemDataRole.EditRole:

            if self.validateRowCol(row, col):
               # Modify your internal data structure
               index = QModelIndex
               index.row = row
               index.column = col
               #self._data[index.row()][index.column()] = str(salue)
               self._data[row][col] = str(value)
               print("setDataCell = " + str(self._data))
               #self.dataChanged.emit(index, index, [role])
               # Emit dataChanged for the specific cell
               self.layoutChanged.emit()
               return True
            
        return False

    #---------------------------------------------------------------------------------------------------------
    def update_table(self, rows, tvGrid):
        self.beginResetModel()  # refresh data  
        self._data = rows  # Replace data with results
        self.endResetModel()
        tvGrid.resizeRowsToContents()  #

    #---------------------------------------------------------------------------------------------------------
    def update_table_single_row(self, row, tvGrid):
        self.beginResetModel()  # refresh data
        print("row = " + str(row))
        self._data.append(row)  # Append new row
        self.endResetModel()
        #vGrid.resizeRowsToContents()  #

    #---------------------------------------------------------------------------------------------------------
    def export_table_to_csv(self):
        #export_rows_to_csv(self.model._data, self.model._headers, parent=self)
        return

    #---------------------------------------------------------------------------------------------------------
    def clean_table(self, tvGrid):
        self.beginResetModel()  # refresh data
        self._data = []  # Replace data with results
        self.endResetModel()
        tvGrid.resizeRowsToContents()  #

    #---------------------------------------------------------------------------------------------------------
    def data(self, index, role=Qt.DisplayRole):
        """
        Return the data stored under the given role for the specified index.

        Args:
            index (QModelIndex): Index specifying the row and column.
            role (int, optional): The role for which data is requested. Defaults to Qt.DisplayRole.

        Returns:
            Any: The value at the specified row and column if valid, otherwise None.
        """
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()

        if role == Qt.DisplayRole:
            #THIS IS CRITICAL FOR VIEWING DATA IN THE GRID
            return self._data[row][col]

        #if role == Qt.TextAlignmentRole:
        #    return Qt.AlignLeft | Qt.AlignVCenter
        
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        Return the header data for a given section, orientation, and role.

        Args:
            section (int): The section number (column index).
            orientation (Qt.Orientation): Horizontal or vertical orientation.
            role (int, optional): The role for which header data is requested. Defaults to Qt.DisplayRole.

        Returns:
            str: The header label for horizontal orientation and display role, otherwise default behavior.
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return super().headerData(section, orientation, role)

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
def pyqt_grid_setColumnWidth(tvGrid, nCol, nLen):
    tvGrid.setColumnWidth(nCol, nLen) 

#---------------------------------------------------------------------------------------------------------
def pyqt_grid_getSelectedRow(tvGrid):
    
    rows = []
    for idx in tvGrid.selectionModel().selectedIndexes():
        rows.append(idx.row())

    return rows

#---------------------------------------------------------------------------------------------------------
