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

"""
https://stackoverflow.com/questions/42660670/collapse-all-methods-in-visual-studio-code

Ctrl + K + Ctrl + 0: fold all levels (namespace, class, method, and block)
Ctrl + K + Ctrl + 1: namespace / @Component(For Angular)
Ctrl + K + Ctrl + 2: class / methods
Ctrl + K + Ctrl + 3: methods / blocks
Ctrl + K + Ctrl + 4: blocks / inner blocks
Ctrl + K + Ctrl + [ or Ctrl + k + ]: current cursor block
Ctrl + K + Ctrl + j: UnFold
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

from aqt.qt import QAction
from aqt.operations.collection import CollectionOp

import aqt
from aqt import mw
from aqt.qt import *
from aqt.reviewer import Reviewer
from anki.consts import CARD_TYPE_NEW, CARD_TYPE_LRN, CARD_TYPE_REV, CARD_TYPE_RELEARNING
from anki.cards import Card
from anki.notes import Note
from aqt import gui_hooks
import anki.template
from anki.template import TemplateRenderOutput, TemplateRenderContext
from anki.hooks import wrap
from aqt.utils import showInfo, showText, tooltip, qconnect
from anki.hooks import addHook
from anki import hooks
import json
from enum import Enum

sys.path.append(os.path.dirname(__file__))

# from application.MiddleEnd.MasteryCardGrader import masteryCardAddon
from application.MiddleEnd.MasteryCardGraderWCustomData import masteryCardGrader, masteryCardAdder
from application.MiddleEnd.MasteryDatahandler import masteryDatahandler





#########################################################








#############################################################
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
    # print(current_deck_id)
    
    info = f"DECKIDCURT: {type(current_deck_id)} | {current_deck_id} | InMASTERY: {masteryDatahandler.is_deck_in_mastery(str(current_deck_id))}"
    
    # print(info)
    tooltip(info)
    
    if masteryDatahandler.is_deck_in_mastery(str(current_deck_id)):
    # if some_value:  # Replace `some_value` with your actual condition
        return call_back(*args, **kwargs)  # Call the callback with optional arguments
    else:
        print("Deck not assigned mastery: Callback not executed.")
        
gui_hooks.main_window_did_init.append(lambda: masteryDatahandler.load_config(mw.addonManager.getConfig(__name__)))

# Update the cards Mastery tag apon anwsering again -1 or good +1
# gui_hooks.reviewer_did_init()
gui_hooks.reviewer_did_answer_card.append(
    lambda *args, **kwargs: deck_check_then_call(masteryCardGrader.on_card_grade, *args, **kwargs)
)

# Adding a new note will set first level tag and first card type "Unlocked", other card types with be suspended "Locked"
gui_hooks.add_cards_did_add_note.append(
    lambda *args, **kwargs: deck_check_then_call(masteryCardAdder.add_note_with_mastery, *args, **kwargs)
    )

# # Allows for updating configs while app is running
mw.addonManager.setConfigUpdatedAction(__name__, masteryDatahandler.on_config_update)


from application.FrontEnd.presentation.MasterySetupWindow import MasterySetupWindow
from application.FrontEnd.presentation.PreviewWindow import PreviewWindow
from application.FrontEnd.presentation.ExtentionDebugWindow import ExtentionDebugWindow
from application.MiddleEnd.integreation.UpdateWindowFromAnkiFunctions import add_note_types_to_comboBox
# Add menu action
action = QAction("Mastery Setup", mw)
action.triggered.connect(MasterySetupWindow)
action.triggered.connect(add_note_types_to_comboBox) #TODO Is this needed? I thought we made it so that it loaded always, double check that
mw.form.menuTools.addAction(action)
mw.form

action = QAction("DEBUG", mw)
action.triggered.connect(ExtentionDebugWindow)
mw.form.menuTools.addAction(action)


# # Add to Anki's profile loaded hook
# gui_hooks.profile_did_open.append(initialize)





# action = QAction("Show LOADED MasteryData", mw)
# action.triggered.connect(PreviewWindow)
# mw.form.menuTools.addAction(action)


def some_test():
    mw.statusBar().showMessage("Some Magic text1\nMORE STYUUFF\nsadkjaklsjd", 2500)
    tooltip("Some Magic text")








