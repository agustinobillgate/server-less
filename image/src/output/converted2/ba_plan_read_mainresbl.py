#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_veran, Guest

def ba_plan_read_mainresbl(t_resnr:int):

    prepare_cache ([Bk_veran, Guest])

    mainres_gastnr = 0
    mainres_veran_nr = 0
    mainres_resnr = 0
    gast_karteityp = 0
    avail_mainres = False
    bk_veran = guest = None

    mainres = gast = None

    Mainres = create_buffer("Mainres",Bk_veran)
    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_gastnr, mainres_veran_nr, mainres_resnr, gast_karteityp, avail_mainres, bk_veran, guest
        nonlocal t_resnr
        nonlocal mainres, gast


        nonlocal mainres, gast

        return {"mainres_gastnr": mainres_gastnr, "mainres_veran_nr": mainres_veran_nr, "mainres_resnr": mainres_resnr, "gast_karteityp": gast_karteityp, "avail_mainres": avail_mainres}


    mainres = get_cache (Bk_veran, {"veran_nr": [(eq, t_resnr)]})

    if mainres:
        avail_mainres = True
        mainres_gastnr = mainres.gastnr
        mainres_veran_nr = mainres.veran_nr
        mainres_resnr = mainres.resnr

        gast = get_cache (Guest, {"gastnr": [(eq, mainres.gastnr)]})
        gast_karteityp = gast.karteityp

    return generate_output()