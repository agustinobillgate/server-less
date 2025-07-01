#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant, L_segment

def prepare_chg_supplybl(supply_recid:int):

    prepare_cache ([L_segment])

    segm_bezeich = ""
    t_l_lieferant_list = []
    l_lieferant = l_segment = None

    t_l_lieferant = None

    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant, {"t_recid":int, "email":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm_bezeich, t_l_lieferant_list, l_lieferant, l_segment
        nonlocal supply_recid


        nonlocal t_l_lieferant
        nonlocal t_l_lieferant_list

        return {"segm_bezeich": segm_bezeich, "t-l-lieferant": t_l_lieferant_list}

    l_lieferant = get_cache (L_lieferant, {"_recid": [(eq, supply_recid)]})

    if l_lieferant:
        t_l_lieferant = T_l_lieferant()
        t_l_lieferant_list.append(t_l_lieferant)

        buffer_copy(l_lieferant, t_l_lieferant)

        if l_lieferant.segment1 != 0:

            l_segment = get_cache (L_segment, {"l_segmentcode": [(eq, l_lieferant.segment1)]})

        if l_segment:
            segm_bezeich = l_segment.l_bezeich

    return generate_output()