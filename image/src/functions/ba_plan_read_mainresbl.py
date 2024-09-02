from functions.additional_functions import *
import decimal
from models import Bk_veran, Guest

def ba_plan_read_mainresbl(t_resnr:int):
    mainres_gastnr = 0
    mainres_veran_nr = 0
    mainres_resnr = 0
    gast_karteityp = 0
    avail_mainres = False
    bk_veran = guest = None

    mainres = gast = None

    Mainres = Bk_veran
    Gast = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_gastnr, mainres_veran_nr, mainres_resnr, gast_karteityp, avail_mainres, bk_veran, guest
        nonlocal mainres, gast


        nonlocal mainres, gast
        return {"mainres_gastnr": mainres_gastnr, "mainres_veran_nr": mainres_veran_nr, "mainres_resnr": mainres_resnr, "gast_karteityp": gast_karteityp, "avail_mainres": avail_mainres}


    mainres = db_session.query(Mainres).filter(
            (Mainres.veran_nr == t_resnr)).first()

    if mainres:
        avail_mainres = True
        mainres_gastnr = mainres.gastnr
        mainres_veran_nr = mainres.veran_nr
        mainres_resnr = mainres.resnr

        gast = db_session.query(Gast).filter(
                (Gast.gastnr == mainres.gastnr)).first()
        gast_karteityp = gast.karteityp

    return generate_output()