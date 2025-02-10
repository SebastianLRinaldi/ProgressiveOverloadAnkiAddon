from application.FrontEnd.A_frameworks.gridLayoutFrameworks import *
from application.FrontEnd.A_frameworks.widgetFrameworks import *

class Window(QMainWindow):
    
    focused_in_window = pyqtSignal()
    focus_2 = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Progressive FlashCards")
        self.resize(1000, 600)
        self.setup_stylesheets()
        self.focus_2.connect(self.on_focus)
        
        
    def focusInEvent(self, event):
        print("Window gained focus")
        self.focused_in_window.emit()
        
    def on_focus(self):
        print("Signal received: Window focused!")
    
    def focusInEvent(self, event):
        print("Window gained focus")
        self.focus_2.emit()  # Emit signal
        super().focusInEvent(event)  # Call parent method
    

    def add_widgets_to_window(self, *widgets):
        grid_layout = GridLayout(*widgets, window=self.window)
        central_widget = Widget(grid_layout)
        self.setCentralWidget(central_widget)
        return self

    def show_window(self):
        self.show()
        
    def setup_stylesheets(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a0d1c;
            }
            
            
            QLabel {
                background-color: #AAAAAA;
            }
        """)

