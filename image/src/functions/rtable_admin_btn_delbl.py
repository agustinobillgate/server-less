from functions.additional_functions import *
import decimal
from models import Tisch, H_bill

def rtable_admin_btn_delbl(dept:int, t_tischnr:int):
    flag = 0
    tisch = h_bill = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, tisch, h_bill


        return {"flag": flag}


    tisch = db_session.query(Tisch).filter(
            (Tisch.departement == dept) &  (Tischnr == t_tischnr)).first()

    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == dept) &  (H_bill.tischnr == t_tischnr)).first()

    if h_bill:
        flag = 1
    else:

        tisch = db_session.query(Tisch).first()
        db_session.delete(tisch)

    return generate_output()