#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.hk_statadmin_start_chgstatbl import hk_statadmin_start_chgstatbl
from functions.prepare_hk_statadminbl import prepare_hk_statadminbl
from functions.hk_statadmin_deactivate_ooobl import hk_statadmin_deactivate_ooobl
from functions.hk_statadmin_chg_zistatusbl import hk_statadmin_chg_zistatusbl
from models import Zimkateg, Bediener

room_list_data, Room_list = create_model("Room_list", {"nr":string})

def hk_change_room_statusbl(pvilanguage:int, chgsort:int, user_init:string, room_list_data:[Room_list]):

    prepare_cache ([Bediener])

    msg_str = ""
    lvcarea:string = "hk-change-room-status"
    t_zinr:string = ""
    t_zistatus:int = 0
    ci_date:date = None
    curr_zinr:string = ""
    curr_stat:string = ""
    flag:int = 0
    zimkateg = bediener = None

    bline_list = t_bline_list = room_list = z_list = om_list = t_zimkateg = setup_list = None

    bline_list_data, Bline_list = create_model("Bline_list", {"zinr":string, "selected":bool, "bl_recid":int})
    t_bline_list_data, T_bline_list = create_model("T_bline_list", {"zinr":string, "selected":bool, "bl_recid":int})
    z_list_data, Z_list = create_model("Z_list", {"zinr":string, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":string, "bediener_nr_stat":int, "checkout":bool, "str_reason":string})
    om_list_data, Om_list = create_model("Om_list", {"zinr":string, "ind":int})
    t_zimkateg_data, T_zimkateg = create_model_like(Zimkateg)
    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, lvcarea, t_zinr, t_zistatus, ci_date, curr_zinr, curr_stat, flag, zimkateg, bediener
        nonlocal pvilanguage, chgsort, user_init


        nonlocal bline_list, t_bline_list, room_list, z_list, om_list, t_zimkateg, setup_list
        nonlocal bline_list_data, t_bline_list_data, z_list_data, om_list_data, t_zimkateg_data, setup_list_data

        return {"msg_str": msg_str}

    if chgsort != 4 and chgsort != 5:

        for room_list in query(room_list_data):
            bline_list = Bline_list()
            bline_list_data.append(bline_list)

            bline_list.selected = True
            bline_list.zinr = room_list.nr
        flag, t_zinr, t_zistatus = get_output(hk_statadmin_start_chgstatbl(chgsort, bline_list_data))

        if flag == 4:
            flag = 6

        if flag == 6:
            ci_date, z_list_data, om_list_data, t_bline_list_data, setup_list_data, t_zimkateg_data = get_output(prepare_hk_statadminbl("", 0, 0, 0))

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if t_zistatus == 6:

                if chgsort == 4:
                    msg_str = translateExtended ("Status Changes not possible.", lvcarea, "")
                else:
                    bline_list_data, om_list_data, z_list_data = get_output(hk_statadmin_deactivate_ooobl(bline_list_data, om_list_data, ci_date, bediener.nr, chgsort))
            else:
                bline_list_data, om_list_data, curr_zinr, curr_stat, z_list_data = get_output(hk_statadmin_chg_zistatusbl(bline_list_data, om_list_data, 0, ci_date, chgsort, "", user_init, bediener.nr))
        else:

            if flag == 1:
                msg_str = translateExtended ("To change room status select room(s) first.", lvcarea, "")

            elif flag == 2:
                msg_str = translateExtended ("Set back DO NOT DISTURB to status dirty.", lvcarea, "")

            elif flag == 3:
                msg_str = translateExtended ("DO NOT DISTURB is for Occupied Dirty Rooms only.", lvcarea, "")

            elif flag == 5:
                msg_str = translateExtended ("Status Changes not possible.", lvcarea, "")

    return generate_output()