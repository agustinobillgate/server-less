from functions.additional_functions import *
import decimal
from models import L_artikel, Nation, L_lieferant

def mk_sarticle_btn_helpbl(pvilanguage:int, case_type:int, inpint:int, inpint2:int, inpchar:str):
    outchar = ""
    outint = 0
    str_msg = ""
    lvcarea:str = "mk_sarticle"
    l_artikel = nation = l_lieferant = None

    l_art1 = l_artikel1 = None

    L_art1 = L_artikel
    L_artikel1 = L_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outchar, outint, str_msg, lvcarea, l_artikel, nation, l_lieferant
        nonlocal l_art1, l_artikel1


        nonlocal l_art1, l_artikel1
        return {"outchar": outchar, "outint": outint, "str_msg": str_msg}

    def find_new_artnr():

        nonlocal outchar, outint, str_msg, lvcarea, l_artikel, nation, l_lieferant
        nonlocal l_art1, l_artikel1


        nonlocal l_art1, l_artikel1

        new_artnr = 0

        def generate_inner_output():
            return new_artnr
        L_artikel1 = L_artikel
        L_art1 = L_artikel

        for l_art1 in db_session.query(L_art1).filter(
                (L_art1.zwkum == inpint) &  (L_art1.endkum == inpint2)).all():

            if l_art1.zwkum <= 99 and substring(to_string(l_art1.artnr) , 1, 2) == to_string(l_art1.zwkum, "99") and substring(to_string(l_art1.artnr) , 0, 1) == to_string(l_art1.endkum, "9"):
                new_artnr = l_art1.artnr + 1

                return generate_inner_output()

            elif l_art1.zwkum >= 100 and substring(to_string(l_art1.artnr) , 1, 3) == to_string(l_art1.zwkum, "999") and substring(to_string(l_art1.artnr) , 0, 1) == to_string(l_art1.endkum, "9"):
                new_artnr = l_art1.artnr + 1

                return generate_inner_output()

        if inpint <= 99:
            new_artnr = inpint2 * 1000000 + inpint * 10000 + 1

        elif inpint >= 100:
            new_artnr = inpint2 * 1000000 + inpint * 1000 + 1

        l_artikel1 = db_session.query(L_artikel1).filter(
                (L_artikel1.artnr == new_artnr)).first()

        if l_artikel1:
            new_artnr = 0


        return generate_inner_output()


    if case_type == 1:

        l_art1 = db_session.query(L_art1).filter(
                (L_art1.artnr == inpint)).first()

        if l_art1.betriebsnr != 0:
            str_msg = translateExtended ("This is a special article not for purchasing.", lvcarea, "")
        outchar = l_art1.bezeich
        outint = inpint
    elif case_type == 2:
        outint = find_new_artnr()
    elif case_type == 3:

        nation = db_session.query(Nation).filter(
                (Nation.kurzbez == inpchar)).first()
        outchar = nation.bezeich
    elif case_type == 4:

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == inpint)).first()
        outchar = l_lieferant.firma

    return generate_output()