from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from models import Htparam, L_lager, L_artikel, L_op, L_order, L_lieferant

def discrepancy_inlistbl(sorttype:int, from_lager:int, to_lager:int, from_date:date, to_date:date, from_art:int, to_art:int, mi_rec_chk:bool, mi_ord_chk:bool, mi_all_chk:bool):
    str_list_list = []
    i:int = 0
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    price_decimal:int = 0
    long_digit:bool = False
    note_str:[str] = ["", "", ""]
    deliver_no:str = ""
    htparam = l_lager = l_artikel = l_op = l_order = l_lieferant = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"s":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant


        nonlocal str_list
        nonlocal str_list_list
        return {"str-list": str_list_list}

    def create_list1():

        nonlocal str_list_list, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant


        nonlocal str_list
        nonlocal str_list_list

        epreis:decimal = 0
        diff_flag:bool = False
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.loeschflag < 2) &  (L_op.op_art == 1) &  (L_op.docu_nr != L_op.lscheinnr)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_op.docu_nr) &  (L_order.artnr == l_op.artnr)).first()
                diff_flag = False

                if l_order:

                    if l_order.flag:
                        epreis = l_order.einzelpreis / l_order.txt
                    else:
                        epreis = l_order.einzelpreis

                    if price_decimal == 0:

                        if (epreis - l_op.einzelpreis) > 1 or (l_op.einzelpreis - epreis) > 1:
                            diff_flag = True
                    else:

                        if (epreis - l_op.einzelpreis) > 0.01 or (l_op.einzelpreis - epreis) > 0.01:
                            diff_flag = True

                if diff_flag:
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + l_op.warenwert
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->>,>>>,>>9.99") + note_str[l_op.op_art - 1]
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->,>>>,>>>,>>9") + note_str[l_op.op_art - 1]

                    if l_op.lief_nr != 0:

                        l_lieferant = db_session.query(L_lieferant).filter(
                                (L_lieferant.lief_nr == l_op.lief_nr)).first()

                        if l_lieferant:
                            str_list.s = str_list.s + to_string(l_lieferant.firma, "x(20)")
                        else:
                            str_list.s = str_list.s + "                    "
                    else:
                        str_list.s = str_list.s + "                    "

                    if len(l_op.lscheinnr) > 16:
                        deliver_no = substring(l_op.lscheinnr, len(l_op.lscheinnr) - 15 - 1, 16)
                    else:
                        deliver_no = l_op.lscheinnr
                    str_list.s = str_list.s + to_string(l_op.docu_nr, "x(12)") + to_string(deliver_no, "x(16)")

                    if long_digit:
                        str_list.s = str_list.s + to_string(l_op.einzelpreis, "->,>>>,>>>,>>9") + to_string(epreis, "->,>>>,>>>,>>9")
                    else:
                        str_list.s = str_list.s + to_string(l_op.einzelpreis, "->>,>>>,>>9.99") + to_string(epreis, "->>,>>>,>>9.99")
        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,25 + 1) :
            str_list.s = str_list.s + " "

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_list2():

        nonlocal str_list_list, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant


        nonlocal str_list
        nonlocal str_list_list

        epreis:decimal = 0
        diff_flag:bool = False
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.loeschflag < 2) &  (L_op.op_art == 1) &  (L_op.docu_nr != L_op.lscheinnr)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_op.docu_nr) &  (L_order.artnr == l_op.artnr)).first()
                diff_flag = False

                if l_order:

                    if l_order.flag:
                        epreis = l_order.einzelpreis / l_order.txt
                    else:
                        epreis = l_order.einzelpreis

                    if price_decimal == 0:

                        if (epreis - l_op.einzelpreis) > 1 or (l_op.einzelpreis - epreis) > 1:
                            diff_flag = True
                    else:

                        if (epreis - l_op.einzelpreis) > 0.01 or (l_op.einzelpreis - epreis) > 0.01:
                            diff_flag = True

                if diff_flag:

                    if mi_rec_chk :

                        if l_op.einzelpreis >= epreis:
                            tot_anz = tot_anz + l_op.anzahl
                            tot_amount = tot_amount + l_op.warenwert
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if not long_digit:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->>,>>>,>>9.99") + note_str[l_op.op_art - 1]
                            else:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->,>>>,>>>,>>9") + note_str[l_op.op_art - 1]

                            if l_op.lief_nr != 0:

                                l_lieferant = db_session.query(L_lieferant).filter(
                                        (L_lieferant.lief_nr == l_op.lief_nr)).first()

                                if l_lieferant:
                                    str_list.s = str_list.s + to_string(l_lieferant.firma, "x(20)")
                                else:
                                    str_list.s = str_list.s + "                    "
                            else:
                                str_list.s = str_list.s + "                    "

                            if len(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, len(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(12)") + to_string(deliver_no, "x(16)")

                            if long_digit:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->,>>>,>>>,>>9") + to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->>,>>>,>>9.99") + to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_ord_chk :

                        if epreis >= l_op.einzelpreis:
                            tot_anz = tot_anz + l_op.anzahl
                            tot_amount = tot_amount + l_op.warenwert
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if not long_digit:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->>,>>>,>>9.99") + note_str[l_op.op_art - 1]
                            else:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->,>>>,>>>,>>9") + note_str[l_op.op_art - 1]

                            if l_op.lief_nr != 0:

                                l_lieferant = db_session.query(L_lieferant).filter(
                                        (L_lieferant.lief_nr == l_op.lief_nr)).first()

                                if l_lieferant:
                                    str_list.s = str_list.s + to_string(l_lieferant.firma, "x(20)")
                                else:
                                    str_list.s = str_list.s + "                    "
                            else:
                                str_list.s = str_list.s + "                    "

                            if len(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, len(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(12)") + to_string(deliver_no, "x(16)")

                            if long_digit:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->,>>>,>>>,>>9") + to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->>,>>>,>>9.99") + to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_all_chk :
                        tot_anz = tot_anz + l_op.anzahl
                        tot_amount = tot_amount + l_op.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->>,>>>,>>9.99") + note_str[l_op.op_art - 1]
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->,>>>,>>>,>>9") + note_str[l_op.op_art - 1]

                        if l_op.lief_nr != 0:

                            l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == l_op.lief_nr)).first()

                            if l_lieferant:
                                str_list.s = str_list.s + to_string(l_lieferant.firma, "x(20)")
                            else:
                                str_list.s = str_list.s + "                    "
                        else:
                            str_list.s = str_list.s + "                    "

                        if len(l_op.lscheinnr) > 16:
                            deliver_no = substring(l_op.lscheinnr, len(l_op.lscheinnr) - 15 - 1, 16)
                        else:
                            deliver_no = l_op.lscheinnr
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(12)") + to_string(deliver_no, "x(16)")

                        if long_digit:
                            str_list.s = str_list.s + to_string(l_op.einzelpreis, "->,>>>,>>>,>>9") + to_string(epreis, "->,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_op.einzelpreis, "->>,>>>,>>9.99") + to_string(epreis, "->>,>>>,>>9.99")

        if mi_rec_chk  and tot_anz != 0 and tot_amount != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,25 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_ord_chk  and tot_anz != 0 and tot_amount != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,25 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_all_chk :
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,25 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->,>>>,>>>,>>9")

    def create_list3():

        nonlocal str_list_list, i, tot_anz, tot_amount, price_decimal, long_digit, note_str, deliver_no, htparam, l_lager, l_artikel, l_op, l_order, l_lieferant


        nonlocal str_list
        nonlocal str_list_list

        epreis:decimal = 0
        diff_flag:bool = False
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_lager) &  (L_lager.lager_nr <= to_lager)).all():

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.lager_nr == l_lager.lager_nr) &  (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.artnr >= from_art) &  (L_op.artnr <= to_art) &  (L_op.anzahl != 0) &  (L_op.loeschflag < 2) &  (L_op.op_art == 1) &  (L_op.docu_nr != L_op.lscheinnr)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                l_order = db_session.query(L_order).filter(
                        (L_order.docu_nr == l_op.docu_nr) &  (L_order.artnr == l_op.artnr)).first()
                diff_flag = False

                if l_order:

                    if l_order.flag:
                        epreis = l_order.einzelpreis / l_order.txt
                    else:
                        epreis = l_order.einzelpreis

                    if price_decimal == 0:

                        if (epreis - l_op.einzelpreis) > 1 or (l_op.einzelpreis - epreis) > 1:
                            diff_flag = True
                    else:

                        if (epreis - l_op.einzelpreis) > 0.01 or (l_op.einzelpreis - epreis) > 0.01:
                            diff_flag = True

                if diff_flag:

                    if mi_rec_chk :

                        if l_op.einzelpreis >= epreis:
                            tot_anz = tot_anz + l_op.anzahl
                            tot_amount = tot_amount + l_op.warenwert
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if not long_digit:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->>,>>>,>>9.99") + note_str[l_op.op_art - 1]
                            else:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->,>>>,>>>,>>9") + note_str[l_op.op_art - 1]

                            if l_op.lief_nr != 0:

                                l_lieferant = db_session.query(L_lieferant).filter(
                                        (L_lieferant.lief_nr == l_op.lief_nr)).first()

                                if l_lieferant:
                                    str_list.s = str_list.s + to_string(l_lieferant.firma, "x(20)")
                                else:
                                    str_list.s = str_list.s + "                    "
                            else:
                                str_list.s = str_list.s + "                    "

                            if len(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, len(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(12)") + to_string(deliver_no, "x(16)")

                            if long_digit:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->,>>>,>>>,>>9") + to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->>,>>>,>>9.99") + to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_ord_chk :

                        if epreis >= l_op.einzelpreis:
                            tot_anz = tot_anz + l_op.anzahl
                            tot_amount = tot_amount + l_op.warenwert
                            str_list = Str_list()
                            str_list_list.append(str_list)


                            if not long_digit:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->>,>>>,>>9.99") + note_str[l_op.op_art - 1]
                            else:
                                str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->,>>>,>>>,>>9") + note_str[l_op.op_art - 1]

                            if l_op.lief_nr != 0:

                                l_lieferant = db_session.query(L_lieferant).filter(
                                        (L_lieferant.lief_nr == l_op.lief_nr)).first()

                                if l_lieferant:
                                    str_list.s = str_list.s + to_string(l_lieferant.firma, "x(20)")
                                else:
                                    str_list.s = str_list.s + "                    "
                            else:
                                str_list.s = str_list.s + "                    "

                            if len(l_op.lscheinnr) > 16:
                                deliver_no = substring(l_op.lscheinnr, len(l_op.lscheinnr) - 15 - 1, 16)
                            else:
                                deliver_no = l_op.lscheinnr
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(12)") + to_string(deliver_no, "x(16)")

                            if long_digit:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->,>>>,>>>,>>9") + to_string(epreis, "->,>>>,>>>,>>9")
                            else:
                                str_list.s = str_list.s + to_string(l_op.einzelpreis, "->>,>>>,>>9.99") + to_string(epreis, "->>,>>>,>>9.99")

                    elif mi_all_chk :
                        tot_anz = tot_anz + l_op.anzahl
                        tot_amount = tot_amount + l_op.warenwert
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->>,>>>,>>9.99") + note_str[l_op.op_art - 1]
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_op.anzahl, "->>>,>>9.99") + to_string(l_op.warenwert, "->,>>>,>>>,>>9") + note_str[l_op.op_art - 1]

                        if l_op.lief_nr != 0:

                            l_lieferant = db_session.query(L_lieferant).filter(
                                    (L_lieferant.lief_nr == l_op.lief_nr)).first()

                            if l_lieferant:
                                str_list.s = str_list.s + to_string(l_lieferant.firma, "x(20)")
                            else:
                                str_list.s = str_list.s + "                    "
                        else:
                            str_list.s = str_list.s + "                    "

                        if len(l_op.lscheinnr) > 16:
                            deliver_no = substring(l_op.lscheinnr, len(l_op.lscheinnr) - 15 - 1, 16)
                        else:
                            deliver_no = l_op.lscheinnr
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(12)") + to_string(deliver_no, "x(16)")

                        if long_digit:
                            str_list.s = str_list.s + to_string(l_op.einzelpreis, "->,>>>,>>>,>>9") + to_string(epreis, "->,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_op.einzelpreis, "->>,>>>,>>9.99") + to_string(epreis, "->>,>>>,>>9.99")

        if mi_rec_chk  and tot_anz != 0 and tot_amount != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,25 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_ord_chk  and tot_anz != 0 and tot_amount != 0:
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,25 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->,>>>,>>>,>>9")

        elif mi_all_chk :
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,25 + 1) :
                str_list.s = str_list.s + " "

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->,>>>,>>>,>>9")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical
    price_decimal = get_output(htpint(491))

    if sorttype == 1:
        create_list1()

    elif sorttype == 2:
        create_list2()
    else:
        create_list3()

    return generate_output()