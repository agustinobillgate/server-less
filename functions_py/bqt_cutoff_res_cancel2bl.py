#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.ba_cancreslinebl import ba_cancreslinebl
from models import Bk_veran, Bk_reser, B_storno
from sqlalchemy.orm.attributes import flag_modified

def bqt_cutoff_res_cancel2bl(recid_bk_reser:int, o_resnr:int, cancel_str:string, user_init:string):

    prepare_cache ([Bk_veran, Bk_reser, B_storno])

    bk_veran = bk_reser = b_storno = None

    db_session = local_storage.db_session
    cancel_str = cancel_str.strip()

    def generate_output():
        nonlocal bk_veran, bk_reser, b_storno
        nonlocal recid_bk_reser, o_resnr, cancel_str, user_init

        return {}


    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, o_resnr)]})

    if not bk_veran:

        return generate_output()

    bk_reser = get_cache (Bk_reser, {"_recid": [(eq, recid_bk_reser)]})

    if not bk_reser:

        return generate_output()

    # b_storno = get_cache (B_storno, {"bankettnr": [(eq, bk_reser.veran_nr)],"breslinnr": [(eq, bk_reser.veran_resnr)]})
    b_storno = db_session.query(B_storno).filter(
             (B_storno.bankettnr == bk_reser.veran_nr) &
             (B_storno.breslinnr == bk_reser.veran_resnr)).with_for_update().first()

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
    flag_modified(b_storno, "grund")
    pass
    get_output(ba_cancreslinebl(bk_reser.veran_nr, bk_reser.veran_resnr))

    return generate_output()