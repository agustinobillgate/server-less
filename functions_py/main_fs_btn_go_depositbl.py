#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_veran

def main_fs_btn_go_depositbl(bk_veran_recid:int, fsl_limit_date:date):

    prepare_cache ([Bk_veran])

    bk_veran = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_veran
        nonlocal bk_veran_recid, fsl_limit_date

        return {}


    # bk_veran = get_cache (Bk_veran, {"_recid": [(eq, bk_veran_recid)]})
    bk_veran = db_session.query(Bk_veran).filter(
             (Bk_veran._recid == bk_veran_recid)).with_for_update().first()

    if bk_veran:
        pass
        bk_veran.limit_date = fsl_limit_date


        pass

    return generate_output()