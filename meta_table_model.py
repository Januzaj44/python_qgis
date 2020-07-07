# -*- coding: utf-8 -*-

from qgis.PyQt.QtCore import Qt, QAbstractTableModel, QModelIndex


class MetaTableModel(QAbstractTableModel):
    """ Abstrakcyjna klasa modelu tabeli (wzorzec MVC) """
    def __init__(self, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        # Lista metadanych warstwy (lista słowników)
        self.files_meta = []

    def rowCount(self, parent=None):
        """ Określenie liczby wierszy na podstawie listy słowników """
        return len(self.files_meta)

    def columnCount(self, parent=None):
        """ Stała liczba kolumn """
        return 7

    def headerData(self, section, QtOrientation, role):
        """ Ustawienie nazw dla kolumn """
        if QtOrientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Nazwa'
            elif section == 1:
                return 'Rozmiar'
            elif section == 2:
                return 'Liczba obiektów'
            elif section == 3:
                return 'Liczba kolumn'
            elif section == 4:
                return 'Nazwy kolumn'
            elif section == 5:
                return 'Układ współrzędnych'
            elif section == 6:
                return 'Data modyfikacji'

    def insertRows(self, position, rows, parent=QModelIndex()):
        """ Logika dodawania nowych wierszy """
        # Zgodnie z dokumentacją (https://doc.qt.io/qt-5/qabstractitemmodel.html#insertRows)
        # Powiadomienie, że model ulega zmianie
        self.beginInsertRows(parent, position, position + len(rows) - 1)
        # Dodanie słownika z metadanymi do listy metadanych
        for i, meta in enumerate(rows):
            self.files_meta.insert(position+i, meta)
        # Powiadomienie, że model uległ zmianie
        self.endInsertRows()
        return True

    def removeRows(self, row=None, count=None, parent=QModelIndex()):
        """ Logika usuwania wierszy """
        if count == None:
            count = len(self.files_meta)
        if row == None:
            row = 0
        # Podobnie jak w insert rows (https://doc.qt.io/qt-5/qabstractitemmodel.html#removeRows)
        self.beginRemoveRows(parent, row, row+count-1)
        for i in reversed(list(range(row, row+count))):
            del self.files_meta[i]
        self.endRemoveRows()

    def data(self, index, role):
        """ Logika wyświetlania danych dla danej komórki """
        if not index.isValid():
            return
        # Wybór odpowiadającego komórce elemntu listy 
        file_meta = self.files_meta[index.row()]
        # Zwrócenie odpowiednich wartości w zależności od kolumny pojedynczej komórce
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return file_meta['name']
            if index.column() == 1:
                return file_meta['size']
            if index.column() == 2:
                return file_meta['obj_count']
            if index.column() == 3:
                return file_meta['column_count']
            if index.column() == 4:
                return file_meta['colum_names']
            if index.column() == 5:
                return file_meta['epsg']
            if index.column() == 6:
                return file_meta['modified']