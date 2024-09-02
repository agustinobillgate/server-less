from functions.additional_functions import *
import decimal
from models import Hoteldpt, Htparam, Tisch, Zimmer, Kellner

def prepare_ts_tablebl(pvilanguage:int, dept:int, curr_printer:int, user_init:str):
    b_title = ""
    mc_flag = False
    mc_pos1 = 0
    mc_pos2 = 0
    curr_waiter = 0
    vpos_flag = False
    tbuff_list = []
    zbuff_list = []
    lvcarea:str = "TS_table"
    hoteldpt = htparam = tisch = zimmer = kellner = None

    tbuff = zbuff = None

    tbuff_list, Tbuff = create_model("Tbuff", {"tischnr":int})
    zbuff_list, Zbuff = create_model("Zbuff", {"zinr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_title, mc_flag, mc_pos1, mc_pos2, curr_waiter, vpos_flag, tbuff_list, zbuff_list, lvcarea, hoteldpt, htparam, tisch, zimmer, kellner


        nonlocal tbuff, zbuff
        nonlocal tbuff_list, zbuff_list
        return {"b_title": b_title, "mc_flag": mc_flag, "mc_pos1": mc_pos1, "mc_pos2": mc_pos2, "curr_waiter": curr_waiter, "vpos_flag": vpos_flag, "tbuff": tbuff_list, "zbuff": zbuff_list}


    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    b_title = translateExtended ("Select Table", lvcarea, "")

    htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 336)).first()

    if htparam.feldtyp == 4:
        mc_flag = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 337)).first()
        mc_pos1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 338)).first()
        mc_pos2 = htparam.finteger

    for tisch in db_session.query(Tisch).filter(
            (Tisch.departement == dept)).all():
        tbuff = Tbuff()
        tbuff_list.append(tbuff)

        tbuff.tischnr = tischnr

    for zimmer in db_session.query(Zimmer).all():
        zbuff = Zbuff()
        zbuff_list.append(zbuff)

        zbuff.zinr = zimmer.zinr


    curr_waiter = to_int(user_init)

    kellner = db_session.query(Kellner).filter(
            (Kellner_nr == curr_waiter) &  (Kellner.departement == dept)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 975)).first()
    vpos_flag = (htparam.finteger == 1)

    return generate_output()