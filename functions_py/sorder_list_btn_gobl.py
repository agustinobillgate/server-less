#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, L_orderhdr, L_lieferant, L_artikel, L_order, Parameters

def sorder_list_btn_gobl(user_init:string, sorttype:int, s_artnr:int, from_date:date, to_date:date, from_sup:string, to_sup:string, closepo:bool):

    prepare_cache ([Htparam, Bediener, L_orderhdr, L_lieferant, L_order, Parameters])

    str_list_data = []
    amount1:Decimal = to_decimal("0.0")
    amount2:Decimal = to_decimal("0.0")
    long_digit:bool = False
    show_price:bool = False
    price_decimal:int = 0
    htparam = bediener = l_orderhdr = l_lieferant = l_artikel = l_order = parameters = None

    str_list = cost_list = None

    str_list_data, Str_list = create_model("Str_list", {"docu_nr":string, "s":string, "dunit":string, "content":int, "lief_nr":int, "warenwert":Decimal})
    cost_list_data, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})
    
    set_cache(Htparam, None, [["paramnr"]], True, [], ["paramnr"])
    set_cache(Bediener, None, [["userinit"]], True, [], ["userinit"])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        return {"str-list": str_list_data}

    def create_list1():

        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(L_order.docu_nr, L_order.pos).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_order.pos > 0) & (L_order.loeschflag == 1) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(L_order.docu_nr, L_order.pos).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


    def create_list11():

        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        i:int = 0
        tot_anz:Decimal = to_decimal("0.0")

        if closepo == False:
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).filter(
                     (L_order.artnr == s_artnr) & (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(L_order.bestelldatum, L_order.docu_nr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).filter(
                     (L_order.artnr == s_artnr) & (L_order.pos > 0) & (L_order.loeschflag == 1) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(L_order.bestelldatum, L_order.docu_nr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


    def create_list2():

        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_orderhdr_obj_list = {}
            for l_orderhdr, l_order, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order.betriebsnr == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_orderhdr.lieferdatum >= from_date) & (L_orderhdr.lieferdatum <= to_date)).order_by(L_orderhdr.lieferdatum, L_lieferant.firma, L_order.artnr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_orderhdr_obj_list.get(l_orderhdr._recid):
                    continue
                else:
                    l_orderhdr_obj_list[l_orderhdr._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert =  to_decimal(l_order.warenwert)
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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_orderhdr_obj_list = {}
            for l_orderhdr, l_order, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.loeschflag == 1) & (L_order.betriebsnr == 0)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_orderhdr.lieferdatum >= from_date) & (L_orderhdr.lieferdatum <= to_date)).order_by(L_lieferant.firma, L_orderhdr.lieferdatum, L_order.artnr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_orderhdr_obj_list.get(l_orderhdr._recid):
                    continue
                else:
                    l_orderhdr_obj_list[l_orderhdr._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert =  to_decimal(l_order.warenwert)
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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


    def create_list22():

        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_orderhdr_obj_list = {}
            for l_orderhdr, l_order, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order.betriebsnr == 0) & (L_order.artnr == s_artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_orderhdr.lieferdatum >= from_date) & (L_orderhdr.lieferdatum <= to_date)).order_by(L_lieferant.firma, L_orderhdr.lieferdatum).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_orderhdr_obj_list.get(l_orderhdr._recid):
                    continue
                else:
                    l_orderhdr_obj_list[l_orderhdr._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert =  to_decimal(l_order.warenwert)
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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_orderhdr_obj_list = {}
            for l_orderhdr, l_order, l_lieferant, l_artikel in db_session.query(L_orderhdr, L_order, L_lieferant, L_artikel).join(L_order,(L_order.docu_nr == L_orderhdr.docu_nr) & (L_order.pos > 0) & (L_order.loeschflag == 1) & (L_order.betriebsnr == 0) & (L_order.artnr == s_artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_orderhdr.lieferdatum >= from_date) & (L_orderhdr.lieferdatum <= to_date)).order_by(L_lieferant.firma, L_orderhdr.lieferdatum).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_orderhdr_obj_list.get(l_orderhdr._recid):
                    continue
                else:
                    l_orderhdr_obj_list[l_orderhdr._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

                str_list.lief_nr = l_order.lief_nr
                str_list.docu_nr = l_order.docu_nr
                str_list.dunit = l_order.lief_fax[2]
                str_list.content = l_order.txtnr
                str_list.warenwert =  to_decimal(l_order.warenwert)
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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


    def create_list3():

        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(cost_list.nr, L_orderhdr.bestelldatum, L_order.docu_nr, L_lieferant.firma, L_order.artnr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            str_list_data.clear()
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_lieferant, l_artikel in db_session.query(L_order, L_orderhdr, L_lieferant, L_artikel).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_lieferant,(L_lieferant.lief_nr == L_order.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).join(L_artikel,(L_artikel.artnr == L_order.artnr)).filter(
                     (L_order.pos > 0) & (L_order.loeschflag == 1) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(cost_list.nr, L_orderhdr.bestelldatum, L_order.docu_nr, L_lieferant.firma, L_order.artnr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


    def create_list33():

        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        i:int = 0
        tot_anz:Decimal = to_decimal("0.0")

        if closepo == False:
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).filter(
                     (L_order.artnr == s_artnr) & (L_order.pos > 0) & (L_order.loeschflag == 0) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(cost_list.nr, L_orderhdr.bestelldatum, L_order.docu_nr, L_lieferant.firma, L_order.artnr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")

        elif closepo :
            amount1 =  to_decimal("0")
            amount2 =  to_decimal("0")

            l_order_obj_list = {}
            for l_order, l_orderhdr, l_artikel, l_lieferant in db_session.query(L_order, L_orderhdr, L_artikel, L_lieferant).join(L_orderhdr,(L_orderhdr.lief_nr == L_order.lief_nr) & (L_orderhdr.docu_nr == L_order.docu_nr)).join(L_artikel,(L_artikel.artnr == L_order.artnr)).join(L_lieferant,(L_lieferant.lief_nr == L_orderhdr.lief_nr) & (L_lieferant.firma >= (from_sup).lower()) & (L_lieferant.firma <= (to_sup).lower())).filter(
                     (L_order.artnr == s_artnr) & (L_order.pos > 0) & (L_order.loeschflag == 1) & (L_order.bestelldatum >= from_date) & (L_order.bestelldatum <= to_date) & (L_order.betriebsnr == 0)).order_by(cost_list.nr, L_orderhdr.bestelldatum, L_order.docu_nr, L_lieferant.firma, L_order.artnr).all():
                cost_list = query(cost_list_data, (lambda cost_list: cost_list.nr == l_orderhdr.angebot_lief[0]), first=True)
                if not cost_list:
                    continue

                if l_order_obj_list.get(l_order._recid):
                    continue
                else:
                    l_order_obj_list[l_order._recid] = True


                str_list = Str_list()
                str_list_data.append(str_list)

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
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")
                str_list.s = str_list.s + to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list.s = str_list.s + to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")
            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


    def create_costlist():

        nonlocal str_list_data, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, cost_list
        nonlocal str_list_data, cost_list_data

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_data.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})
    show_price = htparam.flogical

    if substring(bediener.permissions, 21, 1) != ("0").lower() :
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