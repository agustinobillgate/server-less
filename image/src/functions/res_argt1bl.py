from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Pricecod, Arrangement, Prmarket, Ratecode, Waehrung

def res_argt1bl(new_contrate:bool, prcode:str, ankunft:date, abreise:date, curr_marknr:int, pax:int, nightstay:int):
    s_list_list = []
    pricecod = arrangement = prmarket = ratecode = waehrung = None

    s_list = None

    s_list_list, S_list = create_model("S_list", {"argtnr":int, "arrangement":str, "argt_bez":str, "reihenfolge":int, "flag":int, "marknr":int, "market":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal s_list_list, pricecod, arrangement, prmarket, ratecode, waehrung


        nonlocal s_list
        nonlocal s_list_list
        return {"s-list": s_list_list}

    def create_list():

        nonlocal s_list_list, pricecod, arrangement, prmarket, ratecode, waehrung


        nonlocal s_list
        nonlocal s_list_list

        for pricecod in db_session.query(Pricecod).filter(
                (func.lower(Pricecod.code) == (prcode).lower())).all():

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == pricecod.argtnr)).first()

            if arrangement and not arrangement.weeksplit:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.marknr == pricecod.marknr and s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.marknr = pricecod.marknr
                    s_list.flag = 2

                    prmarket = db_session.query(Prmarket).filter(
                            (Prmarket.nr == pricecod.marknr)).first()

                    if prmarket:
                        s_list.market = prmarket.bezeich

                if s_list.flag >= 1 and ratecode.zikatnr == pricecod.ratecode.zikatnr and ankunft >= pricecod.startperiode and ankunft <= pricecod.endperiode:
                    s_list.flag = s_list.flag - 1

                if s_list.flag >= 1 and ratecode.zikatnr == pricecod.ratecode.zikatnr and abreise >= pricecod.startperiode and abreise <= pricecod.endperiode:
                    s_list.flag = s_list.flag - 1

        for arrangement in db_session.query(Arrangement).filter(
                (Arrangement.segmentcode == 0)).all():

            s_list = query(s_list_list, filters=(lambda s_list :s_list.argtnr == arrangement.argtnr), first=True)

            if not s_list and not arrangement.weeksplit:
                s_list = S_list()
                s_list_list.append(s_list)

                buffer_copy(arrangement, s_list)
                s_list.flag = 2

        if curr_marknr != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr


    def new_create_list():

        nonlocal s_list_list, pricecod, arrangement, prmarket, ratecode, waehrung


        nonlocal s_list
        nonlocal s_list_list

        for ratecode in db_session.query(Ratecode).filter(
                (Ratecode.code == prcode)).all():

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement.argtnr == ratecode.argtnr)).first()

            if arrangement and not arrangement.weeksplit:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.marknr == ratecode.marknr and s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.marknr = ratecode.marknr
                    s_list.flag = 2

                    prmarket = db_session.query(Prmarket).filter(
                            (Prmarket.nr == ratecode.marknr)).first()

                    if prmarket:
                        s_list.market = prmarket.bezeich

                if s_list.flag >= 1 and ratecode.zikatnr == ratecode.zikatnr and ankunft >= ratecode.startperiode and ankunft <= ratecode.endperiode:
                    s_list.flag = s_list.flag - 1

                if s_list.flag >= 1 and ratecode.zikatnr == ratecode.zikatnr and abreise >= ratecode.startperiode and abreise <= ratecode.endperiode:
                    s_list.flag = s_list.flag - 1

        if pax == 0 and nightstay == 0:

            arrangement_obj_list = []
            for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrungsnr == Arrangement.betriebsnr)).filter(
                    (Arrangement.segmentcode == 0) &  (not Arrangement.weeksplit)).all():
                if arrangement._recid in arrangement_obj_list:
                    continue
                else:
                    arrangement_obj_list.append(arrangement._recid)

                s_list = query(s_list_list, filters=(lambda s_list :s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list and not arrangement.weeksplit:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.flag = 2

        else:

            arrangement_obj_list = []
            for arrangement, waehrung in db_session.query(Arrangement, Waehrung).join(Waehrung,(Waehrungsnr == Arrangement.betriebsnr)).filter(
                    (Arrangement.segmentcode == 0) &  ((Arrangement.waeschewechsel == pax) |  (Arrangement.waeschewechsel == 0)) &  ((Arrangement.handtuch == nightstay) |  (Arrangement.handtuch == 0)) &  (not Arrangement.weeksplit)).all():
                if arrangement._recid in arrangement_obj_list:
                    continue
                else:
                    arrangement_obj_list.append(arrangement._recid)

                s_list = query(s_list_list, filters=(lambda s_list :s_list.argtnr == arrangement.argtnr), first=True)

                if not s_list and not arrangement.weeksplit:
                    s_list = S_list()
                    s_list_list.append(s_list)

                    buffer_copy(arrangement, s_list)
                    s_list.flag = 2


        if curr_marknr != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.marknr == curr_marknr)):
                s_list.reihenfolge = curr_marknr


    if new_contrate:
        new_create_list()
    else:
        create_list()

    return generate_output()