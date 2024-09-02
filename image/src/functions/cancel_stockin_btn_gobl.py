from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, L_artikel, L_lieferant, L_op, L_ophdr, L_untergrup

def cancel_stockin_btn_gobl(pvilanguage:int, all_supp:bool, sorttype:int, from_grp:int, store:int, from_date:date, to_date:date, show_price:bool, from_supp:str):
    str_list_list = []
    tot_anz:decimal = 0
    tot_amount:decimal = 0
    i:int = 0
    unit_price:decimal = 0
    long_digit:bool = False
    lvcarea:str = "cancel_stockin"
    htparam = bediener = l_artikel = l_lieferant = l_op = l_ophdr = l_untergrup = None

    str_list = usr = None

    str_list_list, Str_list = create_model("Str_list", {"h_recid":int, "l_recid":int, "lief_nr":int, "billdate":date, "artnr":int, "lager_nr":int, "docu_nr":str, "lscheinnr":str, "invoice_nr":str, "qty":decimal, "epreis":decimal, "warenwert":decimal, "deci1_3":decimal, "s":str}, {"lscheinnr": ""})

    Usr = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list
        return {"str-list": str_list_list}

    def create_list1():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        Usr = Bediener
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()
                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)


                if show_price:
                    unit_price = l_op.einzelpreis
                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert
                        str_list.deci1_3 = l_op.deci1[2]

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,29 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = t_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "GRAND TOTAL"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list1a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        Usr = Bediener
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_op.lscheinnr

                if lscheinnr != l_op.lscheinnr:
                    lscheinnr = l_op.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_op.lscheinnr

                if lscheinnr != l_op.lscheinnr:
                    lscheinnr = l_op.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,29 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = t_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "GRAND TOTAL"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list1b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        Usr = Bediener
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup, l_lieferant in db_session.query(L_op, L_artikel, L_untergrup, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                    for i in range(1,6 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup, l_lieferant in db_session.query(L_op, L_artikel, L_untergrup, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                    for i in range(1,6 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
        for i in range(1,6 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = t_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
        str_list.s = str_list.s + to_string("T O T A L", "x(18)")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "GRAND TOTAL"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list11():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        Usr = Bediener
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl
                    str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lief_nr == 0:
                    lief_nr = l_lieferant.lief_nr

                if lief_nr != l_lieferant.lief_nr:
                    lief_nr = l_lieferant.lief_nr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,29 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = t_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "GRAND TOTAL"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list11a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        Usr = Bediener
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_op.lscheinnr

                if lscheinnr != l_op.lscheinnr:
                    lscheinnr = l_op.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_op.lscheinnr

                if lscheinnr != l_op.lscheinnr:
                    lscheinnr = l_op.lscheinnr
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + "T O T A L"
                    for i in range(1,29 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "T O T A L"
        for i in range(1,29 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = t_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "GRAND TOTAL"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list11b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        Usr = Bediener
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup, l_lieferant in db_session.query(L_op, L_artikel, L_untergrup, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                    for i in range(1,6 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = []
            for l_op, l_artikel, l_untergrup, l_lieferant in db_session.query(L_op, L_artikel, L_untergrup, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr > 0) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                if lscheinnr == "":
                    lscheinnr = l_untergrup.bezeich

                if lscheinnr != l_untergrup.bezeich:
                    str_list = Str_list()
                    str_list_list.append(str_list)

                    for i in range(1,17 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                    for i in range(1,6 + 1) :
                        str_list.s = str_list.s + " "
                    str_list.qty = t_anz

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz = 0
                    t_amt = 0
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz = t_anz + l_op.anzahl

                if show_price:
                    t_amt = t_amt + l_op.warenwert
                tot_anz = tot_anz + l_op.anzahl

                if show_price:
                    tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
        for i in range(1,6 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = t_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
        str_list.s = str_list.s + to_string("T O T A L", "x(18)")
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "GRAND TOTAL"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty = tot_anz

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list2a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
        Usr = Bediener
        str_list_list.clear()
        tot_anz = 0
        tot_amount = 0

        l_lieferant = db_session.query(L_lieferant).filter(
                (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

        if store == 0:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()
                tot_anz = tot_anz + l_op.anzahl
                tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                else:
                    str_list = Str_list()
                    str_list_list.append(str_list)


                    if l_ophdr:
                        str_list.invoice_nr = l_ophdr.fibukonto
                        str_list.h_recid = l_ophdr._recid
                    str_list.l_recid = l_op._recid
                    str_list.lief_nr = l_op.lief_nr
                    str_list.billdate = l_op.datum
                    str_list.artnr = l_op.artnr
                    str_list.lager_nr = l_op.lager_nr
                    str_list.docu_nr = l_op.docu_nr
                    str_list.lscheinnr = l_op.lscheinnr
                    str_list.qty = l_op.anzahl
                    str_list.epreis = l_op.einzelpreis

                    if show_price:
                        str_list.warenwert = l_op.warenwert

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = []
            for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                    (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.lager_nr == store) &  (L_op.op_art == 1)).all():
                if l_op._recid in l_op_obj_list:
                    continue
                else:
                    l_op_obj_list.append(l_op._recid)


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == "reason":
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = db_session.query(L_ophdr).filter(
                        (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()
                tot_anz = tot_anz + l_op.anzahl
                tot_amount = tot_amount + l_op.warenwert

                if show_price:
                    unit_price = l_op.einzelpreis

                str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty = str_list.qty + l_op.anzahl

                    if show_price:
                        str_list.warenwert = str_list.warenwert + l_op.warenwert
                    substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                    if not long_digit:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                    else:
                        substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9"). END
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")
                str_list = Str_list()
                str_list_list.append(str_list)

                for i in range(1,17 + 1) :
                    str_list.s = str_list.s + " "
                str_list.s = str_list.s + "G R T T L"
                for i in range(1,27 + 1) :
                    str_list.s = str_list.s + " "
                str_list.qty = tot_anz

                if not long_digit:
                    str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
                else:
                    str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

            Usr = Bediener
            str_list_list.clear()
            tot_anz = 0
            tot_amount = 0

            l_lieferant = db_session.query(L_lieferant).filter(
                    (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

            if store == 0:

                l_op_obj_list = []
                for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_op.lscheinnr

                    if lscheinnr != l_op.lscheinnr:
                        lscheinnr = l_op.lscheinnr
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "T O T A L"
                        for i in range(1,29 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            else:

                l_op_obj_list = []
                for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_op.lscheinnr

                    if lscheinnr != l_op.lscheinnr:
                        lscheinnr = l_op.lscheinnr
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "T O T A L"
                        for i in range(1,29 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,29 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = t_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "GRAND TOTAL"
            for i in range(1,27 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = tot_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list2b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
            Usr = Bediener
            str_list_list.clear()
            tot_anz = 0
            tot_amount = 0

            l_lieferant = db_session.query(L_lieferant).filter(
                    (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

            if store == 0:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_untergrup.bezeich

                    if lscheinnr != l_untergrup.bezeich:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                        for i in range(1,6 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                        lscheinnr = l_untergrup.bezeich
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            else:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_untergrup.bezeich

                    if lscheinnr != l_untergrup.bezeich:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                        for i in range(1,6 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                        lscheinnr = l_untergrup.bezeich
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
            for i in range(1,6 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = t_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
            str_list.s = str_list.s + to_string("T O T A L", "x(18)")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "GRAND TOTAL"
            for i in range(1,27 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = tot_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list22():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
            Usr = Bediener
            str_list_list.clear()
            tot_anz = 0
            tot_amount = 0

            l_lieferant = db_session.query(L_lieferant).filter(
                    (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

            if store == 0:

                l_op_obj_list = []
                for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            else:

                l_op_obj_list = []
                for l_op, l_artikel in db_session.query(L_op, L_artikel).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.lager_nr == store) &  (L_op.op_art == 1)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()
                    tot_anz = tot_anz + l_op.anzahl
                    tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "GRAND TOTAL"
            for i in range(1,27 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = tot_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list22a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
            Usr = Bediener
            str_list_list.clear()
            tot_anz = 0
            tot_amount = 0

            l_lieferant = db_session.query(L_lieferant).filter(
                    (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

            if store == 0:

                l_op_obj_list = []
                for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_op.lscheinnr

                    if lscheinnr != l_op.lscheinnr:
                        lscheinnr = l_op.lscheinnr
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "T O T A L"
                        for i in range(1,29 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            else:

                l_op_obj_list = []
                for l_op, l_artikel, l_lieferant in db_session.query(L_op, L_artikel, L_lieferant).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_op.lscheinnr

                    if lscheinnr != l_op.lscheinnr:
                        lscheinnr = l_op.lscheinnr
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + "T O T A L"
                        for i in range(1,29 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "T O T A L"
            for i in range(1,29 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = t_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "GRAND TOTAL"
            for i in range(1,27 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = tot_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    def create_list22b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal usr


        nonlocal str_list, usr
        nonlocal str_list_list

        t_anz:decimal = 0
        t_amt:decimal = 0
        lief_nr:int = 0
        lscheinnr:str = ""
        usrid:str = ""
        reason:str = ""
        str1:str = ""
        usrtime:str = ""
            Usr = Bediener
            str_list_list.clear()
            tot_anz = 0
            tot_amount = 0

            l_lieferant = db_session.query(L_lieferant).filter(
                    (func.lower(L_lieferant.firma) == (from_supp).lower())).first()

            if store == 0:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_untergrup.bezeich

                    if lscheinnr != l_untergrup.bezeich:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                        for i in range(1,6 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                        lscheinnr = l_untergrup.bezeich
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            else:

                l_op_obj_list = []
                for l_op, l_artikel, l_untergrup in db_session.query(L_op, L_artikel, L_untergrup).join(L_artikel,(L_artikel.artnr == L_op.artnr) &  (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == l_artikel.zwkum)).filter(
                        (L_op.datum >= from_date) &  (L_op.datum <= to_date) &  (L_op.lief_nr == l_lieferant.lief_nr) &  (L_op.loeschflag == 2) &  (L_op.op_art == 1) &  (L_op.lager_nr == store)).all():
                    if l_op._recid in l_op_obj_list:
                        continue
                    else:
                        l_op_obj_list.append(l_op._recid)


                    reason = ""
                    str1 = ""
                    usrtime = ""
                    for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                        str1 = entry(i - 1, l_op.stornogrund, ";")

                        if entry(0, str1, ":") == "reason":
                            reason = entry(1, str1, ":")
                        else:
                            usrtime = str1

                    l_ophdr = db_session.query(L_ophdr).filter(
                            (func.lower(L_ophdr.op_typ) == "STI") &  (L_ophdr.lscheinnr == l_op.lscheinnr) &  (L_ophdr.datum == l_op.datum)).first()

                    if lscheinnr == "":
                        lscheinnr = l_untergrup.bezeich

                    if lscheinnr != l_untergrup.bezeich:
                        str_list = Str_list()
                        str_list_list.append(str_list)

                        for i in range(1,17 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
                        for i in range(1,6 + 1) :
                            str_list.s = str_list.s + " "
                        str_list.qty = t_anz

                        if not long_digit:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                        lscheinnr = l_untergrup.bezeich
                        t_anz = 0
                        t_amt = 0
                        str_list = Str_list()
                        str_list_list.append(str_list)

                    t_anz = t_anz + l_op.anzahl

                    if show_price:
                        t_amt = t_amt + l_op.warenwert
                    tot_anz = tot_anz + l_op.anzahl

                    if show_price:
                        tot_amount = tot_amount + l_op.warenwert

                    if show_price:
                        unit_price = l_op.einzelpreis

                    str_list = query(str_list_list, filters=(lambda str_list :str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                    if str_list:
                        str_list.qty = str_list.qty + l_op.anzahl

                        if show_price:
                            str_list.warenwert = str_list.warenwert + l_op.warenwert
                        substring(str_list.s, 55, 13) = to_string(str_list.qty, "->,>>>,>>9.99")

                        if not long_digit:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>>,>>>,>>9.99")
                        else:
                            substring(str_list.s, 68, 15) = to_string(str_list.warenwert, "->>,>>>,>>>,>>9")
                    else:
                        str_list = Str_list()
                        str_list_list.append(str_list)


                        if l_ophdr:
                            str_list.invoice_nr = l_ophdr.fibukonto
                            str_list.h_recid = l_ophdr._recid
                        str_list.l_recid = l_op._recid
                        str_list.lief_nr = l_op.lief_nr
                        str_list.billdate = l_op.datum
                        str_list.artnr = l_op.artnr
                        str_list.lager_nr = l_op.lager_nr
                        str_list.docu_nr = l_op.docu_nr
                        str_list.lscheinnr = l_op.lscheinnr
                        str_list.qty = l_op.anzahl
                        str_list.epreis = l_op.einzelpreis

                        if show_price:
                            str_list.warenwert = l_op.warenwert

                        if not long_digit:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                        else:
                            str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensort, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                        if l_op.docu_nr == l_op.lscheinnr:
                            str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase   ", lvcarea, "") , "x(16)")
                        else:
                            str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                        if not long_digit:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string(lscheinnr, "x(32)")
            for i in range(1,6 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = t_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
            str_list.s = str_list.s + to_string("T O T A L", "x(18)")
            str_list = Str_list()
            str_list_list.append(str_list)

            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,17 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + "GRAND TOTAL"
            for i in range(1,27 + 1) :
                str_list.s = str_list.s + " "
            str_list.qty = tot_anz

            if not long_digit:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if all_supp and sorttype == 1:

        if from_grp == 0:
            create_list1()
        else:
            create_list11()

    elif not all_supp and sorttype == 1:

        if from_grp == 0:
            create_list2()
        else:
            create_list22()

    elif all_supp and sorttype == 2:

        if from_grp == 0:
            create_list1a()
        else:
            create_list11a()

    elif not all_supp and sorttype == 2:

        if from_grp == 0:
            create_list2a()
        else:
            create_list22a()

    elif all_supp and sorttype == 3:

        if from_grp == 0:
            create_list1b()
        else:
            create_list11b()

    elif not all_supp and sorttype == 3:

        if from_grp == 0:
            create_list2b()
        else:
            create_list22b()

    return generate_output()