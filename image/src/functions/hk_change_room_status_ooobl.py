from functions.additional_functions import *
import decimal
from datetime import date
from functions.hk_statadmin_start_chgstatbl import hk_statadmin_start_chgstatbl
from functions.prepare_hk_statadminbl import prepare_hk_statadminbl
from sqlalchemy import func
from functions.hk_statadmin_activate_ooobl import hk_statadmin_activate_ooobl
from models import Zimkateg, Bediener, Outorder

room_list_list, Room_list = create_model("Room_list", {"nr":str})

def hk_change_room_status_ooobl(pvilanguage:int, user_init:str, from_date:date, to_date:date, dept:int, reason:str, service_flag:bool, room_list_list:[Room_list]):
    rec_id = 0
    msg_str = ""
    lvcarea:str = "hk-change-room-status"
    t_zinr:str = ""
    t_zistatus:int = 0
    ci_date:date = None
    flag:int = 0
    zimkateg = bediener = outorder = None

    bline_list = t_bline_list = room_list = z_list = om_list = t_zimkateg = setup_list = None

    bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})
    t_bline_list_list, T_bline_list = create_model_like(Bline_list)
    z_list_list, Z_list = create_model("Z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str})
    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})
    t_zimkateg_list, T_zimkateg = create_model_like(Zimkateg)
    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rec_id, msg_str, lvcarea, t_zinr, t_zistatus, ci_date, flag, zimkateg, bediener, outorder
        nonlocal pvilanguage, user_init, from_date, to_date, dept, reason, service_flag


        nonlocal bline_list, t_bline_list, room_list, z_list, om_list, t_zimkateg, setup_list
        nonlocal bline_list_list, t_bline_list_list, room_list_list, z_list_list, om_list_list, t_zimkateg_list, setup_list_list
        return {"rec_id": rec_id, "msg_str": msg_str}

    for room_list in query(room_list_list):
        bline_list = Bline_list()
        bline_list_list.append(bline_list)

        bline_list.selected = True
        bline_list.zinr = room_list.nr
    flag, t_zinr, t_zistatus = get_output(hk_statadmin_start_chgstatbl(4, bline_list))

    if flag == 4:
        flag = 6

    if flag == 6:
        ci_date, z_list_list, om_list_list, t_bline_list_list, setup_list_list, t_zimkateg_list = get_output(prepare_hk_statadminbl("", 0, 0, 0))

        if not bediener or not(bediener.userinit.lower()  == (user_init).lower()):
            bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        bline_list_list, om_list_list, flag, msg_str, z_list_list = get_output(hk_statadmin_activate_ooobl(bline_list, om_list, pvilanguage, from_date, to_date, ci_date, dept, reason, service_flag, bediener.nr))

        if flag == 1:
            msg_str = translateExtended ("Overlapping O-O-O or O-M record found!", lvcarea, "") + " " + to_string(bline_list.zinr)
        else:

            if not room_list:
                room_list = query(room_list_list, first=True)

            if room_list:

                if not outorder or not(outorder.zinr == room_list.nr and outorder.gespstart == from_date and outorder.gespende == to_date):
                    outorder = db_session.query(Outorder).filter(
                        (Outorder.zinr == room_list.nr) &  (Outorder.gespstart == from_date) &  (Outorder.gespende == to_date)).first()

                if outorder:
                    rec_id = outorder._recid
    else:

        if flag == 1:
            msg_str = translateExtended ("To change room status select room(s) first.", lvcarea, "")

        elif flag == 5:
            msg_str = translateExtended ("Status Changes not possible.", lvcarea, "")

    return generate_output()