from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import L_orderhdr, Bediener, L_order, L_artikel, Dml_art, Queasy, Dml_artdep

def dml_list_create_pr_11bl(c_list:[C_list], s_list:[S_list], curr_dept:int, rec_id:int, dunit_price:bool, selected_date:date, user_init:str):
    t_l_orderhdr_list = []
    l_orderhdr = bediener = l_order = l_artikel = dml_art = queasy = dml_artdep = None

    c_list = s_list = t_l_orderhdr = s1_list = c1_list = None

    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":str, "artnr":int, "bezeich":str, "qty":decimal, "a_qty":decimal, "price":decimal, "l_price":decimal, "unit":str, "content":decimal, "amount":decimal, "deliver":decimal, "dept":int, "supplier":str, "id":str, "cid":str, "price1":decimal, "qty1":decimal, "lief_nr":int, "approved":bool, "remark":str, "soh":decimal})
    s_list_list, S_list = create_model("S_list", {"s_flag":str, "selected":bool, "artnr":int, "bezeich":str, "qty":decimal, "qty0":decimal, "price":decimal})
    t_l_orderhdr_list, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

    S1_list = S_list
    s1_list_list = s_list_list

    C1_list = C_list
    c1_list_list = c_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_orderhdr_list, l_orderhdr, bediener, l_order, l_artikel, dml_art, queasy, dml_artdep
        nonlocal s1_list, c1_list


        nonlocal c_list, s_list, t_l_orderhdr, s1_list, c1_list
        nonlocal c_list_list, s_list_list, t_l_orderhdr_list
        return {"t-l-orderhdr": t_l_orderhdr_list}

    def create_pr():

        nonlocal t_l_orderhdr_list, l_orderhdr, bediener, l_order, l_artikel, dml_art, queasy, dml_artdep
        nonlocal s1_list, c1_list


        nonlocal c_list, s_list, t_l_orderhdr, s1_list, c1_list
        nonlocal c_list_list, s_list_list, t_l_orderhdr_list

        pos:int = 0
        S1_list = S_list
        C1_list = C_list

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_orderhdr.betriebsnr = 10
        l_orderhdr.gedruckt = None
        l_orderhdr.lief_fax[1] = " ; ; ; "
        l_orderhdr.lief_fax[0] = bediener.username
        l_orderhdr.txtnr = curr_dept

        l_orderhdr = db_session.query(L_orderhdr).first()
        l_order = L_order()
        db_session.add(l_order)

        l_order.docu_nr = l_orderhdr.docu_nr
        l_order.pos = 0
        l_order.bestelldatum = l_orderhdr.bestelldatum
        l_order.op_art = 1

        for s1_list in query(s1_list_list, filters=(lambda s1_list :s1_list.selected)):

            l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == s1_list.artnr)).first()
            pos = pos + 1
            l_order = L_order()
            db_session.add(l_order)

            l_order.docu_nr = l_orderhdr.docu_nr
            l_order.artnr = l_artikel.artnr
            l_order.pos = pos
            l_order.bestelldatum = l_orderhdr.bestelldatum
            l_order.op_art = 1
            l_order.lief_fax[0] = bediener.username
            l_order.lief_fax[2] = l_artikel.traubensort
            l_order.anzahl = s1_list.qty
            l_order.einzelpreis = s1_list.price
            l_order.txtnr = 1
            l_order.flag = dunit_price
            l_order.warenwert = s1_list.qty * s1_list.price
            l_order.quality = to_string(0, "99.99 ") + to_string(0, "99.99") +\
                    to_string(0, " 99.99")

            if l_artikel.lief_einheit != 0:
                l_order.warenwert = l_order.warenwert * l_artikel.lief_einheit

                if dunit_price:
                    l_order.einzelpreis = l_order.einzelpreis * l_artikel.lief_einheit
                l_order.txtnr = l_artikel.lief_einheit

            c1_list = query(c1_list_list, filters=(lambda c1_list :c1_list.artnr == s1_list.artnr), first=True)

            if s1_list.qty == s1_list.qty0:
                c1_list_list.remove(c1_list)
            else:
                c1_list.qty = s1_list.qty0 - s1_list.qty

            if curr_dept == 0:

                dml_art = db_session.query(Dml_art).filter(
                            (Dml_art.artnr == s1_list.artnr) &  (Dml_art.datum == selected_date)).first()

                if dml_art:

                    if s1_list.qty == s1_list.qty0:

                        queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 202) &  (Queasy.number1 == curr_dept) &  (Queasy.number2 == dml_art.artnr) &  (Queasy.date1 == dml_art.datum)).first()

                        if queasy:

                            queasy = db_session.query(Queasy).first()
                            db_session.delete(queasy)

                        db_session.delete(dml_art)
                    else:
                        dml_art.anzahl = s1_list.qty0 - s1_list.qty

                        dml_art = db_session.query(Dml_art).first()
            else:

                dml_artdep = db_session.query(Dml_artdep).filter(
                            (Dml_artdep.artnr == s1_list.artnr) &  (Dml_artdep.datum == selected_date) &  (Dml_artdep.departement == curr_dept)).first()

                if dml_artdep:

                    if s1_list.qty == s1_list.qty0:

                        queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 202) &  (Queasy.number1 == dml_artdep.departement) &  (Queasy.number2 == dml_artdep.artnr) &  (Queasy.date1 == dml_artdep.datum)).first()

                        if queasy:

                            queasy = db_session.query(Queasy).first()
                            db_session.delete(queasy)

                        db_session.delete(dml_artdep)
                    else:
                        dml_artdep.anzahl = s1_list.qty0 - s1_list.qty

                        dml_artdep = db_session.query(Dml_artdep).first()

            for dml_artdep in db_session.query(Dml_artdep).filter(
                        (Dml_artdep.datum == selected_date) &  (Dml_artdep.departement == curr_dept)).all():

                if re.match(".*!.*",dml_artdep.chginit):
                    dml_artdep.chginit = replace_str(dml_artdep.chginit, "!", "")


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    l_orderhdr = db_session.query(L_orderhdr).filter(
            (L_orderhdr._recid == rec_id)).first()
    create_pr()

    l_orderhdr = db_session.query(L_orderhdr).first()
    t_l_orderhdr = T_l_orderhdr()
    t_l_orderhdr_list.append(t_l_orderhdr)

    buffer_copy(l_orderhdr, t_l_orderhdr)
    t_l_orderhdr.rec_id = l_orderhdr._recid

    return generate_output()