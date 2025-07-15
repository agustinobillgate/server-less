#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.mk_resline_set_ratebl import mk_resline_set_ratebl
from models import Res_line, Arrangement

reslin_list_data, Reslin_list = create_model_like(Res_line)

def mk_resline_leave_argbl(pvilanguage:int, res_mode:string, old_arg:string, contcode:string, curr_arg:string, fixed_rate:bool, ebdisc_flag:bool, kbdisc_flag:bool, rate_readonly:bool, bookdate:date, reslin_list_data:[Reslin_list]):

    prepare_cache ([Res_line, Arrangement])

    value_ok = False
    restricted_disc = False
    new_rate = None
    msg_str = ""
    rate_tooltip = None
    lvcarea:string = "mk-resline"
    res_line = arrangement = None

    reslin_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal value_ok, restricted_disc, new_rate, msg_str, rate_tooltip, lvcarea, res_line, arrangement
        nonlocal pvilanguage, res_mode, old_arg, contcode, curr_arg, fixed_rate, ebdisc_flag, kbdisc_flag, rate_readonly, bookdate


        nonlocal reslin_list

        return {"curr_arg": curr_arg, "value_ok": value_ok, "restricted_disc": restricted_disc, "new_rate": new_rate, "msg_str": msg_str, "rate_tooltip": rate_tooltip}

    def leave_argt():

        nonlocal value_ok, restricted_disc, new_rate, msg_str, rate_tooltip, lvcarea, res_line, arrangement
        nonlocal pvilanguage, res_mode, old_arg, contcode, curr_arg, fixed_rate, ebdisc_flag, kbdisc_flag, rate_readonly, bookdate


        nonlocal reslin_list

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, reslin_list.arrangement)]})

        if not arrangement:
            msg_str = translateExtended ("No such Arrangement", lvcarea, "")

            return

        if (reslin_list.resstatus == 11 or reslin_list.resstatus == 13) and (reslin_list.erwachs + reslin_list.kind1) == 0:

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == reslin_list.resnr) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6)) & (Res_line.zinr == reslin_list.zinr)).first()

            if res_line and res_line.arrangement != reslin_list.arrangement:
                msg_str = translateExtended ("Wrong Arrangement as Room Sharer with adult = 0", lvcarea, "")

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

            if (res_mode.lower()  == ("new").lower()  or res_mode.lower()  == ("insert").lower()):
                restricted_disc, new_rate, rate_tooltip = get_output(mk_resline_set_ratebl(False, fixed_rate, ebdisc_flag, kbdisc_flag, rate_readonly, reslin_list.gastnr, res_mode, curr_arg, contcode, bookdate, reslin_list_data))
        else:

            res_line = get_cache (Res_line, {"resnr": [(eq, reslin_list.resnr)],"reslinnr": [(eq, reslin_list.reslinnr)]})

            if res_line and (curr_arg != res_line.arrangement):
                msg_str = translateExtended ("Arrangement changed, re-check the RoomRate.", lvcarea, "")


    reslin_list = query(reslin_list_data, first=True)
    leave_argt()

    return generate_output()