#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guestbook

def delete_guestbookbl(gastno:int):
    guestbook = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestbook
        nonlocal gastno

        return {}


    guestbook = get_cache (Guestbook, {"gastnr": [(eq, gastno)]})

    if guestbook:
        db_session.delete(guestbook)
        pass

    return generate_output()