from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_lager, L_artikel, L_op, L_untergrup, L_hauptgrp, Queasy, Bediener

def stock_translist1_btn_go_1bl(trans_code:str, m_grp:int, sorttype:int, m_str:int, mattype:int, from_art:int, to_art:int, from_date:date, to_date:date, show_price:bool, expense_amt:bool):
    it_exist = False
    t_list_list = []
    l_lager = l_artikel = l_op = l_untergrup = l_hauptgrp = queasy = bediener = None

    t_list = l_store = usr = None

    t_list_list, T_list = create_model("T_list", {"datum":date, "lager_nr":int, "pos":int, "op_art":int, "lscheinnr":str, "f_bezeich":str, "t_bezeich":str, "artnr":str, "bezeich":str, "einheit":str, "content":decimal, "price":str, "qty":decimal, "val":decimal, "id":str, "cat_bez":str, "main_bez":str, "subgrp_bez":str})

    L_store = L_lager
    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_list, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list
        return {"it_exist": it_exist, "t-list": t_list_list}

    def create_list():

        nonlocal it_exist, t_list_list, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list

        lscheinnr:str = ""
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        unit_expense:decimal = 0
        L_store = L_lager
        it_exist = False
        t_list_list.clear()
        qty = 0
        val = 0
        lscheinnr = ""

        if m_str != 0:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == m_str) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  ((L_op.op_art == 2) |  (L_op.op_art == 4)) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_untergrup = db_session.query(L_untergrup).filter(
                        (L_untergrup.zwkum == l_artikel.zwkum)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_list.append(t_list)

                add_id()
                t_list.lager_nr = l_op.lager_nr
                t_list.pos = l_op.pos
                t_list.op_art = l_op.op_art
                t_list.datum = l_op.datum
                t_list.lscheinnr = lscheinnr

                if l_op.op_art == 4:
                    t_list.f_bezeich = l_lager.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich
                else:
                    t_list.t_bezeich = l_lager.bezeich

                    if l_store:
                        t_list.f_bezeich = l_store.bezeich
                t_list.artnr = to_string(l_op.artnr, "9999999")
                t_list.bezeich = l_artikel.bezeich
                t_list.einheit = l_artikel.masseinheit
                t_list.content = l_artikel.inhalt
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = l_op.warenwert
                            val = val + l_op.warenwert
                            t_val = t_val + l_op.warenwert


                    else:
                        unit_expense = 0

                        for queasy in db_session.query(Queasy).filter(
                                (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                            unit_expense = queasy.deci1
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = unit_expense * l_op.anzahl
                            val = val + t_list.val
                            t_val = t_val + t_list.val


                qty = qty + l_op.anzahl
                t_list.qty = l_op.anzahl
                t_qty = t_qty + l_op.anzahl


        else:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_untergrup = db_session.query(L_untergrup).filter(
                        (L_untergrup.zwkum == l_artikel.zwkum)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_list.append(t_list)

                add_id()
                t_list.lager_nr = l_op.lager_nr
                t_list.pos = l_op.pos
                t_list.op_art = l_op.op_art
                t_list.datum = l_op.datum
                t_list.lscheinnr = lscheinnr
                t_list.f_bezeich = l_lager.bezeich
                t_list.artnr = to_string(l_op.artnr, "9999999")
                t_list.bezeich = l_artikel.bezeich
                t_list.einheit = l_artikel.masseinheit
                t_list.content = l_artikel.inhalt
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_store:
                    t_list.t_bezeich = l_store.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = l_op.warenwert
                            val = val + l_op.warenwert
                            t_val = t_val + l_op.warenwert


                    else:
                        unit_expense = 0

                        for queasy in db_session.query(Queasy).filter(
                                (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                            unit_expense = queasy.deci1
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = unit_expense * l_op.anzahl
                            val = val + t_list.val
                            t_val = t_val + t_list.val


                qty = qty + l_op.anzahl
                t_list.qty = l_op.anzahl
                t_qty = t_qty + l_op.anzahl

        if qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty = qty
            t_list.val = val

        if t_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty = t_qty
            t_list.val = t_val

    def create_list_trans():

        nonlocal it_exist, t_list_list, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list

        lscheinnr:str = ""
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        unit_expense:decimal = 0
        L_store = L_lager
        it_exist = False
        t_list_list.clear()
        qty = 0
        val = 0
        lscheinnr = ""

        if m_str != 0:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == m_str) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  ((L_op.op_art == 2) |  (L_op.op_art == 4)) &  (L_op.herkunftflag == 1) &  (func.lower(L_op.lscheinnr) == (trans_code).lower())).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_untergrup = db_session.query(L_untergrup).filter(
                        (L_untergrup.zwkum == l_artikel.zwkum)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_list.append(t_list)

                add_id()
                t_list.lager_nr = l_op.lager_nr
                t_list.pos = l_op.pos
                t_list.op_art = l_op.op_art
                t_list.datum = l_op.datum
                t_list.lscheinnr = lscheinnr

                if l_op.op_art == 4:
                    t_list.f_bezeich = l_lager.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich
                else:
                    t_list.t_bezeich = l_lager.bezeich

                    if l_store:
                        t_list.f_bezeich = l_store.bezeich
                t_list.artnr = to_string(l_op.artnr, "9999999")
                t_list.bezeich = l_artikel.bezeich
                t_list.einheit = l_artikel.masseinheit
                t_list.content = l_artikel.inhalt
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = l_op.warenwert
                            val = val + l_op.warenwert
                            t_val = t_val + l_op.warenwert


                    else:
                        unit_expense = 0

                        for queasy in db_session.query(Queasy).filter(
                                (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                            unit_expense = queasy.deci1
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = unit_expense * l_op.anzahl
                            val = val + t_list.val
                            t_val = t_val + t_list.val


                qty = qty + l_op.anzahl
                t_list.qty = l_op.anzahl
                t_qty = t_qty + l_op.anzahl


        else:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.op_art == 4) &  (L_op.herkunftflag == 1) &  (func.lower(L_op.lscheinnr) == (trans_code).lower())).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_untergrup = db_session.query(L_untergrup).filter(
                        (L_untergrup.zwkum == l_artikel.zwkum)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_list.append(t_list)

                add_id()
                t_list.lager_nr = l_op.lager_nr
                t_list.pos = l_op.pos
                t_list.op_art = l_op.op_art
                t_list.datum = l_op.datum
                t_list.lscheinnr = lscheinnr
                t_list.f_bezeich = l_lager.bezeich
                t_list.artnr = to_string(l_op.artnr, "9999999")
                t_list.bezeich = l_artikel.bezeich
                t_list.einheit = l_artikel.masseinheit
                t_list.content = l_artikel.inhalt
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_store:
                    t_list.t_bezeich = l_store.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = l_op.warenwert
                            val = val + l_op.warenwert
                            t_val = t_val + l_op.warenwert


                    else:
                        unit_expense = 0

                        for queasy in db_session.query(Queasy).filter(
                                (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                            unit_expense = queasy.deci1
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val = unit_expense * l_op.anzahl
                            val = val + t_list.val
                            t_val = t_val + t_list.val


                qty = qty + l_op.anzahl
                t_list.qty = l_op.anzahl
                t_qty = t_qty + l_op.anzahl

        if qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty = qty
            t_list.val = val

    def create_lista():

        nonlocal it_exist, t_list_list, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list

        curr_artnr:int = 0
        lscheinnr:str = ""
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        do_it2:bool = False
        unit_expense:decimal = 0
        L_store = L_lager
        it_exist = False
        t_list_list.clear()
        qty = 0
        val = 0
        curr_artnr = 0

        if m_str != 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == m_str) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  ((L_op.op_art == 2) |  (L_op.op_art == 4)) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    add_id()
                    t_list.lager_nr = l_op.lager_nr
                    t_list.pos = l_op.pos
                    t_list.op_art = l_op.op_art
                    t_list.datum = l_op.datum
                    t_list.lscheinnr = lscheinnr

                    if l_op.op_art == 4:
                        t_list.f_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.t_bezeich = l_store.bezeich
                    else:
                        t_list.t_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.f_bezeich = l_store.bezeich
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.content = l_artikel.inhalt
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = l_op.warenwert
                                val = val + l_op.warenwert
                                t_val = t_val + l_op.warenwert


                        else:
                            unit_expense = 0

                            for queasy in db_session.query(Queasy).filter(
                                    (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                                unit_expense = queasy.deci1
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = unit_expense * l_op.anzahl
                                val = val + t_list.val
                                t_val = t_val + t_list.val


                    t_list.qty = l_op.anzahl
                    qty = qty + l_op.anzahl
                    t_qty = t_qty + l_op.anzahl
        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    add_id()
                    t_list.lager_nr = l_op.lager_nr
                    t_list.pos = l_op.pos
                    t_list.op_art = l_op.op_art
                    t_list.datum = l_op.datum
                    t_list.lscheinnr = lscheinnr
                    t_list.f_bezeich = l_lager.bezeich
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.content = l_artikel.inhalt
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = l_op.warenwert
                                val = val + l_op.warenwert
                                t_val = t_val + l_op.warenwert


                        else:
                            unit_expense = 0

                            for queasy in db_session.query(Queasy).filter(
                                    (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                                unit_expense = queasy.deci1
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = unit_expense * l_op.anzahl
                                val = val + t_list.val
                                t_val = t_val + t_list.val


                    t_list.qty = l_op.anzahl
                    qty = qty + l_op.anzahl
                    t_qty = t_qty + l_op.anzahl

        if qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty = qty
            t_list.val = val

        if t_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty = t_qty
            t_list.val = t_val

    def create_list1():

        nonlocal it_exist, t_list_list, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list

        lscheinnr:str = ""
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        do_it2:bool = False
        unit_expense:decimal = 0
        L_store = L_lager
        it_exist = False
        t_list_list.clear()
        qty = 0
        val = 0
        lscheinnr = ""

        if m_str != 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.lager_nr == m_str) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  ((L_op.op_art == 2) |  (L_op.op_art == 4)) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                lscheinnr = l_op.lscheinnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    add_id()
                    t_list.lager_nr = l_op.lager_nr
                    t_list.pos = l_op.pos
                    t_list.op_art = l_op.op_art
                    t_list.datum = l_op.datum
                    t_list.lscheinnr = lscheinnr

                    if l_op.op_art == 4:
                        t_list.f_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.t_bezeich = l_store.bezeich
                    else:
                        t_list.t_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.f_bezeich = l_store.bezeich
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.content = l_artikel.inhalt
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = l_op.warenwert
                                val = val + l_op.warenwert
                                t_val = t_val + l_op.warenwert


                        else:
                            unit_expense = 0

                            for queasy in db_session.query(Queasy).filter(
                                    (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                                unit_expense = queasy.deci1
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = unit_expense * l_op.anzahl
                                val = val + t_list.val
                                t_val = t_val + t_list.val


                    t_list.qty = l_op.anzahl
                    qty = qty + l_op.anzahl
                    t_qty = t_qty + l_op.anzahl
        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                lscheinnr = l_op.lscheinnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    add_id()
                    t_list.lager_nr = l_op.lager_nr
                    t_list.pos = l_op.pos
                    t_list.op_art = l_op.op_art
                    t_list.datum = l_op.datum
                    t_list.lscheinnr = lscheinnr
                    t_list.f_bezeich = l_lager.bezeich
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.content = l_artikel.inhalt
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = l_op.warenwert
                                val = val + l_op.warenwert
                                t_val = t_val + l_op.warenwert


                        else:
                            unit_expense = 0

                            for queasy in db_session.query(Queasy).filter(
                                    (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                                unit_expense = queasy.deci1
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = unit_expense * l_op.anzahl
                                val = val + t_list.val
                                t_val = t_val + t_list.val


                    t_list.qty = l_op.anzahl
                    qty = qty + l_op.anzahl
                    t_qty = t_qty + l_op.anzahl

        if qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty = qty
            t_list.val = val

        if t_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty = t_qty
            t_list.val = t_val

    def create_list1a():

        nonlocal it_exist, t_list_list, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list

        curr_artnr:int = 0
        lscheinnr:str = ""
        qty:decimal = 0
        val:decimal = 0
        t_qty:decimal = 0
        t_val:decimal = 0
        do_it2:bool = False
        unit_expense:decimal = 0
        L_store = L_lager
        it_exist = False
        t_list_list.clear()
        qty = 0
        val = 0
        curr_artnr = 0

        if m_str != 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.op_art == m_str) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  ((L_op.op_art == 2) |  (L_op.op_art == 4)) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    add_id()
                    t_list.lager_nr = l_op.lager_nr
                    t_list.pos = l_op.pos
                    t_list.op_art = l_op.op_art
                    t_list.datum = l_op.datum
                    t_list.lscheinnr = lscheinnr

                    if l_op.op_art == 4:
                        t_list.f_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.t_bezeich = l_store.bezeich
                    else:
                        t_list.t_bezeich = l_lager.bezeich

                        if l_store:
                            t_list.f_bezeich = l_store.bezeich
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.content = l_artikel.inhalt
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = l_op.warenwert
                                val = val + l_op.warenwert
                                t_val = t_val + l_op.warenwert


                        else:
                            unit_expense = 0

                            for queasy in db_session.query(Queasy).filter(
                                    (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                                unit_expense = queasy.deci1
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = unit_expense * l_op.anzahl
                                val = val + t_list.val
                                t_val = t_val + t_list.val


                    t_list.qty = l_op.anzahl
                    qty = qty + l_op.anzahl
                    t_qty = t_qty + l_op.anzahl
        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.op_art == 4) &  (L_op.herkunftflag == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                it_exist = True

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == l_op.lager_nr)).first()

                l_store = db_session.query(L_store).filter(
                        (L_store.lager_nr == l_op.pos)).first()

                l_hauptgrp = db_session.query(L_hauptgrp).filter(
                        (L_hauptgrp.endkum == l_artikel.endkum)).first()

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    t_list.price = "Total"
                    t_list.qty = qty
                    t_list.val = val
                    qty = 0
                    val = 0
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_list.append(t_list)

                    add_id()
                    t_list.lager_nr = l_op.lager_nr
                    t_list.pos = l_op.pos
                    t_list.op_art = l_op.op_art
                    t_list.datum = l_op.datum
                    t_list.lscheinnr = lscheinnr
                    t_list.f_bezeich = l_lager.bezeich
                    t_list.artnr = to_string(l_op.artnr, "9999999")
                    t_list.bezeich = l_artikel.bezeich
                    t_list.einheit = l_artikel.masseinheit
                    t_list.content = l_artikel.inhalt
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = l_op.warenwert
                                val = val + l_op.warenwert
                                t_val = t_val + l_op.warenwert


                        else:
                            unit_expense = 0

                            for queasy in db_session.query(Queasy).filter(
                                    (Queasy.key == 121) &  (Queasy.number1 == l_op.artnr) &  (Queasy.date1 <= l_op.datum)).all():
                                unit_expense = queasy.deci1
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val = unit_expense * l_op.anzahl
                                val = val + t_list.val
                                t_val = t_val + t_list.val


                    t_list.qty = l_op.anzahl
                    qty = qty + l_op.anzahl
                    t_qty = t_qty + l_op.anzahl

        if qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Total"
            t_list.qty = qty
            t_list.val = val

        if t_qty != 0:
            t_list = T_list()
            t_list_list.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty = t_qty
            t_list.val = t_val

    def add_id():

        nonlocal it_exist, t_list_list, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal l_store, usr


        nonlocal t_list, l_store, usr
        nonlocal t_list_list


        Usr = Bediener

        usr = db_session.query(Usr).filter(
                (Usr.nr == l_op.fuellflag)).first()

        if usr:
            t_list.id = usr.userinit
        else:
            t_list.id = "??"

    if trans_code != "":
        create_list_trans()
    else:

        if m_grp == 0:

            if sorttype == 1:
                create_list()
            else:
                create_lista()
        else:

            if sorttype == 1:
                create_list1()
            else:
                create_list1a()

    return generate_output()