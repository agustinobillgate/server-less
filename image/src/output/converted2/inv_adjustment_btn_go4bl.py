#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.inv_adjustment_sort3bl import inv_adjustment_sort3bl
from models import L_artikel, L_bestand

def inv_adjustment_btn_go4bl(from_grp:int, sorttype:int, curr_lager:int):

    prepare_cache ([L_artikel, L_bestand])

    c_list_list = []
    zwkum:int = 0
    a_bez:string = ""
    l_artikel = l_bestand = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"artnr":int, "bezeich":string, "munit":string, "inhalt":string, "zwkum":string, "endkum":int, "qty":Decimal, "qty1":Decimal, "fibukonto":string, "avrg_price":Decimal, "cost_center":string, "flag_coa":bool}, {"fibukonto": "0000000000"})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, zwkum, a_bez, l_artikel, l_bestand
        nonlocal from_grp, sorttype, curr_lager


        nonlocal c_list
        nonlocal c_list_list

        return {"c-list": c_list_list}

    def journal_list():

        nonlocal c_list_list, zwkum, a_bez, l_artikel, l_bestand
        nonlocal from_grp, sorttype, curr_lager


        nonlocal c_list
        nonlocal c_list_list


        c_list_list.clear()

        if sorttype <= 2:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.avrg_price =  to_decimal(l_artikel.vk_preis)

        elif sorttype == 3:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

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
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                zwkum = l_artikel.zwkum
                c_list.avrg_price =  to_decimal(l_artikel.vk_preis)


    def journal_list1():

        nonlocal c_list_list, zwkum, a_bez, l_artikel, l_bestand
        nonlocal from_grp, sorttype, curr_lager


        nonlocal c_list
        nonlocal c_list_list


        c_list_list.clear()

        if sorttype <= 2:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True


                c_list = C_list()
                c_list_list.append(c_list)

                c_list.artnr = l_artikel.artnr
                c_list.bezeich = l_artikel.bezeich
                c_list.munit = l_artikel.masseinheit
                c_list.inhalt = to_string(l_artikel.inhalt, ">>>>9.99")
                c_list.endkum = l_artikel.endkum
                c_list.zwkum = to_string(l_artikel.zwkum, ">>>>>>9")
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.avrg_price =  to_decimal(l_artikel.vk_preis)

        elif sorttype == 3:

            l_bestand_obj_list = {}
            l_bestand = L_bestand()
            l_artikel = L_artikel()
            for l_bestand.anz_anf_best, l_bestand.anz_eingang, l_bestand.anz_ausgang, l_bestand._recid, l_artikel.artnr, l_artikel.bezeich, l_artikel.masseinheit, l_artikel.inhalt, l_artikel.endkum, l_artikel.zwkum, l_artikel.vk_preis, l_artikel._recid in db_session.query(L_bestand.anz_anf_best, L_bestand.anz_eingang, L_bestand.anz_ausgang, L_bestand._recid, L_artikel.artnr, L_artikel.bezeich, L_artikel.masseinheit, L_artikel.inhalt, L_artikel.endkum, L_artikel.zwkum, L_artikel.vk_preis, L_artikel._recid).join(L_artikel,(L_artikel.artnr == L_bestand.artnr) & (L_artikel.endkum == from_grp)).filter(
                     (L_bestand.lager_nr == curr_lager)).order_by(L_artikel.zwkum, L_artikel.bezeich).all():
                if l_bestand_obj_list.get(l_bestand._recid):
                    continue
                else:
                    l_bestand_obj_list[l_bestand._recid] = True

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
                c_list.qty =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                c_list.qty1 =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                zwkum = l_artikel.zwkum
                c_list.avrg_price =  to_decimal(l_artikel.vk_preis)


    if from_grp == 0:
        journal_list()
    else:
        journal_list1()

    return generate_output()