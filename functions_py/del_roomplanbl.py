#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Resplan, Zimplan

na_list_data, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":string, "anz":int})

def del_roomplanbl(na_list_data:[Na_list], ci_date:date):

    prepare_cache ([Htparam])

    i = 0
    htparam = resplan = zimplan = None

    na_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, htparam, resplan, zimplan
        nonlocal ci_date


        nonlocal na_list

        return {"na-list": na_list_data, "i": i}

    def del_roomplan():

        nonlocal i, htparam, resplan, zimplan
        nonlocal ci_date


        nonlocal na_list

        # resplan = get_cache (Resplan, {"datum": [(ge, ci_date)]})
        resplan = db_session.query(Resplan).filter(
                 (Resplan.datum >= ci_date)).with_for_update().first()

        na_list = query(na_list_data, filters=(lambda na_list: na_list.reihenfolge == 1), first=True)
        while None != resplan:
            i = i + 1
            na_list.anz = na_list.anz + 1
            # pass
            db_session.delete(resplan)
            db_session.refresh(resplan,with_for_update=True)
            # pass

            curr_recid = resplan._recid
            resplan = db_session.query(Resplan).filter(
                     (Resplan.datum >= ci_date) & (Resplan._recid > curr_recid)).first()

        # zimplan = get_cache (Zimplan, {"datum": [(ge, ci_date)]})
        zimplan = db_session.query(Zimplan).filter(
                 (Zimplan.datum >= ci_date)).with_for_update().first()
        while None != zimplan:
            i = i + 1
            na_list.anz = na_list.anz + 1
            # pass
            db_session.delete(zimplan)
            db_session.refresh(zimplan,with_for_update=True)
            # pass

            curr_recid = zimplan._recid
            zimplan = db_session.query(Zimplan).filter(
                     (Zimplan.datum >= ci_date) & (Zimplan._recid > curr_recid)).first()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 592)]})
    htparam.flogical = True


    pass
    del_roomplan()

    return generate_output()