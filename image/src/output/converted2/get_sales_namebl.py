#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def get_sales_namebl(nr:int):

    prepare_cache ([Bediener])

    username = ""
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal username, bediener
        nonlocal nr

        return {"username": username}


    bediener = get_cache (Bediener, {"nr": [(eq, nr)]})

    if bediener:
        username = bediener.username

    return generate_output()