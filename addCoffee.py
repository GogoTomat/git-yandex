import io
import sqlite3

from PyQt6.QtWidgets import QWidget
from PyQt6 import uic


template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>408</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QLineEdit" name="nameEdit">
   <property name="geometry">
    <rect>
     <x>280</x>
     <y>20</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QLabel" name="label">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>20</y>
     <width>131</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Название сорта</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="degreeEdit">
   <property name="geometry">
    <rect>
     <x>280</x>
     <y>50</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLabel" name="label_2">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>50</y>
     <width>131</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Степень обжарки</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_3">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>110</y>
     <width>131</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Описание вкуса</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="groundbeansEdit">
   <property name="geometry">
    <rect>
     <x>280</x>
     <y>80</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="tasteEdit">
   <property name="geometry">
    <rect>
     <x>280</x>
     <y>110</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QLabel" name="label_4">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>80</y>
     <width>131</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Молотый/в зернах</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_5">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>170</y>
     <width>131</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Объем упаковки</string>
   </property>
  </widget>
  <widget class="QLabel" name="label_6">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>140</y>
     <width>131</width>
     <height>16</height>
    </rect>
   </property>
   <property name="text">
    <string>Цена</string>
   </property>
  </widget>
  <widget class="QLineEdit" name="priceEdit">
   <property name="geometry">
    <rect>
     <x>280</x>
     <y>140</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QLineEdit" name="volumeEdit">
   <property name="geometry">
    <rect>
     <x>280</x>
     <y>170</y>
     <width>113</width>
     <height>21</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
  </widget>
  <widget class="QPushButton" name="sendButton">
   <property name="geometry">
    <rect>
     <x>280</x>
     <y>260</y>
     <width>113</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>Отправить</string>
   </property>
  </widget>
  <widget class="QPushButton" name="clearButton">
   <property name="geometry">
    <rect>
     <x>160</x>
     <y>260</y>
     <width>113</width>
     <height>32</height>
    </rect>
   </property>
   <property name="text">
    <string>Очистить</string>
   </property>
  </widget>
  <widget class="QLabel" name="resultLabel">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>200</y>
     <width>381</width>
     <height>41</height>
    </rect>
   </property>
   <property name="text">
    <string/>
   </property>
   <property name="wordWrap">
    <bool>true</bool>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class addCoffeeValue(QWidget):
    def __init__(self, con):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.con = con
        self.cur = self.con.cursor()
        self.initUI()

    def initUI(self):
        self.edits = [self.nameEdit, self.degreeEdit, self.groundbeansEdit, 
                      self.tasteEdit, self.priceEdit, self.volumeEdit]
        self.clearButton.clicked.connect(self.clear_edits)
        self.sendButton.clicked.connect(self.send_values)

    def clear_edits(self):
        self.clear_result()
        [item.clear() for item in self.edits]

    def send_values(self):
        self.clear_result()
        texts = [item.text() for item in self.edits]
        if len(list(filter(lambda x: str(x) != '', texts))) == len(self.edits):
            texts = [texts[i] if i < 5 else float(texts[i]) for i in range(len(texts))] 
            self.cur.execute('''INSERT INTO coffee_options VALUES (?, ?, ?, ?, ?, ?, ?)''', (None,) + tuple(texts))
            self.con.commit()
            self.resultLabel.setText("Значение успешно добавлено. Обновите таблицу.")
        else:
            self.resultLabel.setText("Одно или несколько значений некорректны, проверьте поля и повторите попытку.")

    def clear_result(self):
        self.resultLabel.clear()