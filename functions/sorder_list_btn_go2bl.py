#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, L_orderhdr, L_lieferant, L_artikel, L_order, Parameters

def sorder_list_btn_go2bl(user_init:string, sorttype:int, s_artnr:int, from_date:date, to_date:date, from_sup:string, to_sup:string, closepo:bool):

    prepare_cache ([Htparam, Bediener, L_orderhdr, L_lieferant, L_artikel, L_order, Parameters])

    po_list_data = []
    delidate:date = None
    amount1:Decimal = to_decimal("0.0")
    amount2:Decimal = to_decimal("0.0")
    long_digit:bool = False
    show_price:bool = False
    price_decimal:int = 0
    htparam = bediener = l_orderhdr = l_lieferant = l_artikel = l_order = parameters = None

    str_list = str_list2 = po_list = cost_list = None

    str_list_data, Str_list = create_model("Str_list", {"docu_nr":string, "s":string, "dunit":string, "content":int, "lief_nr":int, "warenwert":Decimal})
    str_list2_data, Str_list2 = create_model("Str_list2", {"docu_nr":string, "l_order_bestelldatum":string, "l_order_docu_nr":string, "l_order_artnr":string, "l_artikel_bezeich":string, "l_order_anzahl":string, "l_order_preis":string, "l_order_warenwert":string, "l_order_geliefert":string, "l_order_angebot_lief1":string, "l_order_rechnungswert":string, "l_orderhdr_lieferdatum":string, "l_lieferant_firma":string, "cost_list_bezeich":string, "dunit":string, "content":int, "lief_nr":int, "warenwert":Decimal})
    po_list_data, Po_list = create_model("Po_list", {"datum":date, "document_no":string, "artno":int, "artdesc":string, "orderqty":int, "unit_price":Decimal, "amount1":Decimal, "delivered":int, "s_unit":int, "amount2":Decimal, "delivdate":date, "supplier":string})
    cost_list_data, Cost_list = create_model("Cost_list", {"nr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

        return {"po-list": po_list_data}

    def sorder_list_btn_gobl(user_init:string, sorttype:int, s_artnr:int, from_date:date, to_date:date, from_sup:string, to_sup:string, closepo:bool):

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

        def generate_inner_output():
            return (str_list2_data)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
        price_decimal = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
        long_digit = htparam.flogical

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:

            if substring(bediener.permissions, 21, 1) != ("0").lower() :
                show_price = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 43)]})

        if htparam:
            show_price = htparam.flogical
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

        return generate_inner_output()


    def create_list1():

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            str_list2_data.clear()
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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)

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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")
                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)


    def create_list11():

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)

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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)


    def create_list2():

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            str_list2_data.clear()
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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.lief_nr = l_order.lief_nr
                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.warenwer =  to_decimal(l_order.warenwert)
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)

        elif closepo :
            str_list_data.clear()
            str_list2_data.clear()
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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.lief_nr = l_order.lief_nr
                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.warenwert =  to_decimal(l_order.warenwert)
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)


    def create_list22():

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            str_list2_data.clear()
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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.lief_nr = l_order.lief_nr
                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.warenwert =  to_decimal(l_order.warenwert)
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)

        elif closepo :
            str_list_data.clear()
            str_list2_data.clear()
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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.lief_nr = l_order.lief_nr
                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.warenwert =  to_decimal(l_order.warenwert)
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)


    def create_list3():

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

        i:int = 0

        if closepo == False:
            str_list_data.clear()
            str_list2_data.clear()
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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "
            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)

        elif closepo :
            str_list_data.clear()
            str_list2_data.clear()
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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")


                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")
                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)


    def create_list33():

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)

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


                str_list2 = Str_list2()
                str_list2_data.append(str_list2)

                str_list2.docu_nr = l_order.docu_nr
                str_list2.dunit = l_order.lief_fax[2]
                str_list2.content = l_order.txtnr
                str_list2.l_order_bestelldatum = to_string(l_order.bestelldatum)
                str_list2.l_order_docu_nr = to_string(l_order.docu_nr)
                str_list2.l_order_artnr = to_string(l_order.artnr)
                str_list2.l_artikel_bezeich = to_string(l_artikel.bezeich)
                str_list2.l_order_anzahl = to_string(l_order.anzahl)

                if not long_digit:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">>>,>>>,>>9.99")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">>,>>>,>>9.99")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">>>,>>>,>>9.99")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)


                else:

                    if show_price:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(l_order.einzelpreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.einzelpreis)


                        else:
                            str_list.s = str_list.s + to_string(l_order.rechnungspreis, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(l_order.rechnungspreis)


                        str_list.s = str_list.s + to_string(l_order.warenwert, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(l_order.rechnungswert, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(l_order.warenwert)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(l_order.rechnungswert)


                    else:

                        if l_order.geliefert == 0:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        else:
                            str_list.s = str_list.s + to_string(0, ">,>>>,>>>,>>9")


                            str_list2.l_order_preis = to_string(0)


                        str_list.s = str_list.s + to_string(0, ">,>>>>,>>>,>>9")
                        str_list.s = str_list.s + to_string(l_order.geliefert, "->>>,>>9.99") + to_string(l_order.angebot_lief[0], ">>9")
                        str_list.s = str_list.s + to_string(0, ">>,>>>,>>>,>>9")


                        str_list2.l_order_warenwert = to_string(0)
                        str_list2.l_order_geliefert = to_string(l_order.geliefert)
                        str_list2.l_order_angebot_lief1 = to_string(l_order.angebot_lief[0])
                        str_list2.l_order_rechnungswert = to_string(0)

                if l_orderhdr.lieferdatum != None:
                    str_list.s = str_list.s + to_string(l_orderhdr.lieferdatum) + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string(l_orderhdr.lieferdatum)
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                else:
                    str_list.s = str_list.s + " " + to_string(l_lieferant.firma, "x(16)")


                    str_list2.l_orderhdr_lieferdatum = to_string("")
                    str_list2.l_lieferant_firma = to_string(l_lieferant.firma)


                str_list.s = str_list.s + to_string(cost_list.bezeich)


                str_list2.cost_list_bezeich = to_string(cost_list.bezeich)

                if show_price:
                    amount1 =  to_decimal(amount1) + to_decimal(l_order.warenwert)
                    amount2 =  to_decimal(amount2) + to_decimal(l_order.rechnungswert)
                tot_anz =  to_decimal(tot_anz) + to_decimal(l_order.anzahl)
            str_list = Str_list()
            str_list_data.append(str_list)

            for i in range(1,67 + 1) :
                str_list.s = str_list.s + " "


            str_list2 = Str_list2()
            str_list2_data.append(str_list2)

            str_list2.l_order_bestelldatum = to_string("")
            str_list2.l_order_docu_nr = to_string("")
            str_list2.l_order_artnr = to_string("")
            str_list2.l_artikel_bezeich = to_string("")
            str_list2.l_order_anzahl = to_string("")


            str_list.s = str_list.s + to_string("T O T A L", "x(10)")


            str_list2.l_order_preis = to_string("T O T A L", "x(10)")

            if not long_digit:
                str_list.s = str_list.s + to_string(amount1, ">>,>>>,>>>,>>9.99")


                str_list2.l_order_warenwert = to_string(amount1)


            else:
                str_list.s = str_list.s + to_string(amount1, ">,>>>,>>>,>>>,>>9")


                str_list2.l_order_warenwert = to_string(amount1)


    def create_costlist():

        nonlocal po_list_data, delidate, amount1, amount2, long_digit, show_price, price_decimal, htparam, bediener, l_orderhdr, l_lieferant, l_artikel, l_order, parameters
        nonlocal user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo


        nonlocal str_list, str_list2, po_list, cost_list
        nonlocal str_list_data, str_list2_data, po_list_data, cost_list_data

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("CostCenter").lower()) & (Parameters.section == ("Name").lower()) & (Parameters.varname > "")).order_by(Parameters._recid).all():
            cost_list = Cost_list()
            cost_list_data.append(cost_list)

            cost_list.nr = to_int(parameters.varname)
            cost_list.bezeich = parameters.vstring


    str_list2_data = sorder_list_btn_gobl(user_init, sorttype, s_artnr, from_date, to_date, from_sup, to_sup, closepo)
    po_list_data.clear()

    for str_list2 in query(str_list2_data):

        if matches(str_list2.l_order_preis,r"*T O T A L*"):
            po_list = Po_list()
            po_list_data.append(po_list)

            po_list.artdesc = "T O T A L"
            po_list.amount1 =  to_decimal(to_decimal(str_list2.l_order_warenwert) )


        else:
            po_list = Po_list()
            po_list_data.append(po_list)

            po_list.datum = date_mdy(str_list2.l_order_bestelldatum)
            po_list.document_no = str_list2.l_order_docu_nr
            po_list.artno = to_int(str_list2.l_order_artnr)
            po_list.artdesc = str_list2.l_artikel_bezeich
            po_list.orderqty = to_int(str_list2.l_order_anzahl)
            po_list.unit_price =  to_decimal(to_decimal(str_list2.l_order_preis) )
            po_list.amount1 =  to_decimal(to_decimal(str_list2.l_order_warenwert) )
            po_list.delivered = to_int(str_list2.l_order_geliefert)
            po_list.s_unit = to_int(str_list2.l_order_angebot_lief1)
            po_list.amount2 =  to_decimal(to_decimal(str_list2.l_order_rechnungswert) )
            po_list.delivdate = date_mdy(str_list2.l_orderhdr_lieferdatum)
            po_list.supplier = str_list2.l_lieferant_firma

    return generate_output()