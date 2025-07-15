#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_func

def main_fs_proc_btn_help3bl(bkf_veran_nr:int, bkf_veran_seite:int, bkf_raeume1:string, ending_i:int, begin_i:int):

    prepare_cache ([Bk_reser, Bk_func])

    t_uhrzeit = ""
    err = 0
    bk_reser = bk_func = None

    rsv2 = bk_reser1 = bkfc = None

    Rsv2 = create_buffer("Rsv2",Bk_reser)
    Bk_reser1 = create_buffer("Bk_reser1",Bk_reser)
    Bkfc = create_buffer("Bkfc",Bk_func)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_uhrzeit, err, bk_reser, bk_func
        nonlocal bkf_veran_nr, bkf_veran_seite, bkf_raeume1, ending_i, begin_i
        nonlocal rsv2, bk_reser1, bkfc


        nonlocal rsv2, bk_reser1, bkfc

        return {"t_uhrzeit": t_uhrzeit, "err": err}


    bk_reser1 = get_cache (Bk_reser, {"veran_nr": [(eq, bkf_veran_nr)],"veran_resnr": [(eq, bkf_veran_seite)]})

    if bk_reser1:

        rsv2 = get_cache (Bk_reser, {"datum": [(eq, bk_reser1.datum)],"raum": [(eq, bkf_raeume1)],"resstatus": [(eq, bk_reser1.resstatus)],"von_i": [(ge, ending_i)],"bis_i": [(le, begin_i)],"_recid": [(ne, bk_reser1._recid)]})

        if not rsv2:
            err = 1
        else:
            err = 2

            bkfc = get_cache (Bk_func, {"veran_nr": [(eq, bkf_veran_nr)],"veran_seite": [(eq, bkf_veran_seite)]})
            t_uhrzeit = bkfc.uhrzeiten[0]

    return generate_output()