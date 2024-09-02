from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_orderhdr, L_order, Gl_acct

def pr_list_update_list_1bl(s_list:[S_list], docu_nr:str):
    l_orderhdr = l_order = gl_acct = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":str, "po_nr":str, "deptnr":int, "str0":str, "bestelldatum":str, "lieferdatum":str, "pos":int, "artnr":int, "bezeich":str, "qty":decimal, "str3":str, "dunit":str, "lief_einheit":decimal, "str4":str, "userinit":str, "pchase_nr":str, "pchase_date":date, "app_rej":str, "rej_reason":str, "cid":str, "cdate":date, "instruct":str, "konto":str, "supno":int, "currno":int, "duprice":decimal, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "anzahl":int, "txtnr":int, "suppn1":str, "supp1":int, "suppn2":str, "supp2":int, "suppn3":str, "supp3":int, "supps":str, "einzelpreis":decimal, "amount":decimal, "stornogrund":str, "besteller":str, "lief_fax2":str, "last_pdate":date, "last_pprice":decimal, "zeit":int, "min_bestand":decimal, "max_bestand":decimal, "del_reason":str, "desc_coa":str, "lief_fax3":str, "masseinheit":str, "lief_fax_2":str, "ek_letzter":decimal, "supplier":str, "vk_preis":decimal, "a_firma":str, "last_pbook":decimal}, {"pos": 999999})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr, l_order, gl_acct


        nonlocal s_list
        nonlocal s_list_list
        return {}

    def update_list():

        nonlocal l_orderhdr, l_order, gl_acct


        nonlocal s_list
        nonlocal s_list_list

        nr:int = 0

        l_orderhdr = db_session.query(L_orderhdr).filter(
                (func.lower(L_orderhdr.(docu_nr).lower()) == (docu_nr).lower())).first()
        nr = l_orderhdr._recid

        s_list = query(s_list_list, filters=(lambda s_list :s_list.s_recid == nr), first=True)
        s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
        s_list.instruct = l_orderhdr.lief_fax[2]

        for s_list in query(s_list_list, filters=(lambda s_list :s_list.(docu_nr).lower().lower()  == (docu_nr).lower()  and s_list.artnr > 0)):

            l_order = db_session.query(L_order).filter(
                    (L_order._recid == s_list.s_recid)).first()
            s_list.qty = l_order.anzahl
            s_list.zeit = l_order.zeit

            if l_order.anzahl != 0:
                s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")
            s_list.konto = l_order.stornogrund
            s_list.approved = l_orderhdr.lief_fax[1] != "" AND1 + get_index(l_orderhdr.lief_fax[1], "|") == 0 and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
            s_list.rejected = l_orderhdr.lief_fax[1] != "" AND1 + get_index(l_orderhdr.lief_fax[1], "|") > 0

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == l_order.stornogrund)).first()

            if gl_acct:
                s_list.konto = l_order.stornogrund
                s_list.stornogrund = l_order.stornogrund

        if l_orderhdr.lief_fax[1] != "":

            s_list = query(s_list_list, filters=(lambda s_list :s_list.(docu_nr).lower().lower()  == (docu_nr).lower()  and s_list.artnr == 0), first=True)
            IF1 + get_index(l_orderhdr.lief_fax[1], "|") = 0 THEN

            if entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " ":
                s_list.approved = True


            else:
                s_list.approved = False


            else:
                s_list.rejected = True
        IF1 + get_index(l_orderhdr.lief_fax[1], "|") = 0 THEN

        if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
            s_list.app_rej = ""


        else:
            s_list.app_rej = entry(0, l_orderhdr.lief_fax[1], ";") + ";" + entry(1, l_orderhdr.lief_fax[1], ";") + ";" + entry(2, l_orderhdr.lief_fax[1], ";") + ";" + entry(3, l_orderhdr.lief_fax[1], ";")
        IF1 + get_index(l_orderhdr.lief_fax[1], "|") > 0 THEN
        s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
        s_list.app_rej = trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";"))


    update_list()

    return generate_output()