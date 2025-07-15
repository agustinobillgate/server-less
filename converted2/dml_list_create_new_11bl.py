#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup, L_artikel, L_bestand

def dml_list_create_new_11bl(user_init:string, curr_dept:int):

    prepare_cache ([L_untergrup, L_artikel, L_bestand])

    c_list_data = []
    l_untergrup = l_artikel = l_bestand = None

    c_list = None

    c_list_data, C_list = create_model("C_list", {"zwkum":int, "grp":string, "artnr":int, "bezeich":string, "qty":Decimal, "a_qty":Decimal, "price":Decimal, "l_price":Decimal, "unit":string, "content":Decimal, "amount":Decimal, "deliver":Decimal, "dept":int, "supplier":string, "id":string, "cid":string, "price1":Decimal, "qty1":Decimal, "lief_nr":int, "approved":bool, "remark":string, "soh":Decimal, "dml_nr":string, "qty2":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_data, l_untergrup, l_artikel, l_bestand
        nonlocal user_init, curr_dept


        nonlocal c_list
        nonlocal c_list_data

        return {"c-list": c_list_data}

    def create_new():

        nonlocal c_list_data, l_untergrup, l_artikel, l_bestand
        nonlocal user_init, curr_dept


        nonlocal c_list
        nonlocal c_list_data

        l_artikel_obj_list = {}
        l_artikel = L_artikel()
        l_untergrup = L_untergrup()
        for l_artikel.artnr, l_artikel.bezeich, l_artikel.ek_aktuell, l_artikel.lief_einheit, l_artikel.ek_letzter, l_artikel.traubensorte, l_artikel._recid, l_untergrup.bezeich, l_untergrup.zwkum, l_untergrup._recid in db_session.query(L_artikel.artnr, L_artikel.bezeich, L_artikel.ek_aktuell, L_artikel.lief_einheit, L_artikel.ek_letzter, L_artikel.traubensorte, L_artikel._recid, L_untergrup.bezeich, L_untergrup.zwkum, L_untergrup._recid).join(L_untergrup,(L_untergrup.zwkum == L_artikel.zwkum)).filter(
                 (L_artikel.bestellt)).order_by(L_artikel._recid).all():
            if l_artikel_obj_list.get(l_artikel._recid):
                continue
            else:
                l_artikel_obj_list[l_artikel._recid] = True


            c_list = C_list()
            c_list_data.append(c_list)

            c_list.artnr = l_artikel.artnr
            c_list.grp = l_untergrup.bezeich
            c_list.zwkum = l_untergrup.zwkum
            c_list.bezeich = l_artikel.bezeich
            c_list.price =  to_decimal(l_artikel.ek_aktuell) * to_decimal(l_artikel.lief_einheit)
            c_list.l_price =  to_decimal(l_artikel.ek_letzter)
            c_list.unit = l_artikel.traubensorte
            c_list.content =  to_decimal(l_artikel.lief_einheit)
            c_list.price1 =  to_decimal(c_list.price)
            c_list.id = user_init
            c_list.dept = curr_dept

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, l_artikel.artnr)],"lager_nr": [(eq, 0)]})

            if l_bestand:
                c_list.soh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)


    for c_list in query(c_list_data):
        c_list_data.remove(c_list)
    create_new()

    return generate_output()