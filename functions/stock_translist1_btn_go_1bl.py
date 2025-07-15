#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_lager, L_artikel, L_op, L_untergrup, L_hauptgrp, Queasy, Bediener

def stock_translist1_btn_go_1bl(trans_code:string, m_grp:int, sorttype:int, m_str:int, mattype:int, from_art:int, to_art:int, from_date:date, to_date:date, show_price:bool, expense_amt:bool):

    prepare_cache ([L_lager, L_artikel, L_op, L_untergrup, L_hauptgrp, Queasy, Bediener])

    it_exist = False
    t_list_data = []
    l_lager = l_artikel = l_op = l_untergrup = l_hauptgrp = queasy = bediener = None

    t_list = None

    t_list_data, T_list = create_model("T_list", {"datum":date, "lager_nr":int, "pos":int, "op_art":int, "lscheinnr":string, "f_bezeich":string, "t_bezeich":string, "artnr":string, "bezeich":string, "einheit":string, "content":Decimal, "price":string, "qty":Decimal, "val":Decimal, "id":string, "cat_bez":string, "main_bez":string, "subgrp_bez":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal it_exist, t_list_data, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal trans_code, m_grp, sorttype, m_str, mattype, from_art, to_art, from_date, to_date, show_price, expense_amt


        nonlocal t_list
        nonlocal t_list_data

        return {"it_exist": it_exist, "t-list": t_list_data}

    def create_list():

        nonlocal it_exist, t_list_data, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal trans_code, m_grp, sorttype, m_str, mattype, from_art, to_art, from_date, to_date, show_price, expense_amt


        nonlocal t_list
        nonlocal t_list_data

        lscheinnr:string = ""
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        unit_expense:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        it_exist = False
        t_list_data.clear()
        qty =  to_decimal("0")
        val =  to_decimal("0")
        lscheinnr = ""

        if m_str != 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == m_str) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & ((L_op.op_art == 2) | (L_op.op_art == 4)) & (L_op.herkunftflag == 1)).order_by(L_op.op_art, L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_data.append(t_list)

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
                t_list.content =  to_decimal(l_artikel.inhalt)
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(l_op.warenwert)
                            val =  to_decimal(val) + to_decimal(l_op.warenwert)
                            t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                    else:
                        unit_expense =  to_decimal("0")

                        for queasy in db_session.query(Queasy).filter(
                                 (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                            unit_expense =  to_decimal(queasy.deci1)
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                            val =  to_decimal(val) + to_decimal(t_list.val)
                            t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                t_list.qty =  to_decimal(l_op.anzahl)
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)


        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_data.append(t_list)

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
                t_list.content =  to_decimal(l_artikel.inhalt)
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_store:
                    t_list.t_bezeich = l_store.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(l_op.warenwert)
                            val =  to_decimal(val) + to_decimal(l_op.warenwert)
                            t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                    else:
                        unit_expense =  to_decimal("0")

                        for queasy in db_session.query(Queasy).filter(
                                 (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                            unit_expense =  to_decimal(queasy.deci1)
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                            val =  to_decimal(val) + to_decimal(t_list.val)
                            t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                t_list.qty =  to_decimal(l_op.anzahl)
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)

        if qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)

        if t_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty =  to_decimal(t_qty)
            t_list.val =  to_decimal(t_val)


    def create_list_trans():

        nonlocal it_exist, t_list_data, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal trans_code, m_grp, sorttype, m_str, mattype, from_art, to_art, from_date, to_date, show_price, expense_amt


        nonlocal t_list
        nonlocal t_list_data

        lscheinnr:string = ""
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        unit_expense:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        it_exist = False
        t_list_data.clear()
        qty =  to_decimal("0")
        val =  to_decimal("0")
        lscheinnr = ""

        if m_str != 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == m_str) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & ((L_op.op_art == 2) | (L_op.op_art == 4)) & (L_op.herkunftflag == 1) & (L_op.lscheinnr == (trans_code).lower())).order_by(L_op.op_art, L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_data.append(t_list)

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
                t_list.content =  to_decimal(l_artikel.inhalt)
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(l_op.warenwert)
                            val =  to_decimal(val) + to_decimal(l_op.warenwert)
                            t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                    else:
                        unit_expense =  to_decimal("0")

                        for queasy in db_session.query(Queasy).filter(
                                 (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                            unit_expense =  to_decimal(queasy.deci1)
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                            val =  to_decimal(val) + to_decimal(t_list.val)
                            t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                t_list.qty =  to_decimal(l_op.anzahl)
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)


        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.op_art == 4) & (L_op.herkunftflag == 1) & (L_op.lscheinnr == (trans_code).lower())).order_by(L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                lscheinnr = l_op.lscheinnr
                t_list = T_list()
                t_list_data.append(t_list)

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
                t_list.content =  to_decimal(l_artikel.inhalt)
                t_list.cat_bez = l_lager.bezeich
                t_list.main_bez = l_hauptgrp.bezeich
                t_list.subgrp_bez = l_untergrup.bezeich

                if l_store:
                    t_list.t_bezeich = l_store.bezeich

                if l_op.anzahl != 0 and show_price:

                    if not expense_amt:
                        t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(l_op.warenwert)
                            val =  to_decimal(val) + to_decimal(l_op.warenwert)
                            t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                    else:
                        unit_expense =  to_decimal("0")

                        for queasy in db_session.query(Queasy).filter(
                                 (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                            unit_expense =  to_decimal(queasy.deci1)
                            break
                        t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                        if show_price:
                            t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                            val =  to_decimal(val) + to_decimal(t_list.val)
                            t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                t_list.qty =  to_decimal(l_op.anzahl)
                t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)

        if qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)


    def create_lista():

        nonlocal it_exist, t_list_data, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal trans_code, m_grp, sorttype, m_str, mattype, from_art, to_art, from_date, to_date, show_price, expense_amt


        nonlocal t_list
        nonlocal t_list_data

        curr_artnr:int = 0
        lscheinnr:string = ""
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        do_it2:bool = False
        unit_expense:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        it_exist = False
        t_list_data.clear()
        qty =  to_decimal("0")
        val =  to_decimal("0")
        curr_artnr = 0

        if m_str != 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.lager_nr == m_str) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & ((L_op.op_art == 2) | (L_op.op_art == 4)) & (L_op.herkunftflag == 1)).order_by(L_op.op_art, L_artikel.bezeich, L_op.datum, L_op.lager_nr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.content =  to_decimal(l_artikel.inhalt)
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(l_op.warenwert)
                                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                        else:
                            unit_expense =  to_decimal("0")

                            for queasy in db_session.query(Queasy).filter(
                                     (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                                unit_expense =  to_decimal(queasy.deci1)
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                                val =  to_decimal(val) + to_decimal(t_list.val)
                                t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                    t_list.qty =  to_decimal(l_op.anzahl)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_artikel.bezeich, L_op.datum, L_op.lager_nr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.content =  to_decimal(l_artikel.inhalt)
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(l_op.warenwert)
                                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                        else:
                            unit_expense =  to_decimal("0")

                            for queasy in db_session.query(Queasy).filter(
                                     (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                                unit_expense =  to_decimal(queasy.deci1)
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                                val =  to_decimal(val) + to_decimal(t_list.val)
                                t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                    t_list.qty =  to_decimal(l_op.anzahl)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)

        if qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)

        if t_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty =  to_decimal(t_qty)
            t_list.val =  to_decimal(t_val)


    def create_list1():

        nonlocal it_exist, t_list_data, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal trans_code, m_grp, sorttype, m_str, mattype, from_art, to_art, from_date, to_date, show_price, expense_amt


        nonlocal t_list
        nonlocal t_list_data

        lscheinnr:string = ""
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        do_it2:bool = False
        unit_expense:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        it_exist = False
        t_list_data.clear()
        qty =  to_decimal("0")
        val =  to_decimal("0")
        lscheinnr = ""

        if m_str != 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.lager_nr == m_str) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & ((L_op.op_art == 2) | (L_op.op_art == 4)) & (L_op.herkunftflag == 1)).order_by(L_op.op_art, L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                lscheinnr = l_op.lscheinnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.content =  to_decimal(l_artikel.inhalt)
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(l_op.warenwert)
                                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                        else:
                            unit_expense =  to_decimal("0")

                            for queasy in db_session.query(Queasy).filter(
                                     (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                                unit_expense =  to_decimal(queasy.deci1)
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                                val =  to_decimal(val) + to_decimal(t_list.val)
                                t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                    t_list.qty =  to_decimal(l_op.anzahl)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_op.lscheinnr, L_op.zeit).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if lscheinnr != l_op.lscheinnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                lscheinnr = l_op.lscheinnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.content =  to_decimal(l_artikel.inhalt)
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(l_op.warenwert)
                                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                        else:
                            unit_expense =  to_decimal("0")

                            for queasy in db_session.query(Queasy).filter(
                                     (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                                unit_expense =  to_decimal(queasy.deci1)
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                                val =  to_decimal(val) + to_decimal(t_list.val)
                                t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                    t_list.qty =  to_decimal(l_op.anzahl)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)

        if qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)

        if t_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty =  to_decimal(t_qty)
            t_list.val =  to_decimal(t_val)


    def create_list1a():

        nonlocal it_exist, t_list_data, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal trans_code, m_grp, sorttype, m_str, mattype, from_art, to_art, from_date, to_date, show_price, expense_amt


        nonlocal t_list
        nonlocal t_list_data

        curr_artnr:int = 0
        lscheinnr:string = ""
        qty:Decimal = to_decimal("0.0")
        val:Decimal = to_decimal("0.0")
        t_qty:Decimal = to_decimal("0.0")
        t_val:Decimal = to_decimal("0.0")
        do_it2:bool = False
        unit_expense:Decimal = to_decimal("0.0")
        l_store = None
        L_store =  create_buffer("L_store",L_lager)
        it_exist = False
        t_list_data.clear()
        qty =  to_decimal("0")
        val =  to_decimal("0")
        curr_artnr = 0

        if m_str != 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.op_art == m_str) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & ((L_op.op_art == 2) | (L_op.op_art == 4)) & (L_op.herkunftflag == 1)).order_by(L_op.op_art, L_artikel.bezeich, L_op.datum, L_op.lager_nr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.content =  to_decimal(l_artikel.inhalt)
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(l_op.warenwert)
                                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                        else:
                            unit_expense =  to_decimal("0")

                            for queasy in db_session.query(Queasy).filter(
                                     (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                                unit_expense =  to_decimal(queasy.deci1)
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                                val =  to_decimal(val) + to_decimal(t_list.val)
                                t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                    t_list.qty =  to_decimal(l_op.anzahl)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)
        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lager_nr, l_op.pos, l_op.lscheinnr, l_op.op_art, l_op.datum, l_op.artnr, l_op.warenwert, l_op.anzahl, l_op.fuellflag, l_op._recid, l_artikel.zwkum, l_artikel.endkum, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel._recid, l_untergrup.bezeich, l_untergrup.betriebsnr, l_untergrup._recid in db_session.query(L_op.lager_nr, L_op.pos, L_op.lscheinnr, L_op.op_art, L_op.datum, L_op.artnr, L_op.warenwert, L_op.anzahl, L_op.fuellflag, L_op._recid, L_artikel.zwkum, L_artikel.endkum, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel._recid, L_untergrup.bezeich, L_untergrup.betriebsnr, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == m_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.op_art == 4) & (L_op.herkunftflag == 1)).order_by(L_artikel.bezeich, L_op.datum, L_op.lager_nr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                it_exist = True

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, l_op.lager_nr)]})

                l_store = get_cache (L_lager, {"lager_nr": [(eq, l_op.pos)]})

                l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, l_artikel.endkum)]})

                if curr_artnr != l_op.artnr and qty != 0:
                    t_list = T_list()
                    t_list_data.append(t_list)

                    t_list.price = "Total"
                    t_list.qty =  to_decimal(qty)
                    t_list.val =  to_decimal(val)
                    qty =  to_decimal("0")
                    val =  to_decimal("0")
                curr_artnr = l_op.artnr
                do_it2 = True

                if (mattype == 1 and l_untergrup.betriebsnr == 1) or (mattype == 2 and l_untergrup.betriebsnr == 0):
                    do_it2 = False

                if do_it2:
                    t_list = T_list()
                    t_list_data.append(t_list)

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
                    t_list.content =  to_decimal(l_artikel.inhalt)
                    t_list.cat_bez = l_lager.bezeich
                    t_list.main_bez = l_hauptgrp.bezeich
                    t_list.subgrp_bez = l_untergrup.bezeich

                    if l_store:
                        t_list.t_bezeich = l_store.bezeich

                    if l_op.anzahl != 0 and show_price:

                        if not expense_amt:
                            t_list.price = to_string((l_op.warenwert / l_op.anzahl) , ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(l_op.warenwert)
                                val =  to_decimal(val) + to_decimal(l_op.warenwert)
                                t_val =  to_decimal(t_val) + to_decimal(l_op.warenwert)


                        else:
                            unit_expense =  to_decimal("0")

                            for queasy in db_session.query(Queasy).filter(
                                     (Queasy.key == 121) & (Queasy.number1 == l_op.artnr) & (Queasy.date1 <= l_op.datum)).order_by(Queasy.date1.desc()).yield_per(100):
                                unit_expense =  to_decimal(queasy.deci1)
                                break
                            t_list.price = to_string(unit_expense, ">>>,>>>,>>9.99")

                            if show_price:
                                t_list.val =  to_decimal(unit_expense) * to_decimal(l_op.anzahl)
                                val =  to_decimal(val) + to_decimal(t_list.val)
                                t_val =  to_decimal(t_val) + to_decimal(t_list.val)


                    t_list.qty =  to_decimal(l_op.anzahl)
                    qty =  to_decimal(qty) + to_decimal(l_op.anzahl)
                    t_qty =  to_decimal(t_qty) + to_decimal(l_op.anzahl)

        if qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Total"
            t_list.qty =  to_decimal(qty)
            t_list.val =  to_decimal(val)

        if t_qty != 0:
            t_list = T_list()
            t_list_data.append(t_list)

            t_list.price = "Grand Total"
            t_list.qty =  to_decimal(t_qty)
            t_list.val =  to_decimal(t_val)


    def add_id():

        nonlocal it_exist, t_list_data, l_lager, l_artikel, l_op, l_untergrup, l_hauptgrp, queasy, bediener
        nonlocal trans_code, m_grp, sorttype, m_str, mattype, from_art, to_art, from_date, to_date, show_price, expense_amt


        nonlocal t_list
        nonlocal t_list_data

        usr = None
        Usr =  create_buffer("Usr",Bediener)

        usr = get_cache (Bediener, {"nr": [(eq, l_op.fuellflag)]})

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