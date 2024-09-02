from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Eg_location, Htparam, L_lager, Eg_property, Bediener

def prepare_eg_propertylist_webbl(user_init:str):
    engid = 0
    groupid = 0
    store_number = 0
    q1_list_list = []
    t_eg_location_list = []
    t_queasy_list = []
    queasy = eg_location = htparam = l_lager = eg_property = bediener = None

    t_queasy = t_eg_location = q1_list = None

    t_queasy_list, T_queasy = create_model_like(Queasy)
    t_eg_location_list, T_eg_location = create_model_like(Eg_location)
    q1_list_list, Q1_list = create_model("Q1_list", {"nr":int, "bezeich":str, "maintask":int, "char3":str, "char2":str, "zinr":str, "datum":date, "brand":str, "capacity":str, "dimension":str, "type":str, "price":decimal, "spec":str, "location":int, "activeflag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, store_number, q1_list_list, t_eg_location_list, t_queasy_list, queasy, eg_location, htparam, l_lager, eg_property, bediener


        nonlocal t_queasy, t_eg_location, q1_list
        nonlocal t_queasy_list, t_eg_location_list, q1_list_list
        return {"engid": engid, "groupid": groupid, "store_number": store_number, "q1-list": q1_list_list, "t-eg-location": t_eg_location_list, "t-queasy": t_queasy_list}

    def define_group():

        nonlocal engid, groupid, store_number, q1_list_list, t_eg_location_list, t_queasy_list, queasy, eg_location, htparam, l_lager, eg_property, bediener


        nonlocal t_queasy, t_eg_location, q1_list
        nonlocal t_queasy_list, t_eg_location_list, q1_list_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def define_engineering():

        nonlocal engid, groupid, store_number, q1_list_list, t_eg_location_list, t_queasy_list, queasy, eg_location, htparam, l_lager, eg_property, bediener


        nonlocal t_queasy, t_eg_location, q1_list
        nonlocal t_queasy_list, t_eg_location_list, q1_list_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    define_group()
    define_engineering()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1061)).first()

    if htparam.finteger != 0:

        l_lager = db_session.query(L_lager).filter(
                (L_lager.lager_nr == htparam.finteger)).first()

        if l_lager:
            store_number = l_lager.lager_nr

    eg_property_obj_list = []
    for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).all():
        if eg_property._recid in eg_property_obj_list:
            continue
        else:
            eg_property_obj_list.append(eg_property._recid)


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.nr = eg_property.nr
        q1_list.bezeich = eg_property.bezeich
        q1_list.maintask = queasy.number1
        q1_list.char3 = queasy.char1
        q1_list.char2 = eg_Location.bezeich
        q1_list.zinr = eg_property.zinr
        q1_list.datum = eg_property.datum
        q1_list.brand = eg_property.brand
        q1_list.capacity = eg_property.capacity
        q1_list.dimension = eg_property.dimension
        q1_list.TYPE = eg_property.TYPE
        q1_list.price = eg_property.price
        q1_list.Spec = eg_property.Spec
        q1_list.location = eg_property.location
        q1_list.activeflag = eg_property.activeflag

    for eg_location in db_session.query(Eg_location).all():
        t_eg_location = T_eg_location()
        t_eg_location_list.append(t_eg_location)

        buffer_copy(eg_location, t_eg_location)

    for queasy in db_session.query(Queasy).filter(
            (Queasy.KEY == 133)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()