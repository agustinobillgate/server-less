from functions.additional_functions import *
import decimal
from models import Bk_reser

def prepare_chg_bastatus_linebl(r_recid:int):
    sorttype = 0
    bk_reser_resstatus = 0
    bk_reser = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sorttype, bk_reser_resstatus, bk_reser


        return {"sorttype": sorttype, "bk_reser_resstatus": bk_reser_resstatus}


    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser._recid == r_recid)).first()

    if bk_reser and bk_reser.resstatus <= 2:
        sorttype = bk_reser.resstatus
        bk_reser_resstatus = bk_reser.resstatus

    return generate_output()