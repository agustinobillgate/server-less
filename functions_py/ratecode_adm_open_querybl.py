#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 30/10/2025
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Ratecode, Arrangement, Guest, Guest_pr, Prmarket

def ratecode_adm_open_querybl(pvilanguage:int, prcode:string, market:string, market_nr:int, zikatnr:int, argtnr:int):

    prepare_cache ([Arrangement, Guest, Prmarket])

    comments = ""
    tb3_data = []
    lvcarea:string = "ratecode-admin"
    ratecode = arrangement = guest = guest_pr = prmarket = None

    tb3 = None

    tb3_data, Tb3 = create_model_like(Ratecode, {"s_recid":int})

    db_session = local_storage.db_session
    prcode = prcode.strip()
    market = market.strip()

    def generate_output():
        nonlocal comments, tb3_data, lvcarea, ratecode, arrangement, guest, guest_pr, prmarket
        nonlocal pvilanguage, prcode, market, market_nr, zikatnr, argtnr


        nonlocal tb3
        nonlocal tb3_data

        return {"comments": comments, "tb3": tb3_data}

    def open_query():

        nonlocal comments, tb3_data, lvcarea, ratecode, arrangement, guest, guest_pr, prmarket
        nonlocal pvilanguage, prcode, market, market_nr, zikatnr, argtnr


        nonlocal tb3
        nonlocal tb3_data


        comments = ""

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtnr)]})

        if arrangement.zuordnung != "":
            comments = trim(to_string(arrangement.arrangement, "x(5)")) + translateExtended (" - comments:", lvcarea, "") + chr_unicode(10) + arrangement.zuordnung + chr_unicode(10)

        guest_pr_obj_list = {}
        for guest_pr, guest in db_session.query(Guest_pr, Guest).join(Guest,(Guest.gastnr == Guest_pr.gastnr)).filter(
                 (Guest_pr.code == (prcode))).order_by(Guest.name).all():
            if guest_pr_obj_list.get(guest_pr._recid):
                continue
            else:
                guest_pr_obj_list[guest_pr._recid] = True

            if guest.bemerkung != "" and (length(comments) + length(guest.bemerkung) + length(guest.name)) <= 30000:
                comments = comments + guest.name + translateExtended (" - Comment:", lvcarea, "") + " " + guest.bemerkung + chr_unicode(10)

        prmarket = get_cache (Prmarket, {"nr": [(eq, market_nr)]})

        if prmarket:

            for ratecode in db_session.query(Ratecode).filter(
                     (Ratecode.marknr == prmarket.nr) & (Ratecode.code == (prcode)) & (Ratecode.argtnr == argtnr) & (Ratecode.zikatnr == zikatnr)).order_by(Ratecode.startperiode, Ratecode.wday, Ratecode.erwachs, Ratecode.kind1, Ratecode.kind2).all():
                tb3 = Tb3()
                tb3_data.append(tb3)

                buffer_copy(ratecode, tb3)
                tb3.s_recid = to_int(ratecode._recid)

    open_query()

    return generate_output()