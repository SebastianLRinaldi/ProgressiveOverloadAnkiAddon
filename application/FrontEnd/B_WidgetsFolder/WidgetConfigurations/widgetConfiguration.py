import os
import sys
import time
import re

import threading
from threading import Thread
from enum import Enum
from queue import Queue
from typing import List
from datetime import timedelta

from PyQt6.QtCore import Qt
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from application.FrontEnd.A_frameworks.widgetFrameworks import ConnectedWidget, IsolatedWidget


class Button(QPushButton, IsolatedWidget):
    def __init__(self, text="Click me!", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QPushButton.__init__(self, text, *args, **kwargs)

    def update_label(self, text):
        self.setText(text)


class LineEdit(QLineEdit, IsolatedWidget):
    def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QLineEdit.__init__(self, text, *args, **kwargs)

    def update_label(self, text):
        self.setText(text)


class ComboBox(QComboBox, IsolatedWidget):
    
    focused_in = pyqtSignal()
    focused_out = pyqtSignal()
    beforePopup = pyqtSignal()  
    
    
    
    def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QComboBox.__init__(self, *args, **kwargs)
        self.setStyleSheet("combobox-popup: 0;")
        self.setMaxVisibleItems(15)
        # self.activated.connect(lambda: print("ACTIVED"))
        
    def update_items(self, items):
        self.clear()
        self.addItems(items)
        
    def focusInEvent(self, event):
        # print("ComboBox gained focus")
        self.focused_in.emit()
        
    def focusOutEvent(self, event):
        # print("ComboBox lost focus")
        self.focused_out.emit()
        
    def showPopup(self):
        """Emit a signal before showing the dropdown."""
        self.beforePopup.emit()  # Emit the custom signal
        super().showPopup()  # Open the dropdown normally
        


class CheckBox(QCheckBox, IsolatedWidget):
    def __init__(self, text="Check me!", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QCheckBox.__init__(self, text, *args, **kwargs)

    def update_label(self, text):
        self.setText(text)


class RadioButton(QRadioButton, IsolatedWidget):
    def __init__(self, text="Select me!", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QRadioButton.__init__(self, text, *args, **kwargs)

    def update_label(self, text):
        self.setText(text)


class Slider(QSlider, IsolatedWidget):
    def __init__(self, orientation=Qt.Orientation.Horizontal, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QSlider.__init__(self, orientation, *args, **kwargs)

    def update_value(self, value):
        self.setValue(value)


class SpinBox(QSpinBox, IsolatedWidget):
    def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QSpinBox.__init__(self, *args, **kwargs)

    def update_value(self, value):
        self.setValue(value)


class TextEdit(QTextEdit, IsolatedWidget):
    def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QTextEdit.__init__(self, text, *args, **kwargs)

    def update_text(self, text):
        self.setText(text)


class TableWidget(QTableWidget, IsolatedWidget):
    def __init__(self, rows=5, cols=5, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QTableWidget.__init__(self, rows, cols, *args, **kwargs)

    def update_cell(self, row, col, value):
        self.setItem(row, col, QTableWidgetItem(value))


class TableWidgetItem(QTableWidgetItem, IsolatedWidget):
    def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QTableWidgetItem.__init__(self, text, *args, **kwargs)

    def update_text(self, text):
        self.setText(text)


class ProgressBar(QProgressBar, IsolatedWidget):
    def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QProgressBar.__init__(self, *args, **kwargs)

    def update_progress(self, value):
        self.setValue(value)


# class TabWidget(QTabWidget, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTabWidget.__init__(self, *args, **kwargs)

#     def add_tab(self, widget, title):
#         self.addTab(widget, title)


# class GroupBox(QGroupBox, IsolatedWidget):
#     def __init__(self, title="Group Box", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QGroupBox.__init__(self, title, *args, **kwargs)

#     def update_title(self, title):
#         self.setTitle(title)


# class Frame(QFrame, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QFrame.__init__(self, *args, **kwargs)

#     def update_style(self, style):
#         self.setStyleSheet(style)


# class Dial(QDial, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QDial.__init__(self, *args, **kwargs)

#     def update_value(self, value):
#         self.setValue(value)

class ListWidget(QListWidget, IsolatedWidget):
    def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QListWidget.__init__(self, *args, **kwargs)

    def update_items(self, items):
        self.clear()
        self.addItems(items)
        
    def addMasteryItem(self, templateMasteryItem: QWidget):
        item = QListWidgetItem()
        item.setSizeHint(templateMasteryItem.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, templateMasteryItem)


class Label(QLabel, IsolatedWidget):
    def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QLabel.__init__(self, text, *args, **kwargs)

    def update_label(self, text):
        self.setText(text)


class CalendarWidget(QCalendarWidget, IsolatedWidget):
    def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QCalendarWidget.__init__(self, *args, **kwargs)

    def update_selected_date(self, date):
        self.setSelectedDate(date)


# class DateEdit(QDateEdit, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QDateEdit.__init__(self, *args, **kwargs)

#     def update_date(self, date):
#         self.setDate(date)


# class TimeEdit(QTimeEdit, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTimeEdit.__init__(self, *args, **kwargs)

#     def update_time(self, time):
#         self.setTime(time)


# class SpinBoxDouble(QDoubleSpinBox, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QDoubleSpinBox.__init__(self, *args, **kwargs)

#     def update_value(self, value):
#         self.setValue(value)


# class ToolButton(QToolButton, IsolatedWidget):
#     def __init__(self, text="Tool Button", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QToolButton.__init__(self, *args, **kwargs)

#     def update_label(self, text):
#         self.setText(text)


# class Menu(QMenu, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QMenu.__init__(self, *args, **kwargs)

#     def add_action(self, action):
#         self.addAction(action)


# class Action(QAction, IsolatedWidget):
#     def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QAction.__init__(self, text, *args, **kwargs)

#     def update_text(self, text):
#         self.setText(text)


# class StackWidget(QStackedWidget, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QStackedWidget.__init__(self, *args, **kwargs)

#     def update_current_widget(self, index):
#         self.setCurrentIndex(index)


# class TabBar(QTabBar, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTabBar.__init__(self, *args, **kwargs)

#     def update_tabs(self, tabs):
#         self.clear()
#         for tab in tabs:
#             self.addTab(tab)


# class ProgressDialog(QProgressDialog, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QProgressDialog.__init__(self, *args, **kwargs)

#     def update_progress(self, value):
#         self.setValue(value)


# class PlainTextEdit(QPlainTextEdit, IsolatedWidget):
#     def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QPlainTextEdit.__init__(self, text, *args, **kwargs)

#     def update_text(self, text):
#         self.setPlainText(text)


# class FrameLayout(QVBoxLayout, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QVBoxLayout.__init__(self, *args, **kwargs)

#     def update_widgets(self, widgets):
#         for widget in widgets:
#             self.addWidget(widget)
            
            
# class RadioButton(QRadioButton, IsolatedWidget):
#     def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QRadioButton.__init__(self, text, *args, **kwargs)

#     def update_label(self, text):
#         self.setText(text)


# class LineEdit(QLineEdit, IsolatedWidget):
#     def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QLineEdit.__init__(self, text, *args, **kwargs)

#     def update_text(self, text):
#         self.setText(text)


# class ComboBox(QComboBox, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QComboBox.__init__(self, *args, **kwargs)

#     def update_items(self, items):
#         self.clear()
#         self.addItems(items)


# class Slider(QSlider, IsolatedWidget):
#     def __init__(self, orientation=Qt.Orientation.Horizontal, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QSlider.__init__(self, orientation, *args, **kwargs)

#     def update_value(self, value):
#         self.setValue(value)


# class ProgressBar(QProgressBar, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QProgressBar.__init__(self, *args, **kwargs)

#     def update_progress(self, value):
#         self.setValue(value)


# class TableWidget(QTableWidget, IsolatedWidget):
#     def __init__(self, rowCount=0, columnCount=0, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTableWidget.__init__(self, rowCount, columnCount, *args, **kwargs)

#     def update_table(self, data):
#         for row, row_data in enumerate(data):
#             for col, item in enumerate(row_data):
#                 self.setItem(row, col, QTableWidgetItem(str(item)))


# class TreeWidget(QTreeWidget, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTreeWidget.__init__(self, *args, **kwargs)

#     def update_tree(self, items):
#         self.clear()
#         for item in items:
#             self.addTopLevelItem(QTreeWidgetItem([item]))


# class GroupBox(QGroupBox, IsolatedWidget):
#     def __init__(self, title="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QGroupBox.__init__(self, title, *args, **kwargs)

#     def update_title(self, title):
#         self.setTitle(title)


# class HSlider(QSlider, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QSlider.__init__(self, Qt.Orientation.Horizontal, *args, **kwargs)

#     def update_value(self, value):
#         self.setValue(value)


# class VSlider(QSlider, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QSlider.__init__(self, Qt.Vertical, *args, **kwargs)

#     def update_value(self, value):
#         self.setValue(value)


# class ScrollBar(QScrollBar, IsolatedWidget):
#     def __init__(self, orientation=Qt.Orientation.Horizontal, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QScrollBar.__init__(self, orientation, *args, **kwargs)

#     def update_value(self, value):
#         self.setValue(value)


# class DockWidget(QDockWidget, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QDockWidget.__init__(self, *args, **kwargs)

#     def update_title(self, title):
#         self.setWindowTitle(title)


# class Splitter(QSplitter, IsolatedWidget):
#     def __init__(self, orientation=Qt.Orientation.Horizontal, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QSplitter.__init__(self, orientation, *args, **kwargs)

#     def update_widgets(self, widgets):
#         for widget in widgets:
#             self.addWidget(widget)


# class Frame(QFrame, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QFrame.__init__(self, *args, **kwargs)

#     def update_style(self, style):
#         self.setFrameShape(style)


# class ToolBox(QToolBox, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QToolBox.__init__(self, *args, **kwargs)

#     def update_widgets(self, widgets):
#         for widget in widgets:
#             self.addItem(widget, widget.objectName())


# class MessageBox(QMessageBox, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QMessageBox.__init__(self, *args, **kwargs)

#     def update_message(self, message):
#         self.setText(message)
        
# class TextEdit(QTextEdit, IsolatedWidget):
#     def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTextEdit.__init__(self, text, *args, **kwargs)

#     def update_text(self, text):
#         self.setPlainText(text)


# class DateEdit(QDateEdit, IsolatedWidget):
#     def __init__(self, date=QDate.currentDate(), widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QDateEdit.__init__(self, date, *args, **kwargs)

#     def update_date(self, date):
#         self.setDate(date)


# class TimeEdit(QTimeEdit, IsolatedWidget):
#     def __init__(self, time=QTime.currentTime(), widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTimeEdit.__init__(self, time, *args, **kwargs)

#     def update_time(self, time):
#         self.setTime(time)


class SpinBox(QSpinBox, IsolatedWidget):
    def __init__(self, value=0, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        QSpinBox.__init__(self, *args, **kwargs)

    def update_value(self, value):
        self.setValue(value)


# class DoubleSpinBox(QDoubleSpinBox, IsolatedWidget):
#     def __init__(self, value=0.0, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QDoubleSpinBox.__init__(self, *args, **kwargs)

#     def update_value(self, value):
#         self.setValue(value)


# class ListView(QListView, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QListView.__init__(self, *args, **kwargs)

#     def update_items(self, items):
#         model = QStandardItemModel(self)
#         for item in items:
#             model.appendRow(QStandardItem(item))
#         self.setModel(model)


# class TableView(QTableView, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTableView.__init__(self, *args, **kwargs)

#     def update_data(self, data):
#         model = QStandardItemModel(self)
#         for row_data in data:
#             row = []
#             for item in row_data:
#                 row.append(QStandardItem(str(item)))
#             model.appendRow(row)
#         self.setModel(model)


# class QLabel(QLabel, IsolatedWidget):
#     def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QLabel.__init__(self, text, *args, **kwargs)

#     def update_text(self, text):
#         self.setText(text)


# class TabWidget(QTabWidget, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTabWidget.__init__(self, *args, **kwargs)

#     def update_tabs(self, tabs):
#         self.clear()
#         for tab, content in tabs:
#             self.addTab(content, tab)


# class TreeView(QTreeView, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QTreeView.__init__(self, *args, **kwargs)

#     def update_items(self, items):
#         model = QStandardItemModel(self)
#         root_node = QStandardItem("Root")
#         model.appendRow(root_node)
#         for item in items:
#             root_node.appendRow(QStandardItem(item))
#         self.setModel(model)


# class PlainTextEdit(QPlainTextEdit, IsolatedWidget):
#     def __init__(self, text="", widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QPlainTextEdit.__init__(self, text, *args, **kwargs)

#     def update_text(self, text):
#         self.setPlainText(text)


# class ColorDialog(QColorDialog, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QColorDialog.__init__(self, *args, **kwargs)

#     def update_color(self, color):
#         self.setCurrentColor(color)


# class FileDialog(QFileDialog, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QFileDialog.__init__(self, *args, **kwargs)

#     def update_directory(self, directory):
#         self.setDirectory(directory)


# class FontDialog(QFontDialog, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QFontDialog.__init__(self, *args, **kwargs)

#     def update_font(self, font):
#         self.setCurrentFont(font)


# class InputDialog(QInputDialog, IsolatedWidget):
#     def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
#         IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
#         QInputDialog.__init__(self, *args, **kwargs)

#     def update_text(self, text):
#         self.setTextValue(text)