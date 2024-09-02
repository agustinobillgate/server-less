from functions.additional_functions import *
import decimal
from models import Bill

def fo_inv_del_billbl(bil_recid:int):
    msgstr = ""
    curr_recid:int = 0
    bill = None

    t_bill = None

    T_bill = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msgstr, curr_recid, bill
        nonlocal t_bill


        nonlocal t_bill
        return {"msgstr": msgstr}


    t_bill = db_session.query(T_bill).filter(
            (T_bill._recid == bil_recid)).first()

    if t_bill:
        db_session.delete(t_bill)

        msgstr = "Bill Deleted"
    else:
        msgstr = "Can't found bill record id"

    return generate_output()