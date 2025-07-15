from functions.additional_functions import *
import decimal
from models import Htparam, L_lager, L_artikel, L_bestand, L_pprice

def min_onhand_btn_gobl(sorttype:int, main_grp:int, from_store3:int, to_store3:int, show_price:bool):
    s_list_list = []
    long_digit:bool = False
    htparam = l_lager = l_artikel = l_bestand = l_pprice = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"s":str, "s2":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal s_list
        nonlocal s_list_list
        return {"s-list": s_list_list}

    def create_list():

        nonlocal s_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal s_list
        nonlocal s_list_list

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:decimal = to_decimal("0.0")
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        s_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_store3) & (L_lager.lager_nr <= to_store3)).order_by(L_lager._recid).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2) & (L_artikel.min_bestand  > 0)).order_by(L_artikel.artnr).all():
                curr_best =  to_decimal("0")

                l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.artnr == l_artikel.artnr) & (L_bestand.lager_nr == l_lager.lager_nr)).first()

                if l_bestand:
                    curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if curr_best < l_artikel.min_best:
                        i = i + 1

                        if i == 1:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.s = " "
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_artikel.min_best, " >>>,>>9.99") + to_string(curr_best, "->>>,>>9.99")

                        if show_price:
                            s_list.s = s_list.s + to_string(l_artikel.vk_preis, ">,>>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9.99")

                            if long_digit:
                                s_list.s2 = to_string(l_artikel.vk_preis, ">>,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">>,>>>,>>>,>>9")
                            else:
                                s_list.s2 = to_string(l_artikel.vk_preis, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99")

                        if l_artikel.lieferfrist > 0:

                            l_pprice = db_session.query(L_pprice).filter(
                                     (L_pprice.artnr == l_artikel.artnr) & (L_pprice.counter == l_artikel.lieferfrist)).first()

                            if l_pprice:
                                s_list.s = s_list.s + to_string(l_pprice.bestelldatum, "99/99/99")


    def create_list2():

        nonlocal s_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice
        nonlocal sorttype, main_grp, from_store3, to_store3, show_price


        nonlocal s_list
        nonlocal s_list_list

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:decimal = to_decimal("0.0")
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        s_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                 (L_lager.lager_nr >= from_store3) & (L_lager.lager_nr <= to_store3)).order_by(L_lager._recid).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.artnr >= n1) & (L_artikel.artnr <= n2) & (L_artikel.min_bestand  > 0)).order_by(L_artikel.bezeich).all():
                curr_best =  to_decimal("0")

                l_bestand = db_session.query(L_bestand).filter(
                         (L_bestand.artnr == l_artikel.artnr) & (L_bestand.lager_nr == l_lager.lager_nr)).first()

                if l_bestand:
                    curr_best =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

                    if curr_best < l_artikel.min_best:
                        i = i + 1

                        if i == 1:
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.s = " "
                            s_list = S_list()
                            s_list_list.append(s_list)

                            s_list.s = " " + to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")
                        s_list = S_list()
                        s_list_list.append(s_list)

                        s_list.s = to_string(l_artikel.artnr, "9999999") + to_string(l_artikel.bezeich, "x(36)") + to_string(l_artikel.min_best, " >>>,>>9.99") + to_string(curr_best, "->>>,>>9.99")

                        if show_price:
                            s_list.s = s_list.s + to_string(l_artikel.vk_preis, ">,>>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">,>>>,>>>,>>9.99")

                            if long_digit:
                                s_list.s2 = to_string(l_artikel.vk_preis, ">>,>>>,>>>,>>9") + to_string(l_artikel.ek_aktuell, ">>,>>>,>>>,>>9")
                            else:
                                s_list.s2 = to_string(l_artikel.vk_preis, ">>>,>>>,>>9.99") + to_string(l_artikel.ek_aktuell, ">>>,>>>,>>9.99")

                        if l_artikel.lieferfrist > 0:

                            l_pprice = db_session.query(L_pprice).filter(
                                     (L_pprice.artnr == l_artikel.artnr) & (L_pprice.counter == l_artikel.lieferfrist)).first()

                            if l_pprice:
                                s_list.s = s_list.s + to_string(l_pprice.bestelldatum, "99/99/99")


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if sorttype == 1:
        create_list()
    else:
        create_list2()

    return generate_output()