from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, L_order

s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":str, "po_nr":str, "deptnr":int, "str0":str, "bestelldatum":str, "lieferdatum":str, "pos":int, "artnr":int, "bezeich":str, "qty":decimal, "str3":str, "dunit":str, "lief_einheit":decimal, "str4":str, "userinit":str, "pchase_nr":str, "pchase_date":date, "app_rej":str, "rej_reason":str, "cid":str, "cdate":date, "instruct":str, "konto":str, "supno":int, "currno":int, "duprice":decimal, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "anzahl":int, "txtnr":int, "suppn1":str, "supp1":int, "suppn2":str, "supp2":int, "suppn3":str, "supp3":int, "supps":str, "einzelpreis":decimal, "amount":decimal, "stornogrund":str, "besteller":str, "lief_fax2":str}, {"pos": 999999})

def pr_list_btn_delbl(s_list_list:[S_list], s_list_artnr:int, billdate:date, user_init:str):
    del_cur_row = False
    docu_nr:str = ""
    bediener = l_order = None

    s_list = s1_list = None

    S1_list = S_list
    s1_list_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal del_cur_row, docu_nr, bediener, l_order
        nonlocal s_list_artnr, billdate, user_init
        nonlocal s1_list


        nonlocal s_list, s1_list
        nonlocal s_list_list
        return {"del_cur_row": del_cur_row}

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    s_list = query(s_list_list, filters=(lambda s_list: s_list.artnr == s_list_artnr), first=True)

    if s_list_artnr == 0:
        docu_nr = s_list.docu_nr

        l_order = db_session.query(L_order).filter(
                 (L_order.lief_nr == 0) & (L_order.pos == 0) & (L_order.artnr == 0) & (func.lower(L_order.docu_nr) == (docu_nr).lower())).first()

        if not l_order:
            l_order = L_order()
            db_session.add(l_order)

            l_order.docu_nr = docu_nr


        l_order.loeschflag = 2
        l_order.lieferdatum_eff = billdate
        l_order.angebot_lief[2] = bediener.nr

        for s1_list in query(s1_list_list, filters=(lambda s1_list: s1_list.docu_nr.lower()  == (docu_nr).lower())):

            if s1_list.artnr > 0:

                l_order = db_session.query(L_order).filter(
                         (L_order._recid == s1_list.s_recid)).first()
                l_order.loeschflag = 2
                l_order.lieferdatum_eff = billdate
                l_order.angebot_lief[2] = bediener.nr


            s1_list.loeschflag = 2
            s1_list.cid = bediener.username
            s1_list.cdate = billdate

        return generate_output()
    else:
        docu_nr = s_list.docu_nr
        s_list.loeschflag = 2

        l_order = db_session.query(L_order).filter(
                 (L_order._recid == s_list.s_recid)).first()
        l_order.loeschflag = 2
        l_order.lieferdatum_eff = billdate
        l_order.angebot_lief[2] = bediener.nr

        s1_list = query(s1_list_list, filters=(lambda s1_list: s1_list.docu_nr.lower()  == (docu_nr).lower()  and s1_list.artnr > 0 and s1_list.loeschflag <= 1), first=True)

        if not s1_list:

            l_order = db_session.query(L_order).filter(
                     (L_order.lief_nr == 0) & (L_order.pos == 0) & (L_order.artnr == 0) & (func.lower(L_order.docu_nr) == (docu_nr).lower())).first()
            l_order.loeschflag = 2
            l_order.lieferdatum_eff = billdate
            l_order.angebot_lief[2] = bediener.nr

            return generate_output()
        else:
            del_cur_row = True

    return generate_output()