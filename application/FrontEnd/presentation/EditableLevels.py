"""
We can remove this once we save teh add and remove items functions
"""


import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QSpinBox
)

class EditableItem(QWidget):
    def __init__(self, card_text="", level=1):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Card field
        self.card_input = QLineEdit()
        self.card_input.setPlaceholderText("Card")
        self.card_input.setText(card_text)
        layout.addWidget(self.card_input)
        
        # Level field
        self.level_spinbox = QSpinBox()
        self.level_spinbox.setMinimum(1)
        self.level_spinbox.setMaximum(10)
        self.level_spinbox.setValue(level)
        layout.addWidget(self.level_spinbox)

class ItemListWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editable Item List")
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Add buttons
        add_empty_btn = QPushButton("Add Empty Item")
        add_filled_btn = QPushButton("Add Sample Item")
        layout.addWidget(add_empty_btn)
        layout.addWidget(add_filled_btn)
        
        # Connect signals
        add_empty_btn.clicked.connect(self.add_empty_item)
        add_filled_btn.clicked.connect(self.add_sample_item)
        
        # List widget
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        
        # Sample data
        self.add_sample_item()

    def add_empty_item(self):
        """Add an empty EditableItem"""
        item_widget = EditableItem()
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, item_widget)

    def add_sample_item(self):
        """Add a filled EditableItem"""
        item_widget = EditableItem("Sample Card", 5)
        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, item_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemListWindow()
    window.show()
    sys.exit(app.exec())