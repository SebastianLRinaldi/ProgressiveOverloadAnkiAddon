from PyQt6.QtWidgets import QListWidgetItem
# from aqt import mw

# from application.MiddleEnd.MasteryDatahandler import MasteryDataHandler
# from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
# from application.MiddleEnd.integreation.MasterTypes import *





class NoteStructureEditor:
    def __init__(self, data=None):
        
        
        # On init need to load it?
        # or do we need to merege the masterDataHandler?
        # no these are just setters for data tbh
        # MasterDatahandler also manages loading and saving from a dict
        # What this class does it handles adding new info
        # im pretty sure it handles updating too? 
        # Should run the other file of this and check
        
        
        self.data = data or {
            "Note_type_name": 
                {
                "tag_creation": 
                    {
                    "start": 0,
                    "card_type_level_count": 10,
                    "prefix": "level_"
                    },
                "template_levels":
                    {
                    
                    }
            }
        }
        
        
    def get_last_template_stored(self):
        template_levels = self.data["Note_type_name"]["template_levels"]
        if len(template_levels.keys()) != 0 :
            last_template_name = next(reversed(template_levels.keys()))
        else:
            last_template_name = None
        return last_template_name
        

            
    def add_template_level_manual_level_count(self, level_name, manual_card_type_level_count):
        """Add a new template level with calculated end"""
        template_name = self.get_last_template_stored()
        card_type_level_count = manual_card_type_level_count
        
        
        if template_name is not None:
            # start = self.data["Note_type_name"]["template_levels"][template_name]["start"]
            prev_template_end = self.data["Note_type_name"]["template_levels"][template_name]["end"]
            start = prev_template_end + 1
            end = prev_template_end + card_type_level_count
            
            self.data["Note_type_name"]["template_levels"][level_name] = {
                "start": start,
                "end": end
            }
            
        else:
            # Add the new level with start and end based on card_type_level_count and tag level config
            
            start = self.data["Note_type_name"]["tag_creation"]["start"]
            end = start + card_type_level_count - 1 
            
            self.data["Note_type_name"]["template_levels"][level_name] = {
                "start": start,
                "end": end  
            }
        
    # Something like this
# from application.MiddleEnd.integreation.UserTemplateInfoFunctions import get_template_all_data
# def save_template_mastery_to_json():
    # editor = NoteStructureEditor()
    # for template in templates: 
    #     editor.add_template_level_manual_level_count(template_name,reps)
        
        
        
        
    
editor = NoteStructureEditor()
# print(editor.get_last_template_stored())
editor.add_template_level_manual_level_count("template_name_1",10)
editor.add_template_level_manual_level_count("tempalte_name_1.5", 5)
editor.add_template_level_manual_level_count("template_name_2",10)
editor.add_template_level_manual_level_count("template_name_3",10)
editor.add_template_level_manual_level_count("tempalte_name_3.5", 5)

print(editor.data)
