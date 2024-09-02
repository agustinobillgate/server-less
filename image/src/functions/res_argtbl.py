from functions.additional_functions import *
import decimal
from models import Waehrung, Arrangement

def res_argtbl(pax:int, nightstay:int):
    b1_list_list = []
    waehrung = arrangement = None

    b1_list = None

    b1_list_list, B1_list = create_model("B1_list", {"argtnr":int, "wabkurz":str, "arrangement":str, "argt_bez":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_list, waehrung, arrangement


        nonlocal b1_list
        nonlocal b1_list_list
        return {"b1-list": b1_list_list}

    def assign_it():

        nonlocal b1_list_list, waehrung, arrangement


        nonlocal b1_list
        nonlocal b1_list_list


        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.argtnr = arrangement.argtnr
        b1_list.wabkurz = waehrung.wabkurz
        b1_list.arrangement = arrangement
        b1_list.argt_bez = arrangement.argt_bez

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