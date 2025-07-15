#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Bk_reser

def rsv_list_btn_chgbl(output_list_resstatus:int, output_list_resnr:int, output_list_reslinnr:int):

    prepare_cache ([Bk_veran, Bk_reser])

    recid_bk_reser = 0
    avail_bk_reser = False
    bk_veran = bk_reser = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal recid_bk_reser, avail_bk_reser, bk_veran, bk_reser
        nonlocal output_list_resstatus, output_list_resnr, output_list_reslinnr

        return {"recid_bk_reser": recid_bk_reser, "avail_bk_reser": avail_bk_reser}


    if output_list_resstatus == 1:

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, output_list_resnr)]})

        if bk_veran:

            if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) != 0:

                bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(ne, output_list_reslinnr)],"resstatus": [(eq, 1)]})

                if not bk_reser:
                    avail_bk_reser = False

                    return generate_output()
                else:
                    avail_bk_reser = True
                    recid_bk_reser = bk_reser._recid
            else:

                bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(eq, output_list_reslinnr)],"resstatus": [(eq, 1)]})

                if bk_reser:
                    avail_bk_reser = True
                    recid_bk_reser = bk_reser._recid
    else:

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, output_list_resnr)]})

        if bk_veran:

            if (bk_veran.deposit_payment[0] + bk_veran.deposit_payment[1] + bk_veran.deposit_payment[2] + bk_veran.deposit_payment[3] + bk_veran.deposit_payment[4] + bk_veran.deposit_payment[5] + bk_veran.deposit_payment[6] + bk_veran.deposit_payment[7] + bk_veran.deposit_payment[8]) != 0:

                bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(eq, output_list_reslinnr)],"resstatus": [(eq, output_list_resstatus)]})

                if bk_reser:
                    avail_bk_reser = True
                    recid_bk_reser = bk_reser._recid
                else:
                    avail_bk_reser = False

                    return generate_output()
            else:

                bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)],"veran_resnr": [(eq, output_list_reslinnr)],"resstatus": [(eq, output_list_resstatus)]})

                if bk_reser:
                    avail_bk_reser = True
                    recid_bk_reser = bk_reser._recid

    return generate_output()