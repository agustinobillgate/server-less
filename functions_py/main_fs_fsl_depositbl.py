#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran

def main_fs_fsl_depositbl(fsl_veran_nr:int, fsl_deposit:Decimal):
    buf_bkveran_data = []
    bk_veran = None

    buf_bkveran = None

    buf_bkveran_data, Buf_bkveran = create_model_like(Bk_veran)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal buf_bkveran_data, bk_veran
        nonlocal fsl_veran_nr, fsl_deposit


        nonlocal buf_bkveran
        nonlocal buf_bkveran_data

        return {"buf-bkveran": buf_bkveran_data}


    buf_bkveran_data.clear()

    # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, fsl_veran_nr)]})
    bk_veran = db_session.query(Bk_veran).filter(
             (Bk_veran.veran_nr == fsl_veran_nr)).with_for_update().first()

    if bk_veran:
        pass
        bk_veran.deposit =  to_decimal(fsl_deposit)
        buf_bkveran = Buf_bkveran()
        buf_bkveran_data.append(buf_bkveran)

        buffer_copy(bk_veran, buf_bkveran)
        pass
        pass

    return generate_output()