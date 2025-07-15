#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import History, Res_line, Bediener

def hk_rmchange_1bl(from_date:date, to_date:date):

    prepare_cache ([Res_line])

    h_list_data = []
    s1:string = ""
    s2:string = ""
    s3:string = ""
    user_init:string = ""
    history = res_line = bediener = None

    h_list = None

    h_list_data, H_list = create_model_like(History, {"chgdate":string, "tzinr":string, "reason":string, "usr_id":string, "res_name":string, "abreisezeit1":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_list_data, s1, s2, s3, user_init, history, res_line, bediener
        nonlocal from_date, to_date


        nonlocal h_list
        nonlocal h_list_data

        return {"h-list": h_list_data}


    h_list_data.clear()

    for history in db_session.query(History).filter(
             (History.ankunft <= to_date) & (History.abreise >= from_date) & (History.zi_wechsel) & (substring(History.bemerk, 0, 8) >= to_string(from_date)) & (substring(History.bemerk, 0, 8) <= to_string(to_date))).order_by(func.substring(History.bemerk, 0, 8), History.zinr).all():

        res_line = get_cache (Res_line, {"resnr": [(eq, history.resnr)]})

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        s1 = entry(0, history.bemerk, chr_unicode(10))

        if get_index(history.bemerk, chr_unicode(10)) > 0:
            s2 = entry(0, entry(1, history.bemerk, chr_unicode(10)) , chr_unicode(2))
        else:
            s2 = ""
        h_list = H_list()
        h_list_data.append(h_list)

        buffer_copy(history, h_list)
        h_list.reason = s2
        h_list.tzinr = trim(substring(s1, 19))
        h_list.chgdate = substring(history.bemerk, 0, 8)
        h_list.resnr = res_line.resnr
        h_list.reslinnr = res_line.reslinnr
        h_list.abreisezeit1 = res_line.ankzeit
        h_list.res_name = res_line.resname
        usr_id = ""

        if num_entries(history.bemerk, chr_unicode(2)) > 1:
            usr_id = entry(1, history.bemerk, chr_unicode(2))

    return generate_output()