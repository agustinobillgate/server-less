from functions.additional_functions import *
import decimal
from models import Eg_vendor

def prepare_sel_vendorbl():
    t_eg_vendor_list = []
    eg_vendor = None

    t_eg_vendor = None

    t_eg_vendor_list, T_eg_vendor = create_model_like(Eg_vendor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_vendor_list, eg_vendor


        nonlocal t_eg_vendor
        nonlocal t_eg_vendor_list
        return {"t-eg-vendor": t_eg_vendor_list}

    for eg_vendor in db_session.query(Eg_vendor).all():
        t_eg_vendor = T_eg_vendor()
        t_eg_vendor_list.append(t_eg_vendor)

        buffer_copy(eg_vendor, t_eg_vendor)

    return generate_output()