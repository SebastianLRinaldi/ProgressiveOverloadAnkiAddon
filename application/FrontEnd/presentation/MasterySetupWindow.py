
from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.FrontEnd.C_Grouper.TabGroupInitializations.TabGroupInitialization import *
from application.FrontEnd.C_Grouper.WidgetGroupInitializations.WidgetGroupInitialization import *
from application.FrontEnd.C_Grouper.SpliterGroupInitializations.SpliterGroupInitialization import *
from application.FrontEnd.D_WindowFolder.WindowInitializations.windowInitialization import *
from application.FrontEnd.E_combiner.connections import *




"""
The user experince will be just assign how many levels you want to each progression
- later we will make it possible to reorder,
- later later makes sense to also be able to add and remove
- later later later we can edit in the preview
    - would need to either have it opne a html editor, the default editor
        or find the addon that allows editing fields during review (it edits cards feilds not template edit)
    - Make it so that you can drag and drop fields in top or on bottom card
    - You would start with just a blank front and back
        then you have a table of the fields that you can drop in   
"""
def MasterySetupWindow():
        window.add_widgets_to_window(
                
                middleSplit.add_widgets_to_spliter(
                    
                    # See if spliter or tabs look cleaner 
                    deck_setup.add_widgets_to_group(
                        available_decks_tree,
                        deck_status,
                        toggle_deck_connection,
                    ),
                    
                    
                    note_tag_setup.add_widgets_to_group(
                        note_type_drop_down,
                        template_levels_list,
                        tag_prefix_edit,
                        tag_prefix_with_level,
                        save_note_type_mastery_button
                    ),
                    

                    # Need to add a total level count below the list
                    # Along with the max and min prefix_level at the bottom
                    
                    
                    # template_level_setup.add_widgets_to_group(
                    #     tag_prefix_edit,
                    #     tag_prefix_with_level,
                    #     save_note_type_mastery_button
                    # ),
                )
            )
        
        window.show()