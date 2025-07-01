#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def fill_containerbl(ss_artnr1:int, ss_artnr2:int, ss_artnr3:int):

    prepare_cache ([L_artikel])

    ss_bezeich1 = ""
    ss_bezeich2 = ""
    ss_bezeich3 = ""
    ss_preis1 = to_decimal("0.0")
    ss_preis2 = to_decimal("0.0")
    ss_preis3 = to_decimal("0.0")
    l_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ss_bezeich1, ss_bezeich2, ss_bezeich3, ss_preis1, ss_preis2, ss_preis3, l_artikel
        nonlocal ss_artnr1, ss_artnr2, ss_artnr3

        return {"ss_bezeich1": ss_bezeich1, "ss_bezeich2": ss_bezeich2, "ss_bezeich3": ss_bezeich3, "ss_preis1": ss_preis1, "ss_preis2": ss_preis2, "ss_preis3": ss_preis3}


    if ss_artnr1 != 0:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, ss_artnr1)]})

        if l_artikel:
            ss_bezeich1 = l_artikel.bezeich
            ss_preis1 =  to_decimal(l_artikel.ek_aktuell)

    if ss_artnr2 != 0:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, ss_artnr2)]})

        if l_artikel:
            ss_bezeich2 = l_artikel.bezeich
            ss_preis2 =  to_decimal(l_artikel.ek_aktuell)

    if ss_artnr3 != 0:

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, ss_artnr3)]})

        if l_artikel:
            ss_bezeich3 = l_artikel.bezeich
            ss_preis3 =  to_decimal(l_artikel.ek_aktuell)

    return generate_output()