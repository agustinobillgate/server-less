from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Eg_property

def eg_mainscheduleed_propertynrbl(case_type:int, m_propertynr:int, h_location:int, h_zinr:str):
    avail_eg_property = False
    t_maintask = 0
    t_bezeich = ""
    t_queasy_list = []
    queasy = eg_property = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_eg_property, t_maintask, t_bezeich, t_queasy_list, queasy, eg_property


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"avail_eg_property": avail_eg_property, "t_maintask": t_maintask, "t_bezeich": t_bezeich, "t-queasy": t_queasy_list}

    if case_type == 1:

        eg_property = db_session.query(Eg_property).filter(
                (Eg_property.nr == m_propertynr) &  (Eg_property.location == h_location) &  (func.lower(Eg_property.zinr) == (h_zinr).lower())).first()

    elif case_type == 2:

        eg_property = db_session.query(Eg_property).filter(
                (Eg_property.nr == m_propertynr) &  (Eg_property.location == h_location)).first()

    if eg_property:
        avail_eg_property = True
        t_maintask = eg_property.maintask
        t_bezeich = eg_property.bezeich

        for queasy in db_session.query(Queasy).filter(
                (Queasy.KEY == 132) |  (Queasy.KEY == 133)).all():
            t_queasy = T_queasy()
            t_queasy_list.append(t_queasy)

            buffer_copy(queasy, t_queasy)

    return generate_output()