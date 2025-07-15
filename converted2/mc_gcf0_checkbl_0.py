from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Mc_guest, Bediener, Guest, Mc_types, Mc_aclub

def mc_gcf0_checkbl(pvilanguage:int, gastno:int, curr_mode:str, sales_id:str, nr:int, cardnum:str):
    err_code = 0
    msg_str = ""
    lvcarea:str = "mc_gcf"
    gname:str = ""
    mc_guest = bediener = guest = mc_types = mc_aclub = None

    g_list = bbuff = gbuff = gast = tbuff = None

    g_list_list, G_list = create_model_like(Mc_guest)

    Bbuff = Bediener
    Gbuff = Mc_guest
    Gast = Guest
    Tbuff = Mc_types

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, msg_str, lvcarea, gname, mc_guest, bediener, guest, mc_types, mc_aclub
        nonlocal bbuff, gbuff, gast, tbuff

        nonlocal g_list, bbuff, gbuff, gast, tbuff
        nonlocal g_list_list
        print("Code/Str:" + str(err_code) + "/" + msg_str) 
        return {"err_code": err_code, "msg_str": msg_str}

    mc_guest = db_session.query(Mc_guest).filter(
            (Mc_guest.gastnr == gastno)).first()

    if sales_id != "":

        bbuff = db_session.query(Bbuff).filter(
                (func.lower(Bbuff.userinit) == (sales_id).lower())
                ).first()

        if not bbuff:
            msg_str = msg_str + chr(2) + translateExtended ("No such Sales User Initial.", lvcarea, "")
            err_code = 1

        return generate_output()

    mc_types = db_session.query(Mc_types).filter(
            (Mc_types.nr == nr)).first()

    if not mc_types:
        msg_str = msg_str + chr(2) + translateExtended ("No such membership card type number.", lvcarea, "")
        err_code = 2

        return generate_output()

    if curr_mode.lower()  == "new":

        gbuff = db_session.query(Gbuff).filter(
                (func.lower(Gbuff.cardnum)) == (cardnum).lower()).first()

        if gbuff:
            gast = db_session.query(Gast).filter(
                    (Gast.gastnr == gbuff.gastnr)).first()

            if gast:
                gname = gast.name + " " + gast.vorname1 + ", " + gast.anrede1
            msg_str = msg_str + chr(2) + translateExtended ("Card number already exist and owned by", lvcarea, "") + " - " + gname
            err_code = 3

        return generate_output()

    elif curr_mode.lower()  == "chg":

        gbuff = db_session.query(Gbuff).filter(
                (func.lower(Gbuff.cardnum) == (cardnum).lower()) &  
                (Gbuff._recid != mc_guest._recid)).first()

        if gbuff:

            gast = db_session.query(Gast).filter(
                    (Gast.gastnr == gbuff.gastnr)).first()

            if gast:
                gname = gast.name + " " + gast.vorname1 + ", " + gast.anrede1
            
                msg_str = msg_str + chr(2) + translateExtended ("Card number already exist and owned by", lvcarea, "") + " - " + gname
                err_code = 3

            return generate_output()

        tbuff = db_session.query(Tbuff).filter(
                (Tbuff.nr == mc_guest.nr)).first()

        if nr != mc_guest.nr and tbuff.bezeich.lower()  == ("THE ONE").lower():

            mc_aclub = db_session.query(Mc_aclub).filter(
                    (Mc_aclub.key == tbuff.nr) &  
                    (Mc_aclub.cardnum == mc_guest.cardnum)
                ).first()

            if mc_aclub:
                msg_str = msg_str + chr(2) + translateExtended ("THE ONE Point transaction exists, TYPE changes no longer allowed.", lvcarea, "")
                err_code = 4

            return generate_output()