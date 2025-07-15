#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, Bediener, Htparam

def prepare_dml_list2bl(bediener_username:string, user_init:string):

    prepare_cache ([L_orderhdr, Bediener, Htparam])

    currdate = None
    t_l_orderhdr_data = []
    l_orderhdr = bediener = htparam = None

    t_l_orderhdr = None

    t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal currdate, t_l_orderhdr_data, l_orderhdr, bediener, htparam
        nonlocal bediener_username, user_init


        nonlocal t_l_orderhdr
        nonlocal t_l_orderhdr_data

        return {"currdate": currdate, "t-l-orderhdr": t_l_orderhdr_data}

    def new_pr_number():

        nonlocal currdate, t_l_orderhdr_data, l_orderhdr, bediener, htparam
        nonlocal bediener_username, user_init


        nonlocal t_l_orderhdr
        nonlocal t_l_orderhdr_data

        l_orderhdr1 = None
        s:string = ""
        i:int = 1
        docu_nr:string = ""
        L_orderhdr1 =  create_buffer("L_orderhdr1",L_orderhdr)
        l_orderhdr = L_orderhdr()
        db_session.add(l_orderhdr)

        t_l_orderhdr = T_l_orderhdr()
        t_l_orderhdr_data.append(t_l_orderhdr)

        s = "R" + substring(to_string(get_year(currdate)) , 2, 2) + to_string(get_month(currdate) , "99") + to_string(get_day(currdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                     (L_orderhdr1.bestelldatum == currdate)).order_by(L_orderhdr1.docu_nr.desc()).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")
            l_orderhdr.docu_nr = docu_nr
            l_orderhdr.besteller = bediener.username
            l_orderhdr.bestelldatum = currdate
            l_orderhdr.lieferdatum = currdate + timedelta(days=1)

            return
        docu_nr = s + to_string(i, "999")
        l_orderhdr.docu_nr = docu_nr
        l_orderhdr.besteller = bediener_username
        l_orderhdr.bestelldatum = currdate
        l_orderhdr.lieferdatum = currdate + timedelta(days=1)


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    currdate = htparam.fdate
    new_pr_number()
    pass
    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    return generate_output()