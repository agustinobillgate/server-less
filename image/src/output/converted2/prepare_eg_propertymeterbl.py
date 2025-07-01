#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_property, Bediener, Htparam, Eg_propmeter

def prepare_eg_propertymeterbl(user_init:string):

    prepare_cache ([Bediener, Htparam, Eg_propmeter])

    groupid = 0
    engid = 0
    msg = False
    rec_meter_list = []
    t_eg_property_list = []
    eg_property = bediener = htparam = eg_propmeter = None

    t_eg_property = rec_meter = None

    t_eg_property_list, T_eg_property = create_model_like(Eg_property)
    rec_meter_list, Rec_meter = create_model("Rec_meter", {"prop_nr":int, "rec_date":date, "rec_time":int, "rec_by":string, "rec_hour":int, "rec_meter":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, msg, rec_meter_list, t_eg_property_list, eg_property, bediener, htparam, eg_propmeter
        nonlocal user_init


        nonlocal t_eg_property, rec_meter
        nonlocal t_eg_property_list, rec_meter_list

        return {"groupid": groupid, "engid": engid, "msg": msg, "rec-meter": rec_meter_list, "t-eg-property": t_eg_property_list}

    def define_group():

        nonlocal groupid, engid, msg, rec_meter_list, t_eg_property_list, eg_property, bediener, htparam, eg_propmeter
        nonlocal user_init


        nonlocal t_eg_property, rec_meter
        nonlocal t_eg_property_list, rec_meter_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def define_engineering():

        nonlocal groupid, engid, msg, rec_meter_list, t_eg_property_list, eg_property, bediener, htparam, eg_propmeter
        nonlocal user_init


        nonlocal t_eg_property, rec_meter
        nonlocal t_eg_property_list, rec_meter_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


            msg = True


    def create_rec_meter():

        nonlocal groupid, engid, msg, rec_meter_list, t_eg_property_list, eg_property, bediener, htparam, eg_propmeter
        nonlocal user_init


        nonlocal t_eg_property, rec_meter
        nonlocal t_eg_property_list, rec_meter_list


        rec_meter_list.clear()

        for eg_propmeter in db_session.query(Eg_propmeter).order_by(Eg_propmeter._recid).all():
            rec_meter = Rec_meter()
            rec_meter_list.append(rec_meter)

            rec_meter.prop_nr = eg_propmeter.propertynr
            rec_meter.rec_date = eg_propmeter.rec_date
            rec_meter.rec_time = eg_propmeter.rec_time
            rec_meter.rec_by = eg_propmeter.rec_by
            rec_meter.rec_hour = eg_propmeter.val_hour
            rec_meter.rec_meter = eg_propmeter.val_meter


    define_group()
    define_engineering()
    create_rec_meter()

    for eg_property in db_session.query(Eg_property).filter(
             (Eg_property.nr != 0)).order_by(Eg_property._recid).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    return generate_output()