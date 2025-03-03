import json
from enum import Enum
from aqt.utils import showInfo, showText, tooltip, qconnect
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import *

import json
from enum import Enum
from aqt.utils import tooltip

class MasteryUpdate(Enum):
    DECREASE = -1
    STAY = 0
    INCREASE = 1

class AnkiButton(Enum):
    AGAIN = 1
    HARD = 2
    GOOD = 3
    EASY = 4

class mastery_card_grader:
    
    def __init__(self):
        self.MasteryDataLevels = None 

    def set_mastery_data_levels(self, note_type_id_from_anki: int):
        self.MasteryDataLevels = masteryDatahandler.get_all_rep_count_tags(str(note_type_id_from_anki))

    def set_up_mastery_of_note(self, note:Note):
        print(f"Added a note to deck! | NOTE: {note}")
        
        note_type_id = note.note_type()['id']
        self.set_mastery_data_levels(note_type_id)

        card_ids = note.card_ids()
        for index, card_id in enumerate(card_ids):
            card = mw.col.get_card(card_id)
            card.custom_data = json.dumps({
                "rep_count": 0,  # Start fresh
                "index": index,
                "ivl": card.ivl,
                "reps": card.reps
            })
            mw.col.update_card(card)
            print(f"Initialized card {index} with rep_count 0")

        self.suspend_unsuspend_cards_in_note_based_on_rep_of_note(note, new_rep_count_tag_index=0)
        self.set_card_init_state(note)
    
    def get_rep_count(self, card: Card):
        data = json.loads(card.custom_data or '{}')
        return data.get('rep_count', 0)

    def set_rep_count(self, card: Card, rep_count):
        data = json.loads(card.custom_data or '{}')
        data['rep_count'] = rep_count
        card.custom_data = json.dumps(data)

    def adjust_rep_count(self, ease_button, current_rep_count, max_level):
        if ease_button == AnkiButton.AGAIN.value:
            return max(current_rep_count - 1, 0)
        elif ease_button == AnkiButton.GOOD.value:
            return min(current_rep_count + 1, max_level)
        else:
            return current_rep_count

    def sync_rep_count_to_siblings(self, note: Note, new_rep_count):
        for card_id in note.card_ids():
            card = mw.col.get_card(card_id)
            self.set_rep_count(card, new_rep_count)
            mw.col.update_card(card)

    def suspend_unsuspend_cards(self, note: Note, rep_count):
        note_type_id = str(note.note_type()['id'])
        for card_id in note.card_ids():
            card = mw.col.get_card(card_id)
            template_name = card.template()['name']
            min_level = masteryDatahandler.get_note_type_template_min_level(note_type_id, template_name)
            max_level = masteryDatahandler.get_note_type_template_max_level(note_type_id, template_name)
            if min_level <= rep_count <= max_level:
                mw.col.sched.unsuspend_cards([card_id])
            else:
                mw.col.sched.suspend_cards([card_id])



    def on_card_grade(self, card: Card, ease_button):
        note = card.note()
        current_rep_count = self.get_rep_count(card)
        max_level = len(masteryDatahandler.get_all_rep_count_tags(str(note.note_type()['id']))) - 1
        new_rep_count = self.adjust_rep_count(ease_button, current_rep_count, max_level)
        self.sync_rep_count_to_siblings(note, new_rep_count)
        self.suspend_unsuspend_cards(note, new_rep_count)
        tooltip(f"Rep count adjusted: {current_rep_count} → {new_rep_count}", period=4500)

masteryCardGrader = mastery_card_grader()