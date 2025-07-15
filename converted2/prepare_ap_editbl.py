#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_kredit, L_lieferant

def prepare_ap_editbl(recid_ap:int):

    prepare_cache ([L_lieferant])

    firma = ""
    lief_nr = 0
    t_l_kredit_data = []
    l_kredit = l_lieferant = None

    t_l_kredit = None

    t_l_kredit_data, T_l_kredit = create_model_like(L_kredit)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal firma, lief_nr, t_l_kredit_data, l_kredit, l_lieferant
        nonlocal recid_ap


        nonlocal t_l_kredit
        nonlocal t_l_kredit_data

        return {"firma": firma, "lief_nr": lief_nr, "t-l-kredit": t_l_kredit_data}

    l_kredit = get_cache (L_kredit, {"_recid": [(eq, recid_ap)]})

    if l_kredit:
        t_l_kredit = T_l_kredit()
        t_l_kredit_data.append(t_l_kredit)

        buffer_copy(l_kredit, t_l_kredit)

        l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, l_kredit.lief_nr)]})

        if l_lieferant:
            firma = l_lieferant.firma
            lief_nr = l_lieferant.lief_nr

    return generate_output()