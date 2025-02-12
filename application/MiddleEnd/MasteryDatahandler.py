import json
from typing import Optional, Any, Union, Dict
from pathlib import Path
from application.MiddleEnd.integreation.MasterTypes import NoteTypeItem

class MasteryDataHandler:
    def __init__(self, json_path: Optional[Union[str, Path]] = None):
        """
        Initialize the MasteryDataHandler class.
        
        Args:
            json_path: Path to JSON file (optional). If provided, loads the file immediately.
        """
        self.json_path = json_path
        self.data: Dict[str, Any] = {}
        if json_path:
            self.load_json(json_path)

    def load_json(self, json_path: Union[str, Path]) -> None:
        """Load JSON data from file."""
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f) or {}
            
    def save_json(self) -> None:
        """Save JSON data to file."""
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    
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
    def set_deck(self, deck_id: str, deck_info: Dict[str, Any]) -> None:
        self.data["decks"][deck_id] = deck_info
        
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

            
    def add_template_level_manual_level_count(self, note_type_item: NoteTypeItem, template_name_to_update, card_type_total_rep_count):
        """Add a new template level with calculated end"""
        note_type_id = note_type_item.note_type_id

        last_template_name = self.get_last_template_stored(note_type_id)
        
        if last_template_name is not None:
            # start = self.data["note_types"][note_type_id]["templates"][template_name]["start"]
            prev_template_end = self.data["note_types"][note_type_id]["templates"][last_template_name]["max_level"]
            start = prev_template_end + 1
            end = prev_template_end + card_type_total_rep_count
            
            self.data["note_types"][note_type_id]["templates"][template_name_to_update] = {
                "template_name": template_name_to_update,
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
                            "template_reps": card_type_total_rep_count,
                            "min_level": start,
                            "max_level": end
                        }
                    }
                }