#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def copy_hartikel_read_hartikelbl(art1:int, dept1:int):

    prepare_cache ([H_artikel])

    t_bez = ""
    avail_hartikel = False
    h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bez, avail_hartikel, h_artikel
        nonlocal art1, dept1

        return {"t_bez": t_bez, "avail_hartikel": avail_hartikel}


    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.artnr == art1) & (H_artikel.departement == dept1) & (H_artikel.activeflag)).first()

    if h_artikel:
        t_bez = h_artikel.bezeich
        avail_hartikel = True

    return generate_output()