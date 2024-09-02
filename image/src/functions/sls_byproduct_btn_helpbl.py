from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Bediener

def sls_byproduct_btn_helpbl(usr_init:str):
    usr_name = ""
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal usr_name, bediener


        return {"usr_name": usr_name}


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (usr_init).lower())).first()
    usr_name = bediener.username

    return generate_output()