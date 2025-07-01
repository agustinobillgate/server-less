#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, L_orderhdr, L_order

s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":string, "po_nr":string, "deptnr":int, "str0":string, "bestelldatum":string, "lieferdatum":string, "pos":int, "artnr":int, "bezeich":string, "qty":Decimal, "str3":string, "dunit":string, "lief_einheit":Decimal, "str4":string, "userinit":string, "pchase_nr":string, "pchase_date":date, "app_rej":string, "rej_reason":string, "cid":string, "cdate":date, "instruct":string, "konto":string, "supno":int, "currno":int, "duprice":Decimal, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "anzahl":int, "txtnr":int, "suppn1":string, "supp1":int, "suppn2":string, "supp2":int, "suppn3":string, "supp3":int, "supps":string, "einzelpreis":Decimal, "amount":Decimal, "stornogrund":string, "besteller":string, "lief_fax2":string, "last_pdate":date, "last_pprice":Decimal, "zeit":int, "min_bestand":Decimal, "max_bestand":Decimal, "del_reason":string, "desc_coa":string, "lief_fax3":string, "masseinheit":string, "lief_fax_2":string, "ek_letzter":Decimal, "supplier":string, "vk_preis":Decimal, "a_firma":string, "last_pbook":Decimal}, {"pos": 999999})

def pr_list_update_slist_1bl(s_list_list:[S_list], lief_nr:int, po_nr:string, billdate:date, user_init:string):

    prepare_cache ([Bediener, L_orderhdr, L_order])

    bediener = l_orderhdr = l_order = None

    s_list = s_list1 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bediener, l_orderhdr, l_order
        nonlocal lief_nr, po_nr, billdate, user_init


        nonlocal s_list, s_list1

        return {"s-list": s_list_list}

    def update_slist():

        nonlocal bediener, l_orderhdr, l_order
        nonlocal lief_nr, po_nr, billdate, user_init


        nonlocal s_list, s_list1

        curr_pr:string = ""
        S_list1 = S_list
        s_list1_list = s_list_list
        curr_pr = ""

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.selected and s_list.artnr > 0), sort_by=[("docu_nr",False)]):

            l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, po_nr)]})

            l_order = get_cache (L_order, {"artnr": [(eq, s_list.artnr)],"lief_nr": [(eq, lief_nr)],"op_art": [(eq, 2)],"docu_nr": [(eq, po_nr)]})

            if l_order:
                s_list.po_nr = l_order.docu_nr

                l_order = get_cache (L_order, {"_recid": [(eq, s_list.s_recid)]})

                if l_order:
                    l_order.lief_fax[1] = po_nr
                    l_order.loeschflag = 1
                    l_order.bestelldatum = billdate
                    pass
                    s_list.pchase_nr = l_order.lief_fax[1]
                    s_list.pchase_date = billdate
                    s_list.loeschflag = 1

                if l_orderhdr and l_orderhdr.lief_fax[1] != "":

                    if get_index(l_orderhdr.lief_fax[1], "|") == 0:

                        if num_entries(l_orderhdr.lief_fax[1], ";") >= 3:
                            s_list.approved = True


                        else:
                            s_list.approved = False


                    else:
                        s_list.rejected = True

                if curr_pr != s_list.docu_nr:
                    curr_pr = s_list.docu_nr

                    l_order = get_cache (L_order, {"docu_nr": [(eq, curr_pr)],"pos": [(eq, 0)]})
                    l_order.loeschflag = 1
                    pass

                    s_list1 = query(s_list1_list, filters=(lambda s_list1: s_list1.artnr == 0 and s_list1.docu_nr == s_list.docu_nr), first=True)
                    s_list1.loeschflag = 1
        curr_pr = ""

        for s_list in query(s_list_list, filters=(lambda s_list: s_list.selected and s_list.artnr > 0), sort_by=[("docu_nr",False)]):

            if curr_pr != s_list.docu_nr:
                curr_pr = s_list.docu_nr

                l_order = get_cache (L_order, {"docu_nr": [(eq, curr_pr)],"artnr": [(gt, 0)],"pos": [(gt, 0)],"loeschflag": [(eq, 0)],"op_art": [(eq, 1)],"lief_nr": [(eq, 0)]})

                if not l_order:

                    l_order = get_cache (L_order, {"docu_nr": [(eq, curr_pr)],"pos": [(eq, 0)]})
                    l_order.loeschflag = 1
                    l_order.lieferdatum_eff = billdate
                    l_order.angebot_lief[2] = bediener.nr


                    pass

                    s_list1 = query(s_list1_list, filters=(lambda s_list1: s_list1.docu_nr.lower()  == (curr_pr).lower()  and s_list1.artnr == 0), first=True)
                    s_list1.loeschflag = 1
                    s_list1.cdate = billdate
                    s_list1.cid = bediener.userinit


            s_list.selected = False
            s_list.loeschflag = 1


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    update_slist()

    return generate_output()