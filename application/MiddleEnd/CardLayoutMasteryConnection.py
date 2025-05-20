import json

def test_msg():
    print("SOME CHANGE HAPPENED")



"""
    aqt main.py
    # Tools
    qconnect(m.actionNoteTypes.triggered, self.onNoteTypes)

    def onNoteTypes(self) -> None:
        import aqt.models
        aqt.models.Models(self, self, fromMain=True)

    aqt models.py
    def onCards(self) -> None:
        from aqt.clayout import CardLayout

    aqt clayout
    if not self._isCloze():
        a = m.addAction(tr.card_templates_add_card_type())
        assert a is not None
        qconnect(a.triggered, self.onAddCard)
"""

# def my_hook(notetype):
#     print(f"WE GOT IT: {notetype}")
#     # print("Note type edited:", notetype["name"])
#     # print("Templates:", [t["name"] for t in notetype["tmpls"]])

# # gui_hooks.current_note_type_did_change.append(test_msg)
# mw.form.actionNoteTypes.triggered.connect(my_hook)


# gui_hooks.card_layout_will_show()

from aqt.clayout import CardLayout
import copy




def diff_note_types(original, updated):
    result = {
        'name_changed': original['name'] != updated['name'],
        'name_original': original['name'],
        'name_updated': updated['name'],
        'renamed': [],
        'reordered': [],
        'added': [],
        'removed': []
    }

    orig_templates = {t['id']: t for t in original['tmpls']}
    upd_templates = {t['id']: t for t in updated['tmpls']}

    orig_order = [t['id'] for t in original['tmpls']]
    upd_order = [t['id'] for t in updated['tmpls']]

    # Removed
    for tid in orig_templates:
        if tid not in upd_templates:
            # result['removed'].append(orig_templates[tid]['name'])
            result['removed'].append({
                "id": tid,
                str(orig_order.index(tid)): orig_templates[tid]['name']
            })

    # Added
    for tid in upd_templates:
        if tid not in orig_templates:
            # result['added'].append(upd_templates[tid]['name'])
            result['added'].append({
                "id": tid,
                str(upd_order.index(tid)): upd_templates[tid]['name']
            })
    # Renamed
    for tid in orig_templates:
        if tid in upd_templates and orig_templates[tid]['name'] != upd_templates[tid]['name']:
            result['renamed'].append({
                "id": tid,
                "from": orig_templates[tid]['name'],
                "to": upd_templates[tid]['name']
            })

    # Reordered
    common_ids = [tid for tid in orig_order if tid in upd_order]
    for tid in common_ids:
        if orig_order.index(tid) != upd_order.index(tid):
            result['reordered'].append({
                "id": tid,
                "name": orig_templates[tid]['name'],
                "from_pos": orig_order.index(tid),
                "to_pos": upd_order.index(tid)
            })

    return result



def on_op_complete(changes, handler, dialog, original):
    if not isinstance(dialog, CardLayout):
        pass
    else:
        updated = dialog.note.note_type()
        print(f"Got Updates - {dialog.note.id}")
        results = diff_note_types(original, updated)
        print(json.dumps(results, indent=4, ensure_ascii=False))

        # Will find a better way to manage this
        # gui_hooks.operation_did_execute.remove(lambda changes, handler: on_op_complete(changes, handler, dialog, original))


    

def on_card_layout_show(dialog: CardLayout):
    original = dialog.note.note_type()
    
    print(f"Saved Orginal {dialog.note.id}")

    
    
#     gui_hooks.operation_did_execute.append(lambda changes, handler: on_op_complete(changes, handler, dialog, original))

# gui_hooks.card_layout_will_show.append(on_card_layout_show)




class CardLayoutMasteryConnection():

    def __init__(self):
        self.dialog = None
        self.original = None


    def diff_note_types(self, original, updated):
        result = {
            'name_changed': original['name'] != updated['name'],
            'name_original': original['name'],
            'name_updated': updated['name'],
            'renamed': [],
            'reordered': [],
            'added': [],
            'removed': []
        }

        orig_templates = {t['id']: t for t in original['tmpls']}
        upd_templates = {t['id']: t for t in updated['tmpls']}

        orig_order = [t['id'] for t in original['tmpls']]
        upd_order = [t['id'] for t in updated['tmpls']]

        # Removed
        for tid in orig_templates:
            if tid not in upd_templates:
                # result['removed'].append(orig_templates[tid]['name'])
                result['removed'].append({
                    "id": tid,
                    str(orig_order.index(tid)): orig_templates[tid]['name']
                })

        # Added
        for tid in upd_templates:
            if tid not in orig_templates:
                # result['added'].append(upd_templates[tid]['name'])
                result['added'].append({
                    "id": tid,
                    str(upd_order.index(tid)): upd_templates[tid]['name']
                })
        # Renamed
        for tid in orig_templates:
            if tid in upd_templates and orig_templates[tid]['name'] != upd_templates[tid]['name']:
                result['renamed'].append({
                    "id": tid,
                    "from": orig_templates[tid]['name'],
                    "to": upd_templates[tid]['name']
                })

        # Reordered
        common_ids = [tid for tid in orig_order if tid in upd_order]
        for tid in common_ids:
            if orig_order.index(tid) != upd_order.index(tid):
                result['reordered'].append({
                    "id": tid,
                    "name": orig_templates[tid]['name'],
                    "from_pos": orig_order.index(tid),
                    "to_pos": upd_order.index(tid)
                })

        return result



    def on_op_complete(self, changes, handler):
        if not isinstance(self.dialog, CardLayout):
            pass
        else:
            updated = self.dialog.note.note_type()
            print(f"Got Updates - {self.dialog.note.id}")
            results = diff_note_types(self.original, updated)
            print(json.dumps(results, indent=4, ensure_ascii=False))
            self.dialog = None
            self.original = None


            # Will find a better way to manage this
            # gui_hooks.operation_did_execute.remove(lambda changes, handler: on_op_complete(changes, handler, dialog, original))


        

    def on_card_layout_show(self, dialog: CardLayout):
        self.original = dialog.note.note_type()
        self.dialog = dialog
        print(f"Saved Orginal {dialog.note.id}")