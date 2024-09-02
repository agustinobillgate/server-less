from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bk_rset

def ba_rmsetup_btndelbl(rset_bezeich:str):
    bk_rset = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_rset


        return {}


    bk_rset = db_session.query(Bk_rset).filter(
            (func.lower(Bk_rset.bezeich) == (rset_bezeich).lower())).first()
    db_session.delete(bk_rset)

    return generate_output()