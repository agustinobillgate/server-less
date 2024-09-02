from functions.additional_functions import *
import decimal
from models import Gl_journal

def update_bemerkbl(jou_recid:int):
    gl_journal = None

    note_list = gl_jou = None

    note_list_list, Note_list = create_model("Note_list", {"s_recid":int, "bemerk":str, "add_note":str, "orig_note":str})

    Gl_jou = Gl_journal

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_journal
        nonlocal gl_jou


        nonlocal note_list, gl_jou
        nonlocal note_list_list
        return {}

    def create_new_note():

        nonlocal gl_journal
        nonlocal gl_jou


        nonlocal note_list, gl_jou
        nonlocal note_list_list

        s1:str = ""
        s2:str = ""
        n:int = 0
        note_list = Note_list()
        note_list_list.append(note_list)

        note_list.s_recid = gl_journal._recid
        n = 1 + get_index(gl_journal.bemerk, ";&&")

        if n > 0:
            s1 = substring(gl_journal.bemerk, 0, n - 1)
            note_list.s_recid = gl_journal._recid
            note_list.bemerk = substring(gl_journal.bemerk, 0, n - 1)
            note_list.add_note = substring(gl_journal.bemerk, n - 1, LENGTH (gl_journal.bemerk))


        else:
            note_list.s_recid = gl_journal._recid
            note_list.bemerk = gl_journal.bemerk


        note_list.orig_note = note_list.bemerk

    def update_bemerk():

        nonlocal gl_journal
        nonlocal gl_jou


        nonlocal note_list, gl_jou
        nonlocal note_list_list


        Gl_jou = Gl_journal

        for note_list in query(note_list_list, filters=(lambda note_list :note_list.bemerk != orig_note)):
            note_list.orig_note = note_list.bemerk

            gl_jou = db_session.query(Gl_jou).filter(
                    (Gl_jou._recid == note_list.s_recid)).first()

            if gl_jou:

                gl_jou = db_session.query(Gl_jou).first()
                gl_jou.bemerk = note_list.bemerk + note_list.add_note

                gl_jou = db_session.query(Gl_jou).first()

    gl_journal = db_session.query(Gl_journal).filter(
            (Gl_journal._recid == jou_recid)).first()
    create_new_note()
    update_bemerk()

    return generate_output()