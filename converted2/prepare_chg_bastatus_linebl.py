#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser

def prepare_chg_bastatus_linebl(r_recid:int):

    prepare_cache ([Bk_reser])

    sorttype = 0
    bk_reser_resstatus = 0
    bk_reser = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sorttype, bk_reser_resstatus, bk_reser
        nonlocal r_recid

        return {"sorttype": sorttype, "bk_reser_resstatus": bk_reser_resstatus}


    bk_reser = get_cache (Bk_reser, {"_recid": [(eq, r_recid)]})

    if bk_reser and bk_reser.resstatus <= 2:
        sorttype = bk_reser.resstatus
        bk_reser_resstatus = bk_reser.resstatus

    return generate_output()