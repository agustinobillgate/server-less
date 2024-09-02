from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order, L_orderhdr, Bediener, L_artikel, Gl_acct, L_lieferant

def pr_list_btn_go_1bl(po_nr:str, pr_nr:str, curr_dept:int, lief_nr:int, po_type:int, billdate:date, user_init:str, s_list:[S_list]):
    curr_pos:int = 0
    temp_nr:str = ""
    l_order = l_orderhdr = bediener = l_artikel = gl_acct = l_lieferant = None

    s_list = s_list1 = l_od1 = l_odhdr = bod = l_orderhdr1 = None

    s_list_list, S_list = create_model("S_list", {"selected":bool, "flag":bool, "loeschflag":int, "approved":bool, "rejected":bool, "s_recid":int, "docu_nr":str, "po_nr":str, "deptnr":int, "str0":str, "bestelldatum":str, "lieferdatum":str, "pos":int, "artnr":int, "bezeich":str, "qty":decimal, "str3":str, "dunit":str, "lief_einheit":decimal, "str4":str, "userinit":str, "pchase_nr":str, "pchase_date":date, "app_rej":str, "rej_reason":str, "cid":str, "cdate":date, "instruct":str, "konto":str, "supno":int, "currno":int, "duprice":decimal, "du_price1":decimal, "du_price2":decimal, "du_price3":decimal, "anzahl":int, "txtnr":int, "suppn1":str, "supp1":int, "suppn2":str, "supp2":int, "suppn3":str, "supp3":int, "supps":str, "einzelpreis":decimal, "amount":decimal, "stornogrund":str, "besteller":str, "lief_fax2":str, "last_pdate":date, "last_pprice":decimal, "zeit":int, "min_bestand":decimal, "max_bestand":decimal, "del_reason":str, "desc_coa":str, "lief_fax3":str, "masseinheit":str, "lief_fax_2":str, "ek_letzter":decimal, "supplier":str, "vk_preis":decimal, "a_firma":str, "last_pbook":decimal}, {"pos": 999999})

    S_list1 = S_list
    s_list1_list = s_list_list

    L_od1 = L_order
    L_odhdr = L_orderhdr
    Bod = L_order
    L_orderhdr1 = L_orderhdr

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_pos, temp_nr, l_order, l_orderhdr, bediener, l_artikel, gl_acct, l_lieferant
        nonlocal s_list1, l_od1, l_odhdr, bod, l_orderhdr1


        nonlocal s_list, s_list1, l_od1, l_odhdr, bod, l_orderhdr1
        nonlocal s_list_list
        return {}

    def get_ponum(lief_nr:int, pr:str):

        nonlocal curr_pos, temp_nr, l_order, l_orderhdr, bediener, l_artikel, gl_acct, l_lieferant
        nonlocal s_list1, l_od1, l_odhdr, bod, l_orderhdr1


        nonlocal s_list, s_list1, l_od1, l_odhdr, bod, l_orderhdr1
        nonlocal s_list_list

        docu_nr = ""
        s:str = ""
        i:int = 1

        def generate_inner_output():
            return docu_nr
        L_orderhdr1 = L_orderhdr

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == lief_nr)).first()
        s = "P" + substring(to_string(get_year(billdate)) , 2, 2) + to_string(get_month(billdate) , "99") + to_string(get_day(billdate) , "99")

        for l_orderhdr1 in db_session.query(L_orderhdr1).filter(
                (L_orderhdr1.bestelldatum == billdate) &  (L_orderhdr1.betriebsnr <= 1) &  (L_orderhdr1.docu_nr.op("~")("P.*"))).all():
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

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    for s_list1 in query(s_list1_list, filters=(lambda s_list1 :s_list1.selected  and s_list1.artnr > 0)):

        if pr_nr == "":
            pr_nr = s_list1.docu_nr
            temp_nr = s_list1.docu_nr

            if po_type == 1:
                po_nr = get_ponum(lief_nr, pr_nr)
                l_orderhdr = L_orderhdr()
                db_session.add(l_orderhdr)

                l_orderhdr.lief_nr = lief_nr
                l_orderhdr.docu_nr = po_nr
                l_orderhdr.angebot_lief[2] = s_list1.currNo

                l_orderhdr = db_session.query(L_orderhdr).first()
        else:

            if temp_nr != s_list1.docu_nr:
                pr_nr = pr_nr + " | " + s_list1.docu_nr
                temp_nr = s_list1.docu_nr

                if po_type == 1:

                    bod = db_session.query(Bod).filter(
                            (func.lower(Bod.docu_nr) == (po_nr).lower()) &  (Bod.pos == 0) &  (Bod.bestelldatum == billdate) &  (Bod.lief_nr == lief_nr) &  (Bod.op_art == 2) &  (Bod.betriebsnr == 2)).first()

                    if bod:

                        bod = db_session.query(Bod).first()
                        bod.lief_fax[0] = pr_nr

                        bod = db_session.query(Bod).first()


        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_list1.artnr)).first()

        l_od1 = db_session.query(L_od1).filter(
                (L_od1._recid == s_list1.s_recid)).first()

        if curr_dept == 0:

            l_odhdr = db_session.query(L_odhdr).filter(
                    (L_odhdr.docu_nr == l_od1.docu_nr) &  (L_odhdr.betriebsnr >= 9) &  (L_odhdr.lief_nr == 0)).first()

            if l_odhdr:
                curr_dept = l_odhdr.angebot_lief[0]

        l_order = db_session.query(L_order).filter(
                (L_order.artnr == s_list1.artnr) &  (L_order.op_art == 2) &  (L_order.bestelldatum == billdate) &  (func.lower(L_order.docu_nr) == (po_nr).lower()) &  (L_order.stornogrund == s_list1.konto)).first()

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto == l_order.stornogrund)).first()

        if l_order:

            l_order = db_session.query(L_order).first()
            l_order.anzahl = l_order.anzahl + s_list1.qty
            l_order.warenwert = l_order.anzahl * l_order.einzelpreis

            l_order = db_session.query(L_order).first()
        else:
            curr_pos = curr_pos + 1
            l_order = L_order()
            db_session.add(l_order)


            if s_list1.duprice == 0:
                l_order.einzelpreis = l_artikel.ek_aktuell * l_artikel.lief_einheit
            else:
                l_order.einzelpreis = s_list1.duprice
            l_order.artnr = s_list1.artnr
            l_order.anzahl = s_list1.qty
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
            l_order.angebot_lief[2] = s_list1.currNo
            l_order.warenwert = l_order.anzahl * l_order.einzelpreis
            l_order.besteller = s_list1.instruct
            l_order.zeit = s_list1.zeit
            l_order.lief_fax[2] = l_artikel.traubensort

            if gl_acct:
                s_list.desc_coa = gl_acct.bezeich

            l_order = db_session.query(L_order).first()

    return generate_output()