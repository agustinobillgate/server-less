#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel, Nation, L_lieferant

def mk_sarticle_btn_helpbl(pvilanguage:int, case_type:int, inpint:int, inpint2:int, inpchar:string):

    prepare_cache ([L_artikel, Nation, L_lieferant])

    outchar = ""
    outint = 0
    str_msg = ""
    lvcarea:string = "mk-sarticle"
    l_artikel = nation = l_lieferant = None

    l_art1 = None

    L_art1 = create_buffer("L_art1",L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal outchar, outint, str_msg, lvcarea, l_artikel, nation, l_lieferant
        nonlocal pvilanguage, case_type, inpint, inpint2, inpchar
        nonlocal l_art1


        nonlocal l_art1

        return {"outchar": outchar, "outint": outint, "str_msg": str_msg}

    def find_new_artnr():

        nonlocal outchar, outint, str_msg, lvcarea, l_artikel, nation, l_lieferant
        nonlocal pvilanguage, case_type, inpint, inpint2, inpchar
        nonlocal l_art1


        nonlocal l_art1

        new_artnr = 0
        l_artikel1 = None
        l_art1 = None

        def generate_inner_output():
            return (new_artnr)

        L_artikel1 =  create_buffer("L_artikel1",L_artikel)
        L_art1 =  create_buffer("L_art1",L_artikel)

        for l_art1 in db_session.query(L_art1).filter(
                 (L_art1.zwkum == inpint) & (L_art1.endkum == inpint2)).order_by(L_art1.artnr.desc()).all():

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

        l_artikel1 = get_cache (L_artikel, {"artnr": [(eq, new_artnr)]})

        if l_artikel1:
            new_artnr = 0

        return generate_inner_output()

    if case_type == 1:

        l_art1 = get_cache (L_artikel, {"artnr": [(eq, inpint)]})

        if l_art1.betriebsnr != 0:
            str_msg = translateExtended ("This is a special article not for purchasing.", lvcarea, "")
        outchar = l_art1.bezeich
        outint = inpint
    elif case_type == 2:
        outint = find_new_artnr()
    elif case_type == 3:

        nation = get_cache (Nation, {"kurzbez": [(eq, inpchar)]})
        outchar = nation.bezeich
    elif case_type == 4:

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, inpint)]})
        outchar = l_lieferant.firma

    return generate_output()