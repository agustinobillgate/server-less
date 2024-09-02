from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Fa_lager

def fa_artlist_locatebl(locate:str):
    avail_fa_lager = False
    fa_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_fa_lager, fa_lager


        return {"avail_fa_lager": avail_fa_lager}


    fa_lager = db_session.query(Fa_lager).filter(
            (func.lower(Fa_lager.bezeich) == (locate).lower())).first()

    if fa_lager:
        avail_fa_lager = True

    return generate_output()