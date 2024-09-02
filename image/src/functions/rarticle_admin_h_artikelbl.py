from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import H_artikel

def rarticle_admin_h_artikelbl(case_type:int, h_artnr:int, dept:int, h_bezeich:str):
    flag = 0
    h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_artikel


        return {"flag": flag}


    if case_type == 1:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == h_artnr) &  (H_artikel.departement == dept)).first()

    elif case_type == 2:

        h_artikel = db_session.query(H_artikel).filter(
                (func.lower(H_artikel.bezeich) == (h_bezeich).lower()) &  (H_artikel.departement == dept) &  (H_artikel.artnr != h_artnr)).first()

    if h_artikel:
        flag = 1

    return generate_output()