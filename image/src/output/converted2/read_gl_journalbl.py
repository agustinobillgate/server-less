#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_journal

def read_gl_journalbl(case_type:int, int1:int, int2:int, int3:int, deci1:Decimal, deci2:Decimal, char1:string, char2:string, char3:string, date1:date, date2:date):
    t_gl_journal_list = []
    rechnr:string = ""
    gl_journal = None

    t_gl_journal = None

    t_gl_journal_list, T_gl_journal = create_model_like(Gl_journal, {"b_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_gl_journal_list, rechnr, gl_journal
        nonlocal case_type, int1, int2, int3, deci1, deci2, char1, char2, char3, date1, date2


        nonlocal t_gl_journal
        nonlocal t_gl_journal_list

        return {"t-gl-journal": t_gl_journal_list}

    if case_type == 1:

        gl_journal = get_cache (Gl_journal, {"jnr": [(eq, int1)]})

        if gl_journal:
            t_gl_journal = T_gl_journal()
            t_gl_journal_list.append(t_gl_journal)

            buffer_copy(gl_journal, t_gl_journal)
            t_gl_journal.b_recid = gl_journal._recid


    elif case_type == 2:

        gl_journal = get_cache (Gl_journal, {"_recid": [(eq, int1)]})

        if gl_journal:
            t_gl_journal = T_gl_journal()
            t_gl_journal_list.append(t_gl_journal)

            buffer_copy(gl_journal, t_gl_journal)
            t_gl_journal.b_recid = gl_journal._recid


    elif case_type == 3:

        gl_journal = db_session.query(Gl_journal).filter(
                 ((num_entries(Gl_journal.bemerk, "-") > 0) & (trim(entry(0, Gl_journal.bemerk, "-")) == (char1).lower())) | ((num_entries(Gl_journal.bemerk, "-") == 0) & (Gl_journal.bemerk == (char1).lower()))).first()

        if gl_journal:
            t_gl_journal = T_gl_journal()
            t_gl_journal_list.append(t_gl_journal)

            buffer_copy(gl_journal, t_gl_journal)
            t_gl_journal.b_recid = gl_journal._recid

    return generate_output()