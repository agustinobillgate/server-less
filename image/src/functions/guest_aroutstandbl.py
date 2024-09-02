from functions.additional_functions import *
import decimal
from models import Debitor

def guest_aroutstandbl(gastno:int, zahlungsart:int):
    outstand = 0
    debitor = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstand, debitor


        return {"outstand": outstand}


    for debitor in db_session.query(Debitor).filter(
            (Debitor.artnr == zahlungsart) &  (Debitor.gastnr == gastno) &  (Debitor.opart <= 1)).all():
        outstand = outstand + debitor.saldo

    return generate_output()