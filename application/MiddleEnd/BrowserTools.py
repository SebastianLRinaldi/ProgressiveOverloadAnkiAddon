import functools

from collections.abc import Sequence, Iterator
from collections.abc import Sized
from gettext import ngettext
from typing import Callable
from typing import Optional

from anki.cards import Card
from anki.notes import Note
from anki.collection import Collection, OpChanges
from anki.decks import DeckConfigDict
from aqt import qconnect
from aqt.browser import Browser
from aqt.operations import CollectionOp
from aqt.operations import ResultWithChanges
from aqt.qt import QKeySequence
from aqt.utils import tooltip

from aqt.browser import Browser



from application.MiddleEnd.MasteryCardGraderWCustomData import masteryCardGrader, masteryCardAdder, masteryDatahandler

def with_undo_entry(undo_msg: str):
    def decorator(function: Callable):
        @functools.wraps(function)
        def wrapper(col: Collection, *args, **kwargs) -> ResultWithChanges:
            pos = col.add_custom_undo_entry(undo_msg)
            function(col, *args, **kwargs)
            return col.merge_undo_entries(pos)

        return wrapper

    return decorator

def is_new(card: Card) -> bool:
    return card.type == 0 and card.queue == 0

def get_selected_cards(browser: Browser) -> Iterator[Card]:
    return map(browser.col.get_card, set(browser.selected_cards()))

def get_selected_notes(browser: Browser) -> Iterator[Note]:
    return map(browser.col.get_note, set(browser.selected_notes()))

def notify_user(msg: str) -> None:
    tooltip(msg, period=7000)  # 7 seconds
    print(msg)

def format_message_custom_data_updates(accepted: Sized) -> str:
    msg = []

    if (num_accepted := len(accepted)) > 0:
        msg.append(
            ngettext(
                f"{num_accepted} card was updated with new note count.",
                f"{num_accepted} cards were updated with new note count.",
                num_accepted,
            )
        )

    return " ".join(msg)


def set_correct_custom_data(col, card: Card):
    # card_cnt = masteryCardAdder.get_card_success_count(card)
    # note_cnt = masteryCardAdder.get_note_success_count(card)
    # print(f"cardsct={card_cnt} notesct={note_cnt} | tmpl={card.template()['name']} |tmpl_id={card.template()['id']} ")

    card_cnt = masteryCardAdder.get_card_success_count(card)
    note_cnt = masteryCardAdder.get_note_success_count(card)
    tmpl_name = card.template()['name']
    tmpl_id = card.template()['id']
    
    print(f"cardsct={card_cnt:<3}  notesct={note_cnt:<3}  | tmpl={tmpl_name:<30} | tmpl_id={tmpl_id}")

    masteryCardAdder.set_success_count_data(card, 0,0)
    # masteryCardAdder.set_note_success_count(card, note_cnt+3)
    # masteryCardAdder.suspend_unsuspend_cards_ruled


@with_undo_entry(undo_msg="Set Cards with Blank Internal Data")
def set_cards_custom_data(col: Collection, cards: Sequence[Card]) -> OpChanges:
    for card in cards:
        set_correct_custom_data(col, card)

    # save the cards and add an undo entry.
    return col.update_cards(cards)


def get_cards_to_update_custom_data(browser: Browser):
    selected_cards = list(get_selected_cards(browser))
    # new_cards = list(filter(is_new, selected_cards))

    if len(selected_cards) < 1:
        notify_user("No  cards selected. Nothing to do.")
    else:
        CollectionOp(parent=browser, 
                    op=lambda col: set_cards_custom_data(col, selected_cards)).success(
                    lambda out: notify_user(
                format_message_custom_data_updates(
                    selected_cards))
        ).run_in_background()







def format_message_update_suspension(accepted: Sized) -> str:
    msg = []

    if (num_accepted := len(accepted)) > 0:
        msg.append(
            ngettext(
                f"{num_accepted} card is now correctly suspended/unsuspended..",
                f"{num_accepted} cards are now correctly suspended/unsuspended.",
                num_accepted,
            )
        )

    return " ".join(msg)


def set_correct_note_count(col, note: Note):
    note_count = None
    target_template_name= 'Level 1'
    # Find the card with the target template name and get its note_count
    for card in note.cards():
        if card.template()['name'] == target_template_name:
            note_count = masteryCardAdder.get_note_success_count(card)
            break

    if note_count is None:
        print(f"No card with template '{target_template_name}' found.")
        return
    
    # Set this note_count on all cards of the note
    # ! ONLY need to worry about +/- note count if we add or remove a card
    # ! For simple moving cards around just to current card note count
    for card in note.cards():
        masteryCardAdder.set_note_success_count(card, note_count) # we can +/- here
    
    # Update suspend/unsuspend based on new note_count
    masteryCardAdder.suspend_unsuspend_cards_ruled(note, note_count) # do the same amount +/- here





@with_undo_entry(undo_msg="Set corrected unlock Notes")
def set_note_suspension(col: Collection, notes: Sequence[Note]) -> OpChanges:
    for note in notes:
        set_correct_note_count(col, note)


    # save the cards and add an undo entry.
    return col.update_notes(notes)


def get_note_to_update_suspension_stats(browser: Browser):
    selected_notes = list(get_selected_notes(browser))

    if len(selected_notes) < 1:
        notify_user("No Notes selected. Nothing to do.")
    else:
        CollectionOp(parent=browser, 
                    op=lambda col: set_note_suspension(col, selected_notes)).success(
                    lambda out: notify_user(
                format_message_update_suspension(
                    selected_notes))
        ).run_in_background()




def move_graduated_notes(col: Collection, notes: Sequence[Note]) -> OpChanges:
    moved_notes = []
    for note in notes:
        max_level = 21
        for card in note.cards():
            note_level = masteryCardAdder.get_note_success_count(card)
            if note_level >= max_level or note.has_tag("status::understandable"):
                print(f"Graduating note {note.id} with level {note_level}")
                masteryCardAdder.move_note_to_deck(note)
                moved_notes.append(note)
                break  # only need to move once per note

    return col.update_notes(moved_notes)

def get_note_to_graduate(browser: Browser):
    selected_notes = list(get_selected_notes(browser))

    if not selected_notes:
        notify_user("No Notes selected. Nothing to do.")
    else:
        CollectionOp(parent=browser, 
                    op=lambda col: move_graduated_notes(col, selected_notes)).success(
            lambda _: notify_user("Graduated eligible notes.")
        ).run_in_background()




def on_browser_menus_did_init(browser: Browser) -> None:
    action = browser.form.menu_Cards.addAction("Set Custom Data Blank 0-0")
    qconnect(action.triggered, functools.partial(get_cards_to_update_custom_data, browser=browser))

    action = browser.form.menu_Cards.addAction("Resuspension Of Levels with Set Note Count")
    qconnect(action.triggered, functools.partial(get_note_to_update_suspension_stats, browser=browser))

    action = browser.form.menu_Cards.addAction("Graduate Notes to New Deck")
    qconnect(action.triggered, functools.partial(get_note_to_graduate, browser=browser))