from functions.additional_functions import *
import decimal
from models import H_artikel

def ts_restinv_split_itembl(artnr:int, departement:int):
    avail_h_art = False
    h_artikel = None

    h_art = None

    H_art = H_artikel

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_art, h_artikel
        nonlocal h_art


        nonlocal h_art
        return {"avail_h_art": avail_h_art}


    h_art = db_session.query(H_art).filter(
            (H_art.artnr == artnr) &  (H_art.departement == departement) &  (H_art.artart == 0)).first()

    if h_art:
        avail_h_art = True

    return generate_output()