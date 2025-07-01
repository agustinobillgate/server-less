#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Eg_location, Htparam, L_lager, Bediener

def prepare_eg_propertylist_webbl(user_init:string):

    prepare_cache ([Htparam, L_lager, Bediener])

    engid = 0
    groupid = 0
    store_number = 0
    q1_list_list = []
    t_eg_location_list = []
    t_queasy_list = []
    queasy = eg_location = htparam = l_lager = bediener = None

    t_queasy = t_eg_location = q1_list = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    q1_list_list, Q1_list = create_model("Q1_list", {"nr":int, "bezeich":string, "maintask":int, "char3":string, "char2":string, "zinr":string, "datum":date, "brand":string, "capacity":string, "dimension":string, "type":string, "price":Decimal, "spec":string, "location":int, "activeflag":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, store_number, q1_list_list, t_eg_location_list, t_queasy_list, queasy, eg_location, htparam, l_lager, bediener
        nonlocal user_init


        nonlocal t_queasy, t_eg_location, q1_list
        nonlocal t_queasy_list, t_eg_location_list, q1_list_list

        return {"engid": engid, "groupid": groupid, "store_number": store_number, "q1-list": q1_list_list, "t-eg-location": t_eg_location_list, "t-queasy": t_queasy_list}

    def define_group():

        nonlocal engid, groupid, store_number, q1_list_list, t_eg_location_list, t_queasy_list, queasy, eg_location, htparam, l_lager, bediener
        nonlocal user_init


        nonlocal t_queasy, t_eg_location, q1_list
        nonlocal t_queasy_list, t_eg_location_list, q1_list_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal engid, groupid, store_number, q1_list_list, t_eg_location_list, t_queasy_list, queasy, eg_location, htparam, l_lager, bediener
        nonlocal user_init


        nonlocal t_queasy, t_eg_location, q1_list
        nonlocal t_queasy_list, t_eg_location_list, q1_list_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    define_group()
    define_engineering()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1061)]})

    if htparam.finteger != 0:

        l_lager = get_cache (L_lager, {"lager_nr": [(eq, htparam.finteger)]})

        if l_lager:
            store_number = l_lager.lager_nr

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 133)).order_by(Queasy._recid).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()