#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Hoteldpt, Htparam, Tisch, Zimmer, Kellner

def prepare_ts_tablebl(pvilanguage:int, dept:int, curr_printer:int, user_init:string):

    prepare_cache ([Htparam, Tisch, Zimmer])

    b_title = ""
    mc_flag = False
    mc_pos1 = 0
    mc_pos2 = 0
    curr_waiter = 1
    vpos_flag = False
    tbuff_data = []
    zbuff_data = []
    lvcarea:string = "TS-table"
    hoteldpt = htparam = tisch = zimmer = kellner = None

    tbuff = zbuff = None

    tbuff_data, Tbuff = create_model("Tbuff", {"tischnr":int})
    zbuff_data, Zbuff = create_model("Zbuff", {"zinr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_title, mc_flag, mc_pos1, mc_pos2, curr_waiter, vpos_flag, tbuff_data, zbuff_data, lvcarea, hoteldpt, htparam, tisch, zimmer, kellner
        nonlocal pvilanguage, dept, curr_printer, user_init


        nonlocal tbuff, zbuff
        nonlocal tbuff_data, zbuff_data

        return {"b_title": b_title, "mc_flag": mc_flag, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "curr_waiter": curr_waiter, "vpos_flag": vpos_flag, "tbuff": tbuff_data, "zbuff": zbuff_data}


    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    b_title = translateExtended ("Select Table", lvcarea, "")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 336)]})

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 337)]})
        mc_pos1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 338)]})
        mc_pos2 = htparam.finteger

    for tisch in db_session.query(Tisch).filter(
             (Tisch.departement == dept)).order_by(Tisch._recid).all():
        tbuff = Tbuff()
        tbuff_data.append(tbuff)

        tbuff.tischnr = tisch.tischnr

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        zbuff = Zbuff()
        zbuff_data.append(zbuff)

        zbuff.zinr = zimmer.zinr


    curr_waiter = to_int(user_init)

    kellner = get_cache (Kellner, {"kellner_nr": [(eq, curr_waiter)],"departement": [(eq, dept)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 975)]})
    vpos_flag = (htparam.finteger == 1)

    return generate_output()