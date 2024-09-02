from functions.additional_functions import *
import decimal
from models import Fa_kateg

def fa_artlist_katnrbl(fa_art_katnr:str):
    avail_fa_kateg = False
    fa_kateg_rate = 0
    fa_kateg = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_fa_kateg, fa_kateg_rate, fa_kateg


        return {"avail_fa_kateg": avail_fa_kateg, "fa_kateg_rate": fa_kateg_rate}


    fa_kateg = db_session.query(Fa_kateg).filter(
            (Fa_kateg.katnr == to_int(fa_art_katnr))).first()

    if fa_kateg:
        avail_fa_kateg = True
        fa_kateg_rate = fa_kateg.rate

    return generate_output()