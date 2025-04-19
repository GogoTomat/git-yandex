import sys
import io
import sqlite3

from PyQt6.QtWidgets import QWidget, QApplication, QTableWidgetItem
from PyQt6 import uic
from PyQt6.QtCore import Qt, QPoint
from addCoffee import addCoffeeValue


template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>630</width>
    <height>299</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QPushButton" name="pushButton">
   <property name="geometry">
    <rect>
     <x>450</x>
     <y>260</y>
     <width>171</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>Получить данные</string>
   </property>
  </widget>
  <widget class="QTableWidget" name="tableWidget">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>10</y>
     <width>611</width>
     <height>251</height>
    </rect>
   </property>
   <property name="columnCount">
    <number>7</number>
   </property>
   <attribute name="horizontalHeaderCascadingSectionResizes">
    <bool>false</bool>
   </attribute>
   <attribute name="horizontalHeaderDefaultSectionSize">
    <number>87</number>
   </attribute>
   <attribute name="horizontalHeaderHighlightSections">
    <bool>true</bool>
   </attribute>
   <attribute name="horizontalHeaderShowSortIndicator" stdset="0">
    <bool>false</bool>
   </attribute>
   <attribute name="horizontalHeaderStretchLastSection">
    <bool>false</bool>
   </attribute>
   <column/>
   <column/>
   <column/>
   <column/>
   <column/>
   <column/>
   <column/>
  </widget>
  <widget class="QPushButton" name="addButton">
   <property name="geometry">
    <rect>
     <x>260</x>
     <y>260</y>
     <width>171</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>Добавить значение</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Coffee(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.set_values)
        self.addButton.clicked.connect(self.add_values)
        self.tableWidget.itemChanged.connect(self.change_value)
        self.con = sqlite3.connect("coffee.sqlite")
        self.cur = self.con.cursor()
        self.modified = dict()

    def set_values(self):
        result = self.cur.execute("SELECT * FROM coffee_options").fetchall()
        self.titles = [descr[0] for descr in self.cur.description]
        self.tableWidget.clear()
        if result:
            self.tableWidget.setRowCount(len(result))
            for row, value in enumerate(result):
                for column, value1 in enumerate(value):
                    value1 = QTableWidgetItem(str(value1))
                    if column == 0:
                        value1.setFlags(value1.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.tableWidget.setItem(row, column, value1)

    def add_values(self):
        self.addCoffee = addCoffeeValue(self.con)
        self.addCoffee.show()

    def change_value(self, item):
        if self.tableWidget.currentRow() != -1:
            self.modified[self.titles[item.column()]] = item.text()
            print(self.modified)
            que = "UPDATE coffee_options SET\n"
            que += "\n".join([f"{key}='{self.modified.get(key)}'" for key in self.modified.keys()])
            que += "WHERE id = ?"
            self.cur.execute(que, (self.tableWidget.item(item.row(), 0).text(), ))
            self.con.commit()
            self.set_values()

    def closeEvent(self, event):
        if self.addCoffee:
            self.addCoffee.close()
        self.con.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    coffee = Coffee()
    coffee.show()
    sys.exit(app.exec())
