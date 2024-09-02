from functions.additional_functions import *
import decimal
from datetime import date
from functions.mk_resline_set_ratebl import mk_resline_set_ratebl
from models import Res_line, Arrangement

def mk_resline_leave_argbl(pvilanguage:int, res_mode:str, old_arg:str, contcode:str, curr_arg:str, fixed_rate:bool, ebdisc_flag:bool, kbdisc_flag:bool, rate_readonly:bool, bookdate:date, reslin_list:[Reslin_list]):
    value_ok = False
    restricted_disc = False
    new_rate = 0
    msg_str = ""
    rate_tooltip = ""
    lvcarea:str = "mk_resline"
    res_line = arrangement = None

    reslin_list = None

    reslin_list_list, Reslin_list = create_model_like(Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal value_ok, restricted_disc, new_rate, msg_str, rate_tooltip, lvcarea, res_line, arrangement


        nonlocal reslin_list
        nonlocal reslin_list_list
        return {"value_ok": value_ok, "restricted_disc": restricted_disc, "new_rate": new_rate, "msg_str": msg_str, "rate_tooltip": rate_tooltip}

    def leave_argt():

        nonlocal value_ok, restricted_disc, new_rate, msg_str, rate_tooltip, lvcarea, res_line, arrangement


        nonlocal reslin_list
        nonlocal reslin_list_list

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == reslin_list.arrangement)).first()

        if not arrangement:
            msg_str = translateExtended ("No such Arrangement", lvcarea, "")

            return

        if (reslin_list.resstatus == 11 or reslin_list.resstatus == 13) and (reslin_list.erwachs + reslin_list.kind1) == 0:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reslin_list.resnr) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6)) &  (Res_line.zinr == reslin_list.zinr)).first()

            if res_line and res_line.arrangement != reslin_list.arrangement:
                msg_str = translateExtended ("Wrong Arrangement as Room Sharer with adult  ==  0", lvcarea, "")

                return

        if arrangement.waeschewechsel != 0 and reslin_list.erwachs != arrangement.waeschewechsel:
            msg_str = translateExtended ("Wrong Arrangement / Adult", lvcarea, "")

            return

        if arrangement.handtuch != 0 and reslin_list.anztage != arrangement.handtuch:
            msg_str = translateExtended ("Wrong Arrangement / Night of Stay", lvcarea, "")

            return
        value_ok = True
        curr_arg = reslin_list.arrangement

        if curr_arg.lower()  != (old_arg).lower() :

            if (res_mode.lower()  == "new" or res_mode.lower().lower()  == "insert"):
                restricted_disc, new_rate, rate_tooltip = get_output(mk_resline_set_ratebl(False, fixed_rate, ebdisc_flag, kbdisc_flag, rate_readonly, reslin_list.gastnr, res_mode, curr_arg, contcode, bookdate, reslin_list))
        else:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reslin_list.resnr) &  (Res_line.reslinnr == reslin_list.reslinnr)).first()

            if res_line and (curr_arg != res_line.arrangement):
                msg_str = translateExtended ("Arrangement changed, re_check the RoomRate.", lvcarea, "")

    reslin_list = query(reslin_list_list, first=True)
    leave_argt()

    return generate_output()