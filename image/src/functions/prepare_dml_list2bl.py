from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, Bediener, Htparam

def prepare_dml_list2bl(bediener_username:str, user_init:str):
    currdate = None
    t_l_orderhdr_list = []
    l_orderhdr = bediener = htparam = None

    t_l_orderhdr = l_orderhdr1 = None

    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    L_orderhdr1 = L_orderhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal currdate, t_l_orderhdr_list, l_orderhdr, bediener, htparam
        nonlocal l_orderhdr1


        nonlocal t_l_orderhdr, l_orderhdr1
        nonlocal t_l_orderhdr_list
        return {"currdate": currdate, "t-l-orderhdr": t_l_orderhdr_list}

    def new_pr_number():

        nonlocal currdate, t_l_orderhdr_list, l_orderhdr, bediener, htparam
        nonlocal l_orderhdr1


        nonlocal t_l_orderhdr, l_orderhdr1
        nonlocal t_l_orderhdr_list

        s:str = ""
        i:int = 1
        docu_nr:str = ""
        L_orderhdr1 = L_orderhdr
        l_orderhdr = L_orderhdr()
        db_session.add(l_orderhdr)

        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_list.append(t_l_orderhdr)

        s = "R" + substring(to_string(get_year(currdate)) , 2, 2) + to_string(get_month(currdate) , "99") + to_string(get_day(currdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                    (L_orderhdr1.bestelldatum == currdate)).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")
            l_orderhdr.docu_nr = docu_nr
            l_orderhdr.besteller = bediener.username
            l_orderhdr.bestelldatum = currdate
            l_orderhdr.lieferdatum = currdate + 1

            return
        docu_nr = s + to_string(i, "999")
        l_orderhdr.docu_nr = docu_nr
        l_orderhdr.besteller = bediener_username
        l_orderhdr.bestelldatum = currdate
        l_orderhdr.lieferdatum = currdate + 1


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    currdate = htparam.fdate
    new_pr_number()

    l_orderhdr = db_session.query(L_orderhdr).first()
    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    return generate_output()