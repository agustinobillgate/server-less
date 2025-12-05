#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, remark area
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_veran, Bk_func
from sqlalchemy.orm.attributes import flag_modified

def rsv_list_update_resstatusbl(output_list_resnr:int, output_list_reslinnr:int, r_status:int, c_status:string):

    prepare_cache ([Bk_reser, Bk_veran, Bk_func])

    output_list_str = ""
    output_list_resstatus = 0
    output_list_sob = ""
    gastnr = 0
    output_list_gastnr = 0
    bk_reser = bk_veran = bk_func = None

    db_session = local_storage.db_session
    c_status = c_status.strip()

    def generate_output():
        nonlocal output_list_str, output_list_resstatus, output_list_sob, gastnr, output_list_gastnr, bk_reser, bk_veran, bk_func
        nonlocal output_list_resnr, output_list_reslinnr, r_status, c_status

        return {"output_list_resnr": output_list_resnr, "output_list_reslinnr": output_list_reslinnr, "output_list_str": output_list_str, "output_list_resstatus": output_list_resstatus, "output_list_sob": output_list_sob, "gastnr": gastnr, "output_list_gastnr": output_list_gastnr}

    def update_resstatus():

        nonlocal output_list_str, output_list_resstatus, output_list_sob, gastnr, output_list_gastnr, bk_reser, bk_veran, bk_func
        nonlocal output_list_resnr, output_list_reslinnr, r_status, c_status

        deposit:Decimal = to_decimal("0.0")
        total_paid:Decimal = to_decimal("0.0")

        # bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, output_list_resnr)],"veran_seite": [(eq, output_list_reslinnr)]})
        bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == output_list_resnr) &
            (Bk_reser.veran_seite == output_list_reslinnr)).with_for_update().first()

        if bk_reser:
            bk_reser.resstatus = r_status


            pass

        # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, output_list_resnr)]})
        bk_veran = db_session.query(Bk_veran).filter(
            (Bk_veran.veran_nr == output_list_resnr)).with_for_update().first

        if bk_veran:
            bk_veran.resstatus = r_status
            gastnr = bk_veran.gastnr
            output_list_gastnr = bk_veran.gastnr
            deposit =  to_decimal(bk_veran.deposit)
            total_paid =  to_decimal(bk_veran.total_paid)


            pass

        # bk_func = get_cache (Bk_func, {"veran_nr": [(eq, output_list_resnr)],"veran_seite": [(eq, output_list_reslinnr)]})
        bk_func = db_session.query(Bk_func).filter(
            (Bk_func.veran_nr == output_list_resnr) &
            (Bk_func.veran_seite == output_list_reslinnr)).with_for_update().first()

        if bk_func:
            bk_func.resstatus = r_status
            bk_func.r_resstatus[0] = r_status
            bk_func.c_resstatus[0] = c_status
            output_list_resnr = bk_func.veran_nr
            output_list_reslinnr = bk_func.veran_seite
            output_list_resstatus = bk_func.resstatus
            output_list_sob = bk_func.technik[1]
            output_list_str = to_string(bk_func.bis_datum, "99/99/99") +\
                    to_string(bk_func.bestellt__durch, "x(32)") +\
                    to_string(bk_func.v_kontaktperson[0], "x(32)") +\
                    to_string(bk_func.zweck[0], "x(18)") +\
                    to_string(bk_func.raeume[0], "x(12)") +\
                    to_string(bk_func.uhrzeit, "x(13)") +\
                    to_string(bk_func.personen, ">,>>>")
            output_list_str = output_list_str +\
                    to_string(deposit, ">>>,>>>,>>9") +\
                    to_string(total_paid, ">>>,>>>,>>9")
            output_list_str = output_list_str +\
                    to_string(bk_func.vgeschrieben, "x(2)") +\
                    to_string(bk_func.veran_nr, ">>>,>>>") +\
                    to_string(bk_func.veran_seite, ">>>") +\
                    to_string(bk_func.c_resstatus[0], "x(1)")


            pass
        flag_modified(bk_func, "r_resstatus")
        flag_modified(bk_func, "c_resstatus")

    update_resstatus()

    return generate_output()