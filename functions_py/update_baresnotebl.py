#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran

def update_baresnotebl(resnr:int, efield_screen_value:string):

    prepare_cache ([Bk_veran])

    bk_veran = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_veran
        nonlocal resnr, efield_screen_value

        return {}


    # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})
    bk_veran = db_session.query(Bk_veran).filter(
             (Bk_veran.veran_nr == resnr)).with_for_update().first()

    if bk_veran:
        bk_veran.bemerkung = efield_screen_value


    return generate_output()