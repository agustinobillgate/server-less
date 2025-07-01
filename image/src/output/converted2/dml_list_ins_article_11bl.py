#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, L_untergrup, L_bestand

def dml_list_ins_article_11bl(artnr:int, user_init:string, curr_dept:int):

    prepare_cache ([L_artikel, L_untergrup, L_bestand])

    c_list_list = []
    l_artikel = l_untergrup = l_bestand = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, l_artikel, l_untergrup, l_bestand
        nonlocal artnr, user_init, curr_dept


        nonlocal c_list
        nonlocal c_list_list

        return {"c-list": c_list_list}

    def ins_article():

        nonlocal c_list_list, l_artikel, l_untergrup, l_bestand
        nonlocal artnr, user_init, curr_dept


        nonlocal c_list
        nonlocal c_list_list

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, artnr)]})

        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})
        c_list = C_list()
        c_list_list.append(c_list)

        c_list.artnr = l_artikel.artnr
        c_list.grp = l_untergrup.bezeich
        c_list.zwkum = l_untergrup.zwkum
        c_list.bezeich = l_artikel.bezeich
        c_list.price =  to_decimal(l_artikel.ek_aktuell)
        c_list.unit = l_artikel.traubensorte
        c_list.content =  to_decimal(l_artikel.inhalt)
        c_list.price1 =  to_decimal(c_list.price)
        c_list.id = user_init
        c_list.dept = curr_dept

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

        if l_bestand:
            c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

    ins_article()

    return generate_output()