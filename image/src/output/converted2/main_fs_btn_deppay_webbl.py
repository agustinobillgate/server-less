#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser

def main_fs_btn_deppay_webbl(veran_nr:int, veran_seite:int, curr_date:date):

    prepare_cache ([Bk_reser])

    error_nr = 0
    bk_reser = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_nr, bk_reser
        nonlocal veran_nr, veran_seite, curr_date

        return {"error_nr": error_nr}


    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, veran_nr)],"veran_seite": [(eq, veran_seite)],"resstatus": [(eq, 1)]})

    if not bk_reser:
        error_nr = 1

        return generate_output()

    if bk_reser.datum <= curr_date and bk_reser:
        error_nr = 2

        return generate_output()

    return generate_output()