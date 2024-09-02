from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_location, Bediener, Htparam, Queasy

def prepare_eg_locationbl(user_init:str):
    groupid = 0
    engid = 0
    t_eg_location_list = []
    building_list = []
    eg_location = bediener = htparam = queasy = None

    building = t_eg_location = qbuff = None

    building_list, Building = create_model("Building", {"build_nr":int, "char1":str})
    t_eg_location_list, T_eg_location = create_model_like(Eg_location, {"rec_id":int})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal qbuff


        nonlocal building, t_eg_location, qbuff
        nonlocal building_list, t_eg_location_list
        return {"groupid": groupid, "engid": engid, "t-eg-location": t_eg_location_list, "building": building_list}

    def define_group():

        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal qbuff


        nonlocal building, t_eg_location, qbuff
        nonlocal building_list, t_eg_location_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal qbuff


        nonlocal building, t_eg_location, qbuff
        nonlocal building_list, t_eg_location_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def create_build_nr():

        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal qbuff


        nonlocal building, t_eg_location, qbuff
        nonlocal building_list, t_eg_location_list


        Qbuff = Queasy
        building_list.clear()
        building = Building()
        building_list.append(building)

        building.build_nr = 0
        building.char1 = ""

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 135)).all():
            building = Building()
            building_list.append(building)

            building.build_nr = qbuff.number1
            building.char1 = qbuff.char1

    define_group()
    define_engineering()
    create_build_nr()

    for eg_location in db_session.query(Eg_location).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)
        t_eg_location.rec_id = eg_location._recid

    return generate_output()