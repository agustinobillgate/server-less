from functions.additional_functions import *
import decimal
from models import Briefzei, Brief

def delete_briefzeibl(case_type:int, int1:int, int2:int):
    successflag = False
    briefzei = brief = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, briefzei, brief


        return {"successflag": successflag}


    if case_type == 1:

        briefzei = db_session.query(Briefzei).filter(
                (Briefzei.briefnr == int1) &  (Briefzei.briefzeilnr == int2)).first()

        if briefzei:
            db_session.delete(briefzei)

            successflag = True


    elif case_type == 2:

        briefzei = db_session.query(Briefzei).filter(
                (Briefzei.briefnr == int1) &  (Briefzei.briefzeilnr == 1)).first()

        if briefzei:
            db_session.delete(briefzei)


        brief = db_session.query(Brief).filter(
                (Brief.briefnr == int2)).first()

        if brief:
            db_session.delete(brief)

            successflag = True

    return generate_output()