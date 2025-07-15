#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def aktline_list_read_bedienerbl(user_init:string):

    prepare_cache ([Bediener])

    sales_name = ""
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sales_name, bediener
        nonlocal user_init

        return {"sales_name": sales_name}


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    if bediener:
        sales_name = bediener.username

    return generate_output()