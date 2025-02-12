"""
The suspension works now and levels can go up and down -> 1/29/25

---
Need to have a debug window
need to be able to set ids and indexs for options
Auto note Max or min level --> Auto Suspend and unsuspend of course
---


1/30/25
on note creation 
 - it sets tag level to 0 
and or  
 - suspends higher level cards for that note
on a hook for on note creation. 


- Need to make a config file that sets the deck id
- Make a window to configure for multipel decks and multiple levels and progressions 

- Need to check if a note from a deck got its tags updated/edited either from the browser or the edit button and if it was a level tag update 
    then sus or unsus the card types
    
- Need to add in the config what note types have what levels can do deck check too as an option
    But basically each note types has a collection of card types that can have different levels




2/10/25
Got The app working besides some small uder experince things like
- only do grading and card add suspension when its a specific deck
- need to find sutable settings for anki schudel so that 
    newly suspended cards doesn't show up as new card during the review that they got upgraded to
    or make some note about if you want that use these settings vs settings that don't do that
    
2/11/25
Got all the backend features working for the window and am just about to work on deck checking before grading and adding
deck checking in a super clean way now work pretty well I would say

ONLY small bug is that if a deck slips past then self.MasteryData is None and that causes errors
Another small thing is I can't unassign note types from mastery which would be nice for debugging and
    cleaning the MasteryData

Also would be nice to have some hooks connected to remove deck from mastery and remove notetype from mastery
    if the User deletes them within anki
    
Need to also add in feature or button or attach it to the save button
if you ahve MasteryLevels already and cards and you add/subtract tempaltes or reps it will automaticall resuspend/unsuspend all teh cards 
    that are attached to the note type in your deck
    - Will also need to do this for a premade deck atatch tags 
    - For the future be able to set tags on premade decks and kinda filter or make your own filter for what cards get what "starting" tag
"""
# C:\Users\epics\AppData\Local\Programs\Anki\anki-console.bat



from aqt.qt import QAction
from aqt.operations.collection import CollectionOp

import aqt
from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from anki.cards import Card
from anki.notes import Note
from aqt import gui_hooks
import anki.template
from anki.template import TemplateRenderOutput, TemplateRenderContext
from anki.hooks import wrap
from aqt.utils import showInfo, showInfo, qconnect
from anki.hooks import addHook
from anki import hooks

from enum import Enum

sys.path.append(os.path.dirname(__file__))

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


class mastery_card_grader:
    def __init__(self):
        self.target_deck = None
        self.set_target_deck_from_config()
        
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
            
            self.suspend_unsuspend_cards_in_note_based_on_rep_of_note(note, new_rep_count_tag_index)
        else:
            print("MIN OR MAX level has been reached")



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
        
        mw.col.update_note(note)
        # op = mw.col.save()
        # CollectionOp(parent=mw, op=op).run_in_background()







    """
    Need to make sure we can set multiple tiers for level seperate from templates/cards in notes
    and it still suspend the right card_ids

    levels 1-10
    cards 1-3

    1,2,3
    card 1

    4,5,6,7
    card 2

    8,9,10
    card 3


    Will probally adjust new_rep_count_tag_index before checking aganst the card_ids 
    in the future

    """
    def suspend_unsuspend_cards_in_note_based_on_rep_of_note(self, note:Note, new_rep_count_tag_index=0):
        # note_id = 1738139190318
        # note = mw.col.get_note(note_id)
        card_ids = note.card_ids()
        note_type_info = note.note_type()
        
        template_names_with_index = [f"{idx}:{template['name']}" for idx, template in enumerate(note_type_info['tmpls'])]
        template_names = [f"{template['name']}" for template in note_type_info['tmpls']]
        print(card_ids)
        print(template_names_with_index)
        print(template_names)
        
        """
        for index in len (reps) or for index, cardtype in enumerate (list of cardtypes)
            minReps[index]
            maxReps[index]
            if new_rep_count_tag_index is between min <= x <= max 
                new_card_unlocked_index = index
                
                
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
        
        
        
        
        """
        Should define what Mastery holds and what anki holds and what is the same thing just different wording
        template
        templates
        
        card_type
        card_types
        
        note_type
        note_types
        
        cards
        notes
        
        all the ids
        """
        note_type_id = str(note.note_type()["id"])
        
        for index, template_name in enumerate(template_names):
            # note_type_template = masteryDatahandler.get_a_note_type_template(note_type_id, template_name)
            note_type_template_min_level = masteryDatahandler.get_note_type_template_min_level(note_type_id, template_name)
            note_type_template_max_level = masteryDatahandler.get_note_type_template_max_level(note_type_id, template_name)
            
            
            print(f"MIN: {note_type_template_min_level} <= | new_tag: {new_rep_count_tag_index} | <= MAX: {note_type_template_max_level}")
            
            if note_type_template_min_level <= new_rep_count_tag_index <= note_type_template_max_level:
                # unsuspend card_ids[index] this is unlocked now
                unlocked_card_type = card_ids[index]
                
                card = mw.col.get_card(unlocked_card_type)
                
                mw.col.sched.unsuspend_cards([unlocked_card_type])
                print(f"UNLOCKED | card_id: {unlocked_card_type} | template_name_index: {index}  | TemplateIndex:{card.ord} | {template_names[card.ord]}")
                
                
            else:
                # suspend card_ids[index] this is locked now
                locked_card_type = card_ids[index]
                
                card = mw.col.get_card(locked_card_type)
                
                mw.col.sched.suspend_cards([locked_card_type])
                print(f"LOCKED | card_id: {locked_card_type} | template_name_index: {index}  | TemplateIndex:{card.ord} | {template_names[card.ord]}")
            
            


        
        
        # for index, card_id in enumerate(card_ids):
        #     card = mw.col.get_card(card_id)
        #     if index == new_rep_count_tag_index:
        #         mw.col.sched.unsuspend_cards([card_id])
                
        #         print(f"UNLOCKED | card_id: {card_id} | card_id_note_index: {index}  | TemplateIndex:{card.ord} | {template_names[card.ord]}")
        #     else:
        #         mw.col.sched.suspend_cards([card_id])
                
        #         print(f"LOCKED | card_id: {card_id} | card_id_note_index: {index}  | TemplateIndex:{card.ord} | {template_names[card.ord]}")






    def set_up_mastery_of_note(self, note:Note):
        print(f"Added a note to deck! | NOTE: {note}")
        
        note_type_id = note.note_type()['id']
        self.set_mastery_data_levels(note_type_id)
        
        # If no mastery level is found, add the first level (LEVEL_0)
        note.add_tag(self.MasteryDataLevels[0])
        note.flags
        print(f"Added FIRST mastery level to other tags: {note.tags}")
        # for updating tags you need to have a update called for the tags to stick
        mw.col.update_note(note)
        self.suspend_unsuspend_cards_in_note_based_on_rep_of_note(note, new_rep_count_tag_index=0)
        




























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
        mw.deckBrowser.refresh()
        



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
        mw.deckBrowser.refresh()
        







        
    def suspend_locked_card(self):
        # A card from a note
        card_id = 1738138852201
        mw.col.sched.suspend_cards([card_id])
        mw.col.update_card(mw.col.get_card(card_id))

        print(f"SUSPENDED a CARD: {card_id}")
        mw.deckBrowser.refresh()
        

        
    def unsuspend_locked_card(self):
        # A card from a note
        card_id = 1738138852201
        mw.col.sched.unsuspend_cards([card_id])
        mw.col.update_card(mw.col.get_card(card_id))
        
        print(f"UNSUSPENDED a CARD: {card_id}")
        mw.deckBrowser.refresh()
        


    def get_target_deck(self):
        """Retrieve the deck name from the add-on's configuration."""
        config = mw.addonManager.getConfig(__name__)
        return config.get("target_deck", "Default")
    
    def set_target_deck_from_config(self):
        self.target_deck = self.get_target_deck()

    def show_target_deck(self):
        target_deck = self.get_target_deck()
        showInfo(f"Config:{target_deck} \n Enabled: {self.target_deck}")


    def on_config_change(self, updated_config):
        """Function triggered when config updates."""
        new_deck = updated_config.get("target_deck", "Default")
        showInfo(f"Config updated! New target deck: {new_deck}")
    






mastery_card_addon = mastery_card_grader()

# actionGrade1 = QAction("_1: Fake AGAIN PRESS ", mw)
# qconnect(actionGrade1.triggered, lambda:mastery_card_addon.on_card_grade(button_pushed=1))
# mw.form.menuTools.addAction(actionGrade1)

# actionGrade2 = QAction("_2 Fake GOOD PRESS ", mw)
# qconnect(actionGrade2.triggered, lambda:mastery_card_addon.on_card_grade(button_pushed=3))
# mw.form.menuTools.addAction(actionGrade2)

# actionGrade3 = QAction("_3 Fake (un)suspend card based on tag grade ", mw)
# qconnect(actionGrade3.triggered, lambda:mastery_card_addon.suspend_unsuspend_cards_in_note_based_on_rep_of_note(2))
# mw.form.menuTools.addAction(actionGrade3)

# action1 = QAction("A: suspend_locked_notes", mw)
# qconnect(action1.triggered, mastery_card_addon.suspend_locked_notes)
# mw.form.menuTools.addAction(action1)

# action1 = QAction("AA: unsuspend_locked_cards_in_a_note", mw)
# qconnect(action1.triggered, mastery_card_addon.unsuspend_locked_cards_in_a_note)
# mw.form.menuTools.addAction(action1)

# action2 = QAction("B: suspend_locked_card", mw)
# qconnect(action2.triggered, mastery_card_addon.suspend_locked_card)
# mw.form.menuTools.addAction(action2)

# action3 = QAction("BB: unsuspend_locked_cards", mw)
# qconnect(action3.triggered, mastery_card_addon.unsuspend_locked_card)
# mw.form.menuTools.addAction(action3)



def deck_check_then_call(call_back, *args, **kwargs):
    # Example condition
    current_deck_id = mw.col.decks.get_current_id()
    print(current_deck_id)
    print(f"DECKIDCURT: {type(current_deck_id)} | {current_deck_id} | InMASTERY: {masteryDatahandler.is_deck_in_mastery(str(current_deck_id))}")
    
    if masteryDatahandler.is_deck_in_mastery(str(current_deck_id)):
    # if some_value:  # Replace `some_value` with your actual condition
        return call_back(*args, **kwargs)  # Call the callback with optional arguments
    else:
        print("Condition not met. Callback not executed.")
        

# Update the cards Mastery tag apon anwsering again -1 or good +1
# gui_hooks.reviewer_did_init()
gui_hooks.reviewer_did_answer_card.append(
    lambda *args, **kwargs: deck_check_then_call(mastery_card_addon.on_card_grade, *args, **kwargs)
)

# Adding a new note will set first level tag and first card type "Unlocked", other card types with be suspended "Locked"
gui_hooks.add_cards_did_add_note.append(
    lambda *args, **kwargs: deck_check_then_call(mastery_card_addon.set_up_mastery_of_note, *args, **kwargs)
    )

# # Allows for updating configs while app is running
# mw.addonManager.setConfigUpdatedAction(__name__, mastery_card_addon.on_config_change)


from application.FrontEnd.presentation.MasterySetupWindow import MasterySetupWindow
from application.FrontEnd.presentation.PreviewWindow import PreviewWindow
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import add_note_types_to_comboBox
# Add menu action
action = QAction("Mastery Setup", mw)
action.triggered.connect(MasterySetupWindow)
action.triggered.connect(add_note_types_to_comboBox)
mw.form.menuTools.addAction(action)


action = QAction("Show LOADED MasteryData", mw)
action.triggered.connect(PreviewWindow)
mw.form.menuTools.addAction(action)

# action = QAction("Show Single Card Viewer", mw)
# action.triggered.connect(PreviewWindow)
# mw.form.menuTools.addAction(action)


# # Add to Anki's profile loaded hook
# gui_hooks.profile_did_open.append(initialize)









