# from application.MiddleEnd.MasteryDatahandler import MasteryDataHandler
# from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
# from application.MiddleEnd.integreation.MasterTypes import *
from application.MiddleEnd.integreation.UserTemplateInfoFunctions import *

import aqt
from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from anki.cards import Card
from anki.notes import Note
from aqt import gui_hooks
import anki.template
from anki.template import TemplateRenderOutput, TemplateRenderContext
from anki.hooks import wrap
from aqt.utils import showInfo, showInfo, qconnect
from anki.hooks import addHook
from anki import hooks

from application.MiddleEnd.MasteryDatahandler import masteryDatahandler

#####################################
# Get Info from Anki
#####################################

def add_note_type_item(name, id):
    item = NoteTypeItem(name, id)
    note_type_drop_down.addItem(name, item)
    
    if masteryDatahandler.is_note_type_in_mastery(id):
        note_type_drop_down.setItemData(note_type_drop_down.count() - 1, QBrush(QColor("green")), Qt.ItemDataRole.ForegroundRole)

def add_note_types_to_comboBox():
    note_type_drop_down.clear()
    
    note_types = mw.col.models.all_names_and_ids()
    
    for note_type in note_types:
        add_note_type_item(note_type.name, note_type.id)

def get_note_type_templates(note_type_item: NoteTypeItem):
        # print(f"Loading data for: {note_type_item.note_type_name} (ID: {note_type_item.note_type_id})")
        # mw.col.models.get(noteitem.note_id) --> dict_keys(['id', 'name', 'type', 'mod', 'usn', 'sortf', 'did', 'tmpls', 'flds', 'css', 'latexPre', 'latexPost', 'latexsvg', 'req'])
        
        # mw.col.models.get(noteitem.note_id)["tmpls"][0].keys() --> dict_keys(['name', 'ord', 'qfmt', 'afmt', 'bqfmt', 'bafmt', 'did', 'bfont', 'bsize', 'id'])
        templates = mw.col.models.get(note_type_item.note_type_id)["tmpls"]
        return templates

def get_decks_from_anki():
    return mw.col.decks.deck_tree() 
    # return mw.col.decks.all_names_and_ids()
    # return mw.col.decks.all()
    
    
# from anki.consts import CARD_TYPE_NEW, CARD_TYPE_LRN, CARD_TYPE_REV, CARD_TYPE_RELEARNING
# class CardState(Enum):
#     NEW = CARD_TYPE_NEW
#     LEARNING = CARD_TYPE_LRN
#     REVIEW = CARD_TYPE_REV
#     RELEARNING = CARD_TYPE_RELEARNING
    
# def set_card_type_on_add(state: str, id:str, card: Card=None):
#     print(f"{state}{type(state)} | {id}{type(id)}")
#     try:
#         temp_card = mw.col.get_card(int(id))
#         temp_card.type = CardState[state].value
#         mw.col.update_card(temp_card)
#         print(f"TEMP CARD: {temp_card} | TYPE: {temp_card.type} - SAVED")
#         mw.deckBrowser.refresh()
#     except Exception as e:
#         print(f"STATE ERROR: {e}")



#####################################
# Get Info from MasteryData
#####################################
# "C:\\Users\\epics\\AppData\\Roaming\\Anki2\\addons21\\ProgressiveOverloadAnkiAddon\\user_files\\masteryData_test.json"
# masteryDatahandler = MasteryDataHandler("C:\\Users\\epics\\AppData\\Roaming\\Anki2\\addons21\\ProgressiveOverloadAnkiAddon\\user_files\\masteryDataWorking.json")





# TODO loading the templates with defaults seems to use dulipcate code so I could clean this up
def load_templates_from_Json(templates: List, note_type_item: NoteTypeItem):
    # Check if note_type has templates stored in MasteryData
    # If it does store the info
    # else default values
    # Get rep count for templates from the note type from MasteryDataJson

    for index, template in enumerate(templates):
        # print(template)
        template_name = template["name"]
        id = template["id"]
        rep_count = 0
        init_card_state = "AUTO" 
        
        if masteryDatahandler.is_template_in_note_type(note_type_item.note_type_id, template_name):
            saved_rep_count = masteryDatahandler.get_note_type_template_rep_count(note_type_item.note_type_id, template_name)
            rep_count = saved_rep_count
            
            saved_init_card_state =  masteryDatahandler.get_note_type_template_init_card_state(note_type_item.note_type_id, template_name)
            init_card_state = saved_init_card_state
        
        item = EditableTemplateListItem(index, template_name, id, rep_count, init_card_state)
        template_levels_list.addMasteryItem(item)
        # print(f"LOADED FROM JSON | {index, template_name, id, rep_count}")
    
def load_templates_with_defaults(templates: List):
    for index, template in enumerate(templates):
        # print(template)
        template_name = template["name"]
        id = template["id"]
        rep_count = 5
        template_init_state = "AUTO" 
        item = EditableTemplateListItem(index, template_name, id, rep_count, template_init_state)
        template_levels_list.addMasteryItem(item)
    
def load_template_list(templates, note_type_item: NoteTypeItem):
    
    template_levels_list.clear()
    
    # print(type(note_type_item))
    # print(note_type_item)
    # print(f"IS IN MASTERYDATA: {masteryDatahandler.is_note_type_in_mastery(note_type_item.note_type_id)}")
    
    if masteryDatahandler.is_note_type_in_mastery(note_type_item.note_type_id):
        load_templates_from_Json(templates, note_type_item)
        
    else:
        load_templates_with_defaults(templates)


def refreash_template_tag_with_prefix(note_type_item: NoteTypeItem):
    tag_prefix = tag_prefix_edit.text()
    
    if masteryDatahandler.is_note_type_in_mastery(note_type_item.note_type_id):
        max_tag_level = len(masteryDatahandler.get_all_rep_count_tags(note_type_item.note_type_id)) - 1
    else:
        max_tag_level = "XXX"
    tag_prefix_with_level.setText(f"{tag_prefix}{max_tag_level}")


def load_template_tag_prefix(note_type_item: NoteTypeItem):
    # Load in tag_prefix
    if masteryDatahandler.is_note_type_in_mastery(note_type_item.note_type_id):
        tag_prefix = masteryDatahandler.get_tag_prefix(note_type_item.note_type_id)
        tag_prefix_edit.setText(tag_prefix)

def load_template_tag_with_prefix(note_type_item: NoteTypeItem):
    # Load in last rep_count_tag
    if masteryDatahandler.is_note_type_in_mastery(note_type_item.note_type_id):
        max_tag_level = len(masteryDatahandler.get_all_rep_count_tags(note_type_item.note_type_id)) - 1
        tag_prefix = masteryDatahandler.get_tag_prefix(note_type_item.note_type_id)
        
    else:
        tag_prefix = tag_prefix_edit.text()
        max_tag_level = "XXX"
        
    tag_prefix_with_level.setText(f"{tag_prefix}{max_tag_level}")
    # print(f"NOTEFOUND: {masteryDatahandler.is_note_type_in_mastery(note_type_item.note_type_id)} TAG: {max_tag_level}")

    
    
def load_all_template_tag_info(note_type_item: NoteTypeItem):
    load_template_tag_prefix(note_type_item)
    load_template_tag_with_prefix(note_type_item)
        



def get_selected_note_type_from_drop_down() -> NoteTypeItem:
    return note_type_drop_down.currentData()


def get_note_type_info(row:int) -> NoteTypeItem:
    # Handle both highlighted and activated signals
    # print(f"row: {row}")
    if row is None:
        # Activated signal was triggered
        result = get_selected_note_type_from_drop_down()
    else:
        # Highlighted signal was triggered
        result = note_type_drop_down.itemData(row)
    return  result


def update_win_info_from_combobox(row: int):
    note_type_item = get_note_type_info(row)
    
    # print(f"get_note_type_info -> {item}")
    
    if note_type_item is not None:
        templates = get_note_type_templates(note_type_item)
        # print(f"get_note_type_templates-> {templates}")
        # print(f"note_type_item2 -> {row}")
        load_template_list(templates, note_type_item)
        load_all_template_tag_info(note_type_item)
        
        
        

def save_window_info_to_json():
    itemWidgets = get_templates_with_level_info()
    
    selectedNoteTypeItem = get_selected_note_type_from_drop_down()
    # print(f"\nBEFORE CLEAN {masteryDatahandler.data}\n")
    masteryDatahandler.clear_previous_template_data(selectedNoteTypeItem.note_type_id)
    
    # print(f"\nBEFORE SAVE {masteryDatahandler.data}\n")
    for index, itemWidget in enumerate(itemWidgets):
        template_name = get_template_name(itemWidget)
        rep_count = get_template_reps(itemWidget)
        init_card_state = get_template_state(itemWidget)
        # print(f"\t{template_name} | reps:{rep_count}")
        
        masteryDatahandler.add_template_level_manual_level_count(selectedNoteTypeItem, template_name, rep_count, init_card_state)
        
        masteryDatahandler.save_json()
        
    save_prefix_and_rep_count_tags(selectedNoteTypeItem)
    
    
def save_prefix_and_rep_count_tags(selectedNoteTypeItem: NoteTypeItem):
    note_type_id = selectedNoteTypeItem.note_type_id
    
    tag_prefix = tag_prefix_edit.text()
    rep_count_tags = masteryDatahandler.create_rep_count_tags(note_type_id, tag_prefix)
    
    masteryDatahandler.set_tag_prefix(note_type_id, tag_prefix)
    masteryDatahandler.set_rep_count_tags(note_type_id, rep_count_tags)
    
    refreash_template_tag_with_prefix(selectedNoteTypeItem)
    
    masteryDatahandler.save_json()
        
    
        
    # print(f"\nAFTER {masteryDatahandler.data}\n")
    



