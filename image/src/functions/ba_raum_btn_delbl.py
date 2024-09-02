from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bk_rset, Bk_raum

def ba_raum_btn_delbl(rec_id:int, t_raum:str):
    err = 0
    bk_rset = bk_raum = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, bk_rset, bk_raum


        return {"err": err}


    bk_rset = db_session.query(Bk_rset).filter(
            (func.lower(Bk_rset.raum) == (t_raum).lower())).first()

    if bk_rset:
        err = 1

        return generate_output()

    bk_raum = db_session.query(Bk_raum).filter(
            (Bk_raum._recid == rec_id)).first()
    db_session.delete(bk_raum)


    return generate_output()