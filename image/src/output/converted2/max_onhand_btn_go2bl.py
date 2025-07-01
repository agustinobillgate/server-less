#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_lager, L_artikel, L_bestand, L_pprice

def max_onhand_btn_go2bl(sorttype:int, main_grp:int, from_store3:int, to_store3:int, show_price:bool):

    prepare_cache ([Htparam, L_lager, L_artikel, L_bestand, L_pprice])

    max_onhand_list_list = []
    long_digit:bool = False
    htparam = l_lager = l_artikel = l_bestand = l_pprice = None

    max_onhand_list = None

    max_onhand_list_list, Max_onhand_list = create_model("Max_onhand_list", {"artnr":int, "name":string, "max_oh":Decimal, "curr_oh":Decimal, "avrgprice":Decimal, "ek_aktuell":Decimal, "datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal max_onhand_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal max_onhand_list
        nonlocal max_onhand_list_list

        return {"max-onhand-list": max_onhand_list_list}

    def create_list():

        nonlocal max_onhand_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal max_onhand_list
        nonlocal max_onhand_list_list

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:Decimal = to_decimal("0.0")
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        max_onhand_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_store3) & (L_lager.lager_nr <= to_store3)).order_by(L_lager._recid).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2) & (L_artikel.anzverbrauch > 0)).order_by(L_artikel.artnr).all():
                curr_best =  to_decimal("0")

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, l_lager.lager_nr)]})

                if l_bestand:
                    curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if curr_best > l_artikel.anzverbrauch:
                        i = i + 1

                        if i == 1:
                            max_onhand_list = Max_onhand_list()
                            max_onhand_list_list.append(max_onhand_list)

                            max_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")


                        max_onhand_list = Max_onhand_list()
                        max_onhand_list_list.append(max_onhand_list)

                        max_onhand_list.artnr = l_artikel.artnr


                        max_onhand_list.name = l_artikel.bezeich


                        max_onhand_list.max_oh =  to_decimal(l_artikel.anzverbrauch)


                        max_onhand_list.curr_oh =  to_decimal(curr_best)


                        max_onhand_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                        max_onhand_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)

                        if l_artikel.lieferfrist > 0:

                            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_artikel.artnr)],"counter": [(eq, l_artikel.lieferfrist)]})

                            if l_pprice:
                                max_onhand_list.datum = l_pprice.bestelldatum


    def create_list2():

        nonlocal max_onhand_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal max_onhand_list
        nonlocal max_onhand_list_list

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:Decimal = to_decimal("0.0")
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        max_onhand_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_store3) & (L_lager.lager_nr <= to_store3)).order_by(L_lager._recid).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2) & (L_artikel.anzverbrauch > 0)).order_by(L_artikel.bezeich).all():
                curr_best =  to_decimal("0")

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, l_lager.lager_nr)]})

                if l_bestand:
                    curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if curr_best > l_artikel.anzverbrauch:
                        i = i + 1

                        if i == 1:
                            max_onhand_list = Max_onhand_list()
                            max_onhand_list_list.append(max_onhand_list)

                            max_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")


                        max_onhand_list = Max_onhand_list()
                        max_onhand_list_list.append(max_onhand_list)

                        max_onhand_list.artnr = l_artikel.artnr


                        max_onhand_list.name = l_artikel.bezeich


                        max_onhand_list.max_oh =  to_decimal(l_artikel.anzverbrauch)


                        max_onhand_list.curr_oh =  to_decimal(curr_best)


                        max_onhand_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                        max_onhand_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)

                        if l_artikel.lieferfrist > 0:

                            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_artikel.artnr)],"counter": [(eq, l_artikel.lieferfrist)]})

                            if l_pprice:
                                max_onhand_list.datum = l_pprice.bestelldatum


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    if sorttype == 1:
        create_list()
    else:
        create_list2()

    return generate_output()