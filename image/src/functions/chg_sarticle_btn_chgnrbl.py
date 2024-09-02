from functions.additional_functions import *
import decimal
from models import L_artikel

def chg_sarticle_btn_chgnrbl(t_l_zwkum:int, t_l_endkum:int, t_l_artnr:int, l_zwkum:int, l_endkum:int, l_artnr:int, artnr:int):
    artnr_ok = False
    l_artikel = None

    l_artikel1 = l_art1 = None

    L_artikel1 = L_artikel
    L_art1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artnr_ok, l_artikel
        nonlocal l_artikel1, l_art1


        nonlocal l_artikel1, l_art1
        return {"artnr_ok": artnr_ok}

    def find_new_artnr(update_flag:bool):

        nonlocal artnr_ok, l_artikel
        nonlocal l_artikel1, l_art1


        nonlocal l_artikel1, l_art1

        new_artnr = 0

        def generate_inner_output():
            return new_artnr
        L_artikel1 = L_artikel
        L_art1 = L_artikel

        if l_zwkum == t_l_zwkum and l_endkum == t_l_endkum and not update_flag:
            new_artnr = t_l_artnr

            return generate_inner_output()

        for l_art1 in db_session.query(L_art1).filter(
                (L_art1.zwkum == l_zwkum) &  (L_art1.endkum == l_endkum)).all():

            if l_art1.zwkum <= 99 and substring(to_string(l_art1.artnr) , 1, 2) == to_string(l_art1.zwkum, "99") and substring(to_string(l_art1.artnr) , 0, 1) == to_string(l_art1.endkum, "9"):
                new_artnr = l_art1.artnr + 1

                return generate_inner_output()

            elif l_art1.zwkum >= 100 and substring(to_string(l_art1.artnr) , 1, 3) == to_string(l_art1.zwkum, "999") and substring(to_string(l_art1.artnr) , 0, 1) == to_string(l_art1.endkum, "9"):
                new_artnr = l_art1.artnr + 1

                return generate_inner_output()

        if l_zwkum <= 99:
            new_artnr = l_endkum * 1000000 + l_zwkum * 10000 + 1

        elif l_zwkum >= 100:
            new_artnr = l_endkum * 1000000 + l_zwkum * 1000 + 1

        l_artikel1 = db_session.query(L_artikel1).filter(
                (L_artikel1.artnr == new_artnr)).first()

        if l_artikel1:
            new_artnr = 0


        return generate_inner_output()

    def check_artno():

        nonlocal artnr_ok, l_artikel
        nonlocal l_artikel1, l_art1


        nonlocal l_artikel1, l_art1

        its_ok = False
        nr:int = 0
        s:str = ""

        def generate_inner_output():
            return its_ok

        if l_zwkum > 99:
            nr = l_endkum * 1000 + l_zwkum
        else:
            nr = l_endkum * 100 + l_zwkum

        if nr > 999:
            s = substring(to_string(l_artnr) , 0, 4)
        else:
            s = substring(to_string(l_artnr) , 0, 3)
        its_ok = (s == to_string(nr))


        return generate_inner_output()

    artnr = find_new_artnr(True)
    artnr_ok = check_artno()

    return generate_output()