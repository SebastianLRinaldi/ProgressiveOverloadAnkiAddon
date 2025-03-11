from aqt.utils import showInfo, showText, tooltip, qconnect
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import *
import random
import time
import json
from enum import Enum, auto
from anki.collection import Collection
from anki.decks import DeckConfigDict
from aqt.utils import tooltip



from anki.collection import Collection, OpChanges
from anki.decks import DeckConfigDict
from aqt import qconnect
from aqt.browser import Browser
from aqt.operations import CollectionOp
from aqt.operations import ResultWithChanges
from aqt.qt import QKeySequence
from aqt.utils import tooltip
import functools



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
    LEVEL_CHANGED_REPS_ZERO = auto()
    LEVEL_CHANGED_REPS_NOT_ZERO = auto()

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
        
        
    # def with_undo_entry(undo_msg: str):
    #     def decorator(function: Callable):
    #         @functools.wraps(function)
    #         def wrapper(self,*args, **kwargs) -> ResultWithChanges:
    #             pos = mw.col.add_custom_undo_entry(undo_msg)
    #             function(mw.col, *args, **kwargs)
    #             return mw.col.merge_undo_entries(pos)

    #         return wrapper

    #     return decorator
    
    def set_success_count_data(self, card: Card, rep_count_card, rep_count_note):
        data = json.loads(card.custom_data or '{}')
        print(f"BDATA: {data} [CC: {rep_count_card}|NC:{rep_count_note}]")
        data['cardsct'] = rep_count_card
        data['notesct'] = rep_count_note
        card.custom_data = json.dumps(data)
        print(f"ADATA: {data} [CC: {rep_count_card}|NC:{rep_count_note}]")
        mw.col.update_card(card)
    
    def set_note_success_count(self, card: Card, note_rep_count):
        data = json.loads(card.custom_data or '{}')
        data['notesct'] = note_rep_count
        card.custom_data = json.dumps(data)
        mw.col.update_card(card)
        
    def set_card_success_count(self, card: Card, card_rep_count):
        data = json.loads(card.custom_data or '{}')
        data['cardsct'] = card_rep_count
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
        print(f" {min_level} <= {success_count} <= {max_level}")
        if min_level <= success_count <= max_level:
            mw.col.sched.unsuspend_cards([card.id])
            # mw.col.update_card(card)
            print(f"unlocked:{template_name}")

        else:
            mw.col.sched.suspend_cards([card.id])
            # mw.col.update_card(card)
            print(f"locked:{template_name}")



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

    # def sync_note_success_count_to_siblings(self, note: Note, new_success_count):
    #     for card in note.cards():
    #         self.set_note_success_count(card, new_success_count)
    
    
    def update_success_count_data(self, active_card:Card, new_card_count, note, new_note_count):
        for card in note.cards():
            print(f"card:{card.id} == {active_card.id}:{card.id == active_card.id}")
            if card.id == active_card.id:
                self.set_success_count_data(card, new_card_count, new_note_count)
            else:
                self.set_note_success_count(card, new_note_count)

        # mw.col.update_cards(note.cards())
        
    def adjust_success_count(self, ease_button, current_count, min_count, max_count):
        # print(f"{ease_button} == {AnkiButton.AGAIN.value} and {current_count} > {min_count}")
        result = current_count
        status = MasteryUpdate.STAY
        if ease_button == AnkiButton.AGAIN.value and current_count > min_count:
            result = max(current_count - 1, min_count)
            status = MasteryUpdate.DECREASE
            print(f"AGAIN {result} - [{current_count} - 1 ={current_count - 1}, {min_count}]")
        elif ease_button == AnkiButton.GOOD.value and current_count < max_count:
            result = min(current_count + 1, max_count)
            status = MasteryUpdate.INCREASE
            print(f"GOOD {result} - [{current_count} + 1={current_count + 1}, {max_count}]")
        return result, status
        
    def get_current_note_success(self, note:Note, card:Card, ease_button):
        print("GETTING NOTE SUCCESS COUT")
        ntID = note.note_type()['id']
        min_note = masteryDatahandler.get_start_number(ntID)
        max_note = len(masteryDatahandler.get_all_rep_count_tags(ntID)) - 1
        current_note_count = self.get_note_success_count(card)
        print(f"getting note count:{current_note_count}")
        new_note_count, update_status = self.adjust_success_count(ease_button, current_note_count, min_note, max_note)
        print(f"After getting new note count:{new_note_count} | status:{update_status}")
        return current_note_count, new_note_count, update_status
        
    def get_current_card_success(self, note:Note, card:Card, ease_button):
        print("GETTING CARD SUCCESS COUT")
        ntID = note.note_type()['id']
        template_name = card.template()['name']
        min_card = masteryDatahandler.get_note_type_template_min_level(ntID, template_name)
        max_card = masteryDatahandler.get_note_type_template_max_level(ntID, template_name)
        current_card_count = self.get_card_success_count(card)
        print(f"getting card count:{current_card_count}")
        new_card_count, update_status = self.adjust_success_count(ease_button, current_card_count, min_card, max_card)
        print(f"After getting new card count:{new_card_count} | status:{update_status}")
        return current_card_count, new_card_count, update_status
    
    def level(self, success_count, note: Note):
        ntID = note.note_type()['id']
        for level, card in enumerate(note.cards()):
            template_name = card.template()['name']
            min_level = masteryDatahandler.get_note_type_template_min_level(ntID, template_name)
            max_level = masteryDatahandler.get_note_type_template_max_level(ntID, template_name)
            if min_level <= success_count <= max_level:
                print(f"{template_name} | MIN:{min_level} <= SUCCT:{success_count} <= MAX:{max_level}")
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
                status = LevelUpStatus.LEVEL_CHANGED_REPS_ZERO
            else:
                # print("PROMPTED")
                status = LevelUpStatus.LEVEL_CHANGED_REPS_NOT_ZERO
        return status
    
    
    def handle_message_for_level_up(self, note: Note, level_up_status, update_status, ease_button, old_count, new_count):
        card = note.cards()[self.level(new_count, note)]
        name = card.template()['name']
        btn = AnkiButton(ease_button)
        same = f"[{old_count} = {new_count}]"
        arrow = f"[{old_count} → {new_count}]"
        
        def notify(msg, period=6000):
            print(msg)
            tooltip(msg, period=period)

        # Define condition-message mappings
        conditions_to_messages = {
            (LevelUpStatus.NO_LEVEL_UP, MasteryUpdate.STAY, AnkiButton.AGAIN): f"Reps min reached: {same} | {name}",
            (LevelUpStatus.NO_LEVEL_UP, MasteryUpdate.STAY, AnkiButton.GOOD): f"Reps max reached: {same} | {name}",
            (LevelUpStatus.NO_LEVEL_UP, MasteryUpdate.INCREASE, AnkiButton.GOOD):f"Reps increased: {arrow} | {name}",
            (LevelUpStatus.NO_LEVEL_UP, MasteryUpdate.DECREASE, AnkiButton.AGAIN): f"Reps decreased: {arrow} | {name}",
            (LevelUpStatus.LEVEL_CHANGED_REPS_ZERO, MasteryUpdate.INCREASE, AnkiButton.GOOD): f"Reps increased: {arrow} | 🎉 NEW LEVEL! {name}",
            (LevelUpStatus.LEVEL_CHANGED_REPS_NOT_ZERO, MasteryUpdate.INCREASE, AnkiButton.GOOD): f"Reps increased: {arrow} | Level ⬆️ {name}",
            (LevelUpStatus.LEVEL_CHANGED_REPS_NOT_ZERO, MasteryUpdate.DECREASE, AnkiButton.AGAIN): f"Reps decreased: {arrow} | Level ⬇️ {name}",
        }

        # Try to get the message based on the combination of (level_up_status, update_status, btn)
        msg = conditions_to_messages.get((level_up_status, update_status, btn))

        if msg:
            notify(msg)
        else:
            notify(f"UNKNOWN-CONDTIONS: {level_up_status}, {update_status}, {btn}, reps[B:{old_count} A:{new_count}]", period=15000)

    def on_card_grade(self, reviewer:Reviewer=None, active_card:Card=None, ease_button=None):
        
        # pos = mw.col.add_custom_undo_entry("CARD MASTERY GRADE UNDO")
        # print(f"LASTSTEP:{mw.col.undo_status().last_step} - 2")
        last = mw.col.undo_status().last_step
        note = active_card.note()
        ntID = note.note_type()['id']
        self.set_mastery_data_levels(ntID) #! IDK if self.masteryLevels needs to be here or util class
        old_note_count, new_note_count, overall_update_status = self.get_current_note_success(note, active_card, ease_button)
        current_card_count, new_card_count, card_update_status = self.get_current_card_success(note, active_card, ease_button)
        level_up_status = self.handle_sched_and_sus_on_level_up(old_note_count, new_note_count, note)
        # mw.col.update_cards(note.cards())
        self.update_success_count_data(active_card, new_card_count, note, new_note_count)
            # user0 = input("PAUSED AFTER sus/unsus")
        # self.set_card_success_count(card, new_card_count)
            # user2 = input("PAUSED AFTER  card cucess count")
        # self.sync_note_success_count_to_siblings(note, new_note_count)
            # user3 = input("PAUSED AFTER  note sibling sync")
        # XXX sus/unsus was here before just as a reminder
        self.handle_message_for_level_up(note, level_up_status, overall_update_status, ease_button, old_note_count, new_note_count)
            # user4 = input("PPAUSED AFTER  sent message")
        
            # user4 = input("PPAUSED AFTER  update message")
        # print(mw.col.undo_status().last_step)
        # mw.col.merge_undo_entries(pos)
        mw.col.merge_undo_entries(last)

        
        
        
        

masteryCardGrader = mastery_card_grader()
