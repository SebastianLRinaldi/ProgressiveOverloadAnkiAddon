from collections import defaultdict
from typing import Dict
from enum import Enum
from anki.decks_pb2 import DeckNameId, DeckTreeNode

from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import *

decks = {
            "Japanese": {
                "N5": True,
                    "Japanese_town": 
                        {
                        "N5.5": True,
                        },
                "N4": False,
                "Kanji Practice": True
            },
            "Grammar": {
                "Basic": False,
                "Intermediate": True
            }
        }

class DeckData(Enum):
    ID = Qt.ItemDataRole.UserRole
    IN_MASTERYDATA = Qt.ItemDataRole.UserRole+1

class StorageMaster():
    def __init__(self):
        self.decks = None
        
    def get_decks(self):
        return self.decks
    
    def set_decks(self, decks):
        self.decks = decks

storeageMaster = StorageMaster()


def build_tree_model(deck_node:DeckTreeNode, parent_item: QStandardItem):
    """ Recursively builds the tree model from DeckTreeNode """
    # Would need to check first if the deck is in MasteryData when we do this step
    item = QStandardItem(deck_node.name)
    item.setData(str(deck_node.deck_id), DeckData.ID.value)
    if masteryDatahandler.is_deck_in_mastery(str(deck_node.deck_id)):
        item.setData(True, DeckData.IN_MASTERYDATA.value)
        item.setForeground(QColor("green"))
    else:
        item.setData(False, DeckData.IN_MASTERYDATA.value)
    
    parent_item.appendRow(item)
    
    for child in deck_node.children:
        build_tree_model(child, item)

def get_tree_model(root_deck):
    """ Creates a tree model from the root deck node """
    model = QStandardItemModel()
    # model.setHorizontalHeaderLabels(["Deck Name"])
    build_tree_model(root_deck, model.invisibleRootItem())
    return model


def populate_tree():
    # print(get_decks_from_anki())
    root_deck = get_decks_from_anki()
    available_decks_tree.setHeaderHidden(True)
    available_decks_tree.setModel(get_tree_model(root_deck))
    available_decks_tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    available_decks_tree.expandAll()
    
    
def get_current_item() -> QStandardItem:
    result = None
    
    index = available_decks_tree.currentIndex()
    model = available_decks_tree.model()
    
    if isinstance(model, QStandardItemModel):
        item = model.itemFromIndex(index)
        if item:
            result = item
    return result    

def update_status():
    """ Updates the MasteryData, status label, and button based on selection. """
    item = get_current_item()
    
    if item:
        if item.data(DeckData.IN_MASTERYDATA.value) == True:
            deck_name = item.text()
            deck_id = item.data(DeckData.ID.value)
            masteryDatahandler.set_deck(deck_id, deck_name)
            deck_status.setText("Connected To Mastery")
        else:
            deck_id = item.data(DeckData.ID.value)
            masteryDatahandler.del_deck(deck_id)
            deck_status.setText("Disconnected From Mastery")
            
        masteryDatahandler.save_json()

def toggle_connection():
    """ Toggles connection state of selected deck and updates UI. """
    item = get_current_item()
    
    if item:
        if item.data(DeckData.IN_MASTERYDATA.value) == False:
            item.setData(True, DeckData.IN_MASTERYDATA.value)
            item.setForeground(QColor("green"))
        else:
            item.setData(False, DeckData.IN_MASTERYDATA.value)
            item.setForeground(QColor("white"))
            
        update_status()
        
        
    

    # available_decks_tree.dataChanged.emit(index, index)
    
    # item = available_decks_tree.itemFromIndex(index)
    
    
    # item.setBackground(QColor("lightblue"))

        # available_decks_tree.
        
        # if item.data(Qt.ItemDataRole.UserRole + 1):
        #     item.sata(QBrush(Qt.GlobalColor.red), Qt.ItemDataRole.ForegroundRole)
        #     item.setForeground(Qt.GlobalColor.red)  # Change text color to red
        #     # item.setBackground(Qt.GlobalColor.yellow)  # Uncomment for background color

    # populate_tree()
    # update_status()
