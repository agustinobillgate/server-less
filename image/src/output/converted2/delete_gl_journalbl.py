from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Gl_journal

def delete_gl_journalbl(case_type:int, int1:int, str1:str):
    successflag = False
    gl_journal = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, gl_journal
        nonlocal case_type, int1, str1


        return {"successflag": successflag}


    if case_type == 1:

        gl_journal = db_session.query(Gl_journal).filter(
                 (Gl_journal._recid == int1)).first()

        if gl_journal:
            db_session.delete(gl_journal)
            pass
            successflag = True


        else:
            successflag = False


    elif case_type == 2:

        for gl_journal in db_session.query(Gl_journal).filter(
                 (func.lower(Gl_journal.bemerk) == (str1).lower())).order_by(Gl_journal._recid).all():
            db_session.delete(gl_journal)
        pass
        successflag = True


    elif case_type == 3:

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == int1)).order_by(Gl_journal._recid).all():
            db_session.delete(gl_journal)
        pass
        successflag = True

    return generate_output()