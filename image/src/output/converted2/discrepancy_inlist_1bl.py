#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from models import Htparam, L_lager, L_artikel, L_op, L_order, L_lieferant

def discrepancy_inlist_1bl(sorttype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, mi_rec_chk:bool, mi_ord_chk:bool, mi_all_chk:bool):

    prepare_cache ([Htparam, L_lager, L_artikel, L_op, L_order, L_lieferant])

    discrepancy_inlist_list = []
    lager_bezeich:string = ""
    i:int = 0
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    long_digit:bool = False
    note_str:List[string] = [" ", "Transfer"]
    deliver_no:string = ""
    htparam = l_lager = l_artikel = l_op = l_order = l_lieferant = None

    str_list = output_list = discrepancy_inlist = None

    str_list_list, Str_list = create_model("Str_list", {"s":string})
    output_list_list, Output_list = create_model("Output_list", {"datum":string, "lager":string, "docunr":string, "art":string, "bezeich":string, "in_qty":string, "amount":string, "epreis1":string, "epreis2":string, "lief":string, "dlvnote":string})
    discrepancy_inlist_list, Discrepancy_inlist = create_model("Discrepancy_inlist", {"datum":date, "lager":string, "docunr":string, "art":string, "bezeich":string, "in_qty":Decimal, "amount":Decimal, "epreis1":Decimal, "epreis2":Decimal, "lief":string, "dlvnote":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal discrepancy_inlist_list, lager_bezeich, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, mi_rec_chk, mi_ord_chk, mi_all_chk


        nonlocal str_list, output_list, discrepancy_inlist
        nonlocal str_list_list, output_list_list, discrepancy_inlist_list

        return {"discrepancy-inlist": discrepancy_inlist_list}

    def create_list1():

        nonlocal discrepancy_inlist_list, lager_bezeich, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, mi_rec_chk, mi_ord_chk, mi_all_chk


        nonlocal str_list, output_list, discrepancy_inlist
        nonlocal str_list_list, output_list_list, discrepancy_inlist_list

        epreis:Decimal = to_decimal("0.0")
        diff_flag:bool = False
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.docu_nr, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op.lager_nr, l_op.lief_nr, l_op.lscheinnr, l_op.einzelpreis, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.docu_nr, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op.lager_nr, L_op.lief_nr, L_op.lscheinnr, L_op.einzelpreis, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.loeschflag < 2) & (L_op.op_art == 1) & (L_op.docu_nr != L_op.lscheinnr)).order_by(L_op.artnr, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)]})
                diff_flag = False

                if l_order:

                    if l_order.flag:
                        epreis =  to_decimal(l_order.einzelpreis) / to_decimal(l_order.txtnr)
                    else:
                        epreis =  to_decimal(l_order.einzelpreis)

                    if price_decimal == 0:

                        if (epreis - l_op.einzelpreis) > 1 or (l_op.einzelpreis - epreis) > 1:
                            diff_flag = True
                    else:

                        if (epreis - l_op.einzelpreis) > 0.01 or (l_op.einzelpreis - epreis) > 0.01:
                            diff_flag = True

                if diff_flag:
                    tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                    if not long_digit:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.datum = to_string(l_op.datum)
                        output_list.lager = to_string(l_op.lager_nr, "99")
                        output_list.art = to_string(l_artikel.artnr, "9999999")
                        output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                        output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                        output_list.amount = to_string(l_op.warenwert, "->>,>>>,>>9.99")
                    else:
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.datum = to_string(l_op.datum)
                        output_list.lager = to_string(l_op.lager_nr, "99")
                        output_list.art = to_string(l_artikel.artnr, "9999999")
                        output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                        output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                        output_list.amount = to_string(l_op.warenwert, "->,>>>,>>>,>>9")

                    if l_op.lief_nr != 0:

                        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                        if l_lieferant:
                            output_list.lief = to_string(l_lieferant.firma, "x(20)")
                        else:
                            output_list.lief = to_string(" ", "x(20)")
                    else:
                        output_list.lief = to_string(" ", "x(20)")

                    if length(l_op.lscheinnr) > 16:
                        deliver_no = substring(l_op.lscheinnr, length(l_op.lscheinnr) - 15 - 1, 16)
                    else:
                        deliver_no = l_op.lscheinnr
                    output_list.docunr = to_string(l_op.docu_nr, "x(12)")
                    output_list.dlvnote = to_string(deliver_no, "x(16)")

                    if long_digit:
                        output_list.epreis1 = to_string(l_op.einzelpreis, "->,>>>,>>>,>>9")
                        output_list.epreis2 = to_string(epreis, "->,>>>,>>>,>>9")
                    else:
                        output_list.epreis1 = to_string(l_op.einzelpreis, "->>,>>>,>>9.99")
                        output_list.epreis2 = to_string(epreis, "->>,>>>,>>9.99")
        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.datum = to_string(" ", "x(8)")
        output_list.lager = to_string(" ", "x(2)")
        output_list.art = to_string(" ", "x(7)")
        output_list.bezeich = to_string("T O T A L", "x(36)")

        if not long_digit:
            output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
            output_list.amount = to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
            output_list.amount = to_string(tot_amount, "->,>>>,>>>,>>9")


    def create_list2():

        nonlocal discrepancy_inlist_list, lager_bezeich, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, mi_rec_chk, mi_ord_chk, mi_all_chk


        nonlocal str_list, output_list, discrepancy_inlist
        nonlocal str_list_list, output_list_list, discrepancy_inlist_list

        epreis:Decimal = to_decimal("0.0")
        diff_flag:bool = False
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.docu_nr, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op.lager_nr, l_op.lief_nr, l_op.lscheinnr, l_op.einzelpreis, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.docu_nr, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op.lager_nr, L_op.lief_nr, L_op.lscheinnr, L_op.einzelpreis, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.loeschflag < 2) & (L_op.op_art == 1) & (L_op.docu_nr != L_op.lscheinnr)).order_by(L_artikel.bezeich, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)]})
                diff_flag = False

                if l_order:

                    if l_order.flag:
                        epreis =  to_decimal(l_order.einzelpreis) / to_decimal(l_order.txtnr)
                    else:
                        epreis =  to_decimal(l_order.einzelpreis)

                    if price_decimal == 0:

                        if (epreis - l_op.einzelpreis) > 1 or (l_op.einzelpreis - epreis) > 1:
                            diff_flag = True
                    else:

                        if (epreis - l_op.einzelpreis) > 0.01 or (l_op.einzelpreis - epreis) > 0.01:
                            diff_flag = True

                if diff_flag:

                    if mi_rec_chk :

                        if l_op.einzelpreis >= epreis:
                            tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                            if not long_digit:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->>,>>>,>>9.99")
                            else:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->,>>>,>>>,>>9")

                            if l_op.lief_nr != 0:

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                                if l_lieferant:
                                    output_list.lief = to_string(l_lieferant.firma, "x(20)")
                                else:
                                    output_list.lief = to_string(" ", "x(20)")
                            else:
                                output_list.lief = to_string(" ", "x(20)")

                            if length(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, length(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            output_list.docunr = to_string(l_op.docu_nr, "x(12)")
                            output_list.dlvnote = to_string(deliver_no, "x(16)")

                            if long_digit:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->,>>>,>>>,>>9")
                                output_list.epreis2 = to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->>,>>>,>>9.99")
                                output_list.epreis2 = to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_ord_chk :

                        if epreis >= l_op.einzelpreis:
                            tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                            if not long_digit:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->>,>>>,>>9.99")
                            else:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->,>>>,>>>,>>9")

                            if l_op.lief_nr != 0:

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                                if l_lieferant:
                                    output_list.lief = to_string(l_lieferant.firma, "x(20)")
                                else:
                                    output_list.lief = to_string(" ", "x(20)")
                            else:
                                output_list.lief = to_string(" ", "x(20)")

                            if length(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, length(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            output_list.docunr = to_string(l_op.docu_nr, "x(12)")
                            output_list.dlvnote = to_string(deliver_no, "x(16)")

                            if long_digit:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->,>>>,>>>,>>9")
                                output_list.epreis2 = to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->>,>>>,>>9.99")
                                output_list.epreis2 = to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_all_chk :
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                        if not long_digit:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.datum = to_string(l_op.datum)
                            output_list.lager = to_string(l_op.lager_nr, "99")
                            output_list.art = to_string(l_artikel.artnr, "9999999")
                            output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                            output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                            output_list.amount = to_string(l_op.warenwert, "->>,>>>,>>9.99")
                        else:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.datum = to_string(l_op.datum)
                            output_list.lager = to_string(l_op.lager_nr, "99")
                            output_list.art = to_string(l_artikel.artnr, "9999999")
                            output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                            output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                            output_list.amount = to_string(l_op.warenwert, "->,>>>,>>>,>>9")

                        if l_op.lief_nr != 0:

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                            if l_lieferant:
                                output_list.lief = to_string(l_lieferant.firma, "x(20)")
                            else:
                                output_list.lief = to_string(" ", "x(20)")
                        else:
                            output_list.lief = to_string(" ", "x(20)")

                        if length(l_op.lscheinnr) > 16:
                            deliver_no = substring(l_op.lscheinnr, length(l_op.lscheinnr) - 15 - 1, 16)
                        else:
                            deliver_no = l_op.lscheinnr
                        output_list.docunr = to_string(l_op.docu_nr, "x(12)")
                        output_list.dlvnote = to_string(deliver_no, "x(16)")

                        if long_digit:
                            output_list.epreis1 = to_string(l_op.einzelpreis, "->,>>>,>>>,>>9")
                            output_list.epreis2 = to_string(epreis, "->,>>>,>>>,>>9")
                        else:
                            output_list.epreis1 = to_string(l_op.einzelpreis, "->>,>>>,>>9.99")
                            output_list.epreis2 = to_string(epreis, "->>,>>>,>>9.99")

        if mi_rec_chk  and tot_anz != 0 and tot_amount != 0:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = to_string(" ", "x(8)")
            output_list.lager = to_string(" ", "x(2)")
            output_list.art = to_string(" ", "x(7)")
            output_list.bezeich = to_string("T O T A L", "x(36)")

            if not long_digit:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_ord_chk  and tot_anz != 0 and tot_amount != 0:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = to_string(" ", "x(8)")
            output_list.lager = to_string(" ", "x(2)")
            output_list.art = to_string(" ", "x(7)")
            output_list.bezeich = to_string("T O T A L", "x(36)")

            if not long_digit:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_all_chk :
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = to_string(" ", "x(8)")
            output_list.lager = to_string(" ", "x(2)")
            output_list.art = to_string(" ", "x(7)")
            output_list.bezeich = to_string("T O T A L", "x(36)")

            if not long_digit:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->,>>>,>>>,>>9")


    def create_list3():

        nonlocal discrepancy_inlist_list, lager_bezeich, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant
        nonlocal sorttype, from_lager, to_lager, from_date, to_date, from_art, to_art, mi_rec_chk, mi_ord_chk, mi_all_chk


        nonlocal str_list, output_list, discrepancy_inlist
        nonlocal str_list_list, output_list_list, discrepancy_inlist_list

        epreis:Decimal = to_decimal("0.0")
        diff_flag:bool = False
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.docu_nr, l_op.artnr, l_op.anzahl, l_op.warenwert, l_op.datum, l_op.lager_nr, l_op.lief_nr, l_op.lscheinnr, l_op.einzelpreis, l_op._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel._recid in db_session.query(L_op.docu_nr, L_op.artnr, L_op.anzahl, L_op.warenwert, L_op.datum, L_op.lager_nr, L_op.lief_nr, L_op.lscheinnr, L_op.einzelpreis, L_op._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.lager_nr == l_lager.lager_nr) & (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.artnr >= from_art) & (L_op.artnr <= to_art) & (L_op.anzahl != 0) & (L_op.loeschflag < 2) & (L_op.op_art == 1) & (L_op.docu_nr != L_op.lscheinnr)).order_by(L_op.datum, L_op.lscheinnr, L_artikel.bezeich).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                l_order = get_cache (L_order, {"docu_nr": [(eq, l_op.docu_nr)],"artnr": [(eq, l_op.artnr)]})
                diff_flag = False

                if l_order:

                    if l_order.flag:
                        epreis =  to_decimal(l_order.einzelpreis) / to_decimal(l_order.txtnr)
                    else:
                        epreis =  to_decimal(l_order.einzelpreis)

                    if price_decimal == 0:

                        if (epreis - l_op.einzelpreis) > 1 or (l_op.einzelpreis - epreis) > 1:
                            diff_flag = True
                    else:

                        if (epreis - l_op.einzelpreis) > 0.01 or (l_op.einzelpreis - epreis) > 0.01:
                            diff_flag = True

                if diff_flag:

                    if mi_rec_chk :

                        if l_op.einzelpreis >= epreis:
                            tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                            if not long_digit:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->>,>>>,>>9.99")
                            else:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->,>>>,>>>,>>9")

                            if l_op.lief_nr != 0:

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                                if l_lieferant:
                                    output_list.lief = to_string(l_lieferant.firma, "x(20)")
                                else:
                                    output_list.lief = to_string(" ", "x(20)")
                            else:
                                output_list.lief = to_string(" ", "x(20)")

                            if length(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, length(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            output_list.docunr = to_string(l_op.docu_nr, "x(12)")
                            output_list.dlvnote = to_string(deliver_no, "x(16)")

                            if long_digit:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->,>>>,>>>,>>9")
                                output_list.epreis2 = to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->>,>>>,>>9.99")
                                output_list.epreis2 = to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_ord_chk :

                        if epreis >= l_op.einzelpreis:
                            tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                            tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                            if not long_digit:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->>,>>>,>>9.99")
                            else:
                                output_list = Output_list()
                                output_list_list.append(output_list)

                                output_list.datum = to_string(l_op.datum)
                                output_list.lager = to_string(l_op.lager_nr, "99")
                                output_list.art = to_string(l_artikel.artnr, "9999999")
                                output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                                output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                                output_list.amount = to_string(l_op.warenwert, "->,>>>,>>>,>>9")

                            if l_op.lief_nr != 0:

                                l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                                if l_lieferant:
                                    output_list.lief = to_string(l_lieferant.firma, "x(20)")
                                else:
                                    output_list.lief = to_string(" ", "x(20)")
                            else:
                                output_list.lief = to_string(" ", "x(20)")

                            if length(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, length(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            output_list.docunr = to_string(l_op.docu_nr, "x(12)")
                            output_list.dlvnote = to_string(deliver_no, "x(16)")

                            if long_digit:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->,>>>,>>>,>>9")
                                output_list.epreis2 = to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                output_list.epreis1 = to_string(l_op.einzelpreis, "->>,>>>,>>9.99")
                                output_list.epreis2 = to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_all_chk :
                        tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                        tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                        if not long_digit:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.datum = to_string(l_op.datum)
                            output_list.lager = to_string(l_op.lager_nr, "99")
                            output_list.art = to_string(l_artikel.artnr, "9999999")
                            output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                            output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                            output_list.amount = to_string(l_op.warenwert, "->>,>>>,>>9.99")
                        else:
                            output_list = Output_list()
                            output_list_list.append(output_list)

                            output_list.datum = to_string(l_op.datum)
                            output_list.lager = to_string(l_op.lager_nr, "99")
                            output_list.art = to_string(l_artikel.artnr, "9999999")
                            output_list.bezeich = to_string(l_artikel.bezeich, "x(36)")
                            output_list.in_qty = to_string(l_op.anzahl, "->>>,>>9.99")
                            output_list.amount = to_string(l_op.warenwert, "->,>>>,>>>,>>9")

                        if l_op.lief_nr != 0:

                            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_op.lief_nr)]})

                            if l_lieferant:
                                output_list.lief = to_string(l_lieferant.firma, "x(20)")
                            else:
                                output_list.lief = to_string(" ", "x(20)")
                        else:
                            output_list.lief = to_string(" ", "x(20)")

                        if length(l_op.lscheinnr) > 16:
                            deliver_no = substring(l_op.lscheinnr, length(l_op.lscheinnr) - 15 - 1, 16)
                        else:
                            deliver_no = l_op.lscheinnr
                        output_list.docunr = to_string(l_op.docu_nr, "x(12)")
                        output_list.dlvnote = to_string(deliver_no, "x(16)")

                        if long_digit:
                            output_list.epreis1 = to_string(l_op.einzelpreis, "->,>>>,>>>,>>9")
                            output_list.epreis2 = to_string(epreis, "->,>>>,>>>,>>9")
                        else:
                            output_list.epreis1 = to_string(l_op.einzelpreis, "->>,>>>,>>9.99")
                            output_list.epreis2 = to_string(epreis, "->>,>>>,>>9.99")

        if mi_rec_chk  and tot_anz != 0 and tot_amount != 0:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = to_string(" ", "x(8)")
            output_list.lager = to_string(" ", "x(2)")
            output_list.art = to_string(" ", "x(7)")
            output_list.bezeich = to_string("T O T A L", "x(36)")

            if not long_digit:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_ord_chk  and tot_anz != 0 and tot_amount != 0:
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = to_string(" ", "x(8)")
            output_list.lager = to_string(" ", "x(2)")
            output_list.art = to_string(" ", "x(7)")
            output_list.bezeich = to_string("T O T A L", "x(36)")

            if not long_digit:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_all_chk :
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.datum = to_string(" ", "x(8)")
            output_list.lager = to_string(" ", "x(2)")
            output_list.art = to_string(" ", "x(7)")
            output_list.bezeich = to_string("T O T A L", "x(36)")

            if not long_digit:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                output_list.in_qty = to_string(tot_anz, "->,>>>,>>9.99")
                output_list.amount = to_string(tot_amount, "->,>>>,>>>,>>9")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    price_decimal = get_output(htpint(491))

    if sorttype == 1:
        create_list1()

    elif sorttype == 2:
        create_list2()
    else:
        create_list3()
    discrepancy_inlist_list.clear()

    for output_list in query(output_list_list):
        discrepancy_inlist = Discrepancy_inlist()
        discrepancy_inlist_list.append(discrepancy_inlist)


        l_lager = get_cache (L_lager, {"lager_nr": [(eq, to_int(output_list.lager))]})

        if l_lager:
            lager_bezeich = l_lager.bezeich


        discrepancy_inlist.datum = date_mdy(output_list.datum)
        discrepancy_inlist.lager = lager_bezeich
        discrepancy_inlist.docunr = output_list.docunr
        discrepancy_inlist.art = output_list.art
        discrepancy_inlist.bezeich = output_list.bezeich
        discrepancy_inlist.in_qty =  to_decimal(to_decimal(output_list.in_qty) )
        discrepancy_inlist.amount =  to_decimal(to_decimal(output_list.amount) )
        discrepancy_inlist.epreis1 =  to_decimal(to_decimal(output_list.epreis1) )
        discrepancy_inlist.epreis2 =  to_decimal(to_decimal(output_list.epreis2) )
        discrepancy_inlist.lief = output_list.lief
        discrepancy_inlist.dlvnote = output_list.dlvnote

    return generate_output()