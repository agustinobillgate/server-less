from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Mathis

def fa_artlist_assetbl(m_list_asset:str, recid_mathis:int):
    avail_mathis1 = False
    mathis1_name = ""
    mathis = None

    mathis1 = None

    Mathis1 = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_mathis1, mathis1_name, mathis
        nonlocal mathis1


        nonlocal mathis1
        return {"avail_mathis1": avail_mathis1, "mathis1_name": mathis1_name}


    mathis1 = db_session.query(Mathis1).filter(
            (func.lower(Mathis1.asset) == (m_list_asset).lower()) &  (Mathis1._recid != recid_mathis)).first()

    if mathis1:
        avail_mathis1 = True
        mathis1_name = mathis1.name

    return generate_output()