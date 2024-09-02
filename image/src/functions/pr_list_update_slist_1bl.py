from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bediener, L_orderhdr, L_order

def pr_list_update_slist_1bl(s_list:[S_list], lief_nr:int, po_nr:str, billdate:date, user_init:str):
    bediener = l_orderhdr = l_order = None

    s_list = s_list1 = None

    s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":str, "po_nr":str, "deptnr":int, "str0":str, "bestelldatum":str, "lieferdatum":str, "pos":int, "artnr":int, "bezeich":str, "qty":decimal, "str3":str, "dunit":str, "lief_einheit":decimal, "str4":str, "userinit":str, "pchase_nr":str, "pchase_date":date, "app_rej":str, "rej_reason":str, "cid":str, "cdate":date, "instruct":str, "konto":str, "supno":int, "currno":int, "duprice":decimal, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "anzahl":int, "txtnr":int, "suppn1":str, "supp1":int, "suppn2":str, "supp2":int, "suppn3":str, "supp3":int, "supps":str, "einzelpreis":decimal, "amount":decimal, "stornogrund":str, "besteller":str, "lief_fax2":str, "last_pdate":date, "last_pprice":decimal, "zeit":int, "min_bestand":decimal, "max_bestand":decimal, "del_reason":str, "desc_coa":str, "lief_fax3":str, "masseinheit":str, "lief_fax_2":str, "ek_letzter":decimal, "supplier":str, "vk_preis":decimal, "a_firma":str, "last_pbook":decimal}, {"pos": 999999})

    S_list1 = S_list
    s_list1_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, l_orderhdr, l_order
        nonlocal s_list1


        nonlocal s_list, s_list1
        nonlocal s_list_list
        return {}

    def update_slist():

        nonlocal bediener, l_orderhdr, l_order
        nonlocal s_list1


        nonlocal s_list, s_list1
        nonlocal s_list_list

        curr_pr:str = ""
        S_list1 = S_list
        curr_pr = ""

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.selected and s_list.artnr > 0)):

            l_orderhdr = db_session.query(L_orderhdr).filter(
                    (func.lower(L_orderhdr.docu_nr) == (po_nr).lower())).first()

            l_order = db_session.query(L_order).filter(
                    (L_order.artnr == s_list.artnr) &  (L_order.lief_nr == lief_nr) &  (L_order.op_art == 2) &  (func.lower(L_order.docu_nr) == (po_nr).lower())).first()

            if l_order:
                s_list.po_nr = l_order.docu_nr

                l_order = db_session.query(L_order).filter(
                        (L_order._recid == s_list.s_recid)).first()

                if l_order:
                    l_order.lief_fax[1] = po_nr
                    l_order.loeschflag = 1
                    l_order.bestelldatum = billdate

                    l_order = db_session.query(L_order).first()
                    s_list.pchase_nr = l_order.lief_fax[1]
                    s_list.pchase_date = billdate
                    s_list.loeschflag = 1

                if l_orderhdr and l_orderhdr.lief_fax[1] != "":
                    IF1 + get_index(l_orderhdr.lief_fax[1], "|") = 0 THEN

                    if num_entries(l_orderhdr.lief_fax[1], ";") >= 3:
                        s_list.approved = True


                    else:
                        s_list.approved = False


                    else:
                        s_list.rejected = True

                if curr_pr != s_list.docu_nr:
                    curr_pr = s_list.docu_nr

                    l_order = db_session.query(L_order).filter(
                            (func.lower(L_order.docu_nr) == (curr_pr).lower()) &  (L_order.pos == 0)).first()
                    l_order.loeschflag = 1

                    l_order = db_session.query(L_order).first()

                    s_list1 = query(s_list1_list, filters=(lambda s_list1 :s_list1.artnr == 0 and s_list1.docu_nr == s_list.docu_nr), first=True)
                    s_list1.loeschflag = 1
        curr_pr = ""

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.selected and s_list.artnr > 0)):

            if curr_pr != s_list.docu_nr:
                curr_pr = s_list.docu_nr

                l_order = db_session.query(L_order).filter(
                        (func.lower(L_order.docu_nr) == (curr_pr).lower()) &  (L_order.artnr > 0) &  (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (L_order.op_art == 1) &  (L_order.lief_nr == 0)).first()

                if not l_order:

                    l_order = db_session.query(L_order).filter(
                            (func.lower(L_order.docu_nr) == (curr_pr).lower()) &  (L_order.pos == 0)).first()
                    l_order.loeschflag = 1
                    l_order.lieferdatum_eff = billdate
                    l_order.angebot_lief[2] = bediener.nr

                    l_order = db_session.query(L_order).first()

                    s_list1 = query(s_list1_list, filters=(lambda s_list1 :s_list1.docu_nr.lower()  == (curr_pr).lower()  and s_list1.artnr == 0), first=True)
                    s_list1.loeschflag = 1
                    s_list1.cdate = billdate
                    s_list1.cid = bediener.userinit


            s_list.selected = False
            s_list.loeschflag = 1

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    update_slist()

    return generate_output()