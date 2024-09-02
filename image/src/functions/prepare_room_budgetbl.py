from functions.additional_functions import *
import decimal
from datetime import date
from models import Zimkateg, Rmbudget, Htparam

def prepare_room_budgetbl():
    price_decimal = 0
    p_110 = None
    t_zimkateg_list = []
    t_rmbudget_list = []
    zimkateg = rmbudget = htparam = None

    t_zimkateg = t_rmbudget = None

    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    t_rmbudget_list, T_rmbudget = create_model_like(Rmbudget, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, p_110, t_zimkateg_list, t_rmbudget_list, zimkateg, rmbudget, htparam


        nonlocal t_zimkateg, t_rmbudget
        nonlocal t_zimkateg_list, t_rmbudget_list
        return {"price_decimal": price_decimal, "p_110": p_110, "t-zimkateg": t_zimkateg_list, "t-rmbudget": t_rmbudget_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    p_110 = htparam.fdate

    for zimkateg in db_session.query(Zimkateg).all():
        t_zimkateg = T_zimkateg()
        t_zimkateg_list.append(t_zimkateg)

        buffer_copy(zimkateg, t_zimkateg)

    for rmbudget in db_session.query(Rmbudget).all():
        t_rmbudget = T_rmbudget()
        t_rmbudget_list.append(t_rmbudget)

        buffer_copy(rmbudget, t_rmbudget)
        t_rmbudget.rec_id = rmbudget._recid

    return generate_output()