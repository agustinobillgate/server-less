from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.read_outorderbl import read_outorderbl
from models import Zimmer, Outorder, Paramtext, Res_line

def mk_resline_room_nobl(pvilanguage:int, res_mode:str, prev_zinr:str, curr_zinr:str, prev_zikat:str, curr_zikat:str, reslin_list_zipreis:decimal, inp_resnr:int, inp_reslinnr:int):
    curr_setup = ""
    msg_str = ""
    inactive_flag = False
    t_zimmer_list = []
    t_outorder_list = []
    lvcarea:str = "mk_resline"
    zimmer = outorder = paramtext = res_line = None

    t_zimmer = t_outorder = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)
    t_outorder_list, T_outorder = create_model_like(Outorder)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_setup, msg_str, inactive_flag, t_zimmer_list, t_outorder_list, lvcarea, zimmer, outorder, paramtext, res_line


        nonlocal t_zimmer, t_outorder
        nonlocal t_zimmer_list, t_outorder_list
        return {"curr_setup": curr_setup, "msg_str": msg_str, "inactive_flag": inactive_flag, "t-zimmer": t_zimmer_list, "t-outorder": t_outorder_list}


    zimmer = db_session.query(Zimmer).filter(
            (func.lower(Zimmer.zinr) == (curr_zinr).lower())).first()

    if not zimmer:
        msg_str = translateExtended ("No such room number:", lvcarea, "") + " " + to_string(curr_zinr)

        return generate_output()
    t_zimmer = T_zimmer()
    t_zimmer_list.append(t_zimmer)

    buffer_copy(zimmer, t_zimmer)

    if zimmer.setup > 0:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == (9200 + zimmer.setup))).first()

        if paramtext:
            curr_setup = substring(paramtext.notes, 0, 1)

    if not zimmer.sleeping:
        msg_str = msg_str + chr(2) + "&W" + translateExtended ("The room is inactive!", lvcarea, "")
        inactive_flag = True

    if prev_zikat.lower()  != (curr_zikat).lower() :

        if reslin_list_zipreis != 0:
            msg_str = msg_str + chr(2) + translateExtended ("The Room Type was changed,", lvcarea, "") + chr(10) + "update the roomrate if necessary."

    if res_mode.lower()  == "qci":

        return generate_output()

    if prev_zinr == "":

        return generate_output()

    if prev_zinr.lower()  == (curr_zinr).lower() :

        return generate_output()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_reslinnr)).first()

    if not res_line:

        return generate_output()

    if res_line.active_flag > 0:

        return generate_output()
    t_outorder_list = get_output(read_outorderbl(1, prev_zinr, inp_resnr, None, None))

    t_outorder = query(t_outorder_list, first=True)

    if t_outorder:
        msg_str = msg_str + chr(2) + translateExtended ("The Room Type was changed,", lvcarea, "")

    return generate_output()