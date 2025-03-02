
from PyQt6.QtWidgets import QListWidgetItem
from aqt import mw

from application.MiddleEnd.MasteryDatahandler import MasteryDataHandler
from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.MiddleEnd.integreation.MasterTypes import *

def get_templates_with_level_info() -> List[EditableTemplateListItem]:
    number_of_items = template_levels_list.count()
    itemWidgets = []
    for index in range(number_of_items):
        # Our items in the list widget store nothing but the EditableTemplateListItem widget
        item = template_levels_list.item(index)
        # To really get the data stores we need to get the widget
        widget = template_levels_list.itemWidget(item)

        itemWidgets.append(widget)
        
    return itemWidgets



def get_template_index(itemWidget: EditableTemplateListItem):
    return itemWidget.template_index

def get_template_name(itemWidget: EditableTemplateListItem):
    return itemWidget.template_name

def get_template_id(itemWidget: EditableTemplateListItem):
    return itemWidget.template_id

def get_template_reps(itemWidget: EditableTemplateListItem):
    return itemWidget.template_reps

def get_template_state(itemWidget: EditableTemplateListItem):
    return itemWidget.initCardState

def get_template_all_data(itemWidget: EditableTemplateListItem):
    return itemWidget.getAllData()