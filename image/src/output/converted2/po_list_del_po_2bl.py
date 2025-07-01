#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, L_orderhdr, L_order, Res_history

q2_list_list, Q2_list = create_model("Q2_list", {"bestelldatum":date, "bezeich":string, "firma":string, "docu_nr":string, "l_orderhdr_lieferdatum":date, "wabkurz":string, "bestellart":string, "gedruckt":date, "l_orderhdr_besteller":string, "l_order_gedruckt":date, "zeit":int, "lief_fax_2":string, "l_order_lieferdatum":date, "lief_fax_3":string, "lieferdatum_eff":date, "lief_fax_1":string, "lief_nr":int, "username":string, "del_reason":string})

def po_list_del_po_2bl(q2_list_list:[Q2_list], user_init:string, billdate:date, l_orderhdr_docu_nr:string, bediener_username:string, curr_mode:string):

    prepare_cache ([Bediener, L_orderhdr, L_order, Res_history])

    bediener = l_orderhdr = l_order = res_history = None

    cost_list = w_list = q2_list = None

    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})
    w_list_list, W_list = create_model("W_list", {"nr":int, "wabkurz":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, l_orderhdr, l_order, res_history
        nonlocal q2_list_list, user_init, billdate, l_orderhdr_docu_nr, bediener_username, curr_mode


        nonlocal cost_list, w_list, q2_list
        nonlocal cost_list_list, w_list_list

        return {}

    def del_reason():

        nonlocal bediener, l_orderhdr, l_order, res_history
        nonlocal q2_list_list, user_init, billdate, l_orderhdr_docu_nr, bediener_username, curr_mode


        nonlocal cost_list, w_list, q2_list
        nonlocal cost_list_list, w_list_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        q2_list = query(q2_list_list, filters=(lambda q2_list: q2_list.docu_nr.lower()  == (l_orderhdr_docu_nr).lower()), first=True)

        l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, q2_list.docu_nr)]})

        if l_orderhdr:
            pass
            l_orderhdr.lief_fax[2] = l_orderhdr.lief_fax[2] + "-" + user_init + ";" + q2_list.del_reason


            pass
            pass


    def del_po():

        nonlocal bediener, l_orderhdr, l_order, res_history
        nonlocal q2_list_list, user_init, billdate, l_orderhdr_docu_nr, bediener_username, curr_mode


        nonlocal cost_list, w_list, q2_list
        nonlocal cost_list_list, w_list_list

        l_od = None
        L_od =  create_buffer("L_od",L_order)

        l_od = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr_docu_nr)],"pos": [(eq, 0)]})

        if l_od:
            pass
            l_od.loeschflag = 2
            l_od.lieferdatum_eff = billdate
            l_od.lief_fax[2] = bediener_username


            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete Po - Document No : " + to_string(l_od.docu_nr)
                res_history.action = "Delete Po"


                pass
                pass
            pass

        for l_od in db_session.query(L_od).filter(
                 (L_od.docu_nr == (l_orderhdr_docu_nr).lower()) & (L_od.pos > 0) & (L_od.loeschflag == 0)).order_by(L_od._recid).all():
            l_od.loeschflag = 2
            l_od.lieferdatum = billdate
            l_od.lief_fax[1] = bediener_username


            pass


    def close_po():

        nonlocal bediener, l_orderhdr, l_order, res_history
        nonlocal q2_list_list, user_init, billdate, l_orderhdr_docu_nr, bediener_username, curr_mode


        nonlocal cost_list, w_list, q2_list
        nonlocal cost_list_list, w_list_list

        l_od = None
        L_od =  create_buffer("L_od",L_order)

        l_od = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr_docu_nr)],"pos": [(eq, 0)]})

        if l_od:
            pass
            l_od.loeschflag = 1
            l_od.lieferdatum_eff = billdate
            l_od.lief_fax[2] = bediener_username


            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Delete Po - Document No : " + to_string(l_od.docu_nr)
                res_history.action = "Delete Po Partial"


                pass
                pass
            pass

        for l_od in db_session.query(L_od).filter(
                 (L_od.docu_nr == (l_orderhdr_docu_nr).lower()) & (L_od.pos > 0) & (L_od.loeschflag == 0)).order_by(L_od._recid).all():
            l_od.loeschflag = 1
            l_od.lieferdatum = billdate
            l_od.lief_fax[1] = bediener_username


            pass

    del_reason()

    if curr_mode.lower()  == ("delete").lower() :
        del_po()

    elif curr_mode.lower()  == ("partial").lower() :
        close_po()

    return generate_output()