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



from aqt.webview import AnkiWebView


class AnkiViewer (AnkiWebView, IsolatedWidget):
    def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        IsolatedWidget.__init__(self, widgetRow, widgetCol, widgetRowSpan, widgetColSpan, *args, **kwargs)
        AnkiWebView.__init__(self, *args, **kwargs)
    