#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.hk_ooo1bl import hk_ooo1bl
from models import Outorder, Bediener, Queasy

def hk_update_ooo_ombl(case_type:int, user_init:string, rec_id:int, from_date:date, to_date:date, service_flag:bool, reason:string, dept:int):

    prepare_cache ([Bediener, Queasy])

    msg_int = 0
    resno = 0
    resname = ""
    ankunft = None
    abreise = None
    ooo_list_ind:int = 0
    user_nr:int = 0
    prev_from_date:date = None
    prev_to_date:date = None
    outorder = bediener = queasy = None

    t_outorder = None

    t_outorder_data, T_outorder = create_model_like(Outorder)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_int, resno, resname, ankunft, abreise, ooo_list_ind, user_nr, prev_from_date, prev_to_date, outorder, bediener, queasy
        nonlocal case_type, user_init, rec_id, from_date, to_date, service_flag, reason, dept


        nonlocal t_outorder
        nonlocal t_outorder_data

        return {"msg_int": msg_int, "resno": resno, "resname": resname, "ankunft": ankunft, "abreise": abreise}

    if dept == None:
        dept = 0

    if service_flag == None:
        service_flag = True

    outorder = get_cache (Outorder, {"_recid": [(eq, rec_id)]})

    if outorder:
        prev_from_date = outorder.gespstart
        prev_to_date = outorder.gespende
        t_outorder = T_outorder()
        t_outorder_data.append(t_outorder)

        buffer_copy(outorder, t_outorder)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        user_nr = bediener.nr
        msg_int, resno, resname, ankunft, abreise, ooo_list_ind = get_output(hk_ooo1bl(case_type, t_outorder_data, from_date, to_date, service_flag, t_outorder.zinr, user_nr, reason, dept, user_init))

        if msg_int == 0:

            for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 195) & (Queasy.char1 == ("ooo;room=" + outorder.zinr + ";from=" + to_string(get_day(prev_from_date) , "99") + "/" + to_string(get_month(prev_from_date) , "99") + "/" + to_string(get_year(prev_from_date) , "9999") + ";to=" + to_string(get_day(prev_to_date) , "99") + "/" + to_string(get_month(prev_to_date) , "99") + "/" + to_string(get_year(prev_to_date) , "9999").lower()))).order_by(Queasy._recid).all():

                if queasy:
                    queasy.char1 = "ooo;room=" + outorder.zinr + ";from=" + to_string(get_day(from_date) , "99") + "/" + to_string(get_month(from_date) , "99") + "/" + to_string(get_year(from_date) , "9999") + ";to=" + to_string(get_day(to_date) , "99") + "/" + to_string(get_month(to_date) , "99") + "/" + to_string(get_year(to_date) , "9999")

    return generate_output()