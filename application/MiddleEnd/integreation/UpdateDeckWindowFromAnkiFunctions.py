from collections import defaultdict
from typing import Dict

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



class StorageMaster():
    def __init__(self):
        self.decks = None
        
    def get_decks(self):
        return self.decks
    
    def set_decks(self, decks):
        self.decks = decks

storeageMaster = StorageMaster()



def build_tree_model(deck_node, parent_item):
    """ Recursively builds the tree model from DeckTreeNode """
    item = QStandardItem(deck_node.name)
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
    print(get_decks_from_anki())
    
    root_deck = get_decks_from_anki()
    available_decks_tree.setHeaderHidden(True)
    available_decks_tree.setModel(get_tree_model(root_deck))
    available_decks_tree.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
    available_decks_tree.expandAll()
    
    
    # model = QStandardItemModel()
    # model.setHorizontalHeaderLabels(["Decks"])
    
    # root_node = model.invisibleRootItem()
    # populate(root_node, get_decks_from_anki())
    # available_decks_tree.setModel(model)

    
    # tree = {}
    # for index, entry in enumerate(get_decks_from_anki()):
    #     print(f" {index} - {entry.name} | {entry.id}")
        
    #     parts = entry.name.split("::")
    #     print(f"\t {parts}")
    #     current = tree
    #     for part in parts:
    #         if part not in current:
    #             current[part] = {}
    #         current = current[part]
            
    # print(tree)
    # return tree


    
    
    
    
    
    # """ Populates the tree widget with decks and their statuses. """
    # available_decks_tree.clear()
    # decks = convert_anki_decks_to_correct_format(get_decks_from_anki())
    # # print(get_decks_from_anki())
    # for parent_deck, children in decks.items():
    #     parent_item = QTreeWidgetItem([parent_deck])
    #     update_item_color(parent_item, any(children.values()))  # Parent is "connected" if any child is
    #     available_decks_tree.addTopLevelItem(parent_item)

    #     for child_deck, is_connected in children.items():
    #         child_item = QTreeWidgetItem([child_deck])
    #         child_item.setData(0, Qt.ItemDataRole.UserRole, (parent_deck, child_deck))  # Store hierarchy
    #         update_item_color(child_item, is_connected)
    #         parent_item.addChild(child_item)

    # available_decks_tree.expandAll()  # Expand all by default


    
    
    
def update_item_color(item, is_connected):
    """ Sets the item's text color based on connection status. """
    item.setForeground(0, QColor("green") if is_connected else QColor("red"))
    
    
def update_status():
    """ Updates the status label and button based on selection. """
    decks = storeageMaster.get_decks()
    
    selected_items = available_decks_tree.selectedItems()
    if selected_items:
        item = selected_items[0]
        parent_deck, child_deck = item.data(0, Qt.ItemDataRole.UserRole) or (item.text(0), None)
        is_connected = decks[parent_deck][child_deck] if child_deck else any(decks[parent_deck].values())

        deck_status.setText(f"{parent_deck + ' > ' + child_deck if child_deck else parent_deck}: {'Connected' if is_connected else 'Disconnected'}")
        toggle_deck_connection.setText("Disconnect" if is_connected else "Connect")
        toggle_deck_connection.setEnabled(True)
    else:
        deck_status.setText("Select a deck")
        toggle_deck_connection.setEnabled(False)

def toggle_connection():
    """ Toggles connection state of selected deck and updates UI. """
    decks = storeageMaster.get_decks()
    
    selected_items = available_decks_tree.selectedItems()
    if selected_items:
        item = selected_items[0]
        parent_deck, child_deck = item.data(0, Qt.ItemDataRole.UserRole) or (item.text(0), None)

        if child_deck:
            # Toggle single child deck
            decks[parent_deck][child_deck] = not decks[parent_deck][child_deck]
        else:
            # Toggle entire parent deck (all children)
            new_state = not any(decks[parent_deck].values())  # Invert state based on current
            decks[parent_deck] = {deck: new_state for deck in decks[parent_deck]}

        populate_tree()
        update_status()
