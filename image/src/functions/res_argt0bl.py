from functions.additional_functions import *
import decimal
from models import Arrangement, Waehrung

def res_argt0bl(pax:int, nightstay:int):
    t_arrangement_list = []
    t_waehrung_list = []
    arrangement = waehrung = None

    t_arrangement = t_waehrung = None

    t_arrangement_list, T_arrangement = create_model_like(Arrangement)
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_arrangement_list, t_waehrung_list, arrangement, waehrung


        nonlocal t_arrangement, t_waehrung
        nonlocal t_arrangement_list, t_waehrung_list
        return {"t-arrangement": t_arrangement_list, "t-waehrung": t_waehrung_list}

    def assign_it():

        nonlocal t_arrangement_list, t_waehrung_list, arrangement, waehrung


        nonlocal t_arrangement, t_waehrung
        nonlocal t_arrangement_list, t_waehrung_list


        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

        t_waehrung = query(t_waehrung_list, filters=(lambda t_waehrung :t_waehrungsnr == waehrungsnr), first=True)

        if not t_waehrung:
            t_waehrung = T_waehrung()
            t_waehrung_list.append(t_waehrung)

            buffer_copy(waehrung, t_waehrung)


    if pax == 0 and nightstay == 0:

        arrangement_obj_list = []
        for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrungsnr == Arrangement.betriebsnr)).filter(
                (Arrangement.segmentcode == 0) &  (not Arrangement.weeksplit)).all():
            if arrangement._recid in arrangement_obj_list:
                continue
            else:
                arrangement_obj_list.append(arrangement._recid)


            assign_it()

    else:

        arrangement_obj_list = []
        for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrungsnr == Arrangement.betriebsnr)).filter(
                (Arrangement.segmentcode == 0) &  ((Arrangement.waeschewechsel == pax) |  (Arrangement.waeschewechsel == 0)) &  ((Arrangement.handtuch == nightstay) |  (Arrangement.handtuch == 0)) &  (not Arrangement.weeksplit)).all():
            if arrangement._recid in arrangement_obj_list:
                continue
            else:
                arrangement_obj_list.append(arrangement._recid)


            assign_it()


    return generate_output()