from functions.additional_functions import *
import decimal
from models import Prtable, Prmarket, Queasy

def prtable_adminbl(t_prtable:[T_prtable], t_prmarket:[T_prmarket], t_queasy:[T_queasy]):
    b1_list_list = []
    prtable = prmarket = queasy = None

    b1_list = t_prtable = t_prmarket = t_queasy = None

    b1_list_list, B1_list = create_model("B1_list", {"nr":int, "marknr":int, "bezeich":str, "char3":str, "logi3":bool, "rec_id":int, "pr_recid":int})
    t_prtable_list, T_prtable = create_model_like(Prtable)
    t_prmarket_list, T_prmarket = create_model_like(Prmarket)
    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, prtable, prmarket, queasy


        nonlocal b1_list, t_prtable, t_prmarket, t_queasy
        nonlocal b1_list_list, t_prtable_list, t_prmarket_list, t_queasy_list
        return {"b1-list": b1_list_list}


    t_prtable = query(t_prtable_list, first=True)

    if t_prtable:
        prtable = Prtable()
        db_session.add(prtable)

        buffer_copy(t_prtable, prtable)


    t_prmarket = query(t_prmarket_list, first=True)

    if t_prmarket:
        prmarket = Prmarket()
        db_session.add(prmarket)

        buffer_copy(t_prmarket, prmarket)


    t_queasy = query(t_queasy_list, first=True)

    if t_queasy:
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy)


    prtable_obj_list = []
    for prtable, prmarket, queasy in db_session.query(Prtable, Prmarket, Queasy).join(Prmarket,(Prmarket.nr == Prtable.marknr)).join(Queasy,(Queasy.key == 18) &  (Queasy.number1 == prmarket.nr)).filter(
            (Prtable.prcode == "")).all():
        if prtable._recid in prtable_obj_list:
            continue
        else:
            prtable_obj_list.append(prtable._recid)


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.nr = prtable.nr
        b1_list.marknr = prtable.marknr
        b1_list.bezeich = prmarket.bezeich
        b1_list.char3 = queasy.char3
        b1_list.logi3 = queasy.logi3
        b1_list.rec_id = prtable._recid
        b1_list.pr_recid = prmarket._recid

    return generate_output()