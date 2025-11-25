#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 25/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Gl_journal

def delete_gl_journalbl(case_type:int, int1:int, str1:string):
    successflag = False
    gl_journal = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, gl_journal
        nonlocal case_type, int1, str1

        return {"successflag": successflag}


    if case_type == 1:

        # gl_journal = get_cache (Gl_journal, {"_recid": [(eq, int1)]})
        gl_journal = db_session.query(Gl_journal).filter(
                     (Gl_journal._recid == int1)).with_for_update().first()

        if gl_journal:
            db_session.delete(gl_journal)
            pass
            successflag = True
        else:
            successflag = False


    elif case_type == 2:
        # Rd, 25/11/2025, .with_for_update added
        for gl_journal in db_session.query(Gl_journal).filter(
                 ((num_entries(Gl_journal.bemerk, "-") > 0) & 
                  (trim(entry(0, Gl_journal.bemerk, "-")) == (str1))) | ((num_entries(Gl_journal.bemerk, "-") == 0) & 
                                                                         (Gl_journal.bemerk == (str1)))).order_by(Gl_journal._recid).with_for_update().all():
            db_session.delete(gl_journal)
        pass
        successflag = True


    elif case_type == 3:
        # Rd, 25/11/2025, .with_for_update added
        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == int1)).order_by(Gl_journal._recid).with_for_update().all():
            db_session.delete(gl_journal)
        pass
        successflag = True

    return generate_output()