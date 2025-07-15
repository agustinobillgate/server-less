#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement, Waehrung

def res_argt0bl(pax:int, nightstay:int):
    t_arrangement_data = []
    t_waehrung_data = []
    arrangement = waehrung = None

    t_arrangement = t_waehrung = None

    t_arrangement_data, T_arrangement = create_model_like(Arrangement)
    t_waehrung_data, T_waehrung = create_model_like(Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_arrangement_data, t_waehrung_data, arrangement, waehrung
        nonlocal pax, nightstay


        nonlocal t_arrangement, t_waehrung
        nonlocal t_arrangement_data, t_waehrung_data

        return {"t-arrangement": t_arrangement_data, "t-waehrung": t_waehrung_data}

    def assign_it():

        nonlocal t_arrangement_data, t_waehrung_data, arrangement, waehrung
        nonlocal pax, nightstay


        nonlocal t_arrangement, t_waehrung
        nonlocal t_arrangement_data, t_waehrung_data


        t_arrangement = T_arrangement()
        t_arrangement_data.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

        t_waehrung = query(t_waehrung_data, filters=(lambda t_waehrung: t_waehrung.waehrungsnr == waehrung.waehrungsnr), first=True)

        if not t_waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_data.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)

    if pax == 0 and nightstay == 0:

        arrangement_obj_list = {}
        for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Arrangement.betriebsnr)).filter(
                 (Arrangement.segmentcode == 0) & not_ (Arrangement.weeksplit)).order_by(Arrangement.argtnr).all():
            if arrangement_obj_list.get(arrangement._recid):
                continue
            else:
                arrangement_obj_list[arrangement._recid] = True


            assign_it()

    else:

        arrangement_obj_list = {}
        for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Arrangement.betriebsnr)).filter(
                 (Arrangement.segmentcode == 0) & ((Arrangement.waeschewechsel == pax) | (Arrangement.waeschewechsel == 0)) & ((Arrangement.handtuch == nightstay) | (Arrangement.handtuch == 0)) & not_ (Arrangement.weeksplit)).order_by(Arrangement.argtnr).all():
            if arrangement_obj_list.get(arrangement._recid):
                continue
            else:
                arrangement_obj_list[arrangement._recid] = True


            assign_it()


    return generate_output()