from functions.additional_functions import *
import decimal
from models import L_lieferant, L_segment

def prepare_chg_supplybl(supply_recid:int):
    segm_bezeich = ""
    t_l_lieferant_list = []
    l_lieferant = l_segment = None

    t_l_lieferant = None

    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant, {"t_recid":int, "email":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal segm_bezeich, t_l_lieferant_list, l_lieferant, l_segment


        nonlocal t_l_lieferant
        nonlocal t_l_lieferant_list
        return {"segm_bezeich": segm_bezeich, "t-l-lieferant": t_l_lieferant_list}

    l_lieferant = db_session.query(L_lieferant).filter(
            (L_lieferant._recid == supply_recid)).first()

    if l_lieferant:
        t_l_lieferant = T_l_lieferant()
        t_l_lieferant_list.append(t_l_lieferant)

        buffer_copy(l_lieferant, t_l_lieferant)

    if l_lieferant.segment1 != 0:

        l_segment = db_session.query(L_segment).filter(
                (L_segmentcode == l_lieferant.segment1)).first()

    if l_segment:
        segm_bezeich = l_segment.l_bezeich

    return generate_output()