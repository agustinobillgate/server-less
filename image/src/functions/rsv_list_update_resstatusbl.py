from functions.additional_functions import *
import decimal
from models import Bk_func, Bk_reser, Bk_veran

def rsv_list_update_resstatusbl(output_list_resnr:int, output_list_reslinnr:int, r_status:int, c_status:str):
    output_list_str = ""
    output_list_resstatus = 0
    output_list_sob = ""
    gastnr = 0
    output_list_gastnr = 0
    bk_func = bk_reser = bk_veran = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_str, output_list_resstatus, output_list_sob, gastnr, output_list_gastnr, bk_func, bk_reser, bk_veran


        return {"output_list_str": output_list_str, "output_list_resstatus": output_list_resstatus, "output_list_sob": output_list_sob, "gastnr": gastnr, "output_list_gastnr": output_list_gastnr}

    def update_resstatus():

        nonlocal output_list_str, output_list_resstatus, output_list_sob, gastnr, output_list_gastnr, bk_func, bk_reser, bk_veran

        bk_func = db_session.query(Bk_func).filter(
                    (Bk_func.veran_nr == output_list_resnr) &  (Bk_func.veran_seite == output_list_reslinnr)).first()
        bk_func.resstatus = r_status
        bk_func.r_resstatus[0] = r_status
        bk_func.c_resstatus[0] = c_status

        bk_func = db_session.query(Bk_func).first()

        bk_reser = db_session.query(Bk_reser).filter(
                    (Bk_reser.veran_nr == output_list_resnr) &  (Bk_reser.veran_seite == output_list_reslinnr)).first()
        bk_reser.resstatus = r_status

        bk_reser = db_session.query(Bk_reser).first()

        bk_veran = db_session.query(Bk_veran).filter(
                    (Bk_veran.veran_nr == output_list_resnr)).first()
        bk_veran.resstatus = r_status

        bk_veran = db_session.query(Bk_veran).first()
        output_list_str = to_string(bk_func.bis_datum, "99/99/99") +\
                to_string(bk_func.bestellt__durch, "x(32)") +\
                to_string(bk_func.v_kontaktperson[0], "x(32)") +\
                to_string(bk_func.zweck[0], "x(18)") +\
                to_string(bk_func.raeume[0], "x(12)") +\
                to_string(bk_func.uhrzeit, "x(13)") +\
                to_string(bk_func.personen, ">,>>>") +\
                to_string(bk_veran.deposit, ">>>,>>>,>>9") +\
                to_string(bk_veran.total_paid, ">>>,>>>,>>9") +\
                to_string(bk_func.vgeschrieben, "x(2)") +\
                to_string(bk_func.veran_nr, ">>>,>>>") +\
                to_string(bk_func.veran_seite, ">>>") +\
                to_string(bk_func.c_resstatus[0], "x(1)")
        output_list_resnr = bk_func.veran_nr
        output_list_reslinnr = bk_func.veran_seite
        output_list_resstatus = bk_func.resstatus


        output_list_sob = bk_func.technik[1]
        gastnr = bk_veran.gastnr
        output_list_gastnr = bk_veran.gastnr


    update_resstatus()

    return generate_output()