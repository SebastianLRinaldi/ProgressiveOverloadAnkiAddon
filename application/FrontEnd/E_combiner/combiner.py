from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.FrontEnd.C_Grouper.TabGroupInitializations.TabGroupInitialization import *
from application.FrontEnd.C_Grouper.WidgetGroupInitializations.WidgetGroupInitialization import *
from application.FrontEnd.C_Grouper.SpliterGroupInitializations.SpliterGroupInitialization import *
from application.FrontEnd.D_WindowFolder.WindowInitializations.windowInitialization import *
from application.FrontEnd.E_combiner.connections import *

"""
Basically want to see the nested widgets and tabs and groups
- also fix it so that it sasys widgets not widges
        exploreTab.add_widges_to_tab(
                    playerControls.add_widges_to_group(
                        button,
                        label,
                        table
                    ),
                    title="Search")


"""


class combiner():
    def __init__(self):
        
        window.add_widgets_to_window(
            
            middleSplit.add_widgets_to_spliter(
                
                note_tag_setup.add_widgets_to_group(
                    note_type_drop_down,
                    set_min_level,
                    set_max_level,
                    tag_prefix_edit,
                    example_tag_with_prefix
                ),
                
                template_level_setup.add_widgets_to_group(
                    template_levels_list,
                    save_note_type_mastery_button
                ),
            )
        )
        window.show_window()






# class combiner():
#     def __init__(self):
        
#         window.add_widgets_to_window(
            
#             middleSplit.add_widgets_to_spliter(
                
#                 calendar_widget,
                
#                 topTab.add_groups_as_tabs(
                    
#                     exploreTab0.add_widgets_to_group(
#                         list_widget,
#                     ),
                    
#                     playerControls.add_widgets_to_group(
#                         button, 
#                     ),
#                 ),
                
#                 bottomTab.add_groups_as_tabs(
                    
#                         exploreTab1.add_widgets_to_group(
#                             text_edit, 
#                         ),
                        
#                         exploreTab2.add_widgets_to_group(
#                             radio_button,
#                             label,  
#                         ),
                        
#                         exploreTab3.add_widgets_to_group(
#                             check_box,
#                         )
#                     )
#             )
#         )
#         window.show_window()
        
        
        
"""
class combiner():
    def __init__(self):

        window.add_widgets_to_window(
            calendar_widget,
            check_box,
            exploreTab.add_widges_to_tab(
                text_edit,
                exploreTab1.add_widges_to_tab(
                    label,
                    playerControls.add_widgets_to_group(
                        button,
                        ),
                ),
            ),
            exploreTab.add_widges_to_tab(
                list_widget,
            ),
            exploreTab2.add_widges_to_tab(
                radio_button,
            )
        )
        window.show_window()
""" 