#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Prtable, Prmarket, Queasy

t_prtable_list, T_prtable = create_model_like(Prtable)
t_prmarket_list, T_prmarket = create_model_like(Prmarket)
t_queasy_list, T_queasy = create_model_like(Queasy)

def prtable_adminbl(t_prtable_list:[T_prtable], t_prmarket_list:[T_prmarket], t_queasy_list:[T_queasy]):

    prepare_cache ([Prtable, Prmarket, Queasy])

    b1_list_list = []
    prtable = prmarket = queasy = None

    b1_list = t_prtable = t_prmarket = t_queasy = None

    b1_list_list, B1_list = create_model("B1_list", {"nr":int, "marknr":int, "bezeich":string, "char3":string, "logi3":bool, "rec_id":int, "pr_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, prtable, prmarket, queasy


        nonlocal b1_list, t_prtable, t_prmarket, t_queasy
        nonlocal b1_list_list

        return {"b1-list": b1_list_list}


    t_prtable = query(t_prtable_list, first=True)

    if t_prtable:
        prtable = Prtable()
        db_session.add(prtable)

        buffer_copy(t_prtable, prtable)
        pass

    t_prmarket = query(t_prmarket_list, first=True)

    if t_prmarket:
        prmarket = Prmarket()
        db_session.add(prmarket)

        buffer_copy(t_prmarket, prmarket)
        pass

    t_queasy = query(t_queasy_list, first=True)

    if t_queasy:
        queasy = Queasy()
        db_session.add(queasy)

        buffer_copy(t_queasy, queasy)
        pass

    prtable_obj_list = {}
    prtable = Prtable()
    prmarket = Prmarket()
    queasy = Queasy()
    for prtable.nr, prtable.marknr, prtable._recid, prmarket.bezeich, prmarket._recid, queasy.char3, queasy.logi3, queasy._recid in db_session.query(Prtable.nr, Prtable.marknr, Prtable._recid, Prmarket.bezeich, Prmarket._recid, Queasy.char3, Queasy.logi3, Queasy._recid).join(Prmarket,(Prmarket.nr == Prtable.marknr)).join(Queasy,(Queasy.key == 18) & (Queasy.number1 == Prmarket.nr)).filter(
             (Prtable.prcode == "")).order_by(Prtable.nr).all():
        if prtable_obj_list.get(prtable._recid):
            continue
        else:
            prtable_obj_list[prtable._recid] = True


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