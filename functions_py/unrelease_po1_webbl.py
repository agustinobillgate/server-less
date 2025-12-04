#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr, Queasy

def unrelease_po1_webbl(docu_nr:string):

    prepare_cache ([L_orderhdr])

    l_orderhdr = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_orderhdr, queasy
        nonlocal docu_nr

        return {}

    l_orderhdr = db_session.query(L_orderhdr).filter(L_orderhdr.docu_nr == docu_nr).with_for_update().first()

    if l_orderhdr:
        l_orderhdr.gedruckt = None

    queasy = db_session.query(Queasy).filter(Queasy.key == 245, Queasy.char1 == docu_nr, Queasy.number1 == 4).with_for_update().first()

    if queasy:
        db_session.delete(queasy)

    return generate_output()