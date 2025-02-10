from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import update_win_info_from_combobox, add_note_types_to_comboBox, save_window_info_to_json
from application.FrontEnd.D_WindowFolder.WindowInitializations.windowInitialization import *
from application.MiddleEnd.integreation.UpdateViewerFunctions import preview_cards_with_template
from application.MiddleEnd.integreation.UserTemplateInfoFunctions import *
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import refreash_template_tag_with_prefix, get_selected_note_type_from_drop_down 


# save_note_type_mastery_button.clicked.connect(lambda: label.setText("Hello"))




# note_type_drop_down.focused_in.connect(add_note_types_to_comboBox)
# note_type_drop_down.focused_out.connect(add_note_types_to_comboBox)
note_type_drop_down.beforePopup.connect(add_note_types_to_comboBox)
note_type_drop_down.highlighted.connect(update_win_info_from_combobox)

tag_prefix_edit.textChanged.connect(lambda: refreash_template_tag_with_prefix(get_selected_note_type_from_drop_down()))


# tag_prefix_edit.editingFinished.connect(lambda: refreash_template_tag_with_prefix(get_selected_note_type_from_drop_down()))


# note_type_drop_down.activated.connect(update_win_info_from_combobox)

# window.focused_in_window.connect(add_note_types_to_comboBox)


template_levels_list.itemDoubleClicked.connect(preview_cards_with_template)

# This will be some function from UpdateJsonFromWindowFunction
# Will there be circular import?
save_note_type_mastery_button.clicked.connect(save_window_info_to_json)











# prev_btn.clicked.connect(show_previous_card)
# next_btn.clicked.connect(show_next_card)