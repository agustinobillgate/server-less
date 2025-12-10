#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Debitor

def delete_debitorbl(case_type:int, int1:int):
    successflag = False
    debitor = None

    t_debitor = None

    t_debitor_data, T_debitor = create_model_like(Debitor, {"tb_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, debitor
        nonlocal case_type, int1


        nonlocal t_debitor
        nonlocal t_debitor_data

        return {"successflag": successflag}

    if case_type == 1:

        # debitor = get_cache (Debitor, {"_recid": [(eq, int1)]})
        debitor = db_session.query(Debitor).filter(
                 (Debitor._recid == int1)).with_for_update().first()

        if debitor:
            db_session.delete(debitor)
            
            successflag = True

    return generate_output()