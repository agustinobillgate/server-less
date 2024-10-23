from functions.additional_functions import *
import decimal
from models import Bk_veran

def ba_plan_btn_notebl(t_resnr:int):
    t_veran_nr = 0
    avail_mainres = False
    bk_veran = None

    mainres = None

    Mainres = create_buffer("Mainres",Bk_veran)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_veran_nr, avail_mainres, bk_veran
        nonlocal t_resnr
        nonlocal mainres


        nonlocal mainres
        return {"t_veran_nr": t_veran_nr, "avail_mainres": avail_mainres}


    mainres = db_session.query(Mainres).filter(
             (Mainres.veran_nr == t_resnr)).first()

    if mainres:
        avail_mainres = True
        t_veran_nr = mainres.veran_nr

    return generate_output()