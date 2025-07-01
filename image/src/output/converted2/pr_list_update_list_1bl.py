#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_orderhdr, L_order, Gl_acct

s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":string, "po_nr":string, "deptnr":int, "str0":string, "bestelldatum":string, "lieferdatum":string, "pos":int, "artnr":int, "bezeich":string, "qty":Decimal, "str3":string, "dunit":string, "lief_einheit":Decimal, "str4":string, "userinit":string, "pchase_nr":string, "pchase_date":date, "app_rej":string, "rej_reason":string, "cid":string, "cdate":date, "instruct":string, "konto":string, "supno":int, "currno":int, "duprice":Decimal, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "anzahl":int, "txtnr":int, "suppn1":string, "supp1":int, "suppn2":string, "supp2":int, "suppn3":string, "supp3":int, "supps":string, "einzelpreis":Decimal, "amount":Decimal, "stornogrund":string, "besteller":string, "lief_fax2":string, "last_pdate":date, "last_pprice":Decimal, "zeit":int, "min_bestand":Decimal, "max_bestand":Decimal, "del_reason":string, "desc_coa":string, "lief_fax3":string, "masseinheit":string, "lief_fax_2":string, "ek_letzter":Decimal, "supplier":string, "vk_preis":Decimal, "a_firma":string, "last_pbook":Decimal}, {"pos": 999999})

def pr_list_update_list_1bl(s_list_list:[S_list], docu_nr:string):

    prepare_cache ([L_orderhdr, L_order])

    l_orderhdr = l_order = gl_acct = None

    s_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr, l_order, gl_acct
        nonlocal docu_nr


        nonlocal s_list

        return {"s-list": s_list_list}

    def update_list():

        nonlocal l_orderhdr, l_order, gl_acct
        nonlocal docu_nr


        nonlocal s_list

        nr:int = 0

        l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, docu_nr)]})
        nr = l_orderhdr._recid

        s_list = query(s_list_list, filters=(lambda s_list: s_list.s_recid == nr), first=True)
        s_list.lieferdatum = to_string(l_orderhdr.lieferdatum)
        s_list.instruct = l_orderhdr.lief_fax[2]

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.docu_nr.lower()  == (docu_nr).lower()  and s_list.artnr > 0)):

            l_order = get_cache (L_order, {"_recid": [(eq, s_list.s_recid)]})
            s_list.qty =  to_decimal(l_order.anzahl)
            s_list.zeit = l_order.zeit

            if l_order.anzahl != 0:
                s_list.str3 = to_string(l_order.anzahl, ">>>,>>9.99")
            s_list.konto = l_order.stornogrund
            s_list.approved = l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") == 0 and entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " "
            s_list.rejected = l_orderhdr.lief_fax[1] != "" and get_index(l_orderhdr.lief_fax[1], "|") > 0

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

            if gl_acct:
                s_list.konto = l_order.stornogrund
                s_list.stornogrund = l_order.stornogrund

        if l_orderhdr.lief_fax[1] != "":

            s_list = query(s_list_list, filters=(lambda s_list: s_list.docu_nr.lower()  == (docu_nr).lower()  and s_list.artnr == 0), first=True)

            if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                if entry(0, l_orderhdr.lief_fax[1], ";") != " " and entry(1, l_orderhdr.lief_fax[1], ";") != " " and entry(2, l_orderhdr.lief_fax[1], ";") != " " and entry(3, l_orderhdr.lief_fax[1], ";") != " ":
                    s_list.approved = True


                else:
                    s_list.approved = False


            else:
                s_list.rejected = True

        if get_index(l_orderhdr.lief_fax[1], "|") == 0:

            if entry(0, l_orderhdr.lief_fax[1], ";") == " " and entry(1, l_orderhdr.lief_fax[1], ";") == " " and entry(2, l_orderhdr.lief_fax[1], ";") == " " and entry(3, l_orderhdr.lief_fax[1], ";") == " ":
                s_list.app_rej = ""


            else:
                s_list.app_rej = entry(0, l_orderhdr.lief_fax[1], ";") + ";" + entry(1, l_orderhdr.lief_fax[1], ";") + ";" + entry(2, l_orderhdr.lief_fax[1], ";") + ";" + entry(3, l_orderhdr.lief_fax[1], ";")

        if get_index(l_orderhdr.lief_fax[1], "|") > 0:
            s_list.rej_reason = trim(entry(2, l_orderhdr.lief_fax[1], "|"))
            s_list.app_rej = trim(entry(3, entry(0, l_orderhdr.lief_fax[1], "|") , ";"))

    update_list()

    return generate_output()