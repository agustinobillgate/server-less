#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Briefzei, Brief

def delete_briefzeibl(case_type:int, int1:int, int2:int):
    successflag = False
    briefzei = brief = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, briefzei, brief
        nonlocal case_type, int1, int2

        return {"successflag": successflag}


    if case_type == 1:

        # briefzei = get_cache (Briefzei, {"briefnr": [(eq, int1)],"briefzeilnr": [(eq, int2)]})
        briefzei = db_session.query(Briefzei).filter(
                 (Briefzei.briefnr == int1) &
                 (Briefzei.briefzeilnr == int2)).with_for_update().first()

        if briefzei:
            db_session.delete(briefzei)
            pass
            successflag = True


    elif case_type == 2:

        # briefzei = get_cache (Briefzei, {"briefnr": [(eq, int1)],"briefzeilnr": [(eq, 1)]})
        briefzei = db_session.query(Briefzei).filter(
                 (Briefzei.briefnr == int1) &
                 (Briefzei.briefzeilnr == 1)).with_for_update().first()

        if briefzei:
            db_session.delete(briefzei)
            pass

        # brief = get_cache (Brief, {"briefnr": [(eq, int2)]})
        brief = db_session.query(Brief).filter(
                 (Brief.briefnr == int2)).with_for_update().first()

        if brief:
            db_session.delete(brief)
            pass
            successflag = True

    return generate_output()