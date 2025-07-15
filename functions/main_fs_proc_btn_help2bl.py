#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_func, Bk_raum

def main_fs_proc_btn_help2bl(room:string, bkf_veran_nr:int, bkf_veran_seite:int, bkf_raeume_1:string):

    prepare_cache ([Bk_reser, Bk_func])

    err = 0
    t_raeume = ""
    bk_reser = bk_func = bk_raum = None

    rsv2 = bk_reser1 = bkfc = None

    Rsv2 = create_buffer("Rsv2",Bk_reser)
    Bk_reser1 = create_buffer("Bk_reser1",Bk_reser)
    Bkfc = create_buffer("Bkfc",Bk_func)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, t_raeume, bk_reser, bk_func, bk_raum
        nonlocal room, bkf_veran_nr, bkf_veran_seite, bkf_raeume_1
        nonlocal rsv2, bk_reser1, bkfc


        nonlocal rsv2, bk_reser1, bkfc

        return {"err": err, "t_raeume": t_raeume}


    bk_raum = get_cache (Bk_raum, {"raum": [(eq, room)]})

    if bk_raum:

        bk_reser1 = get_cache (Bk_reser, {"veran_nr": [(eq, bkf_veran_nr)],"veran_resnr": [(eq, bkf_veran_seite)]})

        if bk_reser1:

            rsv2 = get_cache (Bk_reser, {"datum": [(eq, bk_reser1.datum)],"raum": [(eq, bkf_raeume_1)],"resstatus": [(eq, bk_reser1.resstatus)],"von_i": [(ge, bk_reser1.bis_i)],"bis_i": [(le, bk_reser1.von_i)],"_recid": [(ne, bk_reser1._recid)]})

            if not rsv2:
                err = 1
            else:

                bkfc = get_cache (Bk_func, {"veran_nr": [(eq, bkf_veran_nr)],"veran_seite": [(eq, bkf_veran_seite)]})
                t_raeume = bkfc.raeume[0]
                err = 2

    return generate_output()