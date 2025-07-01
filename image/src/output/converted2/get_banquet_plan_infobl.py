#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ba_plan_disp_resdatabl import ba_plan_disp_resdatabl

def get_banquet_plan_infobl(curr_view:string, rml_bezeich:string, rml_raum:string, rml_nr:int, rml_blocked:int, rml_resnr:int, rml_reslinnr:int, curr_i:int, from_date:date):
    mess_str = ""
    info1 = ""
    info2 = ""
    info3 = ""
    rsl_list = []
    curr_room:string = ""
    curr_status:int = 0
    odate:date = None
    b1_resnr:int = 0
    b1_reslinnr:int = 0
    out_i:int = 0

    rsl = None

    rsl_list, Rsl = create_model("Rsl", {"resnr":int, "reslinnr":int, "resstatus":int, "sdate":date, "ndate":date, "stime":string, "ntime":string, "created_date":date, "venue":string, "userinit":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, info1, info2, info3, rsl_list, curr_room, curr_status, odate, b1_resnr, b1_reslinnr, out_i
        nonlocal curr_view, rml_bezeich, rml_raum, rml_nr, rml_blocked, rml_resnr, rml_reslinnr, curr_i, from_date


        nonlocal rsl
        nonlocal rsl_list

        return {"mess_str": mess_str, "info1": info1, "info2": info2, "info3": info3, "rsl": rsl_list}

    def mrl():

        nonlocal mess_str, info1, info2, info3, rsl_list, curr_room, curr_status, odate, b1_resnr, b1_reslinnr, out_i
        nonlocal curr_view, rml_bezeich, rml_raum, rml_nr, rml_blocked, rml_resnr, rml_reslinnr, curr_i, from_date


        nonlocal rsl
        nonlocal rsl_list


        curr_room = rml_raum
        curr_status = rml_nr
        marking_rml2()


    def marking_rml2():

        nonlocal mess_str, info1, info2, info3, rsl_list, curr_room, curr_status, odate, b1_resnr, b1_reslinnr, out_i
        nonlocal curr_view, rml_bezeich, rml_raum, rml_nr, rml_blocked, rml_resnr, rml_reslinnr, curr_i, from_date


        nonlocal rsl
        nonlocal rsl_list

        old_room:string = ""
        old_status:int = 0

        if rml_blocked != 0:
            mess_str = "This is blocked Reservation!"

            return
        odate = from_date

        if curr_view.lower()  == ("weekly").lower() :
            pass
        marking_rml(curr_i)


    def marking_rml(i:int):

        nonlocal mess_str, info1, info2, info3, rsl_list, curr_room, curr_status, odate, b1_resnr, b1_reslinnr, out_i
        nonlocal curr_view, rml_bezeich, rml_raum, rml_nr, rml_blocked, rml_resnr, rml_reslinnr, curr_i, from_date


        nonlocal rsl
        nonlocal rsl_list


        disp_resdata()
        b1_resnr = rml_resnr
        b1_reslinnr = rml_reslinnr


    def init_info():

        nonlocal mess_str, info1, info2, info3, rsl_list, curr_room, curr_status, odate, b1_resnr, b1_reslinnr, out_i
        nonlocal curr_view, rml_bezeich, rml_raum, rml_nr, rml_blocked, rml_resnr, rml_reslinnr, curr_i, from_date


        nonlocal rsl
        nonlocal rsl_list


        info1 = ""
        info2 = ""
        info3 = ""
        rsl_list.clear()


    def disp_resdata():

        nonlocal mess_str, info1, info2, info3, rsl_list, curr_room, curr_status, odate, b1_resnr, b1_reslinnr, out_i
        nonlocal curr_view, rml_bezeich, rml_raum, rml_nr, rml_blocked, rml_resnr, rml_reslinnr, curr_i, from_date


        nonlocal rsl
        nonlocal rsl_list

        b_time:int = 0
        i:int = 0
        init_info()
        info1, info2, info3, rsl_list = get_output(ba_plan_disp_resdatabl(rml_raum, rml_resnr, rml_reslinnr))

        if curr_view.lower()  == ("daily").lower() :
            b_time = round ((curr_i / 2) , 0) - 1
            info2 = "Date: " + to_string(from_date) + " Time:"

            if round((curr_i / 2) - 0.1, 0) * 2 < curr_i:
                info2 = info2 + to_string(b_time, "99") + ":00 - " + to_string(b_time, "99") + ":30"
            else:
                info2 = info2 + to_string(b_time, "99") + ":30 - " + to_string(b_time + 1, "99") + ":00"
        else:
            info2 = "Date: " + to_string(odate) + " Time:"

            if out_i > 0:
                b_time = round ((out_i / 2) , 0) - 1

                if round ((out_i / 2) - 0.1, 0) * 2 < out_i:
                    info2 = info2 + to_string(b_time, "99") + ":00 - " + to_string(b_time, "99") + ":30"
                else:
                    info2 = info2 + to_string(b_time, "99") + ":30 - " + to_string(b_time + 1, "99") + ":00"
            else:
                b_time = 0
                info2 = info2 + "00:00 - 00:00"

    mrl()

    return generate_output()