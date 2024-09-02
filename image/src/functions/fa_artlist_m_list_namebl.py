from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Mathis

def fa_artlist_m_list_namebl(m_list_name:str):
    mathis1_model = ""
    avail_mathis1 = False
    mathis = None

    mathis1 = None

    Mathis1 = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mathis1_model, avail_mathis1, mathis
        nonlocal mathis1


        nonlocal mathis1
        return {"mathis1_model": mathis1_model, "avail_mathis1": avail_mathis1}


    mathis1 = db_session.query(Mathis1).filter(
            (func.lower(Mathis1.name) == (m_list_name).lower())).first()

    if mathis1:
        avail_mathis1 = True
        mathis1_model = mathis1.model

    return generate_output()