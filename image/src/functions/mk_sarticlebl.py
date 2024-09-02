from functions.additional_functions import *
import decimal
from models import L_untergrup, Queasy, L_hauptgrp, L_lieferant, H_rezept

def mk_sarticlebl(pvilanguage:int, case_type:int, ioint1:int, ioint2:int, inpint:int):
    opt = False
    outchar = ""
    str_msg = ""
    lvcarea:str = "mk_sarticle"
    l_untergrup = queasy = l_hauptgrp = l_lieferant = h_rezept = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal opt, outchar, str_msg, lvcarea, l_untergrup, queasy, l_hauptgrp, l_lieferant, h_rezept


        return {"opt": opt, "outchar": outchar, "str_msg": str_msg}


    if case_type == 1:

        l_untergrup = db_session.query(L_untergrup).filter(
                (L_untergrup.zwkum == ioint1)).first()

        if l_untergrup:
            opt = True

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 29) &  (Queasy.number2 == ioint1)).first()

            if queasy and queasy.number1 != inpint:
                str_msg = translateExtended ("Subgroup_No belongs to other Maingroup", lvcarea, "")
                ioint1 = ioint2

                return generate_output()
            outchar = l_untergrup.bezeich
            ioint2 = l_untergrup.zwkum
        else:
            ioint1 = ioint2

            if ioint2 != 0:
                str_msg = translateExtended ("No such sub_group number found", lvcarea, "")

    elif case_type == 2:

        l_hauptgrp = db_session.query(L_hauptgrp).filter(
                (L_hauptgrp.endkum == ioint1)).first()

        if l_hauptgrp:
            outchar = l_hauptgrp.bezeich
            ioint2 = l_hauptgrp.endkum
            opt = True


        else:
            ioint1 = ioint2

            if ioint2 != 0:
                str_msg = translateExtended ("No such main_group number found", lvcarea, "")

    elif case_type == 3:

        l_lieferant = db_session.query(L_lieferant).filter(
                (L_lieferant.lief_nr == ioint1)).first()

        if l_lieferant:
            ioint2 = ioint1
            outchar = l_lieferant.firma
            opt = True

        elif ioint1 != 0:
            ioint1 = ioint2
            str_msg = translateExtended ("No such Supplier Number found", lvcarea, "")

    elif case_type == 4:

        h_rezept = db_session.query(H_rezept).filter(
                (H_rezept.artnrrezept == ioint1)).first()

        if not h_rezept:
            str_msg = translateExtended ("Recipe does not exist", lvcarea, "")
            ioint1 = inpint
            opt = True


        else:
            outchar = h_rezept.bezeich

    return generate_output()