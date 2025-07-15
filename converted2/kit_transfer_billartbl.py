#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def kit_transfer_billartbl(billart:int, curr_dept:int):

    prepare_cache ([H_artikel])

    t_bezeich = ""
    avail_hartikel = False
    h_artikel = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bezeich, avail_hartikel, h_artikel
        nonlocal billart, curr_dept

        return {"t_bezeich": t_bezeich, "avail_hartikel": avail_hartikel}


    h_artikel = db_session.query(H_artikel).filter(
             (H_artikel.artnr == billart) & (H_artikel.departement == curr_dept) & (H_artikel.activeflag) & (H_artikel.artart == 0)).first()

    if h_artikel:
        t_bezeich = h_artikel.bezeich
        avail_hartikel = True
        return no_apply

    return generate_output()