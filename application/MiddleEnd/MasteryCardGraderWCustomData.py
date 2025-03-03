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

from anki.consts import CARD_TYPE_NEW, CARD_TYPE_LRN, CARD_TYPE_REV, CARD_TYPE_RELEARNING
class CardState(Enum):
    AUTO = CARD_TYPE_NEW
    NEW = CARD_TYPE_NEW
    LEARNING = CARD_TYPE_LRN
    REVIEW = CARD_TYPE_REV
    RELEARNING = CARD_TYPE_RELEARNING




class MasterySharedUtils:
    def set_mastery_data_levels(self, note_type_id_from_anki: int):
        self.MasteryDataLevels = masteryDatahandler.get_all_rep_count_tags(str(note_type_id_from_anki))
        
    def set_note_success_count(self, card: Card, rep_count):
        data = json.loads(card.custom_data or '{}')
        data['notesct'] = rep_count
        card.custom_data = json.dumps(data)
        mw.col.update_card(card)
        
    def set_card_success_count(self, card: Card, rep_count):
        data = json.loads(card.custom_data or '{}')
        data['cardsct'] = rep_count
        card.custom_data = json.dumps(data)
        mw.col.update_card(card)
        
    def get_note_success_count(self, card: Card):
        data = json.loads(card.custom_data or '{}')
        return data.get('notesct', 0)
    
    def get_card_success_count(self, card: Card):
        data = json.loads(card.custom_data or '{}')
        return data.get('cardsct', 0)

    def suspend_unsuspend_a_card(self, note:Note, card: Card, success_count):
        template_name = card.template()['name']
        # print(f"TMPL: {template_name} | NID: {note.id} | NTID: {note.note_type()['id']}")
        
        ntID = note.note_type()['id']
        
        min_level = masteryDatahandler.get_note_type_template_min_level(ntID, template_name)
        max_level = masteryDatahandler.get_note_type_template_max_level(ntID, template_name)
        # print(f" {min_level} <= {success_count} <= {max_level}")
        if min_level <= success_count <= max_level:
            mw.col.sched.unsuspend_cards([card.id])
        else:
            mw.col.sched.suspend_cards([card.id])

    def suspend_unsuspend_cards(self, note:Note, success_count):
        for card in note.cards():
            self.suspend_unsuspend_a_card(note, card, success_count)
        mw.col.update_cards(note.cards())


"""
On grader Init
- set mastery to none


On card add
- set reps in custom data (in all cards held in a note)
- sus/unsus card types level_0 --> level_3



On card grade
- set mastery levels based on the note type
- get stored (success_tag) rep number
    - set rep number to level_0 if not there
- update card rep based on success or failour
"""

class mastery_card_add(MasterySharedUtils):
    def __init__(self):
        self.MasteryDataLevels = None 

    def init_success_count_data(self, note: Note):
        for card in note.cards():
            self.set_card_success_count(card, 0)
            self.set_note_success_count(card, 0)
        mw.col.update_cards(note.cards())
    
    def init_state_of_cards(self, note:Note):
        for index, card in enumerate(note.cards()):
            template_name = card.template()['name']
            ntID = note.note_type()['id']
            # TODO since we need a note type id in our masteryDatahandler we shoudl change the function so that 
            # they just ask for a note and we just do ntID = note.note_type()['id'] there instead of coming to this
            # guessing game of anki's naming conventions
            # note.id is the note that you create
            # note.note_type()['id'] gives us the id of the note type
            state = masteryDatahandler.get_note_type_template_init_card_state(ntID, template_name)
            if state != "AUTO":
                card.type = CardState[state].value
                mw.col.update_card(card)
        # mw.col.update_cards(note.cards())
    
    def add_note_with_mastery(self, note:Note):
        ntID = note.note_type()['id']
        self.set_mastery_data_levels(ntID)
        self.init_success_count_data(note)
        self.init_state_of_cards(note)
        self.suspend_unsuspend_cards(note, 0)
        
masteryCardAdder = mastery_card_add()


# TODO remove prefix stuff since we will be only reliying on numbers store in the custom_data from now on 
class mastery_card_grader(MasterySharedUtils):
    def __init__(self):
        self.MasteryDataLevels = None 

    def sync_note_success_count_to_siblings(self, note: Note, new_success_count):
        for card in note.cards():
            self.set_note_success_count(card, new_success_count)
        mw.col.update_cards(note.cards())

    # def adjustment_of_success_count(self, ease_button, current_success_count, min_count, max_count):
    #     result = None
    #     if ease_button == AnkiButton.AGAIN.value and current_success_count != min_count:
    #         result = MasteryUpdate.DECREASE
    #     elif ease_button == AnkiButton.GOOD.value and current_success_count != max_count:
    #         result = MasteryUpdate.INCREASE
    #     else:
    #         result = MasteryUpdate.STAY
    #     return result 
        
    def adjust_success_count(self, ease_button, current_count, min_count, max_count):
        print(f"{ease_button} == {AnkiButton.AGAIN.value} and {current_count} > {min_count}")
        if ease_button == AnkiButton.AGAIN.value and current_count > min_count:
            return max(current_count - 1, min_count)
        elif ease_button == AnkiButton.GOOD.value and current_count < max_count:
            return min(current_count + 1, max_count)
        return current_count
        
    def update_note_success(self, note:Note, card:Card, ease_button):
        ntID = note.note_type()['id']
        min_note = masteryDatahandler.get_start_number(ntID)
        max_note = len(masteryDatahandler.get_all_rep_count_tags(ntID)) - 1
        current_note = self.get_note_success_count(card)
        new_note_count = self.adjust_success_count(ease_button, current_note, min_note, max_note)
        return current_note, new_note_count
        
        
    def update_card_success(self, note:Note, card:Card, ease_button):
        ntID = note.note_type()['id']
        template_name = card.template()['name']
        min_card = masteryDatahandler.get_note_type_template_min_level(ntID, template_name)
        max_card = masteryDatahandler.get_note_type_template_max_level(ntID, template_name)
        current_card = self.get_card_success_count(card)
        new_card_count = self.adjust_success_count(ease_button, current_card, min_card, max_card)
        return new_card_count
        
        
    def on_card_grade(self, reviewer:Reviewer=None, card:Card=None, ease_button=None):
        note = card.note()
        ntID = note.note_type()['id']
        self.set_mastery_data_levels(ntID)
        current_note, new_note_count = self.update_note_success(note, card, ease_button)
        new_card_count = self.update_card_success(note, card, ease_button)
        self.set_card_success_count(card, new_card_count)
        self.sync_note_success_count_to_siblings(note, new_note_count)
        self.suspend_unsuspend_cards(note, new_note_count)
        tooltip(f"Rep count adjusted: {current_note} → {new_note_count}", period=4500)

masteryCardGrader = mastery_card_grader()
