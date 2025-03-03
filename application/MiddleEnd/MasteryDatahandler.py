import json
from typing import Optional, Any, Union, Dict
from pathlib import Path
from application.MiddleEnd.integreation.MasterTypes import NoteTypeItem
from aqt.qt import QAction
from aqt.operations.collection import CollectionOp
from aqt import mw
from aqt.utils import tooltip

class MasteryDataHandler:
    def __init__(self):
        """
        Initialize the MasteryDataHandler class.
        
        Args:
            json_path: Path to JSON file (optional). If provided, loads the file immediately.
        """
        self.json_path = None
        self.data: Dict[str, Any] = {}
    
    def load_config(self, config: dict):
        path = config.get("mastery_data_path", "Default")
        if path:
            self.load_json(path)
            self.check_path()
    

    def load_json(self, path: Union[str, Path]) -> None:
        """Load JSON data from file."""
        with open(path, 'r', encoding='utf-8') as f:
            self.json_path = path 
            self.data = json.load(f) or {}
    
    def check_path(self):
        mw.statusBar().showMessage(f"CurrentPath: {self.json_path}", 10000)
        # tooltip(f"CurrentPath: {path}")
        # print(config)
    
    def save_json(self) -> None:
        """Save JSON data to file."""
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
            
            
            
    def get_mastery_data_path(self):
        """Retrieve the deck name from the add-on's configuration."""
        config = mw.addonManager.getConfig(__name__)
        print(config)
        # print("var is", config['mastery_data_path'])
        # print(mw.col.all_config())        
        # path = mw.col.get_config("mastery_data_path", "Default")
        # return path

    # def set_target_deck_from_config():
    #     target_deck = get_mastery_data()

    # def show_target_deck(self):
    #     target_deck = get_mastery_data()
    #     showInfo(f"Config:{target_deck} \n Enabled: {target_deck}")
    
    # "C:\\Users\\epics\\AppData\\Roaming\\Anki2\\addons21\\ProgressiveOverloadAnkiAddon\\user_files\\masteryData_test.json"
    # "C:\\Users\\epics\\AppData\\Roaming\\Anki2\\addons21\\ProgressiveOverloadAnkiAddon\\user_files\\masteryDataWorking.json"


    def on_config_update(self, config_data: dict):
        """Function triggered when config updates."""
        updated_path = config_data.get("mastery_data_path", "Default")
        self.load_json(updated_path)
        print(updated_path)
        self.check_path()

    
    ####################################
    # Deck Checkers
    ####################################
    def is_deck_in_mastery(self, deck_id: str) -> bool:
        return str(deck_id) in self.data.get("decks", {})
    
    ####################################
    # Deck Getters
    ####################################
    def get_deck(self, deck_id: str) -> Dict[str, Any]:
        try:
            result = self.data["decks"][str(deck_id)]
        except Exception as e:
            result = None
        return result
    

    ####################################
    # Deck Setters
    ####################################
    def set_deck(self, deck_id: str, deck_name: str) -> None:
        self.data["decks"][deck_id] = {
                "deck_id": deck_id,
                "deck_name": deck_name
                } 
        
    ####################################
    # Deck Delete
    ####################################
    def del_deck(self, deck_id: str) -> None:
        print(f"ID to Del: {type(deck_id)} | {deck_id} | inMaster: {self.is_deck_in_mastery(deck_id)}")
        if self.is_deck_in_mastery(deck_id):
            del self.data["decks"][str(deck_id)]
    
    
    ####################################
    # Check if there is a note_type
    ####################################
    def is_note_type_in_mastery(self, note_type_id: str) -> bool:
        return str(note_type_id) in self.data.get("note_types", {})
    
    ####################################
    # Get all info about a notetypes by note_type_id
    ####################################
    def get_note_type_mastery(self, note_type_id: str) -> Dict[str, Any]:
        try:
            result = self.data["note_types"][str(note_type_id)]
        except Exception as e:
            result = None
        return result
    
    ####################################
    # Get specific info about a note by note_type_id
    ####################################    
    def get_tag_prefix(self, note_type_id: str) -> str:
        try:
            note_info = self.get_note_type_mastery(note_type_id)
            result = note_info["tag_creation_settings"]["tag_prefix"]
        except Exception as e:
            result = None
        return result
    
    def get_start_number(self, note_type_id: str) -> int:
        try:
            note_info = self.get_note_type_mastery(note_type_id)
            result = note_info["tag_creation_settings"]["start_level"]
        except Exception as e:
            result = None
        return result
    
    def get_all_rep_count_tags(self, note_type_id: str) -> list:
        try:
            note_info = self.get_note_type_mastery(note_type_id)
            result = note_info["tag_creation_settings"]["rep_count_tags"]
        except Exception as e:
            result = None
        return result
    
    
    
    ####################################
    # Check if a template is in a note_type
    ####################################
    def is_template_in_note_type(self, note_type_id: str, template_name) -> bool:
        note_type_templates = self.get_note_type_templates(note_type_id)
        return str(template_name) in note_type_templates
    
    
    ####################################
    # Get all info about a template by note_type_id 
    ####################################
    def get_note_type_templates(self, note_type_id: str) -> Dict[str, Any]:
        try:
            note_info = self.get_note_type_mastery(note_type_id)
            result = note_info["templates"]
        except Exception as e:
            result = None
        return result
    
    ####################################
    # Get specific info about a template by note_type_id and template_name
    ####################################
    def get_a_note_type_template(self, note_type_id: str, template_name) -> Dict[str, Any]:
        try:
            note_type_templates = self.get_note_type_templates(note_type_id)
            result = note_type_templates[str(template_name)]
        except Exception as e:
            result = None
        return result
    
    def  get_note_type_template_rep_count(self, note_type_id: str, template_name) -> int:
        try:
            note_type_template = self.get_a_note_type_template(note_type_id, template_name)
            result = note_type_template["template_reps"]
        except Exception as e:
            result = None
        return result
    
    
    def  get_note_type_template_init_card_state(self, note_type_id: str, template_name) -> int:
        try:
            note_type_template = self.get_a_note_type_template(note_type_id, template_name)
            result = note_type_template["init_card_state"]
        except Exception as e:
            result = None
        return result
    
    def  get_note_type_template_min_level(self, note_type_id: str, template_name) -> int:
        try:
            note_type_template = self.get_a_note_type_template(note_type_id, template_name)
            result = note_type_template["min_level"]
        except Exception as e:
            result = None
        return result
    
    def  get_note_type_template_max_level(self, note_type_id: str, template_name) -> int:
        try:
            note_type_template = self.get_a_note_type_template(note_type_id, template_name)
            result = note_type_template["max_level"]
        except Exception as e:
            result = None
        return result
    
    
    
        
    ####################################
    # Set all info about a notetype by note_type_id
    ####################################
    def set_note_type_mastery(self, note_type_id: str, note_info: Dict[str, Any]) -> None:
        self.data["note_types"][note_type_id] = note_info

    ####################################
    # Set specific info about a note by note_type_id
    ####################################
    def set_tag_prefix(self, note_type_id: str, tag_prefix: str) -> None:
        self.get_note_type_mastery(note_type_id)["tag_creation_settings"]["tag_prefix"] = tag_prefix

    def set_start_number(self, note_type_id: str, start_level: int) -> None:
        self.get_note_type_mastery(note_type_id)["tag_creation_settings"]["start_level"] = start_level
        
    def set_rep_count_tags(self, note_type_id: str, rep_count_tags: list[str]) -> None:
        self.get_note_type_mastery(note_type_id)["tag_creation_settings"]["rep_count_tags"] = rep_count_tags

    ####################################
    # Set all templates for a note_type
    ####################################
    def set_note_type_templates(self, note_type_id: str, templates: Dict[str, Any]) -> None:
        self.get_note_type_mastery(note_type_id)["templates"] = templates

    ####################################
    # Set a specific template for a note_type
    ####################################
    def set_a_note_type_template(self, note_type_id: str, template_name, template_info: Dict[str, Any]) -> None:
        self.get_note_type_templates(note_type_id)[template_name] = template_info

    ####################################
    # Set specific info about a template by note_type_id and template_name
    ####################################
    def set_note_type_template_rep_count(self, note_type_id: str, template_name, rep_count: int) -> None:
        self.get_a_note_type_template(note_type_id, template_name)["template_reps"] = rep_count

    def set_note_type_template_min_level(self, note_type_id: str, template_name, min_level: int) -> None:
        self.get_a_note_type_template(note_type_id, template_name)["min_level"] = min_level

    def set_note_type_template_max_level(self, note_type_id: str, template_name, max_level: int) -> None:
        self.get_a_note_type_template(note_type_id, template_name)["max_level"] = max_level
    
    def clear_previous_template_data(self, note_type_id: str):
        if self.is_note_type_in_mastery(note_type_id):
            self.data["note_types"][note_type_id]["templates"] = {}
    
    def get_last_template_stored(self, note_type_id: str):
        # print(self.data)
        
        result = None
        
        if self.is_note_type_in_mastery(note_type_id):
            
            templates = self.data["note_types"][note_type_id]["templates"]
            # print(templates)
            if len(templates.keys()) != 0 :
                result = next(reversed(templates.keys()))
                
                # print(f"\nLTMPNA: {result}\n")
        else:
            result = None
            
        return result
    
    
    def create_rep_count_tags(self, note_type_id: str, tag_prefix: str):
        last_template_name = self.get_last_template_stored(note_type_id)
        rep_count_tags = []
        if last_template_name is not None:
            # start = self.data["note_types"][note_type_id]["templates"][template_name]["start"]
            last_template_max_level = self.data["note_types"][note_type_id]["templates"][last_template_name]["max_level"]
        
            # tag_prefix = self.get_tag_prefix(note_type_id)
            
            for rep in range(last_template_max_level+1):
                rep_count_tags.append(f"{tag_prefix}{rep}")
        return rep_count_tags

            
    def add_template_level_manual_level_count(self, note_type_item: NoteTypeItem, template_name_to_update, card_type_total_rep_count, init_card_state):
        """Add a new template level with calculated end"""
        note_type_id = note_type_item.note_type_id

        last_template_name = self.get_last_template_stored(note_type_id)
        print(f"state: {init_card_state}")
        if last_template_name is not None:
            # start = self.data["note_types"][note_type_id]["templates"][template_name]["start"]
            prev_template_end = self.data["note_types"][note_type_id]["templates"][last_template_name]["max_level"]
            start = prev_template_end + 1
            end = prev_template_end + card_type_total_rep_count
            
            self.data["note_types"][note_type_id]["templates"][template_name_to_update] = {
                "template_name": template_name_to_update,
                "init_card_state": init_card_state,
                "template_reps": card_type_total_rep_count,
                "min_level": start,
                "max_level": end
            }
            
        else:
            start = 0
            end = card_type_total_rep_count-1
            
            self.data["note_types"][note_type_id] = {
                "note_type_id": note_type_id,
                "note_type_name": note_type_item.note_type_name,
                "tag_creation_settings": 
                    {
                        "tag_prefix": "level_",
                        "start_rep": start,
                        "rep_count_tags": []
                    },
                "templates": 
                    {
                        template_name_to_update: {
                            "template_name": template_name_to_update,
                            "init_card_state": init_card_state,
                            "template_reps": card_type_total_rep_count,
                            "min_level": start,
                            "max_level": end
                        }
                    }
                }
            
masteryDatahandler = MasteryDataHandler()