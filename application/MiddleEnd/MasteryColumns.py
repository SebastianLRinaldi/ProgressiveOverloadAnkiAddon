
from aqt.browser import Column, Cell, CellRow
from anki.collection import BrowserColumns as BC
from aqt.browser.table import BrowserRow
from aqt import mw

from application.MiddleEnd.MasteryCardGraderWCustomData import masteryCardAdder

def add_column(columns: dict[str, Column]) -> None:
        columns["SearchProp"] = Column(
        key="searchprop",
        cards_mode_label="Card Count",
        notes_mode_label="Note Count",
        sorting_cards=1,
        sorting_notes=1,
        # sorting_cards=BC.Sorting.SORTING_NONE,
        # sorting_notes=BC.Sorting.SORTING_NONE,
        # uses_cell_font=True,
        # alignment=BC.Alignment.ALIGNMENT_START,
    )


def fill_column(unit_id: int, is_note: bool, row: CellRow, columns: dict[str, Column]) -> CellRow:
    try:
        idx = list(columns).index("SearchProp")
    except ValueError:
        # Column not present, bail out
        return

    cells = list(row.cells)
    # print(f"ID={idx}[SearchProp] | {len(cells)} | {cells[idx]} |LIST={list(columns)}")
    

    if is_note:
        note = mw.col.get_note(unit_id)  # or however you get the note by card id or note id
        card = note.cards()[0]
        note_sct = masteryCardAdder.get_note_success_count(card)
        cells[idx].text = f"notesct={note_sct}"
        
    else:
        card = mw.col.get_card(unit_id)
        card_sct = masteryCardAdder.get_card_success_count(card)
        cells[idx].text = f"cardsct={card_sct}" 




"""
Apply a serach to the column
"""
# from aqt.browser import Column, Cell, CellRow
# from aqt.browser.table import BrowserRow

# SEARCH_EXPR = "prop:cdn:notesct>0"
# _cached_ids = set()

# def add_column(columns: dict[str, Column]) -> None:
#         columns["SearchProp"] = Column(
#         key="searchprop",
#         cards_mode_label="Card Count",
#         notes_mode_label="Note Count",
#     )


# def fill_column(unit_id: int, is_note: bool, row: CellRow, columns: dict[str, Column]) -> CellRow:
#     try:
#         idx = list(columns).index("SearchProp")
#     except ValueError:
#         # Column not present, bail out
#         return

#     if not _cached_ids:
#         _cached_ids.update(mw.col.find_cards(SEARCH_EXPR))

#     cells = list(row.cells)
#     print(f"ID={idx}[SearchProp] | {len(cells)} | {cells[idx]} |LIST={list(columns)}")
    


#     if is_note:
#         note = mw.col.get_note(unit_id)  # or however you get the note by card id or note id
#         # Example: mark cell if note has certain property
#         cells[idx].text = "Note✓" if unit_id in _cached_ids else ""
#     else:
#         card = mw.col.get_card(unit_id)
#         cells[idx].text = "Card✓" if unit_id in _cached_ids else ""



# gui_hooks.browser_did_fetch_columns.append(add_column)
# gui_hooks.browser_did_fetch_row.append(fill_column)
