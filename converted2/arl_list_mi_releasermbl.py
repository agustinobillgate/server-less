#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Res_line, Outorder, Zinrstat, Zimmer

def arl_list_mi_releasermbl(rec_id:int, user_init:string):

    prepare_cache ([Bediener, Res_line, Zinrstat, Zimmer])

    fl_error = 0
    user_nr:int = 0
    oos_flag:bool = False
    bediener = res_line = outorder = zinrstat = zimmer = None

    ubuff = None

    Ubuff = create_buffer("Ubuff",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_error, user_nr, oos_flag, bediener, res_line, outorder, zinrstat, zimmer
        nonlocal rec_id, user_init
        nonlocal ubuff


        nonlocal ubuff

        return {"fl_error": fl_error}


    res_line = get_cache (Res_line, {"_recid": [(eq, rec_id)]})

    if not res_line:

        return generate_output()

    # outorder = get_cache (Outorder, {"zinr": [(eq, res_line.zinr)],"gespstart": [(ge, res_line.ankunft)],"gespende": [(le, res_line.ankunft)]})
    outorder = db_session.query(Outorder).filter(
             (Outorder.zinr == res_line.zinr) & (Outorder.gespstart >= res_line.ankunft) & (Outorder.gespende <= res_line.ankunft)).with_for_update().first()
    if not outorder:
        fl_error = 1

        return generate_output()
    oos_flag = (outorder.betriebsnr == 3 or outorder.betriebsnr == 4)

    if oos_flag and (outorder.gespstart == outorder.gespende):

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "oos")],"datum": [(eq, outorder.gespende)]})

        if not zinrstat:
            zinrstat = Zinrstat()
            db_session.add(zinrstat)

            zinrstat.datum = outorder.gespende
            zinrstat.zinr = "oos"


        zinrstat.zimmeranz = zinrstat.zimmeranz + 1
    pass
    db_session.delete(outorder)
    pass

    ubuff = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if ubuff:
        user_nr = ubuff.nr

    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

    if zimmer.zistatus == 6:
        zimmer.zistatus = 2
        zimmer.bediener_nr_stat = user_nr


    pass
    fl_error = 2

    return generate_output()