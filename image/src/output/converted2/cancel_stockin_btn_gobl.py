#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, L_artikel, L_lieferant, L_op, L_ophdr, L_untergrup

def cancel_stockin_btn_gobl(pvilanguage:int, all_supp:bool, sorttype:int, from_grp:int, store:int, from_date:date, to_date:date, show_price:bool, from_supp:string):

    prepare_cache ([Htparam, L_artikel, L_lieferant, L_op, L_ophdr, L_untergrup])

    str_list_list = []
    tot_anz:Decimal = to_decimal("0.0")
    tot_amount:Decimal = to_decimal("0.0")
    i:int = 0
    unit_price:Decimal = to_decimal("0.0")
    long_digit:bool = False
    lvcarea:string = "cancel-stockin"
    htparam = bediener = l_artikel = l_lieferant = l_op = l_ophdr = l_untergrup = None

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"h_recid":int, "l_recid":int, "lief_nr":int, "billdate":date, "artnr":int, "lager_nr":int, "docu_nr":string, "lscheinnr":string, "invoice_nr":string, "qty":Decimal, "epreis":Decimal, "warenwert":Decimal, "deci1_3":Decimal, "s":string}, {"lscheinnr": ""})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        return {"str-list": str_list_list}

    def create_list1():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_lieferant.firma, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})
                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)


                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)
                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)
                        str_list.deci1_3 =  to_decimal(l_op.deci1[2])

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_lieferant.firma, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list1a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list1b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_untergrup.bezeich, L_op.artnr, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_untergrup.bezeich, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list11():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_lieferant.firma, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)
                    str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_lieferant.firma, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list11a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list11b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_untergrup.bezeich, L_op.artnr, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr > 0) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_untergrup.bezeich, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list2():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.lager_nr == store) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "G R T T L"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list2a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list2b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_untergrup.bezeich, L_op.artnr, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_untergrup.bezeich, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list22():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.lager_nr == store) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)
                tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)") + to_string(l_op.docu_nr, "x(16)") + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        str_list = Str_list()
        str_list_list.append(str_list)

        for i in range(1,17 + 1) :
            str_list.s = str_list.s + " "
        str_list.s = str_list.s + "GRAND TOTAL"
        for i in range(1,27 + 1) :
            str_list.s = str_list.s + " "
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list22a():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_lieferant = L_lieferant()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_lieferant.lief_nr, l_lieferant.firma, l_lieferant._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_lieferant.lief_nr, L_lieferant.firma, L_lieferant._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_lieferant,(L_lieferant.lief_nr == L_op.lief_nr)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_op.datum, L_op.lscheinnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.artnr == l_op.artnr and str_list.lager_nr == l_op.lager_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    def create_list22b():

        nonlocal str_list_list, tot_anz, tot_amount, i, unit_price, long_digit, lvcarea, htparam, bediener, l_artikel, l_lieferant, l_op, l_ophdr, l_untergrup
        nonlocal pvilanguage, all_supp, sorttype, from_grp, store, from_date, to_date, show_price, from_supp


        nonlocal str_list
        nonlocal str_list_list

        t_anz:Decimal = to_decimal("0.0")
        t_amt:Decimal = to_decimal("0.0")
        lief_nr:int = 0
        lscheinnr:string = ""
        usrid:string = ""
        reason:string = ""
        str1:string = ""
        usrtime:string = ""
        usr = None
        Usr =  create_buffer("Usr",Bediener)
        str_list_list.clear()
        tot_anz =  to_decimal("0")
        tot_amount =  to_decimal("0")

        l_lieferant = get_cache (L_lieferant, {"firma": [(eq, from_supp)]})

        if store == 0:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1)).order_by(L_untergrup.bezeich, L_op.artnr, L_op.datum).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
                    else:
                        str_list.s = str_list.s + to_string(l_op.docu_nr, "x(16)")

                    if not long_digit:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(l_op.lscheinnr, "x(20)") + to_string(unit_price, ">>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string(usrtime, "x(26)") + to_string(reason, "x(24)")

        else:

            l_op_obj_list = {}
            l_op = L_op()
            l_artikel = L_artikel()
            l_untergrup = L_untergrup()
            for l_op.lscheinnr, l_op.datum, l_op.stornogrund, l_op.einzelpreis, l_op.anzahl, l_op.warenwert, l_op.docu_nr, l_op.artnr, l_op.lager_nr, l_op._recid, l_op.lief_nr, l_op.deci1, l_artikel.artnr, l_artikel.bezeich, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup._recid in db_session.query(L_op.lscheinnr, L_op.datum, L_op.stornogrund, L_op.einzelpreis, L_op.anzahl, L_op.warenwert, L_op.docu_nr, L_op.artnr, L_op.lager_nr, L_op._recid, L_op.lief_nr, L_op.deci1, L_artikel.artnr, L_artikel.bezeich, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup._recid).join(L_artikel,(L_artikel.artnr == L_op.artnr) & (L_artikel.endkum == from_grp)).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                     (L_op.datum >= from_date) & (L_op.datum <= to_date) & (L_op.lief_nr == l_lieferant.lief_nr) & (L_op.loeschflag == 2) & (L_op.op_art == 1) & (L_op.lager_nr == store)).order_by(L_untergrup.bezeich, L_op.datum, L_op.artnr).all():
                if l_op_obj_list.get(l_op._recid):
                    continue
                else:
                    l_op_obj_list[l_op._recid] = True


                reason = ""
                str1 = ""
                usrtime = ""
                for i in range(1,num_entries(l_op.stornogrund, ";")  + 1) :
                    str1 = entry(i - 1, l_op.stornogrund, ";")

                    if entry(0, str1, ":") == ("reason").lower() :
                        reason = entry(1, str1, ":")
                    else:
                        usrtime = str1

                l_ophdr = get_cache (L_ophdr, {"op_typ": [(eq, "sti")],"lscheinnr": [(eq, l_op.lscheinnr)],"datum": [(eq, l_op.datum)]})

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
                    str_list.qty =  to_decimal(t_anz)

                    if not long_digit:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>>,>>>,>>9.99")
                    else:
                        str_list.s = str_list.s + to_string(t_anz, "->,>>>,>>9.99") + to_string(t_amt, "->>,>>>,>>>,>>9")
                    str_list.s = str_list.s + to_string("T O T A L", "x(18)")
                    lscheinnr = l_untergrup.bezeich
                    t_anz =  to_decimal("0")
                    t_amt =  to_decimal("0")
                    str_list = Str_list()
                    str_list_list.append(str_list)

                t_anz =  to_decimal(t_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    t_amt =  to_decimal(t_amt) + to_decimal(l_op.warenwert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_op.anzahl)

                if show_price:
                    tot_amount =  to_decimal(tot_amount) + to_decimal(l_op.warenwert)

                if show_price:
                    unit_price =  to_decimal(l_op.einzelpreis)

                str_list = query(str_list_list, filters=(lambda str_list: str_list.docu_nr == l_op.docu_nr and str_list.lscheinnr == l_op.lscheinnr and str_list.lager_nr == l_op.lager_nr and str_list.artnr == l_op.artnr and str_list.artnr == l_op.artnr and str_list.epreis == l_op.einzelpreis), first=True)

                if str_list:
                    str_list.qty =  to_decimal(str_list.qty) + to_decimal(l_op.anzahl)

                    if show_price:
                        str_list.warenwert =  to_decimal(str_list.warenwert) + to_decimal(l_op.warenwert)
                    str_list.s = replace_substring(str_list.s, 55, 13, to_string(str_list.qty, "->,>>>,>>9.99"))

                    if not long_digit:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>>,>>>,>>9.99"))
                    else:
                        str_list.s = replace_substring(str_list.s, 68, 15, to_string(str_list.warenwert, "->>,>>>,>>>,>>9"))
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
                    str_list.qty =  to_decimal(l_op.anzahl)
                    str_list.epreis =  to_decimal(l_op.einzelpreis)

                    if show_price:
                        str_list.warenwert =  to_decimal(l_op.warenwert)

                    if not long_digit:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>>,>>>,>>9.99") + to_string(l_lieferant.firma, "x(24)")
                    else:
                        str_list.s = to_string(l_op.datum) + to_string(l_op.lager_nr, "99") + to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(32)") + to_string(l_artikel.traubensorte, "x(6)") + to_string(l_op.anzahl, "->,>>>,>>9.99") + to_string(str_list.warenwert, "->>,>>>,>>>,>>9") + to_string(l_lieferant.firma, "x(24)")

                    if l_op.docu_nr == l_op.lscheinnr:
                        str_list.s = str_list.s + to_string(translateExtended ("Direct Pchase ", lvcarea, "") , "x(16)")
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
        str_list.qty =  to_decimal(t_anz)

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
        str_list.qty =  to_decimal(tot_anz)

        if not long_digit:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>>,>>>,>>9.99")
        else:
            str_list.s = str_list.s + to_string(tot_anz, "->,>>>,>>9.99") + to_string(tot_amount, "->>,>>>,>>>,>>9")


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
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