from PyQt6.QtWidgets import QListWidgetItem
from aqt import mw
from html import escape

from application.MiddleEnd.MasteryDatahandler import MasteryDataHandler
from application.FrontEnd.B_WidgetsFolder.WidgetInitializations.WidgetInitialization import *
from application.MiddleEnd.integreation.MasterTypes import *
from application.FrontEnd.presentation.PreviewWindow import PreviewWindow

def get_selected_NoteType_obeject() -> NoteTypeItem:
    return note_type_drop_down.currentData()


def preview_cards_with_template(item: QListWidgetItem):
    
    # mw.col.models.template_use_count()
    # Get note ids that use the note_type search by NoteType _id
    # mw.col.models.nids()
    # if template has cards is not None:
    #     mw.col.card_ids_of_note()
    # mw.col.models.get(noteitem.note_id) --> dict_keys(['id', 'name', 'type', 'mod', 'usn', 'sortf', 'did', 'tmpls', 'flds', 'css', 'latexPre', 'latexPost', 'latexsvg', 'req'])
        
    # mw.col.models.get(noteitem.note_id)["tmpls"][0].keys() #--> dict_keys(['name', 'ord', 'qfmt', 'afmt', 'bqfmt', 'bafmt', 'did', 'bfont', 'bsize', 'id'])
    # mw.col.models.merge_undo_entries
    
    
    # mw.col.models.field_names()
    
    # qfmt', 'afmt', 'bqfmt', 'bafmt'
    
    selected_note_type_item = get_selected_NoteType_obeject()
    
    template_name = item.text()
    
    # print(mw.col.models.by_name(template_name).keys())
    

    # templates = mw.col.models.get(note_type_item.note_type_id)["tmpls"]
    
    # question, answer = template.get("bqfmt"), template.get("bafmt")
    
    
    template_index = template_levels_list.row(item)
    print("Template Index:", template_index)
    
    some_css = mw.col.models.get(selected_note_type_item.note_type_id)['css']
    q = mw.col.models.get(selected_note_type_item.note_type_id)["tmpls"][template_index]["qfmt"]
    a = mw.col.models.get(selected_note_type_item.note_type_id)["tmpls"][template_index]["afmt"]
    # q = escape(q)
    # a = escape(a)
    # bq = mw.col.models.get(selected_note_type_item.note_type_id)["tmpls"][0]["bqfmt"]
    # ba = mw.col.models.get(selected_note_type_item.note_type_id)["tmpls"][0]["bafmt"]
    
    print(f"======================")
    print(f"qf: {q}")
    print(f"======================")
    print(f"af: {a}")
    print(f"======================")
    
    """
    Get names of template 
    click a name of tempalte 
    we want to view that template 
        but we only have the name
    
    so we need to search for the note_type id
        so we can get more info about the template that we clicked
    
    """
    
    html = f"""
        <style>
        .card-container {{
            display: flex;
            flex-direction: column;
            gap: 20px; /* Space between cards */
        }}

        .card {{
            padding: 20px;
            font-size: 16px;
            background-color: #f4f4f4; /* Card background */
            border-radius: 5px;
            color:black;
        }}

        .front {{
            background-color: #fff; /* White background for the front */
            padding: 20px;
            border-radius: 5px;
        }}

        .back {{
            background-color: #fff; /* White background for the back */
            padding: 20px;
            border-radius: 5px;
        }}
        </style>

        <div class="card-container">
            <div class="card">
                <div class="front">{q}</div>
            </div>
            <div class="card">
                <div class="back">{a}</div>
            </div>
        </div>
    """
    
    web_view.stdHtml(html, css=[some_css])
    
    PreviewWindow()