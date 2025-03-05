from aqt.utils import showInfo, showText, tooltip, qconnect
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import *
import random
import time
import json
from enum import Enum, auto
from anki.collection import Collection
from anki.decks import DeckConfigDict
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
    
class LevelUpStatus(Enum):
    NO_LEVEL_UP = auto()
    LEVEL_UP_REPS_ZERO = auto()
    LEVEL_UP_REPS_NOT_ZERO = auto()

from anki.consts import CARD_TYPE_NEW, CARD_TYPE_LRN, CARD_TYPE_REV, CARD_TYPE_RELEARNING
class CardState(Enum):
    NEW = CARD_TYPE_NEW
    LEARNING = CARD_TYPE_LRN
    REVIEW = CARD_TYPE_REV
    RELEARNING = CARD_TYPE_RELEARNING



# TODO see if you need to update_card with every set or if it works to update_cards after the for loop
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
        
    def current_deck_id(self, card: Card) -> int:
        """
        The original deck the card came from if it's in a filtered deck. Otherwise did=0.
            If odid > 0 → use that (the real deck).
            Else → just use did.
        """
        return card.odid if card.odid > 0 else card.did
    
    def reps_to_graduate(self, card: Card) -> int:

        group_conf: DeckConfigDict = mw.col.decks.config_dict_for_deck_id(self.current_deck_id(card))

        reps_left = len(group_conf["new"]["delays"])

        # print("delays:", group_conf["new"]["delays"], "reps left:", reps_left)
        return reps_left * 1000 + reps_left
    
    def put_in_learning(self, card: Card) -> None:
        cfg = mw.col.decks.config_dict_for_deck_id(self.current_deck_id(card))
        card.type = 1
        card.queue = 1
        card.ivl = 0
        card.due = int(time.time() - random.randint(0, 100))
        card.left = self.reps_to_graduate(card)
        card.reps = 0
        card.lapses = 0
        card.factor = cfg["new"]["initialFactor"]

    def put_in_review(self, card: Card) -> None:
        cfg = mw.col.decks.config_dict_for_deck_id(self.current_deck_id(card))
        # print_nested_dict(cfg)
        card.type = 2
        card.queue = 2
        card.ivl = cfg["new"]["ints"][0]  # Or cfg["new"]["easyIv"] if you're feeling generous
        card.due = mw.col.sched.today + card.ivl
        card.reps = 0
        card.lapses = 0
        card.factor = cfg["new"]["initialFactor"]

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
            if state != "NEW":
                if state == "LEARNING":
                    self.put_in_learning(card)
                elif state == "REVIEW":
                    self.put_in_review(card)
                mw.col.update_card(card)
    
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
        
    def adjust_success_count(self, ease_button, current_count, min_count, max_count):
        # print(f"{ease_button} == {AnkiButton.AGAIN.value} and {current_count} > {min_count}")
        result = current_count
        status = MasteryUpdate.STAY
        if ease_button == AnkiButton.AGAIN.value and current_count > min_count:
            result = max(current_count - 1, min_count)
            status = MasteryUpdate.DECREASE
        elif ease_button == AnkiButton.GOOD.value and current_count < max_count:
            result = min(current_count + 1, max_count)
            status = MasteryUpdate.INCREASE
        return result, status
        
    def update_note_success(self, note:Note, card:Card, ease_button):
        ntID = note.note_type()['id']
        min_note = masteryDatahandler.get_start_number(ntID)
        max_note = len(masteryDatahandler.get_all_rep_count_tags(ntID)) - 1
        current_note_count = self.get_note_success_count(card)
        new_note_count, update_status = self.adjust_success_count(ease_button, current_note_count, min_note, max_note)
        return current_note_count, new_note_count, update_status
        
    def update_card_success(self, note:Note, card:Card, ease_button):
        ntID = note.note_type()['id']
        template_name = card.template()['name']
        min_card = masteryDatahandler.get_note_type_template_min_level(ntID, template_name)
        max_card = masteryDatahandler.get_note_type_template_max_level(ntID, template_name)
        current_card_count = self.get_card_success_count(card)
        new_card_count, update_status = self.adjust_success_count(ease_button, current_card_count, min_card, max_card)
        return new_card_count, update_status
    
    def level(self, success_count, note: Note):
        ntID = note.note_type()['id']
        for level, card in enumerate(note.cards()):
            template_name = card.template()['name']
            min_level = masteryDatahandler.get_note_type_template_min_level(ntID, template_name)
            max_level = masteryDatahandler.get_note_type_template_max_level(ntID, template_name)
            if min_level <= success_count <= max_level:
                return level
        return -1
    
    def did_level_change(self, old_count, new_count, note):
        return self.level(old_count, note) != self.level(new_count, note)
    
    def handle_sched_and_sus_on_level_up(self, old_count, new_count, note: Note) -> LevelUpStatus:
        status = LevelUpStatus.NO_LEVEL_UP
        if self.did_level_change(old_count, new_count, note):
            active_card: Card = note.cards()[self.level(new_count, note)]
            self.suspend_unsuspend_cards(note, new_count)
            if not active_card.reps:
                # print("LEVEL UP")
                # print(f"CHANGED DUE = [B: {card.due} | A:{mw.col.sched.today + 1}]")
                active_card.due = mw.col.sched.today + 1
                mw.col.update_card(active_card)
                status = LevelUpStatus.LEVEL_UP_REPS_ZERO
            else:
                # print("PROMPTED")
                status = LevelUpStatus.LEVEL_UP_REPS_NOT_ZERO
        return status
    
    def handle_message_for_level_up(self, note: Note, level_up_status, update_status, ease_button, old_count, new_count):
        active_card: Card = note.cards()[self.level(new_count, note)]
        template_name = active_card.template()['name']
        if level_up_status == LevelUpStatus.NO_LEVEL_UP:
            if update_status == MasteryUpdate.STAY and AnkiButton(ease_button) == AnkiButton.AGAIN:
                print(f"Reps min reached: [{old_count} = {new_count}] | {template_name}")
                tooltip(f"Reps min reached: [{old_count} = {new_count}] | {template_name}", period=6000)
            elif update_status == MasteryUpdate.STAY and AnkiButton(ease_button) == AnkiButton.GOOD:
                print(f"Reps max reached: [{old_count} = {new_count}] | {template_name}")
                tooltip(f"Reps max reached: [{old_count} = {new_count}] | {template_name}", period=6000)
            else:
                print(f"Reps adjusted: [{old_count} → {new_count}] | {template_name}")
                tooltip(f"Reps adjusted: [{old_count} → {new_count}] | {template_name}", period=6000)
        elif level_up_status == LevelUpStatus.LEVEL_UP_REPS_ZERO:
            print(f"Reps changed: [{old_count} → {new_count}] | 🎉 NEW LEVEL! {template_name}")
            tooltip(f"Reps changed: [{old_count} → {new_count}] | 🎉 NEW LEVEL! {template_name}", period=6000)
        elif level_up_status == LevelUpStatus.LEVEL_UP_REPS_NOT_ZERO:
            if AnkiButton(ease_button) == AnkiButton.GOOD:
                print(f"Reps changed: [{old_count} → {new_count}] | ⬆️ {template_name}")
                tooltip(f"Reps changed: [{old_count} → {new_count}] | ⬆️ {template_name}", period=6000)
            elif AnkiButton(ease_button) == AnkiButton.AGAIN:
                print(f"Reps changed: [{old_count} → {new_count}] | ⬇️ {template_name}")
                tooltip(f"Reps changed: [{old_count} → {new_count}] | ⬇️ {template_name}", period=6000)
            else:
                print(f"Y{level_up_status}, {update_status}, {ease_button}, reps[B:{old_count} A:{new_count}]")
                tooltip(f"Y{level_up_status}, {update_status}, {ease_button}, reps[B:{old_count} A:{new_count}]", period=15000)
        else:
            print(f"Z{level_up_status}, {update_status}, {ease_button}, reps[B:{old_count} A:{new_count}]")
            tooltip(f"Z{level_up_status}, {update_status}, {ease_button}, reps[B:{old_count} A:{new_count}]", period=15000)
        
    def on_card_grade(self, reviewer:Reviewer=None, card:Card=None, ease_button=None):
        note = card.note()
        ntID = note.note_type()['id']
        self.set_mastery_data_levels(ntID) #! IDK if self.masteryLevels needs to be here or util class
        old_note_count, new_note_count, update_status = self.update_note_success(note, card, ease_button)
        new_card_count, card_update_status = self.update_card_success(note, card, ease_button)
        level_up_status = self.handle_sched_and_sus_on_level_up(old_note_count, new_note_count, note)
        self.set_card_success_count(card, new_card_count)
        self.sync_note_success_count_to_siblings(note, new_note_count)
        # XXX sus/unsus was here before just as a reminder
        self.handle_message_for_level_up(note, level_up_status, update_status, ease_button, old_note_count, new_note_count)
        
        

masteryCardGrader = mastery_card_grader()
