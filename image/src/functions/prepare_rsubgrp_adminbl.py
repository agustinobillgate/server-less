from functions.additional_functions import *
import decimal
from models import Wgrpdep, Hoteldpt

def prepare_rsubgrp_adminbl(dept:int):
    hoteldpt_depart = ""
    t_wgrpdep_list = []
    wgrpdep = hoteldpt = None

    t_wgrpdep = None

    t_wgrpdep_list, T_wgrpdep = create_model_like(Wgrpdep, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal hoteldpt_depart, t_wgrpdep_list, wgrpdep, hoteldpt


        nonlocal t_wgrpdep
        nonlocal t_wgrpdep_list
        return {"hoteldpt_depart": hoteldpt_depart, "t-wgrpdep": t_wgrpdep_list}

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    hoteldpt_depart = hoteldpt.depart

    for wgrpdep in db_session.query(Wgrpdep).filter(
            (Wgrpdep.departement == dept)).all():
        t_wgrpdep = T_wgrpdep()
        t_wgrpdep_list.append(t_wgrpdep)

        buffer_copy(wgrpdep, t_wgrpdep)
        t_wgrpdep.rec_id = wgrpdep._recid

    return generate_output()