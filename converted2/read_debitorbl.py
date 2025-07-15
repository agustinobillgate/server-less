#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Debitor

def read_debitorbl(case_type:int, artno:int, billno:int, billdate:date, saldo:Decimal, inp_opart:int, inp_konto:int):
    t_debitor_data = []
    debitor = None

    t_debitor = None

    t_debitor_data, T_debitor = create_model_like(Debitor, {"tb_recid":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_debitor_data, debitor
        nonlocal case_type, artno, billno, billdate, saldo, inp_opart, inp_konto


        nonlocal t_debitor
        nonlocal t_debitor_data

        return {"t-debitor": t_debitor_data}

    if case_type == 1:

        debitor = get_cache (Debitor, {"artnr": [(eq, artno)],"rechnr": [(eq, billno)],"opart": [(eq, inp_opart)],"zahlkonto": [(eq, inp_konto)]})
    elif case_type == 2:

        debitor = get_cache (Debitor, {"artnr": [(eq, artno)],"rechnr": [(eq, billno)],"opart": [(eq, inp_opart)],"zahlkonto": [(gt, inp_konto)]})
    elif case_type == 3:

        debitor = get_cache (Debitor, {"artnr": [(eq, artno)],"rechnr": [(eq, billno)],"opart": [(eq, inp_opart)],"zahlkonto": [(eq, inp_konto)]})
    elif case_type == 4:

        debitor = get_cache (Debitor, {"artnr": [(eq, artno)],"rechnr": [(eq, billno)],"rgdatum": [(eq, billdate)],"opart": [(eq, inp_opart)],"zahlkonto": [(eq, inp_konto)]})
    elif case_type == 5:

        debitor = get_cache (Debitor, {"artnr": [(eq, artno)],"rechnr": [(eq, billno)],"rgdatum": [(eq, billdate)],"saldo": [(eq, saldo)],"opart": [(eq, inp_opart)],"zahlkonto": [(eq, inp_konto)]})
    elif case_type == 6:

        debitor = get_cache (Debitor, {"artnr": [(eq, artno)],"rechnr": [(eq, billno)],"rgdatum": [(eq, billdate)],"saldo": [(eq, - saldo)],"counter": [(eq, inp_opart)]})
    elif case_type == 7:

        debitor = get_cache (Debitor, {"_recid": [(eq, artno)]})
    elif case_type == 8:

        debitor = db_session.query(Debitor).filter(
                 (Debitor.counter == inp_opart) & (Debitor.zahlkonto > 0) & (Debitor.rgdatum <= billdate)).first()
    elif case_type == 9:

        debitor = get_cache (Debitor, {"rechnr": [(eq, billno)],"artnr": [(eq, artno)],"gastnr": [(eq, inp_konto)],"gastnrmember": [(eq, inp_konto)],"rgdatum": [(eq, billdate)],"saldo": [(eq, - saldo)],"counter": [(eq, 0)]})
    elif case_type == 99:

        debitor = get_cache (Debitor, {"_recid": [(eq, artno)]})

    if debitor:
        t_debitor = T_debitor()
        t_debitor_data.append(t_debitor)

        buffer_copy(debitor, t_debitor)
        t_debitor.tb_recid = debitor._recid

    return generate_output()