from functions.additional_functions import *
import decimal
from models import H_rezept

def rarticle_admin_artnrrezeptbl(h_artnrrezept:int, artnr:int):
    flag = 0
    h_rezept = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_rezept


        return {"flag": flag}


    h_rezept = db_session.query(H_rezept).filter(
            (H_rezept.artnrrezept == h_artnrrezept)).first()

    if not h_rezept and artnr != 0:
        flag = 1

    return generate_output()