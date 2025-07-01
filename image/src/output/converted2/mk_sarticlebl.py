#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_untergrup, Queasy, L_hauptgrp, L_lieferant, H_rezept

def mk_sarticlebl(pvilanguage:int, case_type:int, ioint1:int, ioint2:int, inpint:int):

    prepare_cache ([L_untergrup, Queasy, L_hauptgrp, L_lieferant, H_rezept])

    opt = False
    outchar = ""
    str_msg = ""
    lvcarea:string = "mk-sarticle"
    l_untergrup = queasy = l_hauptgrp = l_lieferant = h_rezept = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal opt, outchar, str_msg, lvcarea, l_untergrup, queasy, l_hauptgrp, l_lieferant, h_rezept
        nonlocal pvilanguage, case_type, ioint1, ioint2, inpint

        return {"ioint1": ioint1, "ioint2": ioint2, "opt": opt, "outchar": outchar, "str_msg": str_msg}


    if case_type == 1:

        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, ioint1)]})

        if l_untergrup:
            opt = True

            queasy = get_cache (Queasy, {"key": [(eq, 29)],"number2": [(eq, ioint1)]})

            if queasy and queasy.number1 != inpint:
                str_msg = translateExtended ("Subgroup-No belongs to other Maingroup", lvcarea, "")
                ioint1 = ioint2

                return generate_output()
            outchar = l_untergrup.bezeich
            ioint2 = l_untergrup.zwkum
        else:
            ioint1 = ioint2

            if ioint2 != 0:
                str_msg = translateExtended ("No such sub-group number found", lvcarea, "")

    elif case_type == 2:

        l_hauptgrp = get_cache (L_hauptgrp, {"endkum": [(eq, ioint1)]})

        if l_hauptgrp:
            outchar = l_hauptgrp.bezeich
            ioint2 = l_hauptgrp.endkum
            opt = True


        else:
            ioint1 = ioint2

            if ioint2 != 0:
                str_msg = translateExtended ("No such main-group number found", lvcarea, "")

    elif case_type == 3:

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, ioint1)]})

        if l_lieferant:
            ioint2 = ioint1
            outchar = l_lieferant.firma
            opt = True

        elif ioint1 != 0:
            ioint1 = ioint2
            str_msg = translateExtended ("No such Supplier Number found", lvcarea, "")

    elif case_type == 4:

        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, ioint1)]})

        if not h_rezept:
            str_msg = translateExtended ("Recipe does not exist", lvcarea, "")
            ioint1 = inpint
            opt = True


        else:
            outchar = h_rezept.bezeich

    return generate_output()