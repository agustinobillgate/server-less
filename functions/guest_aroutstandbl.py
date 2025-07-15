#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Debitor

def guest_aroutstandbl(gastno:int, zahlungsart:int):

    prepare_cache ([Debitor])

    outstand = to_decimal("0.0")
    debitor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstand, debitor
        nonlocal gastno, zahlungsart

        return {"outstand": outstand}


    for debitor in db_session.query(Debitor).filter(
             (Debitor.artnr == zahlungsart) & (Debitor.gastnr == gastno) & (Debitor.opart <= 1)).order_by(Debitor._recid).all():
        outstand =  to_decimal(outstand) + to_decimal(debitor.saldo)

    return generate_output()