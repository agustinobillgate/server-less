#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener

def sls_byrefer_btn_helpbl(usr_init:string):

    prepare_cache ([Bediener])

    usr_name = ""
    bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal usr_name, bediener
        nonlocal usr_init

        return {"usr_name": usr_name}


    bediener = get_cache (Bediener, {"userinit": [(eq, usr_init)]})
    usr_name = bediener.username

    return generate_output()