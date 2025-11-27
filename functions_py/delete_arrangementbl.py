#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Argt_line, Arrangement

def delete_arrangementbl(case_type:int, int1:int, int2:int):
    success_flag = False
    argt_line = arrangement = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, argt_line, arrangement
        nonlocal case_type, int1, int2

        return {"success_flag": success_flag}


    if case_type == 1:

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == int1)).order_by(Argt_line._recid).with_for_update().all():
            db_session.delete(argt_line)

        # arrangement = get_cache (Arrangement, {"argtnr": [(eq, int1)]})
        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.argtnr == int1)).with_for_update().first()

        if arrangement:
            db_session.delete(arrangement)
            success_flag = True

    elif case_type == 2:

        for argt_line in db_session.query(Argt_line).filter(
                 (Argt_line.argtnr == int1)).order_by(Argt_line._recid).with_for_update().all():
            db_session.delete(argt_line)

        # arrangement = get_cache (Arrangement, {"_recid": [(eq, int2)]})
        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement._recid == int2)).with_for_update().first()

        if arrangement:
            db_session.delete(arrangement)
            success_flag = True

    return generate_output()