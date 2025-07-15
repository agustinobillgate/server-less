#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Billhis

def read_billhisbl(case_type:int, billno:int, resno:int, reslinno:int):
    bill_exist = False
    t_billhis_data = []
    billhis = None

    t_billhis = None

    t_billhis_data, T_billhis = create_model_like(Billhis)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_exist, t_billhis_data, billhis
        nonlocal case_type, billno, resno, reslinno


        nonlocal t_billhis
        nonlocal t_billhis_data

        return {"bill_exist": bill_exist, "t-billhis": t_billhis_data}


    if case_type == 1:

        billhis = get_cache (Billhis, {"rechnr": [(eq, billno)]})

        if billhis:
            t_billhis = T_billhis()
            t_billhis_data.append(t_billhis)

            buffer_copy(billhis, t_billhis)
            bill_exist = True
    elif case_type == 2:

        billhis = get_cache (Billhis, {"rechnr": [(eq, billno)]})

        if billhis:
            bill_exist = True

    return generate_output()