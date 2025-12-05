#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_orderhdr, Bediener, L_artikel, Gl_acct, L_lieferant
from sqlalchemy.orm.attributes import flag_modified


s_list_data, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":string, "po_nr":string, "deptnr":int, "str0":string, "bestelldatum":string, "lieferdatum":string, "pos":int, "artnr":int, "bezeich":string, "qty":Decimal, "str3":string, "dunit":string, "lief_einheit":Decimal, "str4":string, "userinit":string, "pchase_nr":string, "pchase_date":date, "app_rej":string, "rej_reason":string, "cid":string, "cdate":date, "instruct":string, "konto":string, "supno":int, "currno":int, "duprice":Decimal, "du_price1":Decimal, "du_price2":Decimal, "du_price3":Decimal, "anzahl":int, "txtnr":int, "suppn1":string, "supp1":int, "suppn2":string, "supp2":int, "suppn3":string, "supp3":int, "supps":string, "einzelpreis":Decimal, "amount":Decimal, "stornogrund":string, "besteller":string, "lief_fax2":string, "last_pdate":date, "last_pprice":Decimal, "zeit":int, "min_bestand":Decimal, "max_bestand":Decimal, "del_reason":string, "desc_coa":string, "lief_fax3":string, "masseinheit":string, "lief_fax_2":string, "ek_letzter":Decimal, "supplier":string, "vk_preis":Decimal, "a_firma":string, "last_pbook":Decimal}, {"pos": 999999})

def pr_list_btn_go_1bl(po_nr:string, pr_nr:string, curr_dept:int, lief_nr:int, po_type:int, billdate:date, user_init:string, s_list_data:[S_list]):

    prepare_cache ([L_order, L_orderhdr, Bediener, L_artikel, Gl_acct])

    curr_pos:int = 0
    temp_nr:string = ""
    l_order = l_orderhdr = bediener = l_artikel = gl_acct = l_lieferant = None

    s_list = s_list1 = l_od1 = l_odhdr = bod = None

    S_list1 = S_list
    s_list1_data = s_list_data

    L_od1 = create_buffer("L_od1",L_order)
    L_odhdr = create_buffer("L_odhdr",L_orderhdr)
    Bod = create_buffer("Bod",L_order)

    db_session = local_storage.db_session
    po_nr = po_nr.strip()
    pr_nr = pr_nr.strip()

    def generate_output():
        nonlocal curr_pos, temp_nr, l_order, l_orderhdr, bediener, l_artikel, gl_acct, l_lieferant
        nonlocal po_nr, pr_nr, curr_dept, lief_nr, po_type, billdate, user_init
        nonlocal s_list1, l_od1, l_odhdr, bod
        nonlocal s_list, s_list1, l_od1, l_odhdr, bod

        return {"po_nr": po_nr, "pr_nr": pr_nr, "curr_dept": curr_dept, "lief_nr": lief_nr, "s-list": s_list_data}

    def get_ponum(lief_nr:int, pr:string):

        nonlocal curr_pos, temp_nr, l_order, l_orderhdr, bediener, l_artikel, gl_acct, l_lieferant
        nonlocal po_nr, pr_nr, curr_dept, po_type, billdate, user_init
        nonlocal s_list1, l_od1, l_odhdr, bod
        nonlocal s_list, s_list1, l_od1, l_odhdr, bod

        docu_nr = ""
        l_orderhdr1 = None
        s:string = ""
        i:int = 1

        def generate_inner_output():
            return (docu_nr)

        L_orderhdr1 =  create_buffer("L_orderhdr1",L_orderhdr)

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})
        s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                 (L_orderhdr1.bestelldatum == billdate) & (L_orderhdr1.betriebsnr <= 1) & (matches(L_orderhdr1.docu_nr,"P*"))).order_by(L_orderhdr1.docu_nr.desc()).all():
            i = to_int(substring(l_orderhdr1.docu_nr, 7, 3))
            i = i + 1
            docu_nr = s + to_string(i, "999")
            l_order = L_order()
            db_session.add(l_order)

            l_order.docu_nr = docu_nr
            l_order.pos = 0
            l_order.bestelldatum = billdate
            l_order.lief_nr = lief_nr
            l_order.op_art = 2
            l_order.lief_fax[0] = pr
            l_order.betriebsnr = 2

            return generate_inner_output()
        docu_nr = s + to_string(i, "999")
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = docu_nr
        l_order.pos = 0
        l_order.bestelldatum = billdate
        l_order.lief_nr = lief_nr
        l_order.op_art = 2
        l_order.lief_fax[0] = pr
        l_order.betriebsnr = 2

        return generate_inner_output()

        return generate_inner_output()


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    for s_list1 in query(s_list1_data, filters=(lambda s_list1: s_list1.selected  and s_list1.artnr > 0), sort_by=[("docu_nr",False)]):

        if pr_nr == "":
            pr_nr = s_list1.docu_nr
            temp_nr = s_list1.docu_nr

            if po_type == 1:
                po_nr = get_ponum(lief_nr, pr_nr)
                l_orderhdr = L_orderhdr()
                db_session.add(l_orderhdr)

                l_orderhdr.lief_nr = lief_nr
                l_orderhdr.docu_nr = po_nr
                l_orderhdr.angebot_lief[2] = s_list1.currno


                pass
        else:

            if temp_nr != s_list1.docu_nr:
                pr_nr = pr_nr + " | " + s_list1.docu_nr
                temp_nr = s_list1.docu_nr

                if po_type == 1:

                    # bod = get_cache (L_order, {"docu_nr": [(eq, po_nr)],"pos": [(eq, 0)],"bestelldatum": [(eq, billdate)],"lief_nr": [(eq, lief_nr)],"op_art": [(eq, 2)],"betriebsnr": [(eq, 2)]})
                    bod = db_session.query(L_order).filter(
                             (L_order.docu_nr == po_nr) &
                             (L_order.pos == 0) &
                             (L_order.bestelldatum == billdate) &
                             (L_order.lief_nr == lief_nr) &
                             (L_order.op_art == 2) &
                             (L_order.betriebsnr == 2)).with_for_update().first()
                    if bod:
                        pass
                        bod.lief_fax[0] = pr_nr

            flag_modified(bod, "lief_fax")

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_list1.artnr)]})

        l_od1 = get_cache (L_order, {"_recid": [(eq, s_list1.s_recid)]})

        if curr_dept == 0:

            l_odhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, l_od1.docu_nr)],"betriebsnr": [(ge, 9)],"lief_nr": [(eq, 0)]})

            if l_odhdr:
                curr_dept = l_odhdr.angebot_lief[0]

        # l_order = get_cache (L_order, {"artnr": [(eq, s_list1.artnr)],"op_art": [(eq, 2)],"bestelldatum": [(eq, billdate)],"docu_nr": [(eq, po_nr)],"stornogrund": [(eq, s_list1.konto)]})
        l_order = db_session.query(L_order).filter(
                 (L_order.artnr == s_list1.artnr) &
                 (L_order.op_art == 2) &
                 (L_order.bestelldatum == billdate) &
                 (L_order.docu_nr == po_nr) &
                 (L_order.stornogrund == s_list1.konto)).with_for_update().first()
        if l_order:
            pass
            l_order.anzahl =  to_decimal(l_order.anzahl) + to_decimal(s_list1.qty)
            l_order.warenwert =  to_decimal(l_order.anzahl) * to_decimal(l_order.einzelpreis)
            pass
        else:
            curr_pos = curr_pos + 1
            l_order = L_order()
            db_session.add(l_order)


            if s_list1.duprice == 0:
                l_order.einzelpreis =  to_decimal(l_artikel.ek_aktuell) * to_decimal(l_artikel.lief_einheit)
            else:
                l_order.einzelpreis =  to_decimal(s_list1.duprice)
            l_order.artnr = s_list1.artnr
            l_order.anzahl =  to_decimal(s_list1.qty)
            l_order.txtnr = l_artikel.lief_einheit
            l_order.pos = curr_pos
            l_order.bestelldatum = billdate
            l_order.op_art = 2
            l_order.docu_nr = po_nr
            l_order.lief_nr = lief_nr
            l_order.lief_fax[0] = bediener.username
            l_order.flag = True
            l_order.betriebsnr = 2
            l_order.stornogrund = s_list1.konto
            l_order.angebot_lief[2] = s_list1.currno
            l_order.warenwert =  to_decimal(l_order.anzahl) * to_decimal(l_order.einzelpreis)
            l_order.besteller = s_list1.instruct
            l_order.zeit = s_list1.zeit
            l_order.lief_fax[2] = l_artikel.traubensorte

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_order.stornogrund)]})

            if gl_acct:
                s_list1.desc_coa = gl_acct.bezeich


            flag_modified(l_order, "lief_fax")

    return generate_output()