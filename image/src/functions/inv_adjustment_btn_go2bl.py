from functions.additional_functions import *
import decimal
from functions.inv_adjustment_sort3bl import inv_adjustment_sort3bl
from models import L_artikel, L_bestand

def inv_adjustment_btn_go2bl(from_grp:int, sorttype:int, curr_lager:int):
    c_list_list = []
    zwkum:int = 0
    a_bez:str = ""
    l_artikel = l_bestand = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":str, "munit":str, "inhalt":str, "zwkum":str, "endkum":int, "qty":decimal, "qty1":decimal, "fibukonto":str, "avrg_price":decimal, "cost_center":str}, {"fibukonto": "0000000000"})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, zwkum, a_bez, l_artikel, l_bestand


        nonlocal c_list
        nonlocal c_list_list
        return {"c-list": c_list_list}

    def journal_list():

        nonlocal c_list_list, zwkum, a_bez, l_artikel, l_bestand


        nonlocal c_list
        nonlocal c_list_list


        c_list_list.clear()

        if sorttype <= 2:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.avrg_price = l_artikel.vk_preis


        elif sorttype == 3:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)

                if zwkum != l_artikel.zwkum:
                    a_bez = get_output(inv_adjustment_sort3bl(l_artikel.zwkum))
                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.bezeich = a_bez
                    c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                    c_list.fibukonto = " "


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                zwkum = l_artikel.zwkum
                c_list.avrg_price = l_artikel.vk_preis

    def journal_list1():

        nonlocal c_list_list, zwkum, a_bez, l_artikel, l_bestand


        nonlocal c_list
        nonlocal c_list_list


        c_list_list.clear()

        if sorttype <= 2:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.avrg_price = l_artikel.vk_preis


        elif sorttype == 3:

            l_bestand_obj_list = []
            for l_bestand, l_artikel in db_session.query(L_bestand, L_artikel).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) &  (L_artikel.endkum == from_grp)).filter(
                    (L_bestand.lager_nr == curr_lager)).all():
                if l_bestand._recid in l_bestand_obj_list:
                    continue
                else:
                    l_bestand_obj_list.append(l_bestand._recid)

                if zwkum != l_artikel.zwkum:
                    a_bez = get_output(inv_adjustment_sort3bl(l_artikel.zwkum))
                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.bezeich = a_bez
                    c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                    c_list.fibukonto = " "


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                c_list.qty1 = l_bestand.anz_anf_best + anz_eingang - anz_ausgang
                zwkum = l_artikel.zwkum
                c_list.avrg_price = l_artikel.vk_preis


    if from_grp == 0:
        journal_list()
    else:
        journal_list1()

    return generate_output()