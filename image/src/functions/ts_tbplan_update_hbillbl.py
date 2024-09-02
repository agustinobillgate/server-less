from functions.additional_functions import *
import decimal
from models import H_bill

def ts_tbplan_update_hbillbl(rec_id:int, hostnr:int, pax:int, gname:str, hoga_resnr:int, hoga_reslinnr:int):
    h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill


        return {}


    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    h_bill.resnr = hoga_resnr
    h_bill.reslinnr = hoga_reslinnr
    h_bill.service[1] = hostnr
    h_bill.belegung = pax
    h_bill.bilname = gname

    h_bill = db_session.query(H_bill).first()

    return generate_output()