#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Pricecod, Arrangement, Prmarket, Ratecode, Waehrung

def res_argt1bl(new_contrate:bool, prcode:string, ankunft:date, abreise:date, curr_marknr:int, pax:int, nightstay:int):

    prepare_cache ([Pricecod, Prmarket, Ratecode])

    s_list_data = []
    pricecod = arrangement = prmarket = ratecode = waehrung = None

    s_list = None

    s_list_data, S_list = create_model("S_list", {"argtnr":int, "arrangement":string, "argt_bez":string, "reihenfolge":int, "flag":int, "marknr":int, "market":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_data, pricecod, arrangement, prmarket, ratecode, waehrung
        nonlocal new_contrate, prcode, ankunft, abreise, curr_marknr, pax, nightstay


        nonlocal s_list
        nonlocal s_list_data

        return {"s-list": s_list_data}

    def create_list():

        nonlocal s_list_data, pricecod, arrangement, prmarket, ratecode, waehrung
        nonlocal new_contrate, prcode, ankunft, abreise, curr_marknr, pax, nightstay


        nonlocal s_list
        nonlocal s_list_data

        for pricecod in db_session.query(Pricecod).filter(
                 (Pricecod.code == (prcode).lower())).order_by(Pricecod._recid).all():

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, pricecod.argtnr)]})

            if arrangement and not arrangement.weeksplit:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.marknr == pricecod.marknr and s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.marknr = pricecod.marknr
                    s_list.flag = 2

                    prmarket = get_cache (Prmarket, {"nr": [(eq, pricecod.marknr)]})

                    if prmarket:
                        s_list.market = prmarket.bezeich

                if s_list.flag >= 1 and ratecode.zikatnr == pricecod.zikatnr and ankunft >= pricecod.startperiode and ankunft <= pricecod.endperiode:
                    s_list.flag = s_list.flag - 1

                if s_list.flag >= 1 and ratecode.zikatnr == pricecod.zikatnr and abreise >= pricecod.startperiode and abreise <= pricecod.endperiode:
                    s_list.flag = s_list.flag - 1

        for arrangement in db_session.query(Arrangement).filter(
                 (Arrangement.segmentcode == 0)).order_by(Arrangement._recid).all():

            s_list = query(s_list_data, filters=(lambda s_list: s_list.argtnr == arrangement.argtnr), first=True)

            if not s_list and not arrangement.weeksplit:
                s_list = S_list()
                s_list_data.append(s_list)

                buffer_copy(arrangement, s_list)
                s_list.flag = 2

        if curr_marknr != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr

    def new_create_list():

        nonlocal s_list_data, pricecod, arrangement, prmarket, ratecode, waehrung
        nonlocal new_contrate, prcode, ankunft, abreise, curr_marknr, pax, nightstay


        nonlocal s_list
        nonlocal s_list_data

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == prcode)).order_by(Ratecode._recid).all():

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, ratecode.argtnr)]})

            if arrangement and not arrangement.weeksplit:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.marknr == ratecode.marknr and s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.marknr = ratecode.marknr
                    s_list.flag = 2

                    prmarket = get_cache (Prmarket, {"nr": [(eq, ratecode.marknr)]})

                    if prmarket:
                        s_list.market = prmarket.bezeich

                if s_list.flag >= 1 and ratecode.zikatnr == ratecode.zikatnr and ankunft >= ratecode.startperiode and ankunft <= ratecode.endperiode:
                    s_list.flag = s_list.flag - 1

                if s_list.flag >= 1 and ratecode.zikatnr == ratecode.zikatnr and abreise >= ratecode.startperiode and abreise <= ratecode.endperiode:
                    s_list.flag = s_list.flag - 1

        if pax == 0 and nightstay == 0:

            arrangement_obj_list = {}
            for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Arrangement.betriebsnr)).filter(
                     (Arrangement.segmentcode == 0) & not_ (Arrangement.weeksplit)).order_by(Arrangement.argtnr).all():
                if arrangement_obj_list.get(arrangement._recid):
                    continue
                else:
                    arrangement_obj_list[arrangement._recid] = True

                s_list = query(s_list_data, filters=(lambda s_list: s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list and not arrangement.weeksplit:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.flag = 2

        else:

            arrangement_obj_list = {}
            for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrung.waehrungsnr == Arrangement.betriebsnr)).filter(
                     (Arrangement.segmentcode == 0) & ((Arrangement.waeschewechsel == pax) | (Arrangement.waeschewechsel == 0)) & ((Arrangement.handtuch == nightstay) | (Arrangement.handtuch == 0)) & not_ (Arrangement.weeksplit)).order_by(Arrangement.argtnr).all():
                if arrangement_obj_list.get(arrangement._recid):
                    continue
                else:
                    arrangement_obj_list[arrangement._recid] = True

                s_list = query(s_list_data, filters=(lambda s_list: s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list and not arrangement.weeksplit:
                    s_list = S_list()
                    s_list_data.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.flag = 2


        if curr_marknr != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr

    if new_contrate:
        new_create_list()
    else:
        create_list()

    return generate_output()