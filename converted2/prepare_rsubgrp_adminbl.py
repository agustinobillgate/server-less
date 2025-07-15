#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Wgrpdep, Hoteldpt

def prepare_rsubgrp_adminbl(dept:int):

    prepare_cache ([Hoteldpt])

    hoteldpt_depart = ""
    t_wgrpdep_data = []
    wgrpdep = hoteldpt = None

    t_wgrpdep = None

    t_wgrpdep_data, T_wgrpdep = create_model_like(Wgrpdep, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal hoteldpt_depart, t_wgrpdep_data, wgrpdep, hoteldpt
        nonlocal dept


        nonlocal t_wgrpdep
        nonlocal t_wgrpdep_data

        return {"hoteldpt_depart": hoteldpt_depart, "t-wgrpdep": t_wgrpdep_data}

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    hoteldpt_depart = hoteldpt.depart

    for wgrpdep in db_session.query(Wgrpdep).filter(
             (Wgrpdep.departement == dept)).order_by(Wgrpdep.betriebsnr.desc(), Wgrpdep.zknr).all():
        t_wgrpdep = T_wgrpdep()
        t_wgrpdep_data.append(t_wgrpdep)

        buffer_copy(wgrpdep, t_wgrpdep)
        t_wgrpdep.rec_id = wgrpdep._recid

    return generate_output()