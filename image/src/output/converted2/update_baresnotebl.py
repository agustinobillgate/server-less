#using conversion tools version: 1.0.0.111

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


    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

    if bk_veran:
        pass
        bk_veran.bemerkung = efield_screen_value
        pass
        pass

    return generate_output()