#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Kellner, Kellne1

def prepare_rwaiter_adminbl(dept:int):

    prepare_cache ([Kellne1])

    q1_list_data = []
    t_kellner_data = []
    kellner = kellne1 = None

    q1_list = t_kellner = None

    q1_list_data, Q1_list = create_model("Q1_list", {"kellner_nr":int, "kellnername":string, "kumsatz_nr":int, "kumsatz_nr1":int, "kcredit_nr":int, "kzahl_nr":int, "kzahl_nr1":int, "masterkey":bool, "sprachcode":int, "r_kellner":int, "r_kellne1":int})
    t_kellner_data, T_kellner = create_model_like(Kellner)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, t_kellner_data, kellner, kellne1
        nonlocal dept


        nonlocal q1_list, t_kellner
        nonlocal q1_list_data, t_kellner_data

        return {"q1-list": q1_list_data, "t-kellner": t_kellner_data}


    kellner_obj_list = {}
    for kellner, kellne1 in db_session.query(Kellner, Kellne1).join(Kellne1,(Kellne1.departement == Kellner.departement) & (Kellne1.kellner_nr == Kellner.kellner_nr)).filter(
             (Kellner.departement == dept)).order_by(Kellner.kellner_nr).all():
        if kellner_obj_list.get(kellner._recid):
            continue
        else:
            kellner_obj_list[kellner._recid] = True


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.kellner_nr = kellner.kellner_nr
        q1_list.kellnername = kellner.kellnername
        q1_list.kumsatz_nr = kellner.kumsatz_nr
        q1_list.kumsatz_nr1 = kellne1.kumsatz_nr
        q1_list.kcredit_nr = kellner.kcredit_nr
        q1_list.kzahl_nr = kellner.kzahl_nr
        q1_list.kzahl_nr1 = kellne1.kzahl_nr
        q1_list.masterkey = kellner.masterkey
        q1_list.sprachcode = kellner.sprachcode
        q1_list.r_kellner = kellner._recid
        q1_list.r_kellne1 = kellne1._recid

    for kellner in db_session.query(Kellner).filter(
             (Kellner.departement == dept)).order_by(Kellner._recid).all():
        t_kellner = T_kellner()
        t_kellner_data.append(t_kellner)

        buffer_copy(kellner, t_kellner)

    return generate_output()