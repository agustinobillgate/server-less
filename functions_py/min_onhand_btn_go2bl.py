#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_lager, L_artikel, L_bestand, L_pprice

def min_onhand_btn_go2bl(sorttype:int, main_grp:int, from_store3:int, to_store3:int, show_price:bool):

    prepare_cache ([Htparam, L_lager, L_artikel, L_bestand, L_pprice])

    min_onhand_list_data = []
    long_digit:bool = False
    htparam = l_lager = l_artikel = l_bestand = l_pprice = None

    min_onhand_list = None

    min_onhand_list_data, Min_onhand_list = create_model("Min_onhand_list", {"artnr":int, "name":string, "min_oh":Decimal, "curr_oh":Decimal, "avrgprice":Decimal, "ek_aktuell":Decimal, "datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal min_onhand_list_data, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal min_onhand_list
        nonlocal min_onhand_list_data

        return {"min-onhand-list": min_onhand_list_data}

    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

    def create_list():

        nonlocal min_onhand_list_data, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal min_onhand_list
        nonlocal min_onhand_list_data

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:Decimal = to_decimal("0.0")
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        min_onhand_list_data.clear()

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_store3) & (L_lager.lager_nr <= to_store3)).order_by(L_lager._recid).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2) & (L_artikel.min_bestand > 0)).order_by(L_artikel.artnr).all():
                curr_best =  to_decimal("0")

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, l_lager.lager_nr)]})

                if l_bestand:
                    curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if curr_best < l_artikel.min_bestand:
                        i = i + 1

                        if i == 1:
                            min_onhand_list = Min_onhand_list()
                            min_onhand_list_data.append(min_onhand_list)

                            # min_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
                            min_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + format_fixed_length(l_lager.bezeich, 13)


                        min_onhand_list = Min_onhand_list()
                        min_onhand_list_data.append(min_onhand_list)

                        min_onhand_list.artnr = l_artikel.artnr
                        min_onhand_list.name = l_artikel.bezeich
                        min_onhand_list.min_oh =  to_decimal(l_artikel.min_bestand)
                        min_onhand_list.curr_oh =  to_decimal(curr_best)


                        min_onhand_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                        min_onhand_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)

                        if l_artikel.lieferfrist > 0:

                            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_artikel.artnr)],"counter": [(eq, l_artikel.lieferfrist)]})

                            if l_pprice:
                                min_onhand_list.datum = l_pprice.bestelldatum


    def create_list2():

        nonlocal min_onhand_list_data, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal min_onhand_list
        nonlocal min_onhand_list_data

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:Decimal = to_decimal("0.0")
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        min_onhand_list_data.clear()

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_store3) & (L_lager.lager_nr <= to_store3)).order_by(L_lager._recid).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2) & (L_artikel.min_bestand > 0)).order_by(L_artikel.bezeich).all():
                curr_best =  to_decimal("0")

                l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, l_lager.lager_nr)]})

                if l_bestand:
                    curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if curr_best < l_artikel.min_bestand:
                        i = i + 1

                        if i == 1:
                            min_onhand_list = Min_onhand_list()
                            min_onhand_list_data.append(min_onhand_list)

                            # min_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
                            min_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + format_fixed_length(l_lager.bezeich, 13)


                        min_onhand_list = Min_onhand_list()
                        min_onhand_list_data.append(min_onhand_list)

                        min_onhand_list.artnr = l_artikel.artnr
                        min_onhand_list.name = l_artikel.bezeich
                        min_onhand_list.min_oh =  to_decimal(l_artikel.min_bestand)
                        min_onhand_list.curr_oh =  to_decimal(curr_best)


                        min_onhand_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                        min_onhand_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)

                        if l_artikel.lieferfrist > 0:

                            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_artikel.artnr)],"counter": [(eq, l_artikel.lieferfrist)]})

                            if l_pprice:
                                min_onhand_list.datum = l_pprice.bestelldatum


    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    if sorttype == 1:
        create_list()
    else:
        create_list2()

    return generate_output()