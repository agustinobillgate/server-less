#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser

def main_fs_proc_btn_help1bl(bkf_veran_nr:int, bkf_veran_seite:int, bkf_resstatus:int):

    prepare_cache ([Bk_reser])

    rsv2_resstatus = 0
    avail_rsv2 = False
    bk_reser = None

    rsv2 = bk_reser1 = None

    Rsv2 = create_buffer("Rsv2",Bk_reser)
    Bk_reser1 = create_buffer("Bk_reser1",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rsv2_resstatus, avail_rsv2, bk_reser
        nonlocal bkf_veran_nr, bkf_veran_seite, bkf_resstatus
        nonlocal rsv2, bk_reser1


        nonlocal rsv2, bk_reser1

        return {"rsv2_resstatus": rsv2_resstatus, "avail_rsv2": avail_rsv2}


    bk_reser1 = get_cache (Bk_reser, {"veran_nr": [(eq, bkf_veran_nr)],"veran_resnr": [(eq, bkf_veran_seite)]})

    rsv2 = get_cache (Bk_reser, {"datum": [(eq, bk_reser1.datum)],"raum": [(eq, bk_reser1.raum)],"resstatus": [(eq, bkf_resstatus)],"von_i": [(ge, bk_reser1.bis_i)],"bis_i": [(le, bk_reser1.von_i)],"_recid": [(ne, bk_reser1._recid)]})

    if rsv2:
        rsv2_resstatus = rsv2.resstatus
        avail_rsv2 = True

    return generate_output()