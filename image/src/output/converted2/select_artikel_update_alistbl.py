#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser

def select_artikel_update_alistbl(veran_nr:int, veran_seite:int, curr_date:date):

    prepare_cache ([Bk_reser])

    from_i = 0
    to_i = 0
    bk_reser = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_i, to_i, bk_reser
        nonlocal veran_nr, veran_seite, curr_date

        return {"from_i": from_i, "to_i": to_i}


    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, veran_nr)],"veran_resnr": [(eq, veran_seite)],"resstatus": [(le, 3)],"datum": [(eq, curr_date)]})
    from_i = bk_reser.von_i
    to_i = bk_reser.bis_i

    return generate_output()