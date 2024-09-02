from functions.additional_functions import *
import decimal
from models import H_artikel

def h_2ndprice_h_artikelbl(dept:int):
    avail_h_artikel = False
    h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_artikel, h_artikel


        return {"avail_h_artikel": avail_h_artikel}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.departement == dept)).first()

    if h_artikel:
        avail_h_artikel = True

    return generate_output()