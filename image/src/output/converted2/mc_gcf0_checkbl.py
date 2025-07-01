#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_guest, Bediener, Guest, Mc_types, Mc_aclub

def mc_gcf0_checkbl(pvilanguage:int, gastno:int, curr_mode:string, sales_id:string, nr:int, cardnum:string):

    prepare_cache ([Mc_guest, Guest, Mc_types])

    err_code = 0
    msg_str = ""
    lvcarea:string = "mc-gcf"
    gname:string = ""
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

    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastno)]})

    if sales_id != "":

        bbuff = db_session.query(Bbuff).filter(
                 (Bbuff.userinit == (sales_id).lower())).first()

        if not bbuff:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("No such Sales User Initial.", lvcarea, "")
            err_code = 1

            return generate_output()

    mc_types = get_cache (Mc_types, {"nr": [(eq, nr)]})

    if not mc_types:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("No such membership card type number.", lvcarea, "")
        err_code = 2

        return generate_output()

    if curr_mode.lower()  == ("new").lower() :

        gbuff = get_cache (Mc_guest, {"cardnum": [(eq, cardnum)]})

        if gbuff:

            gast = get_cache (Guest, {"gastnr": [(eq, gbuff.gastnr)]})

            if gast:
                gname = gast.name + " " + gast.vorname1 + ", " + gast.anrede1
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Card number already exist and owned by", lvcarea, "") + " - " + gname
            err_code = 3

            return generate_output()

    elif curr_mode.lower()  == ("chg").lower() :

        gbuff = get_cache (Mc_guest, {"cardnum": [(eq, cardnum)],"_recid": [(ne, mc_guest._recid)]})

        if gbuff:

            gast = get_cache (Guest, {"gastnr": [(eq, gbuff.gastnr)]})

            if gast:
                gname = gast.name + " " + gast.vorname1 + ", " + gast.anrede1
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Card number already exist and owned by", lvcarea, "") + " - " + gname
            err_code = 3

            return generate_output()

        tbuff = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

        if nr != mc_guest.nr and tbuff.bezeich.lower()  == ("THE ONE").lower() :

            mc_aclub = get_cache (Mc_aclub, {"key": [(eq, tbuff.nr)],"cardnum": [(eq, mc_guest.cardnum)]})

            if mc_aclub:
                msg_str = msg_str + chr_unicode(2) + translateExtended ("THE ONE Point transaction exists, TYPE changes no longer allowed.", lvcarea, "")
                err_code = 4

                return generate_output()

    return generate_output()