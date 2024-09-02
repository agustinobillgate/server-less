from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_vendor, Htparam, Bediener

def prepare_eg_vendorbl(user_init:str):
    engid = 0
    groupid = 0
    t_eg_vendor_list = []
    eg_vendor = htparam = bediener = None

    t_eg_vendor = None

    t_eg_vendor_list, T_eg_vendor = create_model_like(Eg_vendor, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_eg_vendor_list, eg_vendor, htparam, bediener


        nonlocal t_eg_vendor
        nonlocal t_eg_vendor_list
        return {"engid": engid, "groupid": groupid, "t-eg-vendor": t_eg_vendor_list}

    def define_engineering():

        nonlocal engid, groupid, t_eg_vendor_list, eg_vendor, htparam, bediener


        nonlocal t_eg_vendor
        nonlocal t_eg_vendor_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, t_eg_vendor_list, eg_vendor, htparam, bediener


        nonlocal t_eg_vendor
        nonlocal t_eg_vendor_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group


    define_group()
    define_engineering()

    for eg_vendor in db_session.query(Eg_vendor).all():
        t_eg_vendor = T_eg_vendor()
        t_eg_vendor_list.append(t_eg_vendor)

        buffer_copy(eg_vendor, t_eg_vendor)
        t_eg_vendor.rec_id = eg_vendor._recid

    return generate_output()