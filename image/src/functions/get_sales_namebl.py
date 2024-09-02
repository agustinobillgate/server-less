from functions.additional_functions import *
import decimal
from models import Bediener

def get_sales_namebl(nr:int):
    username = ""
    bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal username, bediener


        return {"username": username}


    bediener = db_session.query(Bediener).filter(
            (Bediener.nr == nr)).first()

    if bediener:
        username = bediener.username

    return generate_output()