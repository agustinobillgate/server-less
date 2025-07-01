#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Eg_property, Eg_location, Zimmer, Htparam, Bediener

def prepare_eg_propertybl(user_init:string):

    prepare_cache ([Queasy, Htparam, Bediener])

    engid = 0
    groupid = 0
    maintask_list = []
    location_list = []
    t_eg_property_list = []
    t_eg_location_list = []
    queasy_133_list = []
    t_zimmer_list = []
    queasy = eg_property = eg_location = zimmer = htparam = bediener = None

    queasy_133 = maintask = location = t_eg_property = t_eg_location = t_zimmer = None

    queasy_133_list, Queasy_133 = create_model_like(Queasy)
    maintask_list, Maintask = create_model("Maintask", {"main_nr":int, "main_nm":string})
    location_list, Location = create_model("Location", {"loc_nr":int, "loc_nm":string})
    t_eg_property_list, T_eg_property = create_model_like(Eg_property)
    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    t_zimmer_list, T_zimmer = create_model_like(Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, maintask_list, location_list, t_eg_property_list, t_eg_location_list, queasy_133_list, t_zimmer_list, queasy, eg_property, eg_location, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal queasy_133, maintask, location, t_eg_property, t_eg_location, t_zimmer
        nonlocal queasy_133_list, maintask_list, location_list, t_eg_property_list, t_eg_location_list, t_zimmer_list

        return {"engid": engid, "groupid": groupid, "Maintask": maintask_list, "Location": location_list, "t-eg-property": t_eg_property_list, "t-eg-location": t_eg_location_list, "queasy-133": queasy_133_list, "t-zimmer": t_zimmer_list}

    def define_engineering():

        nonlocal engid, groupid, maintask_list, location_list, t_eg_property_list, t_eg_location_list, queasy_133_list, t_zimmer_list, queasy, eg_property, eg_location, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal queasy_133, maintask, location, t_eg_property, t_eg_location, t_zimmer
        nonlocal queasy_133_list, maintask_list, location_list, t_eg_property_list, t_eg_location_list, t_zimmer_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, maintask_list, location_list, t_eg_property_list, t_eg_location_list, queasy_133_list, t_zimmer_list, queasy, eg_property, eg_location, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal queasy_133, maintask, location, t_eg_property, t_eg_location, t_zimmer
        nonlocal queasy_133_list, maintask_list, location_list, t_eg_property_list, t_eg_location_list, t_zimmer_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_location():

        nonlocal engid, groupid, maintask_list, location_list, t_eg_property_list, t_eg_location_list, queasy_133_list, t_zimmer_list, queasy, eg_property, eg_location, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal queasy_133, maintask, location, t_eg_property, t_eg_location, t_zimmer
        nonlocal queasy_133_list, maintask_list, location_list, t_eg_property_list, t_eg_location_list, t_zimmer_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        location_list.clear()

        for qbuff in db_session.query(Qbuff).order_by(Qbuff._recid).all():
            location = Location()
            location_list.append(location)

            location.loc_nr = qbuff.nr
            location.loc_nm = qbuff.bezeich


    def create_maintask():

        nonlocal engid, groupid, maintask_list, location_list, t_eg_property_list, t_eg_location_list, queasy_133_list, t_zimmer_list, queasy, eg_property, eg_location, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal queasy_133, maintask, location, t_eg_property, t_eg_location, t_zimmer
        nonlocal queasy_133_list, maintask_list, location_list, t_eg_property_list, t_eg_location_list, t_zimmer_list

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        maintask_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 133)).order_by(Qbuff._recid).all():
            maintask = Maintask()
            maintask_list.append(maintask)

            maintask.main_nr = qbuff.number1
            maintask.main_nm = qbuff.char1


    define_group()
    define_engineering()
    create_location()
    create_maintask()

    for eg_location in db_session.query(Eg_location).order_by(Eg_location._recid).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for eg_property in db_session.query(Eg_property).order_by(Eg_property._recid).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 133)).order_by(Queasy._recid).all():
        queasy_133 = Queasy_133()
        queasy_133_list.append(queasy_133)

        buffer_copy(queasy, queasy_133)

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()