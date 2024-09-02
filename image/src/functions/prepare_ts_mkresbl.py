from functions.additional_functions import *
import decimal
from models import Queasy, Tisch

def prepare_ts_mkresbl(s_recid:int, curr_dept:int):
    gname = ""
    telefon = ""
    comments = ""
    t_tisch_list = []
    queasy = tisch = None

    t_tisch = None

    t_tisch_list, T_tisch = create_model("T_tisch", {"tischnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gname, telefon, comments, t_tisch_list, queasy, tisch


        nonlocal t_tisch
        nonlocal t_tisch_list
        return {"gname": gname, "telefon": telefon, "comments": comments, "t-tisch": t_tisch_list}

    if s_recid != 0:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == s_recid)).first()
        gname = entry(0, queasy.char2, "&&")
        telefon = trim(substring(queasy.char1, 9))
        comments = entry(1, queasy.char3, ";")

    for tisch in db_session.query(Tisch).filter(
            (Tisch.departement == curr_dept)).all():
        t_tisch = T_tisch()
        t_tisch_list.append(t_tisch)

        t_tischnr = tischnr

    return generate_output()