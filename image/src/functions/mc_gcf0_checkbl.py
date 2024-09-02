from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Mc_guest, Bediener, Guest, Mc_types, Mc_aclub

def mc_gcf0_checkbl(pvilanguage:int, gastno:int, curr_mode:str, sales_id:str, nr:int, cardnum:str):
    err_code = 0
    msg_str = ""
    lvcarea:str = "mc-gcf"
    gname:str = ""
    mc_guest = bediener = guest = mc_types = mc_aclub = None

    g_list = bbuff = gbuff = gast = tbuff = None

    g_list_list, G_list = create_model_like(Mc_guest)

    Bbuff = create_buffer("Bbuff",Bediener)
    Gbuff = create_buffer("Gbuff",Mc_guest)
    Gast = create_buffer("Gast",Guest)
    Tbuff = create_buffer("Tbuff",Mc_types)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, msg_str, lvcarea, gname, mc_guest, bediener, guest, mc_types, mc_aclub
        nonlocal pvilanguage, gastno, curr_mode, sales_id, nr, cardnum
        nonlocal bbuff, gbuff, gast, tbuff

        nonlocal g_list, bbuff, gbuff, gast, tbuff
        nonlocal g_list_list
        return {"err_code": err_code, "msg_str": msg_str}

    if not mc_guest or not(mc_guest.gastnr == gastno):
        mc_guest = db_session.query(Mc_guest).filter(
            (Mc_guest.gastnr == gastno)).first()

    if sales_id != "":

        if not bbuff or not(bbuff.userinit.lower()  == (sales_id).lower()):
            bbuff = db_session.query(Bbuff).filter(
                (func.lower(Bbuff.userinit) == (sales_id).lower())).first()

        if not bbuff:
            msg_str = msg_str + chr(2) + translateExtended ("No such Sales User Initial.", lvcarea, "")
            err_code = 1

        return generate_output()

    if not mc_types or not(mc_types.nr == nr):
        mc_types = db_session.query(Mc_types).filter(
            (Mc_types.nr == nr)).first()

    if not mc_types:
        msg_str = msg_str + chr(2) + translateExtended ("No such membership card type number.", lvcarea, "")
        err_code = 2

        return generate_output()

    if curr_mode.lower()  == ("new").lower() :

        if not gbuff or not(gbuff.cardnum.lower()  == (cardnum).lower()):
            gbuff = db_session.query(Gbuff).filter(
                (func.lower(Gbuff.cardnum) == (cardnum).lower())
                ).first()

        if gbuff:

            if not gast or not(gast.gastnr == gbuff.gastnr):
                gast = db_session.query(Gast).filter(
                    (Gast.gastnr == gbuff.gastnr)).first()

            if gast:
                gname = gast.name + " " + gast.vorname1 + ", " + gast.anrede1
            msg_str = msg_str + chr(2) + translateExtended ("Card number already exist and owned by", lvcarea, "") + " - " + gname
            err_code = 3

        return generate_output()

    elif curr_mode.lower()  == ("chg").lower() :

        # if not gbuff or not(gbuff.cardnum.lower()  == (cardnum).lower()  and gbuff._recid != mc_guest._recid):
        gbuff = db_session.query(Gbuff).filter(
            (func.lower(Gbuff.cardnum) == (cardnum).lower()) &  
            (Gbuff._recid != mc_guest._recid)).first()

        if gbuff:

            # if not gast or not(gast.gastnr == gbuff.gastnr):
            gast = db_session.query(Gast).filter(
                (Gast.gastnr == gbuff.gastnr)).first()

            if gast:
                gname = gast.name + " " + gast.vorname1 + ", " + gast.anrede1
            msg_str = msg_str + chr(2) + translateExtended ("Card number already exist and owned by", lvcarea, "") + " - " + gname
            err_code = 3

            return generate_output()

        # if not tbuff or not(tbuff.nr == mc_guest.nr):
        tbuff = db_session.query(Tbuff).filter(
            (Tbuff.nr == mc_guest.nr)).first()

        if nr != mc_guest.nr and tbuff.bezeich.lower()  == ("THE ONE").lower() :

            # if not mc_aclub or not(mc_aclub.key == tbuff.nr and mc_aclub.cardnum == mc_guest.cardnum):
            mc_aclub = db_session.query(Mc_aclub).filter(
                (Mc_aclub.key == tbuff.nr) &  (Mc_aclub.cardnum == mc_guest.cardnum)).first()

            if mc_aclub:
                msg_str = msg_str + chr(2) + translateExtended ("THE ONE Point transaction exists, TYPE changes no longer allowed.", lvcarea, "")
                err_code = 4

        return generate_output()