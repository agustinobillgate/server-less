#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Waehrung, Arrangement

def res_argtbl(pax:int, nightstay:int):

    prepare_cache ([Waehrung, Arrangement])

    b1_list_data = []
    waehrung = arrangement = None

    b1_list = None

    b1_list_data, B1_list = create_model("B1_list", {"argtnr":int, "wabkurz":string, "arrangement":string, "argt_bez":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b1_list_data, waehrung, arrangement
        nonlocal pax, nightstay


        nonlocal b1_list
        nonlocal b1_list_data

        return {"b1-list": b1_list_data}

    def assign_it():

        nonlocal b1_list_data, waehrung, arrangement
        nonlocal pax, nightstay


        nonlocal b1_list
        nonlocal b1_list_data


        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.argtnr = arrangement.argtnr
        b1_list.wabkurz = waehrung.wabkurz
        b1_list.arrangement = arrangement.arrangement
        b1_list.argt_bez = arrangement.argt_bez


    if pax == 0 and nightstay == 0:

        arrangement_obj_list = {}
        arrangement = Arrangement()
        waehrung = Waehrung()
        for arrangement.argtnr, arrangement.arrangement, arrangement.argt_bez, arrangement._recid, waehrung.wabkurz, waehrung._recid in db_session.query(Arrangement.argtnr, Arrangement.arrangement, Arrangement.argt_bez, Arrangement._recid, Waehrung.wabkurz, Waehrung._recid).join(Waehrung,(Waehrung.waehrungsnr == Arrangement.betriebsnr)).filter(
                 (Arrangement.segmentcode == 0) & not_ (Arrangement.weeksplit)).order_by(Arrangement.argtnr).all():
            if arrangement_obj_list.get(arrangement._recid):
                continue
            else:
                arrangement_obj_list[arrangement._recid] = True


            assign_it()

    else:

        arrangement_obj_list = {}
        arrangement = Arrangement()
        waehrung = Waehrung()
        for arrangement.argtnr, arrangement.arrangement, arrangement.argt_bez, arrangement._recid, waehrung.wabkurz, waehrung._recid in db_session.query(Arrangement.argtnr, Arrangement.arrangement, Arrangement.argt_bez, Arrangement._recid, Waehrung.wabkurz, Waehrung._recid).join(Waehrung,(Waehrung.waehrungsnr == Arrangement.betriebsnr)).filter(
                 (Arrangement.segmentcode == 0) & ((Arrangement.waeschewechsel == pax) | (Arrangement.waeschewechsel == 0)) & ((Arrangement.handtuch == nightstay) | (Arrangement.handtuch == 0)) & not_ (Arrangement.weeksplit)).order_by(Arrangement.argtnr).all():
            if arrangement_obj_list.get(arrangement._recid):
                continue
            else:
                arrangement_obj_list[arrangement._recid] = True


            assign_it()


    return generate_output()