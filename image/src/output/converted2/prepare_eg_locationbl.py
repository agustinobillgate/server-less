#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location, Bediener, Htparam, Queasy

def prepare_eg_locationbl(user_init:string):

    prepare_cache ([Bediener, Htparam, Queasy])

    groupid = 0
    engid = 0
    t_eg_location_list = []
    building_list = []
    eg_location = bediener = htparam = queasy = None

    building = t_eg_location = None

    building_list, Building = create_model("Building", {"build_nr":int, "char1":string})
    t_eg_location_list, T_eg_location = create_model_like(Eg_location, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_list, t_eg_location_list

        return {"groupid": groupid, "engid": engid, "t-eg-location": t_eg_location_list, "building": building_list}

    def define_group():

        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_list, t_eg_location_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_list, t_eg_location_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def create_build_nr():

        nonlocal groupid, engid, t_eg_location_list, building_list, eg_location, bediener, htparam, queasy
        nonlocal user_init


        nonlocal building, t_eg_location
        nonlocal building_list, t_eg_location_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        building_list.clear()
        building = Building()
        building_list.append(building)

        building.build_nr = 0
        building.char1 = ""

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 135)).order_by(Qbuff._recid).all():
            building = Building()
            building_list.append(building)

            building.build_nr = qbuff.number1
            building.char1 = qbuff.char1


    define_group()
    define_engineering()
    create_build_nr()

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)
        t_eg_location.rec_id = eg_location._recid

    return generate_output()