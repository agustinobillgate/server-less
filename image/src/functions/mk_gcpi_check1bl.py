from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener

def mk_gcpi_check1bl(rcvname:str):
    avail_bed = False
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_bed, bediener


        return {"avail_bed": avail_bed}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.username) == (rcvname).lower())).first()

    if bediener:
        avail_bed = True

    return generate_output()