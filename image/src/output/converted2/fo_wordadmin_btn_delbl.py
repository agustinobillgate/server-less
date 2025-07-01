#using conversion tools version: 1.0.0.111

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


    briefzei = get_cache (Briefzei, {"briefnr": [(eq, briefnr)],"briefzeilnr": [(eq, 1)]})

    if briefzei:
        db_session.delete(briefzei)

    brief = get_cache (Brief, {"briefnr": [(eq, int1)]})

    if brief:
        db_session.delete(brief)
    success_flag = True

    return generate_output()