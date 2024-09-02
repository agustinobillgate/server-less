from functions.additional_functions import *
import decimal
from models import Fa_grup

def fa_artlist_gnrbl(fa_art_gnr:str):
    grp_bez = ""
    avail_fa_grup = False
    fa_grup = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal grp_bez, avail_fa_grup, fa_grup


        return {"grp_bez": grp_bez, "avail_fa_grup": avail_fa_grup}


    fa_grup = db_session.query(Fa_grup).filter(
            (Fa_grup.gnr == to_int(fa_art_gnr)) &  (Fa_grup.flag == 0)).first()

    if fa_grup:
        avail_fa_grup = True
        grp_bez = fa_grup.bezeich

    return generate_output()