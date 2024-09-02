from functions.additional_functions import *
import decimal
from functions.ba_cancreslinebl import ba_cancreslinebl
from models import Bk_veran, Bk_reser, B_storno

def bqt_cutoff_res_cancel2bl(recid_bk_reser:int, o_resnr:int, cancel_str:str, user_init:str):
    bk_veran = bk_reser = b_storno = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_veran, bk_reser, b_storno


        return {}


    bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == o_resnr)).first()

    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser._recid == recid_bk_reser)).first()

    b_storno = db_session.query(B_storno).filter(
            (B_storno.bankettnr == bk_reser.veran_nr) &  (B_storno.breslinnr == bk_reser.veran_resnr)).first()

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