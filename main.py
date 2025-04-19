import sys
import io
import sqlite3

from PyQt6.QtWidgets import QWidget, QApplication, QTableWidgetItem
from PyQt6 import uic


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

    def set_values(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("SELECT * FROM coffee_options").fetchall()
        con.close()
        self.tableWidget.clear()
        if result:
            self.tableWidget.setRowCount(len(result))
            self.tableWidget.setColumnCount(len(result[0]))
            for row, value in enumerate(result):
                for column, value1 in enumerate(value):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(value1)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    coffee = Coffee()
    coffee.show()
    sys.exit(app.exec())
