from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Outorder

def mk_resline_reslin_list_zinr1bl(last_zinr:str, r_resnr:int):
    err_code = 0
    outorder = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, outorder
        nonlocal last_zinr, r_resnr


        return {"err_code": err_code}


    outorder = db_session.query(Outorder).filter(
             (func.lower(Outorder.zinr) == (last_zinr).lower()) & (Outorder.betriebsnr == r_resnr)).first()

    if outorder:
        err_code = 1

    return generate_output()