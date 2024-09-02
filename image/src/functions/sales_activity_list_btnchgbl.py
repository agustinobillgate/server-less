from functions.additional_functions import *
import decimal
from models import B_storno

def sales_activity_list_btnchgbl(resnr:int, str:str, outnr:int):
    b_storno = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_storno


        return {}


    b_storno = db_session.query(B_storno).filter(
            (B_storno.bankettnr == resnr)).first()

    b_storno = db_session.query(B_storno).first()
    b_storno.grund[outnr - 1] = str

    b_storno = db_session.query(B_storno).first()

    return generate_output()