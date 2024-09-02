from functions.additional_functions import *
import decimal
from models import H_bill, Queasy, H_queasy

def ts_restinv_del_queasybl(p_list:[P_list], rec_id:int, use_h_queasy:bool):
    h_bill = queasy = h_queasy = None

    p_list = None

    p_list_list, P_list = create_model("P_list", {"rechnr":int, "dept":int, "billno":int, "printed_line":int, "b_recid":int, "last_amount":decimal, "last_famount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill, queasy, h_queasy


        nonlocal p_list
        nonlocal p_list_list
        return {}

    def del_queasy():

        nonlocal h_bill, queasy, h_queasy


        nonlocal p_list
        nonlocal p_list_list

        if not use_h_queasy:

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 4) &  (Queasy.number1 == (h_bill.departement + h_bill.rechnr * 100)) &  (Queasy.number2 >= 0) &  (Queasy.deci2 >= 0)).all():
                db_session.delete(queasy)

        else:

            for h_queasy in db_session.query(H_queasy).filter(
                    (H_queasy.number1 == (h_bill.departement + h_bill.rechnr * 100))).all():
                db_session.delete(h_queasy)


        for p_list in query(p_list_list, filters=(lambda p_list :p_list.rechnr == h_bill.rechnr and p_list.dept == h_bill.departement)):
            p_list_list.remove(p_list)

    h_bill = db_session.query(H_bill).filter(
            (H_bill._recid == rec_id)).first()
    del_queasy()

    return generate_output()