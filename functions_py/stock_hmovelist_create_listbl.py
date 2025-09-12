#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, L_ophis, L_besthis, L_lager, L_lieferant, Gl_acct, L_ophhis

def stock_hmovelist_create_listbl(pvilanguage:int, s_artnr:int, mm:int, yy:int, from_lager:int, to_lager:int, show_price:bool):

    prepare_cache ([Htparam, L_ophis, L_besthis, L_lager, L_lieferant, Gl_acct, L_ophhis])

    anfdate = None
    enddate = None
    str_list_data = []
    lvcarea:string = "fb-flash1"
    tot_anz:Decimal = to_decimal("0.0")
    tot_val:Decimal = to_decimal("0.0")
    t_anz:Decimal = to_decimal("0.0")
    t_val:Decimal = to_decimal("0.0")
    long_digit:bool = False
    htparam = bediener = l_ophis = l_besthis = l_lager = l_lieferant = gl_acct = l_ophhis = None

    str_list = None

    str_list_data, Str_list = create_model("Str_list", {"s":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anfdate, enddate, str_list_data, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, htparam, bediener, l_ophis, l_besthis, l_lager, l_lieferant, gl_acct, l_ophhis
        nonlocal pvilanguage, s_artnr, mm, yy, from_lager, to_lager, show_price


        nonlocal str_list
        nonlocal str_list_data

        return {"anfdate": anfdate, "enddate": enddate, "str-list": str_list_data}

    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

    def create_list():

        nonlocal anfdate, enddate, str_list_data, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, htparam, bediener, l_ophis, l_besthis, l_lager, l_lieferant, gl_acct, l_ophhis
        nonlocal pvilanguage, s_artnr, mm, yy, from_lager, to_lager, show_price


        nonlocal str_list
        nonlocal str_list_data

        t_qty:Decimal = to_decimal("0.0")
        t_wert:Decimal = to_decimal("0.0")
        bemerk:string = ""
        preis:Decimal = to_decimal("0.0")
        wert:Decimal = to_decimal("0.0")
        usr = None
        l_op1 = None
        l_oh = None
        Usr =  create_buffer("Usr",Bediener)
        L_op1 =  create_buffer("L_op1",L_ophis)
        L_oh =  create_buffer("L_oh",L_besthis)
        anfdate = date_mdy(mm, 1, yy)
        enddate = anfdate + timedelta(days=31)
        enddate = date_mdy(get_month(enddate) , 1, get_year(enddate)) - timedelta(days=1)

        l_oh = get_cache (L_besthis, {"artnr": [(eq, s_artnr)],"lager_nr": [(eq, 0)],"anf_best_dat": [(eq, anfdate)]})

        if l_oh:
            t_qty =  to_decimal(l_oh.anz_anf_best) + to_decimal(l_oh.anz_eingang) - to_decimal(l_oh.anz_ausgang)

            if show_price:
                t_wert =  to_decimal(l_oh.val_anf_best) + to_decimal(l_oh.wert_eingang) - to_decimal(l_oh.wert_ausgang)

        str_list_data.clear()
        tot_anz =  to_decimal("0")
        tot_val =  to_decimal("0")

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_lager) & (L_lager.lager_nr <= to_lager)).order_by(L_lager._recid).all():

            l_besthis = get_cache (L_besthis, {"lager_nr": [(eq, l_lager.lager_nr)],"artnr": [(eq, s_artnr)],"anf_best_dat": [(eq, anfdate)]})

            if l_besthis:
                t_anz =  to_decimal(l_besthis.anz_anf_best)

                if show_price:
                    t_val =  to_decimal(l_besthis.val_anf_best)

                str_list = Str_list()
                str_list_data.append(str_list)

                # str_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
                str_list.s = to_string("", "x(8)") + to_string(l_lager.lager_nr, "99") + " " + format_fixed_length(l_lager.bezeich, 13)
                str_list = Str_list()
                str_list_data.append(str_list)


                if show_price:
                    if not long_digit:
                        # str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(l_besthis.val_anf_best, "->>>,>>>,>>9.99"

                        if l_besthis.anz_anf_best >= 0:
                            tmp_anz_anf_best = format_fixed_length(to_string(l_besthis.anz_anf_best, ">>>,>>9.99"), 11)
                        else:
                            tmp_anz_anf_best = to_string(l_besthis.anz_anf_best, "->>>,>>9.99")

                        if l_besthis.val_anf_best >= 0:
                            tmp_val_anf_best = format_fixed_length(to_string(l_besthis.val_anf_best, ">>>,>>>,>>9.99"), 15)
                        else:
                            tmp_val_anf_best = to_string(l_besthis.val_anf_best, "->>>,>>>,>>9.99")

                        str_list.s = l_besthis.anf_best_dat.strftime("%d/%m/%y") + format_fixed_length("", 16) + tmp_anz_anf_best + tmp_val_anf_best
                    else:
                        # str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(l_besthis.val_anf_best, "->>,>>>,>>>,>>9")

                        if l_besthis.anz_anf_best >= 0:
                            tmp_anz_anf_best = format_fixed_length(to_string(l_besthis.anz_anf_best, ">>>,>>9.99"), 11)
                        else:
                            tmp_anz_anf_best = to_string(l_besthis.anz_anf_best, "->>>,>>9.99")

                        if l_besthis.val_anf_best >= 0:
                            tmp_val_anf_best = format_fixed_length(to_string(l_besthis.val_anf_best, ">>,>>>,>>>,>>9"), 15)
                        else:
                            tmp_val_anf_best = to_string(l_besthis.val_anf_best, "->>,>>>,>>>,>>9")

                        str_list.s = l_besthis.anf_best_dat.strftime("%d/%m/%y") + format_fixed_length("", 16) + tmp_anz_anf_best + tmp_val_anf_best
                else:
                    if not long_digit:
                        # str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99")
                        
                        if l_besthis.anz_anf_best >= 0:
                            tmp_anz_anf_best = format_fixed_length(to_string(l_besthis.anz_anf_best, ">>>,>>9.99"), 11)
                        else:
                            tmp_anz_anf_best = to_string(l_besthis.anz_anf_best, "->>>,>>9.99")

                        str_list.s = l_besthis.anf_best_dat.strftime("%d/%m/%y") + format_fixed_length("", 16) + tmp_anz_anf_best + format_fixed_length("0", 15)
                    else:
                        # str_list.s = to_string(l_besthis.anf_best_dat) + to_string(" ", "x(16)") + to_string(l_besthis.anz_anf_best, "->>>,>>9.99") + to_string(0, "->>,>>>,>>>,>>9")

                        if l_besthis.anz_anf_best >= 0:
                            tmp_anz_anf_best = format_fixed_length(to_string(l_besthis.anz_anf_best, ">>>,>>9.99"), 11)
                        else:
                            tmp_anz_anf_best = to_string(l_besthis.anz_anf_best, "->>>,>>9.99")

                        str_list.s = l_besthis.anf_best_dat.strftime("%d/%m/%y") + format_fixed_length("", 16) + tmp_anz_anf_best + format_fixed_length("0", 15)

            for l_ophis in db_session.query(L_ophis).filter(
                     (L_ophis.lager_nr == l_lager.lager_nr) & (L_ophis.artnr == s_artnr) & (L_ophis.datum >= anfdate) & (L_ophis.datum <= enddate) & (not_(matches(L_ophis.fibukonto,"*;CANCELLED*")))).order_by(L_ophis.datum, L_ophis.op_art).all():

                if show_price:
                    preis =  to_decimal(l_ophis.einzelpreis)
                    wert =  to_decimal(l_ophis.warenwert)

                if l_ophis.op_art == 1:
                    bemerk = ""

                    l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_ophis.lief_nr)]})

                    if l_lieferant:
                        bemerk = l_lieferant.firma
                    t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    add_id()

                    # str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                    if l_ophis.anzahl >= 0:
                        tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.99"), 13)
                    else:
                        tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.99")

                    if wert >= 0:
                        tmp_wert = format_fixed_length(to_string(wert, ">>,>>>,>>9.99"), 14)
                    else:
                        tmp_wert = to_string(wert, "->>,>>>,>>9.99")

                    str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(l_ophis.lscheinnr, 16) + format_fixed_length("0.00", 11) + format_fixed_length("0.00", 15) + tmp_anzahl + tmp_wert + format_fixed_length("0.00", 13) + format_fixed_length("0.00", 14) + format_fixed_length("0.00", 11) + format_fixed_length(bemerk, 16)


                elif l_ophis.op_art == 2:

                    l_op1 = get_cache (L_ophis, {"op_art": [(eq, 4)],"datum": [(eq, l_ophis.datum)],"artnr": [(eq, l_ophis.artnr)],"anzahl": [(eq, l_ophis.anzahl)],"lief_nr": [(eq, l_ophis.lager_nr)]})

                    if l_op1:
                        bemerk = translateExtended ("From", lvcarea, "") + " " + to_string(l_op1.lager_nr)
                    else:
                        bemerk = translateExtended ("Transferred", lvcarea, "")

                    t_anz =  to_decimal(t_anz) + to_decimal(l_ophis.anzahl)
                    t_val =  to_decimal(t_val) + to_decimal(wert)
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    add_id()

                    # str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                    if l_ophis.anzahl >= 0:
                        tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.99"), 13)
                    else:
                        tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.99")

                    if wert >= 0:
                        tmp_wert = format_fixed_length(to_string(wert, ">>,>>>,>>9.99"), 14)
                    else:
                        tmp_wert = to_string(wert, "->>,>>>,>>9.99")

                    str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(l_ophis.lscheinnr, 16) + format_fixed_length("0.00", 11) + format_fixed_length("0.00", 15) + tmp_anzahl + tmp_wert + format_fixed_length("0.00", 13) + format_fixed_length("0.00", 14) + format_fixed_length("0.00", 11) + format_fixed_length(bemerk, 16)


                elif l_ophis.op_art == 3:

                    if l_ophis.fibukonto != "":
                        gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophis.fibukonto)]})
                        
                    else:
                        l_ophhis = get_cache (L_ophhis, {"op_typ": [(eq, "stt")],"datum": [(eq, l_ophis.datum)],"lscheinnr": [(eq, l_ophis.lscheinnr)],"fibukonto": [(ne, "")]})

                        if l_ophhis:
                            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, l_ophhis.fibukonto)]})

                    bemerk = ""

                    if gl_acct:
                        bemerk = gl_acct.fibukonto

                    t_anz =  to_decimal(t_anz) - to_decimal(l_ophis.anzahl)
                    t_val =  to_decimal(t_val) - to_decimal(wert)
                    str_list = Str_list()
                    str_list_data.append(str_list)

                    add_id()

                    if not long_digit:
                        # str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                        if l_ophis.anzahl >= 0:
                            tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.99"), 13)
                        else:
                            tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.99")

                        if wert >= 0:
                            tmp_wert = format_fixed_length(to_string(wert, ">>,>>>,>>9.99"), 14)
                        else:
                            tmp_wert = to_string(wert, "->>,>>>,>>9.99")

                        str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(l_ophis.lscheinnr, 16) + format_fixed_length("0.00", 11) + format_fixed_length("0.00", 15) + format_fixed_length("0.00", 13) + format_fixed_length("0.00", 14) + tmp_anzahl + tmp_wert + format_fixed_length("0.00", 11) + format_fixed_length(bemerk, 16)
                    else:
                        # str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, " ->>>,>>>,>>9") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->,>>>,>>>,>>9") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->,>>>,>>>,>>9") + to_string(0, "->>,>>>,>>9") + to_string(bemerk, "x(16)")

                        if l_ophis.anzahl >= 0:
                            tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.99"), 13)
                        else:
                            tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.99")

                        if wert >= 0:
                            tmp_wert = format_fixed_length(to_string(wert, ">,>>>,>>>,>>9"), 14)
                        else:
                            tmp_wert = to_string(wert, "->,>>>,>>>,>>9")

                        str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(l_ophis.lscheinnr, 16) + format_fixed_length("0.00", 11) + format_fixed_length("0.00", 15) + format_fixed_length("0.00", 13) + format_fixed_length("0.00", 14) + tmp_anzahl + tmp_wert + format_fixed_length("0.00", 11) + format_fixed_length(bemerk, 16)

                elif l_ophis.op_art == 4:
                    bemerk = translateExtended ("To Store", lvcarea, "") + " " + to_string(l_ophis.lief_nr)
                    t_anz =  to_decimal(t_anz) - to_decimal(l_ophis.anzahl)
                    t_val =  to_decimal(t_val) - to_decimal(wert)

                    str_list = Str_list()
                    str_list_data.append(str_list)

                    add_id()
                    
                    # str_list.s = to_string(l_ophis.datum) + to_string(l_ophis.lscheinnr, "x(16)") + to_string(0, "->>>,>>9.99") + to_string(0, "->>>,>>>,>>9.99") + to_string(0, "->,>>>,>>9.99") + to_string(0, "->>,>>>,>>9.99") + to_string(l_ophis.anzahl, "->,>>>,>>9.99") + to_string(wert, "->>,>>>,>>9.99") + to_string(0, "->>>,>>9.99") + to_string(bemerk, "x(16)")

                    if l_ophis.anzahl >= 0:
                        tmp_anzahl = format_fixed_length(to_string(l_ophis.anzahl, ">,>>>,>>9.99"), 13)
                    else:
                        tmp_anzahl = to_string(l_ophis.anzahl, "->,>>>,>>9.99")

                    if wert >= 0:
                        tmp_wert = format_fixed_length(to_string(wert, ">>,>>>,>>9.99"), 14)
                    else:
                        tmp_wert = to_string(wert, "->>,>>>,>>9.99")

                    str_list.s = l_ophis.datum.strftime("%d/%m/%y") + format_fixed_length(l_ophis.lscheinnr, 16) + format_fixed_length("0.00", 11) + format_fixed_length("0.00", 15) + format_fixed_length("0.00", 13) + format_fixed_length("0.00", 14) + tmp_anzahl + tmp_wert + format_fixed_length("0.00", 11) + format_fixed_length(bemerk, 16)

            if l_besthis:
                tot_anz =  to_decimal(tot_anz) + to_decimal(t_anz)
                tot_val =  to_decimal(tot_val) + to_decimal(t_val)
                str_list = Str_list()
                str_list_data.append(str_list)

                if not long_digit:
                    # str_list.s = " " + to_string(translateExtended ("Stock Onhand:", lvcarea, "") , "x(16)") + to_string(t_anz, "->>>,>>9.99") + to_string(t_val, "->>>,>>>,>>9.99")

                    if t_anz >= 0:
                        tmp_t_anz = format_fixed_length(to_string(t_anz, ">>>,>>9.99"), 11)
                    else:
                        tmp_t_anz = to_string(t_anz, "->>>,>>9.99")

                    if t_val >= 0:
                        tmp_t_val = format_fixed_length(to_string(t_val, ">>>,>>>,>>9.99"), 15)
                    else:
                        tmp_t_val = to_string(t_val, "->>>,>>>,>>9.99")

                    str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("Stock Onhand:", lvcarea, "") , 16) + tmp_t_anz + tmp_t_val
                else:
                    # str_list.s = " " + to_string(translateExtended ("Stock Onhand:", lvcarea, "") , "x(16)") + to_string(t_anz, "->>>,>>9.99") + to_string(t_val, " ->>>,>>>,>>9")

                    if t_anz >= 0:
                        tmp_t_anz = format_fixed_length(to_string(t_anz, ">>>,>>9.99"), 11)
                    else:
                        tmp_t_anz = to_string(t_anz, "->>>,>>9.99")

                    if t_val >= 0:
                        tmp_t_val = format_fixed_length(to_string(t_val, ">>>,>>>,>>9.99"), 15)
                    else:
                        tmp_t_val = to_string(t_val, "->>>,>>>,>>9.99")

                    str_list.s = to_string("", "x(8)") + format_fixed_length(translateExtended ("Stock Onhand:", lvcarea, "") , 16) + tmp_t_anz + tmp_t_val

                str_list = Str_list()
                str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        str_list = Str_list()
        str_list_data.append(str_list)

        # str_list.s = " " + "T O T A L : " + to_string(t_qty, "->>>,>>9.99") + to_string(t_wert, "->>>,>>>,>>9.99")

        if t_qty >= 0:
            tmp_t_qty = format_fixed_length(to_string(t_qty, ">>>,>>9.99"), 11)
        else:
            tmp_t_qty = to_string(t_qty, "->>>,>>9.99")

        if t_wert >= 0:
            tmp_t_wert = format_fixed_length(to_string(t_wert, ">>>,>>>,>>9.99"), 15)
        else:
            tmp_t_wert = to_string(t_wert, "->>>,>>>,>>9.99")

        str_list.s = to_string("", "x(8)") + "T O T A L : " + tmp_t_qty + tmp_t_wert


    def add_id():

        nonlocal anfdate, enddate, str_list_data, lvcarea, tot_anz, tot_val, t_anz, t_val, long_digit, htparam, bediener, l_ophis, l_besthis, l_lager, l_lieferant, gl_acct, l_ophhis
        nonlocal pvilanguage, s_artnr, mm, yy, from_lager, to_lager, show_price


        nonlocal str_list
        nonlocal str_list_data

        usr = None
        Usr =  create_buffer("Usr",Bediener)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    create_list()

    return generate_output()