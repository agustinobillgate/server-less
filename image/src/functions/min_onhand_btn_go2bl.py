from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_lager, L_artikel, L_bestand, L_pprice

def min_onhand_btn_go2bl(sorttype:int, main_grp:int, from_store3:int, to_store3:int, show_price:bool):
    min_onhand_list_list = []
    long_digit:bool = False
    htparam = l_lager = l_artikel = l_bestand = l_pprice = None

    min_onhand_list = None

    min_onhand_list_list, Min_onhand_list = create_model("Min_onhand_list", {"artnr":int, "name":str, "min_oh":decimal, "curr_oh":decimal, "avrgprice":decimal, "ek_aktuell":decimal, "datum":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal min_onhand_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice


        nonlocal min_onhand_list
        nonlocal min_onhand_list_list
        return {"min-onhand-list": min_onhand_list_list}

    def create_list():

        nonlocal min_onhand_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice


        nonlocal min_onhand_list
        nonlocal min_onhand_list_list

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:decimal = 0
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        min_onhand_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_store3) &  (L_lager.lager_nr <= to_store3)).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                    (L_artikel.artnr >= n1) &  (L_artikel.artnr <= n2) &  (L_artikel.min_best > 0)).all():
                curr_best = 0

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == l_lager.lager_nr)).first()

                if l_bestand:
                    curr_best = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if curr_best < l_artikel.min_best:
                        i = i + 1

                        if i == 1:
                            min_onhand_list = Min_onhand_list()
                            min_onhand_list_list.append(min_onhand_list)

                            min_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")


                        min_onhand_list = Min_onhand_list()
                        min_onhand_list_list.append(min_onhand_list)

                        min_onhand_list.artnr = l_artikel.artnr
                        min_onhand_list.name = l_artikel.bezeich
                        min_onhand_list.min_oh = l_artikel.min_best
                        min_onhand_list.curr_oh = curr_best


                        min_onhand_list.avrgprice = l_artikel.vk_preis
                        min_onhand_list.ek_aktuell = l_artikel.ek_aktuell

                        if l_artikel.lieferfrist > 0:

                            l_pprice = db_session.query(L_pprice).filter(
                                    (L_pprice.artnr == l_artikel.artnr) &  (L_pprice.counter == l_artikel.lieferfrist)).first()

                            if l_pprice:
                                min_onhand_list.datum = l_pprice.bestelldatum

    def create_list2():

        nonlocal min_onhand_list_list, long_digit, htparam, l_lager, l_artikel, l_bestand, l_pprice


        nonlocal min_onhand_list
        nonlocal min_onhand_list_list

        n1:int = 0
        n2:int = 0
        i:int = 0
        curr_best:decimal = 0
        n1 = main_grp * 1000000
        n2 = (main_grp + 1) * 1000000 - 1
        min_onhand_list_list.clear()

        for l_lager in db_session.query(L_lager).filter(
                (L_lager.lager_nr >= from_store3) &  (L_lager.lager_nr <= to_store3)).all():
            i = 0

            for l_artikel in db_session.query(L_artikel).filter(
                    (L_artikel.artnr >= n1) &  (L_artikel.artnr <= n2) &  (L_artikel.min_best > 0)).all():
                curr_best = 0

                l_bestand = db_session.query(L_bestand).filter(
                        (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == l_lager.lager_nr)).first()

                if l_bestand:
                    curr_best = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

                    if curr_best < l_artikel.min_best:
                        i = i + 1

                        if i == 1:
                            min_onhand_list = Min_onhand_list()
                            min_onhand_list_list.append(min_onhand_list)

                            min_onhand_list.name = to_string(l_lager.lager_nr, "99") + " " + to_string(l_lager.bezeich, "x(13)")


                        min_onhand_list = Min_onhand_list()
                        min_onhand_list_list.append(min_onhand_list)

                        min_onhand_list.artnr = l_artikel.artnr
                        min_onhand_list.name = l_artikel.bezeich
                        min_onhand_list.min_oh = l_artikel.min_best
                        min_onhand_list.curr_oh = curr_best


                        min_onhand_list.avrgprice = l_artikel.vk_preis
                        min_onhand_list.ek_aktuell = l_artikel.ek_aktuell

                        if l_artikel.lieferfrist > 0:

                            l_pprice = db_session.query(L_pprice).filter(
                                    (L_pprice.artnr == l_artikel.artnr) &  (L_pprice.counter == l_artikel.lieferfrist)).first()

                            if l_pprice:
                                min_onhand_list.datum = l_pprice.bestelldatum

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    if sorttype == 1:
        create_list()
    else:
        create_list2()

    return generate_output()