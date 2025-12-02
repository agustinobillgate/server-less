#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 25-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Outorder, Bediener, Zimmer

def arl_list_mi_blockrmbl(pvilanguage:int, rec_id:int, creason:string, bediener_nr:int):

    prepare_cache ([Res_line, Outorder, Bediener, Zimmer])

    msg_str = ""
    lvcarea:string = "arl-list"
    user_nr:string = ""
    res_line = outorder = bediener = zimmer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, user_nr, res_line, outorder, bediener, zimmer
        nonlocal pvilanguage, rec_id, creason, bediener_nr

        return {"msg_str": msg_str}


    res_line = get_cache (Res_line, {"_recid": [(eq, rec_id)]})

    if res_line:

        # outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"gespstart": [(ge, res_line.ankunft)],"gespende": [(le, res_line.ankunft)]})
        outorder = db_session.query(Outorder).filter(
            (Outorder.zinr == res_line.zinr) & (Outorder.gespstart >= res_line.ankunft) & (Outorder.gespende <= res_line.ankunft)).with_for_update().first()

        if outorder:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Room already blocked from", lvcarea, "") + " " + to_string(outorder.gespstart) + " " + translateExtended ("to", lvcarea, "") + " " + to_string(outorder.gespend)

            return generate_output()

        bediener = get_cache (Bediener, {"nr": [(eq, bediener_nr)]})

        if bediener:
            user_nr = bediener.userinit
        else:
            user_nr = to_string(bediener_nr)


        outorder = Outorder()
        db_session.add(outorder)

        outorder.zinr = res_line.zinr
        outorder.gespstart = res_line.ankunft
        outorder.gespende = res_line.ankunft
        outorder.betriebsnr = res_line.resnr
        db_session.refresh(outorder, with_for_update=True) 

        pass

        # zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
        zimmer = db_session.query(Zimmer).filter(Zimmer.zinr == res_line.zinr).with_for_update().first()

        if zimmer:
            zimmer.bediener_nr_stat = bediener_nr
            pass
            pass
        db_session.refresh(zimmer, with_for_update=True)

    return generate_output()