#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def gb_delete_document(gastno:int):


    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastno

        return {}


    vhpgb.guestbook = db_session.query(Vhpgb.guestbook).filter(
             (Vhpgb.guestbook.guestbook.gastnr == gastno)).first()

    if vhpgb.guestbook:
        vhpgb.guestbook_list.remove(vhpgb.guestbook)
        pass

    return generate_output()