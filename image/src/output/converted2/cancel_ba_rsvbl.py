#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ba_plan_res_cancel1bl import ba_plan_res_cancel1bl
from functions.ba_plan_res_cancel2bl import ba_plan_res_cancel2bl
from functions.ba_plan_res_cancel3bl import ba_plan_res_cancel3bl
from functions.ba_plan_res_cancel4bl import ba_plan_res_cancel4bl
from functions.ba_plan_check_waitinglistbl import ba_plan_check_waitinglistbl
from models import Bk_reser

def cancel_ba_rsvbl(case_type:int, curr_room:string, curr_status:int, curr_i:int, language_code:int, rml_resnr:int, rml_reslinnr:int, answer_msgstr2:bool, answer_msgstr3:bool, cancel_str:string, user_init:string):
    msg_str1 = ""
    msg_str2 = ""
    msg_str3 = ""
    mess_result = ""
    waiting_list_list = []
    datum:date = None
    raum:string = ""
    von_zeit:string = ""
    bis_zeit:string = ""
    resstatus:int = 0
    b1_resnr:int = 0
    b1_reslinnr:int = 0
    curr_resnr:int = 0
    bk_reser = None

    t_resline = waiting_list = None

    t_resline_list, T_resline = create_model_like(Bk_reser)
    waiting_list_list, Waiting_list = create_model("Waiting_list", {"veran_nr":int, "name":string, "von_zeit":string, "bis_zeit":string, "raum":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str1, msg_str2, msg_str3, mess_result, waiting_list_list, datum, raum, von_zeit, bis_zeit, resstatus, b1_resnr, b1_reslinnr, curr_resnr, bk_reser
        nonlocal case_type, curr_room, curr_status, curr_i, language_code, rml_resnr, rml_reslinnr, answer_msgstr2, answer_msgstr3, cancel_str, user_init


        nonlocal t_resline, waiting_list
        nonlocal t_resline_list, waiting_list_list

        return {"msg_str1": msg_str1, "msg_str2": msg_str2, "msg_str3": msg_str3, "mess_result": mess_result, "waiting-list": waiting_list_list}

    def check_waitinglist(datum:date, raum:string, von_zeit:string, bis_zeit:string, resstatus:int):

        nonlocal msg_str1, msg_str2, msg_str3, mess_result, waiting_list_list, b1_resnr, b1_reslinnr, curr_resnr, bk_reser
        nonlocal case_type, curr_room, curr_status, curr_i, language_code, rml_resnr, rml_reslinnr, answer_msgstr2, answer_msgstr3, cancel_str, user_init


        nonlocal t_resline, waiting_list
        nonlocal t_resline_list, waiting_list_list

        avail_resline:bool = False
        avail_resline, waiting_list_list = get_output(ba_plan_check_waitinglistbl(datum, raum, von_zeit, bis_zeit, resstatus))

        if not avail_resline:

            return

    if user_init == None or user_init == "":
        mess_result = "user init must be filled in"

        return generate_output()

    if case_type == 1:

        if curr_i > 0:
            msg_str1, msg_str2, msg_str3 = get_output(ba_plan_res_cancel1bl(language_code, rml_resnr, rml_reslinnr))
            mess_result = "get messages success"

            return generate_output()
        else:
            mess_result = "Select the reservation first. curr-i cannot using 0 value"

            return generate_output()

    elif case_type == 2:

        if answer_msgstr2 :

            if cancel_str == "":
                mess_result = "Cancel Reason Must be Filled In"

                return generate_output()
            else:
                b1_resnr = rml_resnr
                b1_reslinnr = rml_reslinnr

                if answer_msgstr3 :
                    t_resline_list = get_output(ba_plan_res_cancel2bl(rml_resnr, rml_reslinnr))

                    for t_resline in query(t_resline_list):
                        datum = t_resline.datum
                        raum = t_resline.raum
                        von_zeit = t_resline.von_zeit
                        bis_zeit = t_resline.bis_zeit
                        resstatus = t_resline.resstatus


                        b1_resnr, b1_reslinnr, curr_resnr = get_output(ba_plan_res_cancel3bl(b1_resnr, b1_reslinnr, t_resline.veran_nr, t_resline.veran_resnr, datum, raum, cancel_str, user_init))
                    check_waitinglist(datum, raum, von_zeit, bis_zeit, resstatus)
                    mess_result = "Cancel Banquet Reservation Success"
                else:
                    b1_resnr, b1_reslinnr, curr_resnr, datum, raum, von_zeit, bis_zeit, resstatus = get_output(ba_plan_res_cancel4bl(b1_resnr, b1_reslinnr, rml_resnr, rml_reslinnr, cancel_str, user_init))
                    check_waitinglist(datum, raum, von_zeit, bis_zeit, resstatus)
                    mess_result = "Cancel Banquet Reservation Success"
        else:
            mess_result = "no acction needed with this parameters"

            return generate_output()

    return generate_output()