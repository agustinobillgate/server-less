from functions.additional_functions import *
import decimal
from models import L_artikel, L_untergrup, L_bestand

def dml_list_ins_article_11bl(artnr:int, user_init:str, curr_dept:int):
    c_list_list = []
    l_artikel = l_untergrup = l_bestand = None

    c_list = None

    c_list_list, C_list = create_model("C_list", {"zwkum":int, "grp":str, "artnr":int, "bezeich":str, "qty":decimal, "a_qty":decimal, "price":decimal, "l_price":decimal, "unit":str, "content":decimal, "amount":decimal, "deliver":decimal, "dept":int, "supplier":str, "id":str, "cid":str, "price1":decimal, "qty1":decimal, "lief_nr":int, "approved":bool, "remark":str, "soh":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_list_list, l_artikel, l_untergrup, l_bestand


        nonlocal c_list
        nonlocal c_list_list
        return {"c-list": c_list_list}

    def ins_article():

        nonlocal c_list_list, l_artikel, l_untergrup, l_bestand


        nonlocal c_list
        nonlocal c_list_list

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == artnr)).first()

        l_untergrup = db_session.query(L_untergrup).filter(
                (L_untergrup.zwkum == l_artikel.zwkum)).first()
        c_list = C_list()
        c_list_list.append(c_list)

        c_list.artnr = l_artikel.artnr
        c_list.grp = l_untergrup.bezeich
        c_list.zwkum = l_untergrup.zwkum
        c_list.bezeich = l_artikel.bezeich
        c_list.price = l_artikel.ek_aktuell
        c_list.unit = l_artikel.masseinheit
        c_list.content = l_artikel.inhalt
        c_list.price1 = c_list.price
        c_list.id = user_init
        c_list.dept = curr_dept

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == l_artikel.artnr) &  (L_bestand.lager_nr == 0)).first()

        if l_bestand:
            c_list.soh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang


    ins_article()

    return generate_output()