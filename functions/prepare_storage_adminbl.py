#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_lager, Hoteldpt

def prepare_storage_adminbl():

    prepare_cache ([L_lager, Hoteldpt])

    t_l_lager_data = []
    t_hoteldpt_data = []
    l_lager = hoteldpt = None

    t_l_lager = t_hoteldpt = None

    t_l_lager_data, T_l_lager = create_model("T_l_lager", {"lager_nr":int, "bezeich":string, "betriebsnr":int})
    t_hoteldpt_data, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lager_data, t_hoteldpt_data, l_lager, hoteldpt


        nonlocal t_l_lager, t_hoteldpt
        nonlocal t_l_lager_data, t_hoteldpt_data

        return {"t-l-lager": t_l_lager_data, "t-hoteldpt": t_hoteldpt_data}


    for l_lager in db_session.query(L_lager).order_by(L_lager._recid).all():
        t_l_lager = T_l_lager()
        t_l_lager_data.append(t_l_lager)

        t_l_lager.lager_nr = l_lager.lager_nr
        t_l_lager.bezeich = l_lager.bezeich
        t_l_lager.betriebsnr = l_lager.betriebsnr

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    return generate_output()