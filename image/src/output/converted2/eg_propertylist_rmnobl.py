#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer

def eg_propertylist_rmnobl(rmno:string):
    avail_zimmer = False
    zimmer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_zimmer, zimmer
        nonlocal rmno

        return {"avail_zimmer": avail_zimmer}


    zimmer = get_cache (Zimmer, {"zinr": [(eq, rmno)]})

    if zimmer:
        avail_zimmer = True

    return generate_output()