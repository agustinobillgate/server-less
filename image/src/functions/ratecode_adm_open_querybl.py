from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Ratecode, Arrangement, Guest, Guest_pr, Prmarket

def ratecode_adm_open_querybl(pvilanguage:int, prcode:str, market:str, market_nr:int, zikatnr:int, argtnr:int):
    comments = ""
    tb3_list = []
    lvcarea:str = "ratecode_admin"
    ratecode = arrangement = guest = guest_pr = prmarket = None

    tb3 = None

    tb3_list, Tb3 = create_model_like(Ratecode, {"s_recid":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal comments, tb3_list, lvcarea, ratecode, arrangement, guest, guest_pr, prmarket


        nonlocal tb3
        nonlocal tb3_list
        return {"comments": comments, "tb3": tb3_list}

    def open_query():

        nonlocal comments, tb3_list, lvcarea, ratecode, arrangement, guest, guest_pr, prmarket


        nonlocal tb3
        nonlocal tb3_list


        comments = ""

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == argtnr)).first()

        if arrangement.zuordnung != "":
            comments = trim(to_string(arrangement, "x(5)")) + translateExtended (" - comments:", lvcarea, "") + chr(10) + arrangement.zuordnung + chr(10)

        guest_pr_obj_list = []
        for guest_pr, guest in db_session.query(Guest_pr, Guest).join(Guest,(Guest.gastnr == Guest_pr.gastnr)).filter(
                (func.lower(Guest_pr.code) == (prcode).lower())).all():
            if guest_pr._recid in guest_pr_obj_list:
                continue
            else:
                guest_pr_obj_list.append(guest_pr._recid)

            if guest.bemerk != "" and (len(comments) + len(guest.bemerk) + len(guest.name)) <= 30000:
                comments = comments + guest.name + translateExtended (" - Comment:", lvcarea, "") + " " + guest.bemerk + chr(10)

        prmarket = db_session.query(Prmarket).filter(
                (Prmarket.nr == market_nr)).first()

        if prmarket:

            for ratecode in db_session.query(Ratecode).filter(
                    (Ratecode.marknr == prmarket.nr) &  (func.lower(Ratecode.code) == (prcode).lower()) &  (Ratecode.argtnr == argtnr) &  (Ratecode.zikatnr == zikatnr)).all():
                tb3 = Tb3()
                tb3_list.append(tb3)

                buffer_copy(ratecode, tb3)
                tb3.s_recid = to_int(ratecode._recid)


    open_query()

    return generate_output()