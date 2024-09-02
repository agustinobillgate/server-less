from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_reser

def select_artikel_update_alistbl(veran_nr:int, veran_seite:int, curr_date:date):
    from_i = 0
    to_i = 0
    bk_reser = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_i, to_i, bk_reser


        return {"from_i": from_i, "to_i": to_i}


    bk_reser = db_session.query(Bk_reser).filter(
            (Bk_reser.veran_nr == veran_nr) &  (Bk_reser.veran_resnr == veran_seite) &  (Bk_reser.resstatus <= 3) &  (Bk_reser.datum == curr_date)).first()
    from_i = bk_reser.von_i
    to_i = bk_reser.bis_i

    return generate_output()