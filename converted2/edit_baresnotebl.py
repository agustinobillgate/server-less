#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran

def edit_baresnotebl(resnr:int):

    prepare_cache ([Bk_veran])

    efield = ""
    bk_veran = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal efield, bk_veran
        nonlocal resnr

        return {"efield": efield}


    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

    if bk_veran:
        efield = bk_veran.bemerkung

    return generate_output()