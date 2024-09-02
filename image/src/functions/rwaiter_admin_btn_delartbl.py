from functions.additional_functions import *
import decimal
from models import H_bill, Kellner, Kellne1

def rwaiter_admin_btn_delartbl(dept:int, r_kellner:int, r_kellne1:int, t_kellner_nr:int):
    flag = 0
    h_bill = kellner = kellne1 = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_bill, kellner, kellne1


        return {"flag": flag}


    h_bill = db_session.query(H_bill).filter(
            (H_bill.departement == dept) &  (H_bill.kellner_nr == t_kellner_nr) &  (H_bill.flag == 0)).first()

    if h_bill:
        flag = 1
    else:

        kellner = db_session.query(Kellner).filter(
                (Kellner._recid == r_kellner)).first()

        kellne1 = db_session.query(Kellne1).filter(
                (Kellne1._recid == r_kellne1)).first()

        kellner = db_session.query(Kellner).first()
        db_session.delete(kellner)

        kellne1 = db_session.query(Kellne1).first()
        db_session.delete(kellne1)

    return generate_output()