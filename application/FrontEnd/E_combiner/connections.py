from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import update_win_info_from_combobox, add_note_types_to_comboBox, save_window_info_to_json
from application.FrontEnd.D_WindowFolder.WindowInitializations.windowInitialization import *
from application.MiddleEnd.integreation.UpdateViewerFunctions import preview_cards_with_template
from application.MiddleEnd.integreation.UserTemplateInfoFunctions import *
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import refreash_template_tag_with_prefix, get_selected_note_type_from_drop_down #set_card_type_on_add 
from application.MiddleEnd.integreation.UpdateDeckWindowFromAnkiFunctions import populate_tree, update_status, toggle_connection

available_decks_tree.beforeShow.connect(populate_tree)
available_decks_tree.clicked.connect(update_status)
toggle_deck_connection.clicked.connect(toggle_connection)

note_type_drop_down.beforePopup.connect(add_note_types_to_comboBox)
note_type_drop_down.currentIndexChanged.connect(update_win_info_from_combobox)

tag_prefix_edit.textChanged.connect(lambda: refreash_template_tag_with_prefix(get_selected_note_type_from_drop_down()))
template_levels_list.itemDoubleClicked.connect(preview_cards_with_template)

#! Why is this note circular import
save_note_type_mastery_button.clicked.connect(save_window_info_to_json)



# dbug_info.returnPressed.connect(lambda: set_card_type_on_add(dbug_num.currentText(), dbug_info.text()))



