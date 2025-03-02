class DeckItem():
    def __init__(self, deck_name: str, deck_id: int):
        self.deck_name = deck_name
        self.deck_id = deck_id
        self.notes = []

    def add_note(self, note):
        self.notes.append(note)

    def __str__(self) -> str:
        """Return string representation of the deck."""
        return f"Deck: {self.deck_name} | ID: {self.deck_id} | Notes: {len(self.notes)}"


class TagCreationSettings():
    def __init__(self, num_of_levels_per_template: int, tag_prefix: str, start_number: int):
        self.num_of_levels_per_template = num_of_levels_per_template
        self.tag_prefix = tag_prefix
        self.start_number = start_number

    def generate_tags(self):
        """Generate level tags based on settings."""
        return [f"{self.tag_prefix}{i}" for i in range(self.start_number, self.start_number + self.num_of_levels_per_template)]

    def __str__(self) -> str:
        """Return string representation of tag settings."""
        return f"Tags: {self.tag_prefix}{self.start_number} - {self.tag_prefix}{self.start_number + self.num_of_levels_per_template - 1}"


class NoteTypeItem():
    def __init__(self, note_type_name: str, note_type_id: int, tag_settings: TagCreationSettings=None):
        self.note_type_name = note_type_name
        self.note_type_id = str(note_type_id)
        self.tag_settings = tag_settings

    def __str__(self) -> str:
        """Return string representation of the note type."""
        return f"Note: {self.note_type_name} | ID: {self.note_type_id} | {self.tag_settings}"

class TemplateItem():
    def __init__(self, template_name: str, template_id: int, min_lvl: int=-1, max_lvl: int=-9):
        self.template_name = template_name
        self.template_id = template_id
        self.min_lvl = min_lvl
        self.max_lvl = max_lvl

    def __str__(self) -> str:
        """Return string representation of the item."""
        return f"{self.template_name} | ID: {self.template_id} | ({self.min_lvl}-{self.max_lvl})"


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
    QComboBox,
    QSpinBox,
    
)

# class EditableTemplateListItem(QWidget):
#     def __init__(self, template_name="", level=-1):
#         super().__init__()
#         layout = QHBoxLayout()
#         self.setLayout(layout)
        
#         # Card field
#         self.card_input = QLineEdit()
#         self.card_input.setPlaceholderText("template_name")
#         self.card_input.setText(template_name)
#         layout.addWidget(self.card_input)
        
#         # Level field
#         self.level_spinbox = QSpinBox()
#         # self.level_spinbox.setMinimum(1)
#         # self.level_spinbox.setMaximum(10)
#         self.level_spinbox.setValue(level)
#         layout.addWidget(self.level_spinbox)


class EditableTemplateListItem(QWidget):
    def __init__(self, template_index=-1, template_name="", template_id="", template_reps=-1, state="NEW"):
        super().__init__()
        
        
        self.template_index = template_index
        self.template_name = template_name
        self.template_id = template_id
        self.template_reps = template_reps
        self.initCardState = state
        
        self.data = {
            'index': template_index,
            'name': template_name,
            'id': template_id,
            'reps': template_reps,
            'initState': state
            }
        
        
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        #Template index field
        self.index = QLabel()
        self.index.setText(f"Level: {self.template_index}")
        layout.addWidget(self.index)
        
        # # Template name field
        # self.template_name_input = QLineEdit()
        # self.template_name_input.setText(template_name)
        # layout.addWidget(self.template_name_input)
        
        # Template name field
        self.template_name_input = QLabel()
        self.template_name_input.setText(self.template_name)
        layout.addWidget(self.template_name_input)
        
        #Template id field
        self.id = QLabel()
        self.id.setText(f"{self.template_id}")
        layout.addWidget(self.id)
        
        # Level field
        self.reps_spinbox = QSpinBox()
        self.reps_spinbox.setValue(self.template_reps)
        layout.addWidget(self.reps_spinbox)
        
        # State ComboBox
        self.state_combobox = QComboBox()
        self.state_combobox.addItems(["AUTO", "NEW", "LEARNING", "REVIEW", "RELEARNING"])
        self.state_combobox.setCurrentText(state)
        layout.addWidget(self.state_combobox)
        
        # Could also just do widget.reps_spin_box.value()
        self.reps_spinbox.valueChanged.connect(self.update_reps)
        self.state_combobox.currentTextChanged.connect(self.update_state)
        
    def getAllData(self):
        return self.data
    
    def update_reps(self, value):
        """Update template_reps when QSpinBox value changes."""
        self.template_reps = value  # Update the attribute
        self.data['reps'] = value  # Ensure data dictionary is updated
        
    def update_state(self, state):
        """Update template_reps when QSpinBox value changes."""
        self.initCardState = state
        self.data['initState'] = state        