from functions.additional_functions import *
import decimal
from models import Billhis

def read_billhisbl(case_type:int, billno:int, resno:int, reslinno:int):
    bill_exist = False
    t_billhis_list = []
    billhis = None

    t_billhis = None

    t_billhis_list, T_billhis = create_model_like(Billhis)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_exist, t_billhis_list, billhis


        nonlocal t_billhis
        nonlocal t_billhis_list
        return {"bill_exist": bill_exist, "t-billhis": t_billhis_list}

    pass


    if case_type == 1:

        billhis = db_session.query(Billhis).filter(
                (Billhis.rechnr == billno)).first()

        if billhis:
            t_billhis = T_billhis()
            t_billhis_list.append(t_billhis)

            buffer_copy(billhis, t_billhis)
            bill_exist = True
    elif case_type == 2:

        billhis = db_session.query(Billhis).filter(
                (Billhis.rechnr == billno)).first()

        if billhis:
            bill_exist = True

    return generate_output()