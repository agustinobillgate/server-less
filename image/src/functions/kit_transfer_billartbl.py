from functions.additional_functions import *
import decimal
from models import H_artikel

def kit_transfer_billartbl(billart:int, curr_dept:int):
    t_bezeich = ""
    avail_hartikel = False
    h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bezeich, avail_hartikel, h_artikel


        return {"t_bezeich": t_bezeich, "avail_hartikel": avail_hartikel}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == billart and H_artikel.departement == curr_dept and H_artikel.activeflag and H_artikel.artart == 0)).first()

    if h_artikel:
        t_bezeich = h_artikel.bezeich
        avail_hartikel = True
        return no_apply

    return generate_output()