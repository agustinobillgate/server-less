#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_vendor, Htparam, Bediener

def prepare_eg_vendorbl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    engid = 0
    groupid = 0
    t_eg_vendor_list = []
    eg_vendor = htparam = bediener = None

    t_eg_vendor = None

    t_eg_vendor_list, T_eg_vendor = create_model_like(Eg_vendor, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_eg_vendor_list, eg_vendor, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_vendor
        nonlocal t_eg_vendor_list

        return {"engid": engid, "groupid": groupid, "t-eg-vendor": t_eg_vendor_list}

    def define_engineering():

        nonlocal engid, groupid, t_eg_vendor_list, eg_vendor, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_vendor
        nonlocal t_eg_vendor_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, t_eg_vendor_list, eg_vendor, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_vendor
        nonlocal t_eg_vendor_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group

    define_group()
    define_engineering()

    for eg_vendor in db_session.query(Eg_vendor).order_by(Eg_vendor._recid).all():
        t_eg_vendor = T_eg_vendor()
        t_eg_vendor_list.append(t_eg_vendor)

        buffer_copy(eg_vendor, t_eg_vendor)
        t_eg_vendor.rec_id = eg_vendor._recid

    return generate_output()