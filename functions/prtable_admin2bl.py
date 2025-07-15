#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Prtable, Queasy, Prmarket

def prtable_admin2bl(rec_id:int, nr:int):
    prtable = queasy = prmarket = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal prtable, queasy, prmarket
        nonlocal rec_id, nr

        return {}


    prtable = get_cache (Prtable, {"_recid": [(eq, rec_id)]})
    db_session.delete(prtable)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 18) & (Queasy.number1 == nr)).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    prmarket = get_cache (Prmarket, {"nr": [(eq, nr)]})
    db_session.delete(prmarket)

    return generate_output()