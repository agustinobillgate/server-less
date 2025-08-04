#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Andika 04/08/2025
# gitlab: -
# remarks: -
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, L_orderhdr, L_order

s_list_data, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":string, "po_nr":string, "deptnr":int, "str0":string, "bestelldatum":string, "lieferdatum":string, "pos":int, "artnr":int, "bezeich":string, "qty":Decimal, "str3":string, "dunit":string, "lief_einheit":Decimal, "str4":string, "userinit":string, "pchase_nr":string, "pchase_date":date, "app_rej":string, "rej_reason":string, "cid":string, "cdate":date, "instruct":string, "konto":string, "supno":int, "currno":int, "duprice":Decimal, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "anzahl":int, "txtnr":int, "suppn1":string, "supp1":int, "suppn2":string, "supp2":int, "suppn3":string, "supp3":int, "supps":string, "einzelpreis":Decimal, "amount":Decimal, "stornogrund":string, "besteller":string, "lief_fax2":string, "last_pdate":date, "last_pprice":Decimal, "zeit":int, "min_bestand":Decimal, "max_bestand":Decimal, "del_reason":string, "desc_coa":string, "lief_fax3":string, "masseinheit":string, "lief_fax_2":string, "ek_letzter":Decimal, "supplier":string, "vk_preis":Decimal, "a_firma":string, "last_pbook":Decimal}, {"pos": 999999})

def pr_list_btn_del_1bl(s_list_data:[S_list], s_list_artnr:int, billdate:date, user_init:string):

    prepare_cache ([Bediener, L_orderhdr, L_order])

    del_cur_row = False
    docu_nr:string = ""
    bediener = l_orderhdr = l_order = None

    s_list = s1_list = None

    S1_list = S_list
    s1_list_data = s_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal del_cur_row, docu_nr, bediener, l_orderhdr, l_order
        nonlocal s_list_artnr, billdate, user_init
        nonlocal s1_list


        nonlocal s_list, s1_list

        return {"del_cur_row": del_cur_row}

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    s_list = query(s_list_data, filters=(lambda s_list: s_list.artnr == s_list_artnr), first=True)

    l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, s_list.docu_nr)]})

    if l_orderhdr:
        pass
        l_orderhdr.lief_fax[2] = l_orderhdr.lief_fax[2] + "-" + user_init + ";" + s_list.del_reason


        pass
        pass

    if s_list_artnr == 0:
        docu_nr = s_list.docu_nr

        l_order = get_cache (L_order, {"lief_nr": [(eq, 0)],"pos": [(eq, 0)],"artnr": [(eq, 0)],"docu_nr": [(eq, docu_nr)]})

        if not l_order:
            l_order = L_order()
            if l_order:
                db_session.add(l_order)

                l_order.docu_nr = docu_nr


        l_order.loeschflag = 2
        l_order.lieferdatum_eff = billdate
        l_order.angebot_lief[2] = bediener.nr


        pass

        for s1_list in query(s1_list_data, filters=(lambda s1_list: s1_list.docu_nr.lower()  == (docu_nr).lower())):

            if s1_list.artnr > 0:

                l_order = get_cache (L_order, {"_recid": [(eq, s1_list.s_recid)]})
                if l_order:
                    l_order.loeschflag = 2
                    l_order.lieferdatum_eff = billdate
                    l_order.angebot_lief[2] = bediener.nr


                pass
            s1_list.loeschflag = 2
            s1_list.cid = bediener.username
            s1_list.cdate = billdate

        return generate_output()
    else:
        docu_nr = s_list.docu_nr
        s_list.loeschflag = 2

        l_order = get_cache (L_order, {"_recid": [(eq, s_list.s_recid)]})
        l_order.loeschflag = 2
        l_order.lieferdatum_eff = billdate
        l_order.angebot_lief[2] = bediener.nr


        pass

        s1_list = query(s1_list_data, filters=(lambda s1_list: s1_list.docu_nr.lower()  == (docu_nr).lower()  and s1_list.artnr > 0 and s1_list.loeschflag <= 1), first=True)

        if not s1_list:

            l_order = get_cache (L_order, {"lief_nr": [(eq, 0)],"pos": [(eq, 0)],"artnr": [(eq, 0)],"docu_nr": [(eq, docu_nr)]})
            l_order.loeschflag = 2
            l_order.lieferdatum_eff = billdate
            l_order.angebot_lief[2] = bediener.nr


            pass

            return generate_output()
        else:
            del_cur_row = True

    return generate_output()