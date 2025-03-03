import json
from enum import Enum
from aqt.utils import showInfo, showText, tooltip, qconnect
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import *


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


class mastery_card_grader:
    def __init__(self):        
        #["Level_0", "level_1", "level_2", "level_3"]
        self.MasteryDataLevels = None 

    def set_mastery_data_levels(self, note_type_id_from_anki: int):
        self.MasteryDataLevels = masteryDatahandler.get_all_rep_count_tags(str(note_type_id_from_anki))
        print("----------------")
        # print(f"MASTERY FOR: TYPEIN: {type(note_type_id_from_anki)} | TYPEOUTSTR: {str(note_type_id_from_anki)} | INT: {note_type_id_from_anki}")
        print(f"MASTERY LEVELS: {self.MasteryDataLevels}")
        print("----------------")

    def get_tag_of_successful_rep_count(self, note:Note) -> str:
        result = None
        for level in self.MasteryDataLevels:
            if note.has_tag(level):  # Directly check for the tag
                result = level
                
        return result
        # raise ValueError("No mastery level tag found on note")  # Handle missing tag case

    # MIGHT BE BETTER to find the min and max from the list instead of hard coded
    # Something like 0 and last index
    def adjustment_of_tag_after_grading(self, ease_button, current_rep_count_tag):
        result = None
        # For template get min max levels
        if ease_button == AnkiButton.AGAIN.value and current_rep_count_tag != self.MasteryDataLevels[0]:
            print("User Failed the card")
            # Decrease level unless level is 0
            result = MasteryUpdate.DECREASE
            
        elif ease_button == AnkiButton.GOOD.value and current_rep_count_tag != self.MasteryDataLevels[-1]:
            print("User Passed the card.")
            # Increase level unless level is 4
            result = MasteryUpdate.INCREASE
            
        else:
            result = MasteryUpdate.STAY
            
        return result 

    """
    **Assuming that updating the cards mastery happens after the tag is set on grading
    **Assuming the current tag is the must up to date**
    For cards in note if no mastery level suspend all but the expose card
    - in another function aka on_card_grade 
        we will control the taging
    - in another function we will check the mastery tag of the note 
        then suspend prev card and unsuspend the next level after grading into passing into next level level
        or
        then suspend current card and unsuspend the prev level after grading into failing into last level
    """
    def update_card_mastery(self, note:Note, current_rep_count_tag: str, ease_button):
        print(f"Card has a current mastery level tag: {current_rep_count_tag}")
        
        mastery_adjustment = self.adjustment_of_tag_after_grading(ease_button, current_rep_count_tag )
        
        
        print(f"mastery_adjustment: {mastery_adjustment} => {mastery_adjustment.value}")
        
        if mastery_adjustment != MasteryUpdate.STAY:
            print(f"STORED TOTAL REPS: {self.MasteryDataLevels}")
            
            current_rep_count = self.MasteryDataLevels.index(current_rep_count_tag)
            print(f"current_rep_count: {current_rep_count}")
            
            new_rep_count_tag_index = min(current_rep_count + mastery_adjustment.value, len(self.MasteryDataLevels) - 1)
            print(f"new_rep_count_tag_index: {new_rep_count_tag_index}")
            
            new_rep_count_tag = self.MasteryDataLevels[new_rep_count_tag_index]
            print(f"new_rep_count_tag: {new_rep_count_tag}")
            
            note.remove_tag(current_rep_count_tag)
            note.add_tag(new_rep_count_tag)
            print(f"Updated mastery level: from [{current_rep_count_tag}] to [{new_rep_count_tag}] |{note.tags}|")
            
            status = self.suspend_unsuspend_cards_in_note_based_on_rep_of_note(note, new_rep_count_tag_index)
            
            tooltip(f"Reps adjusted: {current_rep_count_tag} → {new_rep_count_tag} {status}", period=4500)
        else:
            tooltip(f"Level capped/minimum reached | {mastery_adjustment}")
        

    def on_card_grade(self, reviewer:Reviewer=None, card:Card=None, ease_button=None):        
        note = card.note()
        # card.note_type().keys() --> ['id', 'name', 'type', 'mod', 'usn', 'sortf', 'did', 'tmpls', 'flds', 'css', 'latexPre', 'latexPost', 'latexsvg', 'req']
        note_type_id = note.note_type()['id']
        self.set_mastery_data_levels(note_type_id)
        
        
        print(f"Card To Note {note}")
        current_rep_count_tag = self.get_tag_of_successful_rep_count(note)

        if current_rep_count_tag:
            self.update_card_mastery(note, current_rep_count_tag, ease_button)
        else:
            # If no mastery level is found, add the first level (LEVEL_0)
            note.add_tag(self.MasteryDataLevels[0])
            print(f"Added FIRST mastery level: {note.tags}")
            tooltip(f"No Mastery Tag -> Added: {note.tags}")

        
        
        mw.col.update_note(note)
        # op = mw.col.save()
        # CollectionOp(parent=mw, op=op).run_in_background()
        
    # def set_card_type_on_add(state: CardState, card: Card=None):
    #     temp_card = mw.col.get_card(1717780484094)
    #     temp_card.type = state.value
    #     card.flush()

    
    """
    for index, cardtype in enumerate (list of cardtypes)
        cardtype["minReps"]
        cardtype["maxReps"]
        if new_rep_count_tag_index is between min <= x <= max 
            new_card_unlocked_index = index
    
    list of max rep levels of templates
    
    card_types = level_0, level_1, level_2, level_3
    minreps =   0  ,   10    ,  20    ,  30
    maxreps =   9  ,   19   ,   29   ,  39
    """
    def suspend_unsuspend_cards_in_note_based_on_rep_of_note(self, note:Note, new_rep_count_tag_index=0):
        card_ids = note.card_ids()
        note_type_info = note.note_type()
        
        # template_names_with_index = [f"{idx}:{template['name']}" for idx, template in enumerate(note_type_info['tmpls'])]
        template_names = [f"{template['name']}" for template in note_type_info['tmpls']]
        # print(card_ids)
        # print(template_names_with_index)
        # print(template_names)
        
        status_out = ""
        
        note_type_id = str(note.note_type()["id"])
        
        for index, template_name in enumerate(template_names):
            note_type_template_min_level = masteryDatahandler.get_note_type_template_min_level(note_type_id, template_name)
            note_type_template_max_level = masteryDatahandler.get_note_type_template_max_level(note_type_id, template_name)
                        
            card_id = card_ids[index]
            card = mw.col.get_card(card_id)
            if note_type_template_min_level <= new_rep_count_tag_index <= note_type_template_max_level:
                # unsuspend card_ids[index] this is unlocked now
                mw.col.sched.unsuspend_cards([card_id])
                status_out = f"=> {template_name} : UNLOCKED"

            else:
                # suspend card_ids[index] this is locked now
                mw.col.sched.suspend_cards([card_id])

        return status_out
        
    
    def set_card_init_state(self, note:Note):
        card_ids = note.card_ids()
        note_type_info = note.note_type()
        
        template_names = [f"{template['name']}" for template in note_type_info['tmpls']]

        note_type_id = str(note.note_type()["id"])
        
        for index, template_name in enumerate(template_names):
            state = masteryDatahandler.get_note_type_template_init_card_state(note_type_id, template_name)
            
            if state != "AUTO":
                try:
                    card_id = card_ids[index]
                    card = mw.col.get_card(card_id)
                    card.type = CardState[state].value
                    card.custom_data = json.dumps({
                    "text": "SOME TEXT THAT IS IN THIS CARD",
                    "ivl": card.ivl,
                    "reps": card.reps
                })
                    print(f"BEFORE UP - IVL: {card.ivl} | card{card.custom_data}")
                    mw.col.update_card(card)
                    print(f"AFTER UP IVL: {card.ivl} | card{card.custom_data}")
                    # print(f"TEMP CARD: {card} | TYPE: {card.type} - SAVED")
                except Exception as e:
                    print(f"STATE ERROR: {e}")
        # mw.deckBrowser.show()
                
                
    def set_up_mastery_of_note(self, note:Note):
        print(f"Added a note to deck! | NOTE: {note}")
        
        note_type_id = note.note_type()['id']
        self.set_mastery_data_levels(note_type_id)
        
        # If no mastery level is found, add the first level (LEVEL_0)
        note.add_tag(self.MasteryDataLevels[0])
        print(f"Added FIRST mastery level to other tags: {note.tags}")
        # for updating tags you need to have a update called for the tags to stick
        mw.col.update_note(note)
        self.suspend_unsuspend_cards_in_note_based_on_rep_of_note(note, new_rep_count_tag_index=0)
        self.set_card_init_state(note)




    def get_template(self, card:Card):
        print("========TEMPLATES AVALIABLE========")
        # card.note_type().keys() --> ['id', 'name', 'type', 'mod', 'usn', 'sortf', 'did', 'tmpls', 'flds', 'css', 'latexPre', 'latexPost', 'latexsvg', 'req']
        note_type = card.note_type()
        # template_names = [template['name'] for template in note_type['tmpls']]
        template_names = [f"{idx}:{template['name']}" for idx, template in enumerate(note_type['tmpls'])]
        # Print the names
        print(template_names)
        print("========PREV TEMPLATE========")
        # print(f"{card.note_type()["tmpls"][card.ord]["name"]}")
        print(f"Index:{card.ord} | {template_names[card.ord]}")
        print("========NEW TEMPLATE========")
        card.ord = 2
        print(f"Index:{card.ord} | {template_names[card.ord]}")
        print("=======++++=====")
        mw.col.update_card(card)
    # gui_hooks.reviewer_did_show_question.append(get_template)

    # reviewer: Reviewer=None
    # Reviewer._showQuestion = wrap(Reviewer._showQuestion, suspend_locked_cards, 'before')
    def suspend_locked_notes(self):
        # All cards from a note
        note_id = 1738139190318
        mw.col.sched.suspend_notes([note_id])
        
        mw.col.update_note(mw.col.get_note(note_id))
        
        print(f"SUSPENDED a NOTE: {note_id}")
        # mw.deckBrowser.refresh()

    def unsuspend_locked_cards_in_a_note(self):

        # All cards from a note
        note_id = 1738139190318
        note = mw.col.get_note(note_id)
        card_ids = note.card_ids()
        mw.col.sched.unsuspend_cards(card_ids)
        # mw.col.update_cards(mw.col.get_card(card_id))
        # mw.col.sched.suspend_notes([note_id])
        mw.col.update_note(mw.col.get_note(note_id))

        print(f"UNSUSPENDED {len(card_ids)} card from NOTE: {note_id}")
        # mw.deckBrowser.refresh()

    def suspend_locked_card(self):
        # A card from a note
        card_id = 1738138852201
        mw.col.sched.suspend_cards([card_id])
        mw.col.update_card(mw.col.get_card(card_id))

        print(f"SUSPENDED a CARD: {card_id}")
        # mw.deckBrowser.refresh()

    def unsuspend_locked_card(self):
        # A card from a note
        card_id = 1738138852201
        mw.col.sched.unsuspend_cards([card_id])
        mw.col.update_card(mw.col.get_card(card_id))
        
        print(f"UNSUSPENDED a CARD: {card_id}")
        # mw.deckBrowser.refresh()



masteryCardAddon = mastery_card_grader()