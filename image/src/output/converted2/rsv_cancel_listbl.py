#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.ba_cancreslinebl import ba_cancreslinebl
from models import Bk_veran, Bk_reser, Guest, Bk_raum, B_storno

def rsv_cancel_listbl(bqt_resnr:int, bqt_reslinnr:int, user_init:string):

    prepare_cache ([Bk_veran, Bk_reser, B_storno])

    msg_str = ""
    cancel_str:string = ""
    bk_veran = bk_reser = guest = bk_raum = b_storno = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, cancel_str, bk_veran, bk_reser, guest, bk_raum, b_storno
        nonlocal bqt_resnr, bqt_reslinnr, user_init

        return {"msg_str": msg_str}


    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bqt_resnr)]})

    if bk_veran:

        if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) > 0:

            bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(ne, bqt_reslinnr)],"resstatus": [(eq, 1)]})

            if not bk_reser:
                msg_str = "Deposit exists, cancel reservation not possible."

                return generate_output()

        if bk_veran.rechnr > 0:

            bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(ne, bqt_reslinnr)],"resstatus": [(eq, 1)]})

            if not bk_reser:
                msg_str = "Bill exists, cancel reservation not possible."

                return generate_output()

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bqt_resnr)],"veran_seite": [(eq, bqt_reslinnr)]})

        guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_reser.raum)]})

        b_storno = get_cache (B_storno, {"bankettnr": [(eq, bk_reser.veran_nr)],"breslinnr": [(eq, bk_reser.veran_resnr)]})

        if not b_storno:
            b_storno = B_storno()
            db_session.add(b_storno)

        b_storno.bankettnr = bk_reser.veran_nr
        b_storno.breslinnr = bk_reser.veran_resnr
        b_storno.gastnr = bk_veran.gastnr
        b_storno.betrieb_gast = bk_veran.gastnrver
        b_storno.datum = bk_reser.datum
        b_storno.grund[17] = cancel_str + " D*" +\
                to_string(get_current_date(), "99/99/99") + " " + to_string(get_current_time_in_seconds(), "hh:mm:ss") +\
                " " + bk_reser.raum


        b_storno.usercode = user_init
        get_output(ba_cancreslinebl(bk_reser.veran_nr, bk_reser.veran_resnr))

    return generate_output()