#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location, Bediener, Htparam, Queasy

def prepare_eg_locationbl(user_init:string):

    prepare_cache ([Bediener, Htparam, Queasy])

    groupid = 0
    engid = 0
    t_eg_location_data = []
    building_data = []
    eg_location = bediener = htparam = queasy = None

    building = t_eg_location = None

    building_data, Building = create_model("Building", {"build_nr":int, "char1":string})
    t_eg_location_data, T_eg_location = create_model_like(Eg_location, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, t_eg_location_data, building_data, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_data, t_eg_location_data

        return {"groupid": groupid, "engid": engid, "t-eg-location": t_eg_location_data, "building": building_data}

    def define_group():

        nonlocal groupid, engid, t_eg_location_data, building_data, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_data, t_eg_location_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, t_eg_location_data, building_data, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_data, t_eg_location_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def create_build_nr():

        nonlocal groupid, engid, t_eg_location_data, building_data, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_data, t_eg_location_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        building_data.clear()
        building = Building()
        building_data.append(building)

        building.build_nr = 0
        building.char1 = ""

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 135)).order_by(Qbuff._recid).all():
            building = Building()
            building_data.append(building)

            building.build_nr = qbuff.number1
            building.char1 = qbuff.char1


    define_group()
    define_engineering()
    create_build_nr()

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_data.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)
        t_eg_location.rec_id = eg_location._recid

    return generate_output()