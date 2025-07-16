import json
from aqt import mw
from anki.cards import Card
from anki.notes import Note
from aqt.clayout import CardLayout

from application.MiddleEnd.MasteryCardGraderWCustomData import masteryCardAdder, MasterySharedUtils


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


"""
Need to add a if note type in MasteryData then do this
"""
class CardLayoutMasteryConnection():

    def __init__(self, masteryCardAdder):
        self.masteryUtil = MasterySharedUtils()
        self.dialog = None
        self.original = None
        self.updated = None
        self.masteryCardAdder = masteryCardAdder


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
                result['removed'].append({
                    "id": tid,
                    "name": orig_templates[tid]['name'],
                    "position": orig_order.index(tid)
                })

        # Added
        for tid in upd_templates:
            if tid not in orig_templates:
                result['added'].append({
                    "id": tid,
                    "name": upd_templates[tid]['name'],
                    "position": upd_order.index(tid)
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
            self.updated = self.dialog.note.note_type()
            print(f"\nGot Updates - {self.dialog.note.id}")
            results = self.diff_note_types(self.original, self.updated)
            print(json.dumps(results, indent=4, ensure_ascii=False))
            


            # orig_templates = {t['id']: t for t in self.original['tmpls']}
            # upd_templates = {t['id']: t for t in self.updated['tmpls']}

            # orig_order = [t['id'] for t in self.original['tmpls']]
            # upd_order = [t['id'] for t in self.updated['tmpls']]


            # print(json.dumps(orig_templates, indent=4, ensure_ascii=False))
            # print(json.dumps(upd_templates, indent=4, ensure_ascii=False))
            # print(json.dumps(orig_order, indent=4, ensure_ascii=False))
            # print(json.dumps(upd_order, indent=4, ensure_ascii=False))


            reference_json = [...]  # your name-based template JSON
            original_templates = self.original['tmpls']
            updated_order_ids = [t['id'] for t in self.updated['tmpls']]

            # synced_reference = self.reorder_reference_json(reference_json, original_templates, updated_order_ids)



            self.dialog = None
            self.original = None
            self.updated = None


    def on_card_layout_show(self, dialog: CardLayout):
        self.original = dialog.note.note_type()
        self.dialog = dialog
        print(f"Saved Orginal {dialog.note.id}")




    # def reorder_reference_json(self, reference_json, original_templates, updated_order_ids):
    #     # Map names to IDs from original
    #     name_to_id = {t['name']: t['id'] for t in original_templates}
    #     id_to_ref = {name_to_id[entry['name']]: entry for entry in reference_json}

    #     # Reorder based on updated ID order
    #     reordered = [id_to_ref[tid] for tid in updated_order_ids if tid in id_to_ref]
    #     return reordered



    def SetDataLevels(self):
        """
        if levels (templs) are 
            added below higher levels
                (all levels above) must get addtional notecounts

            (These new templates must be correctly suspended in notes)

            removed below higher levels
                (all levels above) must get remove notecounts
        """
        # note_type = mw.col.models.by_name("YourNoteTypeName")



        # get new template order 
        
        # if new template has items above its current oreder index 
        #   then do stuff to those cards only 

        
        keys = list(templates.keys())
        results = {k: templates[k] for k in keys[pos:]}





        
        # # Get all cards with this template
        # def get_all_cards_with_template(self, note:Note):
        #     for index, card in enumerate(note.cards()):
        #         template_name = card.template()['name']


        # self.masteryUtil.get_card_success_count()
















        
        """
        if levels (templs) are reordered
            move pos of original to updated to match in MasteryData
            Resuspend correctly? just keep current card count? or 
            [for all cards below unsuspended max out? 
                Then all cards above unsuspended reset
                Then set current unsuspended at card count 0?]
            ? make it so numbers are set as names too? and force new numbers too
        """


        """
        if current levels in masteryData are
            given addtional reps 
                (all levels above) must get addtional notecounts
                (just that card type) must get addtional card counts

            reduced reps 
                (all levels above) must get a reduction of notecounts
                (just that card type) must get reduction card counts
        """
