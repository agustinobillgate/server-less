from functions.additional_functions import *
import decimal
from models import H_artikel, H_umsatz

def rarticle_admin_btn_delbl(h_artnr:int, h_dept:int):
    flag = 0
    h_artikel = h_umsatz = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, h_artikel, h_umsatz


        return {"flag": flag}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == h_artnr) &  (H_artikel.departement == h_dept)).first()

    h_umsatz = db_session.query(H_umsatz).filter(
            (H_umsatz.artnr == h_artnr) &  (H_umsatz.departement == h_dept)).first()

    if h_umsatz:
        flag = 1
    else:
        flag = 2

        h_artikel = db_session.query(H_artikel).first()
        db_session.delete(h_artikel)

    return generate_output()