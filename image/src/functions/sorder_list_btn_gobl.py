from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Bediener, L_orderhdr, L_lieferant, L_artikel, L_order, Parameters

def sorder_list_btn_gobl(user_init:str, sorttype:int, s_artnr:int, from_date:date, to_date:date, from_sup:str, to_sup:str, closepo:bool):
    str_list_list = []
    amount1:decimal = 0
    amount2:decimal = 0
    long_digit:bool = False
    show_price:bool = False
    price_decimal:int = 0
    htparam = bediener = l_orderhdr = l_lieferant = l_artikel = l_order = parameters = None

    str_list = cost_list = None

    str_list_list, Str_list = create_model("Str_list", {"docu_nr":str, "s":str, "dunit":str, "content":int, "lief_nr":int, "warenwert":decimal})
    cost_list_list, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list
        return {"str-list": str_list_list}

    def create_list1():

        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        i:int = 0

        if closepo == False:
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, Cost_list, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                    (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, Cost_list, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                    (L_order.pos > 0) &  (L_order.loeschflag == 1) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

    def create_list11():

        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        i:int = 0
        tot_anz:decimal = 0

        if closepo == False:
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, Cost_list, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).filter(
                    (L_order.artnr == s_artnr) &  (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
                tot_anz = tot_anz + l_order.anzahl
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, Cost_list, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).filter(
                    (L_order.artnr == s_artnr) &  (L_order.pos > 0) &  (L_order.loeschflag == 1) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
                tot_anz = tot_anz + l_order.anzahl
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

    def create_list2():

        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        i:int = 0

        if closepo == False:
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_orderhdr_obj_list = []
            for l_orderhdr, l_order, cost_list, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, Cost_list, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) &  (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (L_order.betriebsnr == 0)).join(Cost_list,(Cost_list.nr == L_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == l_order.artnr)).filter(
                    (L_orderhdr.lieferdatum >= from_date) &  (L_orderhdr.lieferdatum <= to_date)).all():
                if l_orderhdr._recid in l_orderhdr_obj_list:
                    continue
                else:
                    l_orderhdr_obj_list.append(l_orderhdr._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert = l_order.warenwert
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_orderhdr_obj_list = []
            for l_orderhdr, l_order, cost_list, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, Cost_list, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) &  (L_order.pos > 0) &  (L_order.loeschflag == 1) &  (L_order.betriebsnr == 0)).join(Cost_list,(Cost_list.nr == L_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == l_order.artnr)).filter(
                    (L_orderhdr.lieferdatum >= from_date) &  (L_orderhdr.lieferdatum <= to_date)).all():
                if l_orderhdr._recid in l_orderhdr_obj_list:
                    continue
                else:
                    l_orderhdr_obj_list.append(l_orderhdr._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert = l_order.warenwert
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

    def create_list22():

        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        i:int = 0

        if closepo == False:
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_orderhdr_obj_list = []
            for l_orderhdr, l_order, cost_list, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, Cost_list, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) &  (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (L_order.betriebsnr == 0) &  (L_order.artnr == s_artnr)).join(Cost_list,(Cost_list.nr == L_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == l_order.artnr)).filter(
                    (L_orderhdr.lieferdatum >= from_date) &  (L_orderhdr.lieferdatum <= to_date)).all():
                if l_orderhdr._recid in l_orderhdr_obj_list:
                    continue
                else:
                    l_orderhdr_obj_list.append(l_orderhdr._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert = l_order.warenwert
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_orderhdr_obj_list = []
            for l_orderhdr, l_order, cost_list, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, Cost_list, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) &  (L_order.pos > 0) &  (L_order.loeschflag == 1) &  (L_order.betriebsnr == 0) &  (L_order.artnr == s_artnr)).join(Cost_list,(Cost_list.nr == L_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == l_order.artnr)).filter(
                    (L_orderhdr.lieferdatum >= from_date) &  (L_orderhdr.lieferdatum <= to_date)).all():
                if l_orderhdr._recid in l_orderhdr_obj_list:
                    continue
                else:
                    l_orderhdr_obj_list.append(l_orderhdr._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert = l_order.warenwert
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

    def create_list3():

        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        i:int = 0

        if closepo == False:
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, Cost_list, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                    (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_list.clear()
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, Cost_list, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                    (L_order.pos > 0) &  (L_order.loeschflag == 1) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

    def create_list33():

        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        i:int = 0
        tot_anz:decimal = 0

        if closepo == False:
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, Cost_list, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).filter(
                    (L_order.artnr == s_artnr) &  (L_order.pos > 0) &  (L_order.loeschflag == 0) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
                tot_anz = tot_anz + l_order.anzahl
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            amount1 = 0
            amount2 = 0

            l_order_obj_list = []
            for l_order, l_orderhdr, cost_list, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, Cost_list, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) &  (L_orderhdr.docu_nr == L_order.docu_nr)).join(Cost_list,(Cost_list.nr == l_orderhdr.angebot_lief[0])).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == l_orderhdr.lief_nr) &  (func.lower(L_lieferant.firma) >= (from_sup).lower()) &  (func.lower(L_lieferant.firma) <= (to_sup).lower())).filter(
                    (L_order.artnr == s_artnr) &  (L_order.pos > 0) &  (L_order.loeschflag == 1) &  (L_order.bestelldatum >= from_date) &  (L_order.bestelldatum <= to_date) &  (L_order.betriebsnr == 0)).all():
                if l_order._recid in l_order_obj_list:
                    continue
                else:
                    l_order_obj_list.append(l_order._recid)


                str_list = Str_list()
                str_list_list.append(str_list)

                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.s = to_string(l_order.bestelldatum) +\
                        to_string(l_order.docu_nr, "x(12)") +\
                        to_string(l_order.artnr, "9999999") +\
                        to_string(l_artikel.bezeich, "x(30)") +\
                        to_string(l_order.anzahl, ">>>,>>9.99")

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")
                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")
                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")
                else:
                    str_list.s = str_list.s + "        " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 = amount1 + l_order.warenwert
                    amount2 = amount2 + l_order.rechnungswert
                tot_anz = tot_anz + l_order.anzahl
            str_list = Str_list()
            str_list_list.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

    def create_costlist():

        nonlocal str_list_list, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters


        nonlocal str_list, cost_list
        nonlocal str_list_list, cost_list_list

        for parameters in db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "CostCenter") &  (func.lower(Parameters.section) == "Name") &  (Parameters.varname > "")).all():
            cost_list = Cost_list()
            cost_list_list.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 43)).first()
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != "0":
        show_price = True
    create_costlist()

    if sorttype == 1:

        if s_artnr == 0:
            create_list1()
        else:
            create_list11()

    elif sorttype == 2:

        if s_artnr == 0:
            create_list2()
        else:
            create_list22()

    elif sorttype == 3:

        if s_artnr == 0:
            create_list3()
        else:
            create_list33()

    return generate_output()