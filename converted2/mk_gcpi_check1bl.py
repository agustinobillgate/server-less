#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def mk_gcpi_check1bl(rcvname:string):
    avail_bed = False
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_bed, bediener
        nonlocal rcvname

        return {"avail_bed": avail_bed}


    bediener = get_cache (Bediener, {"username": [(eq, rcvname)]})

    if bediener:
        avail_bed = True

    return generate_output()