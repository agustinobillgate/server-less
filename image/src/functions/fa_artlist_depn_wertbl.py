from functions.additional_functions import *
import decimal
from models import Fa_kateg

def fa_artlist_depn_wertbl(fa_art_katnr:int):
    fa_kateg_nutzjahr = 0
    avail_fa_kateg = False
    fa_kateg = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_kateg_nutzjahr, avail_fa_kateg, fa_kateg


        return {"fa_kateg_nutzjahr": fa_kateg_nutzjahr, "avail_fa_kateg": avail_fa_kateg}


    fa_kateg = db_session.query(Fa_kateg).filter(
            (Fa_kateg.katnr == fa_art_katnr)).first()

    if fa_kateg and fa_kateg.methode == 0:
        avail_fa_kateg = True
        fa_kateg_nutzjahr = fa_kateg.nutzjahr

    return generate_output()