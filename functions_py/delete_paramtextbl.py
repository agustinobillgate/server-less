#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Zimmer

def delete_paramtextbl(case_type:int, int1:int, int2:int, int3:int):
    success_flag = False
    counter:int = 0
    paramtext = zimmer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, counter, paramtext, zimmer
        nonlocal case_type, int1, int2, int3

        return {"success_flag": success_flag}


    if case_type == 1:

        # paramtext = get_cache (Paramtext, {"txtnr": [(eq, int1)],"number": [(eq, int2)],"sprachcode": [(eq, int3)]})
        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == int1) &
                 (Paramtext.number == int2) &
                 (Paramtext.sprachcode == int3)).with_for_update().first()

        if paramtext:
            db_session.delete(paramtext)
            pass
            success_flag = True
    elif case_type == 2:

        # paramtext = get_cache (Paramtext, {"txtnr": [(eq, int1)],"number": [(eq, int2)],"sprachcode": [(eq, int3)]})
        paramtext = db_session.query(Paramtext).filter(
                 (Paramtext.txtnr == int1) &
                 (Paramtext.number == int2) &
                 (Paramtext.sprachcode == int3)).with_for_update().first()

        if paramtext:

            zimmer = get_cache (Zimmer, {"setup": [(eq, paramtext.txtnr - 9200)]})

            if not zimmer and paramtext.txtnr == 230:

                zimmer = get_cache (Zimmer, {"typ": [(eq, paramtext.sprachcode)]})

            if not zimmer:
                db_session.delete(paramtext)
                pass
                success_flag = True

    return generate_output()