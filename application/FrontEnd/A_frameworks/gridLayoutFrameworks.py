import os
import sys
import time
import re

import threading
from threading import Thread
from enum import Enum
from queue import Queue
from typing import Union
from typing import List
from datetime import timedelta

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from application.FrontEnd.A_frameworks.widgetFrameworks import ConnectedWidget, IsolatedWidget


class GridLayout(QGridLayout):
    def __init__(self, *widgets, window: QMainWindow = None):
        super().__init__()  # No arguments here
        for index, widget in enumerate(widgets):
            print(f"{index}: {widget}")
            # try:
            #     widget.set_MainWindow(window)
            # except Exception as e:
            #     print(f"Exception: {e}")
            
            
            self.setWidgetPosition(index, widget)


    def setWidgetPosition(self, index, widget: Union[ConnectedWidget, IsolatedWidget]):
        # print(f'WIDGET: {type(widget)}')
        widgetRow = widget.widgetRow
        widgetCol = widget.widgetCol
        
        if widgetRow == -1 or widgetCol == -1:
            widgetRow = index // 1
            widgetCol = index % 1
            
            # Allow setting span when not negative
            if widget.widgetRowSpan != -1 and widget.widgetColSpan != -1:
                self.addWidget(widget, widgetRow, widgetCol, widget.widgetRowSpan, widget.widgetColSpan)
            else:
                self.addWidget(widget, widgetRow, widgetCol)
        else:
            # Allow setting span when not negative
            if widget.widgetRowSpan != -1 and widget.widgetColSpan != -1:
                self.addWidget(widget, widgetRow, widgetCol, widget.widgetRowSpan, widget.widgetColSpan)
            else:
                self.addWidget(widget, widgetRow, widgetCol)





