from application.FrontEnd.B_WidgetsFolder.WidgetConfigurations.widgetConfiguration import *
from application.FrontEnd.B_WidgetsFolder.WidgetConfigurations.ankiWidgetConfiguration import *
from aqt.webview import AnkiWebView


# deck_options = ComboBox()
# connected_decks = ListWidget()
# connect_deck_button = Button(text="Connect Deck")
# disconnect_deck_button = Button(text="Disconnect Deck")
available_decks_tree = TreeViewWidget()
deck_status = Label(text="Select a deck")
toggle_deck_connection = Button(text="Connect/Disconnect")



##########################
note_type_drop_down = ComboBox(widgetRow=0, widgetCol=0, widgetRowSpan=1, widgetColSpan=2)
template_levels_list = ListWidget()

# set_min_level = SpinBox(0, widgetRow=1, widgetCol=0)
# set_max_level = SpinBox(10, widgetRow=1, widgetCol=1)

# TextEdit
tag_prefix_edit = LineEdit(text="Set Tag prefix EX: level_")

# Label
tag_prefix_with_level = Label(text="EX: PREFIX_###")

# Button
save_note_type_mastery_button = Button(text="SAVE MASTERY FOR NOTE TYPE", widgetRowSpan=1, widgetColSpan=2)
###############################


web_view = AnkiViewer(widgetRowSpan=1, widgetColSpan=2)

prev_btn = Button("PREV CARD")
next_btn = Button("NEXT CARD")







