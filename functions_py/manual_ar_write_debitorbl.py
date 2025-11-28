#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import Debitor

t_debitor_data, T_debitor = create_model_like(Debitor, {"tb_recid":int})

def manual_ar_write_debitorbl(case_type:int, t_debitor_data:[T_debitor]):

    prepare_cache ([Debitor])

    successflag = True
    debitor = None

    t_debitor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal successflag, debitor
        nonlocal case_type


        nonlocal t_debitor

        return {"successflag": successflag}

    t_debitor = query(t_debitor_data, first=True)

    if not t_debitor:

        return generate_output()

    if case_type == 1:
        debitor = Debitor()
        db_session.add(debitor)

        buffer_copy(t_debitor, debitor)
        successflag = True


    elif case_type == 2:

        debitor = db_session.query(Debitor).filter(Debitor._recid == t_debitor.tb_recid).with_for_update().first()  

        if debitor:
            debitor.vesrcod = t_debitor.vesrcod
            debitor.versanddat = t_debitor.versanddat
            debitor.mahnstufe = t_debitor.mahnstufe
            pass
            successflag = True

    return generate_output()