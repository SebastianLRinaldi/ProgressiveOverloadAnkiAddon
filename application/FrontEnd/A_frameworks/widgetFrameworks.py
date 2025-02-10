from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class Widget(QWidget):
    def __init__(self, layout=None):
        super().__init__()
        if layout:
            self.setLayout(layout)
        
        
class ConnectedWidget(QWidget):
    def __init__(self, ui_handler, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        """
        Base class for widgets that initializes common properties like ui_handler,
        widgetRow, and widgetCol.
        
        :param ui_handler: The UI handler instance.
        :param widgetRow: Row index for the widget (default -1).
        :param widgetCol: Column index for the widget (default -1).
        :param *args: Additional arguments for the widget.
        :param **kwargs: Additional keyword arguments for the widget.
        """
        super().__init__(*args, **kwargs)
        self.ui_handler = ui_handler
        self.widgetRow = widgetRow
        self.widgetCol = widgetCol
        self.widgetRowSpan = widgetRowSpan 
        self.widgetColSpan = widgetColSpan
        
class IsolatedWidget(QWidget):
    def __init__(self, widgetRow=-1, widgetCol=-1, widgetRowSpan=-1, widgetColSpan=-1, *args, **kwargs):
        """
        Base class for widgets that do not control or update other elements in the UI.

        :param widgetRow: Row index for the widget (default -1).
        :param widgetCol: Column index for the widget (default -1).
        :param *args: Additional arguments for the widget.
        :param **kwargs: Additional keyword arguments for the widget.
        """
        super().__init__(*args, **kwargs)
        self.widgetRow = widgetRow
        self.widgetCol = widgetCol
        self.widgetRowSpan = widgetRowSpan 
        self.widgetColSpan = widgetColSpan 



