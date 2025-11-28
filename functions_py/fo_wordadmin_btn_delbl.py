#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Briefzei, Brief

def fo_wordadmin_btn_delbl(briefnr:int, int1:int):
    success_flag = False
    briefzei = brief = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, briefzei, brief
        nonlocal briefnr, int1

        return {"success_flag": success_flag}


    # briefzei = get_cache (Briefzei, {"briefnr": [(eq, briefnr)],"briefzeilnr": [(eq, 1)]})
    briefzei = db_session.query(Briefzei).filter(
             (Briefzei.briefnr == briefnr) & (Briefzei.briefzeilnr == 1)).with_for_update().first()

    if briefzei:
        db_session.delete(briefzei)

    # brief = get_cache (Brief, {"briefnr": [(eq, int1)]})
    brief = db_session.query(Brief).filter(Brief.briefnr == int1).with_for_update().first()

    if brief:
        db_session.delete(brief)
    success_flag = True

    return generate_output()