#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 10/10/2025
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal

def update_bemerkbl(jou_recid:int):

    prepare_cache ([Gl_journal])

    gl_journal = None

    note_list = None

    note_list_data, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":string, "add_note":string, "orig_note":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_journal
        nonlocal jou_recid


        nonlocal note_list
        nonlocal note_list_data

        return {}

    def create_new_note():

        nonlocal gl_journal
        nonlocal jou_recid
        nonlocal note_list
        nonlocal note_list_data

        s1:string = ""
        s2:string = ""
        n:int = 0
        note_list = Note_list()
        note_list_data.append(note_list)

        note_list.s_recid = gl_journal._recid
        n = get_index(gl_journal.bemerk, ";&&")

        if n > 0:
            s1 = substring(gl_journal.bemerk, 0, n - 1)
            note_list.s_recid = gl_journal._recid
            note_list.bemerk = substring(gl_journal.bemerk, 0, n - 1)
            note_list.add_note = substring(gl_journal.bemerk, n - 1, length(gl_journal.bemerk))
        else:
            note_list.s_recid = gl_journal._recid
            note_list.bemerk = gl_journal.bemerk


        note_list.orig_note = note_list.bemerk


    def update_bemerk():

        nonlocal gl_journal
        nonlocal jou_recid
        nonlocal note_list
        nonlocal note_list_data

        gl_jou = None
        Gl_jou =  create_buffer("Gl_jou",Gl_journal)

        for note_list in query(note_list_data, filters=(lambda note_list: note_list.bemerk != note_list.orig_note)):
            note_list.orig_note = note_list.bemerk

            gl_jou = get_cache (Gl_journal, {"_recid": [(eq, note_list.s_recid)]})

            if gl_jou:
                pass
                gl_jou.bemerk = note_list.bemerk + note_list.add_note
                pass


    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, jou_recid)]})

    if gl_journal:
        create_new_note()
        update_bemerk()

    return generate_output()