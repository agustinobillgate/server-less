from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_journal

def read_gl_journalbl(case_type:int, int1:int, int2:int, int3:int, deci1:decimal, deci2:decimal, char1:str, char2:str, char3:str, date1:date, date2:date):
    t_gl_journal_list = []
    gl_journal = None

    t_gl_journal = None

    t_gl_journal_list, T_gl_journal = create_model_like(Gl_journal, {"b_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_journal_list, gl_journal


        nonlocal t_gl_journal
        nonlocal t_gl_journal_list
        return {"t-gl-journal": t_gl_journal_list}

    if case_type == 1:

        gl_journal = db_session.query(Gl_journal).filter(
                (Gl_journal.jnr == int1)).first()

        if gl_journal:
            t_gl_journal = T_gl_journal()
            t_gl_journal_list.append(t_gl_journal)

            buffer_copy(gl_journal, t_gl_journal)
            t_gl_journal.b_recid = gl_journal._recid


    elif case_type == 2:

        gl_journal = db_session.query(Gl_journal).filter(
                (Gl_journal._recid == int1)).first()

        if gl_journal:
            t_gl_journal = T_gl_journal()
            t_gl_journal_list.append(t_gl_journal)

            buffer_copy(gl_journal, t_gl_journal)
            t_gl_journal.b_recid = gl_journal._recid


    elif case_type == 3:

        gl_journal = db_session.query(Gl_journal).filter(
                (func.lower(Gl_journal.bemerk) == (char1).lower())).first()

        if gl_journal:
            t_gl_journal = T_gl_journal()
            t_gl_journal_list.append(t_gl_journal)

            buffer_copy(gl_journal, t_gl_journal)
            t_gl_journal.b_recid = gl_journal._recid

    return generate_output()