#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_artikel, L_bestand, L_op, L_ophis, L_pprice

def slow_moving_btn_gobl(storeno:int, main_grp:int, tage:int, show_price:bool):

    prepare_cache ([Htparam, L_artikel, L_bestand, L_pprice])

    s_list_data = []
    htparam = l_artikel = l_bestand = l_op = l_ophis = l_pprice = None

    s_list = None

    s_list_data, S_list = create_model("S_list", {"artnr":int, "name":string, "min_oh":Decimal, "curr_oh":Decimal, "avrgprice":Decimal, "ek_aktuell":Decimal, "datum":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data, htparam, l_artikel, l_bestand, l_op, l_ophis, l_pprice
        nonlocal storeno, main_grp, tage, show_price


        nonlocal s_list
        nonlocal s_list_data

        return {"s-list": s_list_data}

    def create_list1():

        nonlocal s_list_data, htparam, l_artikel, l_bestand, l_op, l_ophis, l_pprice
        nonlocal storeno, main_grp, tage, show_price


        nonlocal s_list
        nonlocal s_list_data

        n1:int = 0
        n2:int = 0
        curr_best:Decimal = to_decimal("0.0")
        transdate:date = None
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        transdate = htparam.fdate
        s_list_data.clear()

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2)).order_by(L_artikel.artnr).all():
            curr_best =  to_decimal("0")

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, storeno)]})

            if l_bestand:
                curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if curr_best > 0:

                l_op = get_cache (L_op, {"op_art": [(eq, 3)],"loeschflag": [(le, 1)],"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, storeno)]})

                if not l_op:

                    l_op = get_cache (L_op, {"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, storeno)]})

                if not l_op:

                    l_ophis = get_cache (L_ophis, {"artnr": [(eq, l_artikel.artnr)],"op_art": [(eq, 3)],"datum": [(ge, (transdate - tage))],"lager_nr": [(eq, storeno)]})

                    if not l_ophis:

                        l_ophis = get_cache (L_ophis, {"artnr": [(eq, l_artikel.artnr)],"op_art": [(eq, 1)],"datum": [(ge, (transdate - tage))],"lager_nr": [(eq, storeno)]})

                    if not l_ophis:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.name = l_artikel.bezeich
                        s_list.min_oh =  to_decimal(l)artikel.min_bestand
                        s_list.curr_oh =  to_decimal(curr_best)

                        if show_price:
                            s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                            s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)

                        if l_artikel.lieferfrist > 0:

                            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_artikel.artnr)],"counter": [(eq, l_artikel.lieferfrist)]})

                            if l_pprice:
                                s_list.datum = l_pprice.bestelldatum


    def create_list():

        nonlocal s_list_data, htparam, l_artikel, l_bestand, l_op, l_ophis, l_pprice
        nonlocal storeno, main_grp, tage, show_price


        nonlocal s_list
        nonlocal s_list_data

        n1:int = 0
        n2:int = 0
        curr_best:Decimal = to_decimal("0.0")
        transdate:date = None
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        transdate = htparam.fdate
        s_list_data.clear()

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2)).order_by(L_artikel.artnr).all():
            curr_best =  to_decimal("0")

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if curr_best > 0:

                l_op = get_cache (L_op, {"op_art": [(eq, 3)],"loeschflag": [(le, 1)],"artnr": [(eq, l_artikel.artnr)]})

                if not l_op:

                    l_op = get_cache (L_op, {"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"artnr": [(eq, l_artikel.artnr)]})

                if not l_op:

                    l_ophis = get_cache (L_ophis, {"artnr": [(eq, l_artikel.artnr)],"op_art": [(eq, 3)],"datum": [(ge, (transdate - tage))]})

                    if not l_ophis:

                        l_ophis = get_cache (L_ophis, {"artnr": [(eq, l_artikel.artnr)],"op_art": [(eq, 1)],"datum": [(ge, (transdate - tage))]})

                    if not l_ophis:
                        s_list = S_list()
                        s_list_data.append(s_list)

                        s_list.artnr = l_artikel.artnr
                        s_list.name = l_artikel.bezeich
                        s_list.min_oh =  to_decimal(l)artikel.min_bestand
                        s_list.curr_oh =  to_decimal(curr_best)

                        if show_price:
                            s_list.avrgprice =  to_decimal(l_artikel.vk_preis)
                            s_list.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)

                        if l_artikel.lieferfrist > 0:

                            l_pprice = get_cache (L_pprice, {"artnr": [(eq, l_artikel.artnr)],"counter": [(eq, l_artikel.lieferfrist)]})

                            if l_pprice:
                                s_list.datum = l_pprice.bestelldatum


    if storeno == 0:
        create_list()
    else:
        create_list1()

    return generate_output()