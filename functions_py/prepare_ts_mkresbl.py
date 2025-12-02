#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added, skip
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Tisch

def prepare_ts_mkresbl(s_recid:int, curr_dept:int):

    prepare_cache ([Queasy, Tisch])

    gname = ""
    telefon = ""
    comments = ""
    t_tisch_data = []
    queasy = tisch = None

    t_tisch = None

    t_tisch_data, T_tisch = create_model("T_tisch", {"tischnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, telefon, comments, t_tisch_data, queasy, tisch
        nonlocal s_recid, curr_dept


        nonlocal t_tisch
        nonlocal t_tisch_data

        return {"gname": gname, "telefon": telefon, "comments": comments, "t-tisch": t_tisch_data}

    if s_recid != 0:

        queasy = get_cache (Queasy, {"_recid": [(eq, s_recid)]})
        gname = entry(0, queasy.char2, "&&")
        telefon = trim(substring(queasy.char1, 9))
        comments = entry(1, queasy.char3, ";")

    for tisch in db_session.query(Tisch).filter(
             (Tisch.departement == curr_dept)).order_by(Tisch._recid).all():
        t_tisch = T_tisch()
        t_tisch_data.append(t_tisch)

        t_tisch.tischnr = tisch.tischnr

    return generate_output()