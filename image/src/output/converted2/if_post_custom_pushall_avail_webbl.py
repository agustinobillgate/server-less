#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.if_custom_pushall_availbl import if_custom_pushall_availbl
from functions.if_custom_pushall_ratebl import if_custom_pushall_ratebl
from functions.update_repeatflag_1bl import update_repeatflag_1bl

t_list_list, T_list = create_model("T_list", {"progavail":string, "hotelcode":string, "pushrate_flag":bool, "pushavail_flag":bool, "period":int})
t_push_list_list, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int, "license":int})

def if_post_custom_pushall_avail_webbl(t_list_list:[T_list], t_push_list_list:[T_push_list], user_init:string, cur_type:string, from_date:date, to_date:date, bookengid:int):
    v_success = False
    error_msg = ""
    do_it:bool = False
    done_avail:bool = False
    done_rate:bool = False
    counter_rate:int = 0
    p_253:bool = False
    cpushrate:bool = False
    cupdavail:bool = False
    inp_str:string = ""
    max_adult:int = 2
    max_child:int = 0
    htl_code:string = ""

    t_list = t_push_list = temp_list = None

    temp_list_list, Temp_list = create_model("Temp_list", {"rcode":string, "rmtype":string, "zikatnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal v_success, error_msg, do_it, done_avail, done_rate, counter_rate, p_253, cpushrate, cupdavail, inp_str, max_adult, max_child, htl_code
        nonlocal user_init, cur_type, from_date, to_date, bookengid


        nonlocal t_list, t_push_list, temp_list
        nonlocal temp_list_list

        return {"v_success": v_success, "error_msg": error_msg}

    def read_param(t_list_list:[T_list]):

        nonlocal v_success, error_msg, do_it, done_avail, done_rate, counter_rate, p_253, cpushrate, cupdavail, inp_str, max_adult, max_child, htl_code
        nonlocal user_init, cur_type, from_date, to_date, bookengid


        nonlocal t_list, t_push_list, temp_list
        nonlocal temp_list_list

        do_it = True
        cupdavail = False
        cpushrate = False
        inp_str = ""
        pushpax:bool = False
        bedsetup:bool = False
        allotment:bool = False
        incl_tentative:bool = False

        def generate_inner_output():
            return (do_it, cupdavail, cpushrate, inp_str)


        t_list = query(t_list_list, first=True)

        if t_list:
            cpushrate = t_list.pushrate_flag
            htl_code = t_list.hotelcode
            cupdavail = t_list.pushavail_flag

            if num_entries(t_list.progavail, "=") >= 3:
                pushpax = logical(entry(2, t_list.progavail, "="))
            else:
                pushpax = False

            if num_entries(t_list.progavail, "=") >= 10:
                allotment = logical(entry(10, t_list.progavail, "="))
                bedsetup = logical(entry(12, t_list.progavail, "="))
            else:
                allotment = False
                bedsetup = False

            if num_entries(t_list.progavail, "=") >= 24:
                incl_tentative = logical(entry(23, t_list.progavail, "="))
            else:
                incl_tentative = False
        else:
            do_it = False
        inp_str = to_string(incl_tentative) + "=" + to_string(pushpax) + "=" + to_string(allotment) + "=" + to_string(bedsetup)

        return generate_inner_output()

    p_253 = get_output(htplogic(253))

    if p_253:
        error_msg = "Night Audit is running, Please wait until it finish."

        return generate_output()
    do_it, cupdavail, cpushrate, inp_str = read_param(t_list_list)

    if do_it:
        temp_list_list.clear()

        for t_push_list in query(t_push_list_list):
            temp_list = Temp_list()
            temp_list_list.append(temp_list)

            temp_list.rcode = t_push_list.rcodevhp
            temp_list.rmtype = t_push_list.rmtypevhp


    else:
        error_msg = "Configuration not complete."

        return generate_output()

    if cupdavail:
        done_avail = get_output(if_custom_pushall_availbl(cur_type, from_date, to_date, bookengid, inp_str, cpushrate, temp_list_list))

    if cpushrate:
        counter_rate = 1
        done_rate = get_output(if_custom_pushall_ratebl(cur_type, counter_rate, inp_str, from_date, to_date, max_adult, max_child, bookengid, temp_list_list))
    get_output(update_repeatflag_1bl(bookengid))
    v_success = True

    return generate_output()