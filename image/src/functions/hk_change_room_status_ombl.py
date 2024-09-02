from functions.additional_functions import *
import decimal
from datetime import date

from sqlalchemy import func

from models import Zimkateg, Bediener

room_list_list, Room_list = create_model("Room_list", {"nr":str})
bline_list = t_bline_list = room_list = z_list = om_list = t_zimkateg = setup_list = None

bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})
t_bline_list_list, T_bline_list = create_model_like(Bline_list)
z_list_list, Z_list = create_model("Z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str})
om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})
t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})

from functions.hk_statadmin_start_chgstatbl import hk_statadmin_start_chgstatbl
from functions.prepare_hk_statadminbl import prepare_hk_statadminbl
from functions.hk_statadmin_chk_btn_exitbl import hk_statadmin_chk_btn_exitbl
from functions.hk_statadmin_chk_btn_exit1bl import hk_statadmin_chk_btn_exit1bl

def hk_change_room_status_ombl(pvilanguage:int, user_init:str, from_date:date, to_date:date, reason:str, room_list_list:[Room_list]):
    msg_str = ""
    lvcarea:str = "hk-change-room-status"
    t_zinr:str = ""
    t_zistatus:int = 0
    ci_date:date = None
    t_resname:str = ""
    flag:int = 0
    zimkateg = bediener = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, t_zinr, t_zistatus, ci_date, t_resname, flag, zimkateg, bediener
        nonlocal pvilanguage, user_init, from_date, to_date, reason
        nonlocal bline_list, room_list

        global t_bline_list, z_list, om_list, t_zimkateg, setup_list
        nonlocal bline_list_list, t_bline_list_list, room_list_list, z_list_list, om_list_list, t_zimkateg_list, setup_list_list
        return {"msg_str": msg_str}

    for room_list in query(room_list_list):
        bline_list = Bline_list()
        bline_list_list.append(bline_list)

        bline_list.selected = True
        bline_list.zinr = room_list.nr
    flag, t_zinr, t_zistatus = get_output(hk_statadmin_start_chgstatbl(5, bline_list))

    if flag == 4:
        flag = 6

    if flag == 6:
        ci_date, z_list_list, om_list_list, t_bline_list_list, setup_list_list, t_zimkateg_list = get_output(prepare_hk_statadminbl("", 0, 0, 0))

        if not bediener or not(bediener.userinit.lower()  == (user_init).lower()):
            bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        flag, msg_str, t_resname = get_output(hk_statadmin_chk_btn_exitbl(pvilanguage, TRUE, 0, t_zinr, from_date, to_date))

        if flag == 1:
            msg_str = translateExtended ("No such reservation number.", lvcarea, "")

        elif flag == 2:
            msg_str = translateExtended ("Guest already checked-in. Blocking no longer possible.", lvcarea, "")

        if flag != 0:

            return generate_output()
        bline_list_list, om_list_list, msg_str, z_list_list = get_output(hk_statadmin_chk_btn_exit1bl(bline_list, om_list, pvilanguage, TRUE, 0, t_zinr, bediener.nr, from_date, to_date, ci_date, reason))
    else:

        if flag == 1:
            msg_str = translateExtended ("To change room status select room(s) first.", lvcarea, "")

        elif flag == 5:
            msg_str = translateExtended ("Status Changes not possible.", lvcarea, "")

    return generate_output()