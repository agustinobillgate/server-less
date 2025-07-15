#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.read_outorderbl import read_outorderbl
from models import Zimmer, Outorder, Paramtext, Res_line

def mk_resline_room_nobl(pvilanguage:int, res_mode:string, prev_zinr:string, curr_zinr:string, prev_zikat:string, curr_zikat:string, reslin_list_zipreis:Decimal, inp_resnr:int, inp_reslinnr:int):

    prepare_cache ([Paramtext, Res_line])

    curr_setup = ""
    msg_str = ""
    inactive_flag = False
    t_zimmer_data = []
    t_outorder_data = []
    lvcarea:string = "mk-resline"
    zimmer = outorder = paramtext = res_line = None

    t_zimmer = t_outorder = None

    t_zimmer_data, T_zimmer = create_model_like(Zimmer)
    t_outorder_data, T_outorder = create_model_like(Outorder)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_setup, msg_str, inactive_flag, t_zimmer_data, t_outorder_data, lvcarea, zimmer, outorder, paramtext, res_line
        nonlocal pvilanguage, res_mode, prev_zinr, curr_zinr, prev_zikat, curr_zikat, reslin_list_zipreis, inp_resnr, inp_reslinnr


        nonlocal t_zimmer, t_outorder
        nonlocal t_zimmer_data, t_outorder_data

        return {"curr_setup": curr_setup, "msg_str": msg_str, "inactive_flag": inactive_flag, "t-zimmer": t_zimmer_data, "t-outorder": t_outorder_data}


    zimmer = get_cache (Zimmer, {"zinr": [(eq, curr_zinr)]})

    if not zimmer:
        msg_str = translateExtended ("No such room number:", lvcarea, "") + " " + to_string(curr_zinr)

        return generate_output()
    t_zimmer = T_zimmer()
    t_zimmer_data.append(t_zimmer)

    buffer_copy(zimmer, t_zimmer)

    if zimmer.setup > 0:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, (9200 + zimmer.setup))]})

        if paramtext:
            curr_setup = substring(paramtext.notes, 0, 1)

    if not zimmer.sleeping:
        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("The room is inactive!", lvcarea, "")
        inactive_flag = True

    if prev_zikat.lower()  != (curr_zikat).lower() :

        if reslin_list_zipreis != 0:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("The Room Type was changed,", lvcarea, "") + chr_unicode(10) + "update the roomrate if necessary."

    if res_mode.lower()  == ("qci").lower() :

        return generate_output()

    if prev_zinr == "":

        return generate_output()

    if prev_zinr.lower()  == (curr_zinr).lower() :

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, inp_reslinnr)]})

    if not res_line:

        return generate_output()

    if res_line.active_flag > 0:

        return generate_output()
    t_outorder_data = get_output(read_outorderbl(1, prev_zinr, inp_resnr, None, None))

    t_outorder = query(t_outorder_data, first=True)

    if t_outorder:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("The Room Type was changed,", lvcarea, "")

    return generate_output()