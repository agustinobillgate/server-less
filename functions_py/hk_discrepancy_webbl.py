#using conversion tools version: 1.0.0.117

# =======================================
# Rulita, 15-10-2025 
# Tiket ID : 6526C2 | New compile program
# =======================================
# Rd, 27/11/2025, with_for_update added
# =======================================
from functions.additional_functions import *
from decimal import Decimal
from models import Zimmer, Bediener, Res_line

def hk_discrepancy_webbl(pvilanguage:int, case_type:string, zinno:string, housestat:int, feat:string, fo_stat1:string, 
                         hk_stat1:string, user_init:string, hk_str:string, fo_pax:int, fo_ch1:int, hk_pax:int, hk_ch1:int):

    prepare_cache ([Zimmer, Bediener, Res_line])

    msg_str = ""
    fo_stat = ""
    hk_stat = ""
    hkdiscrepancy_list_data = []
    rmplan_data = []
    lvcarea:string = "hk-discrepancy"
    i:int = 0
    zimmer = bediener = res_line = None

    hkdiscrepancy_list = rmplan = room = usr = None

    hkdiscrepancy_list_data, Hkdiscrepancy_list = create_model("Hkdiscrepancy_list", {"zinr":string, "features":string, "etage":int, "bezeich":string, "house_status":int, "zistatus":int, "userinit":string, "nr":int, "fo_status":string, "hk_status":string, "fo_a":int, "hk_a":int, "fo_ch":int, "hk_ch":int, "reason":string, "zeit":string})
    rmplan_data, Rmplan = create_model("Rmplan", {"nr":int, "str":string})

    Room = create_buffer("Room",Zimmer)
    Usr = create_buffer("Usr",Bediener)

    db_session = local_storage.db_session
    case_type = case_type.strip()
    zinno = zinno.strip()
    feat = feat.strip()
    fo_stat1 = fo_stat1.strip()
    hk_stat1 = hk_stat1.strip()
    hk_str = hk_str.strip()

    def generate_output():
        nonlocal msg_str, fo_stat, hk_stat, hkdiscrepancy_list_data, rmplan_data, lvcarea, i, zimmer, bediener, res_line
        nonlocal pvilanguage, case_type, zinno, housestat, feat, fo_stat1, hk_stat1, user_init, hk_str, fo_pax, fo_ch1, hk_pax, hk_ch1
        nonlocal room, usr


        nonlocal hkdiscrepancy_list, rmplan, room, usr
        nonlocal hkdiscrepancy_list_data, rmplan_data

        return {"fo_pax": fo_pax, "fo_ch1": fo_ch1, "msg_str": msg_str, "fo_stat": fo_stat, "hk_stat": hk_stat, "hkdiscrepancy-list": hkdiscrepancy_list_data, "rmplan": rmplan_data}

    def disp_it():

        nonlocal msg_str, fo_stat, hk_stat, hkdiscrepancy_list_data, rmplan_data, lvcarea, i, zimmer, bediener, res_line
        nonlocal pvilanguage, case_type, zinno, housestat, feat, fo_stat1, hk_stat1, user_init, hk_str, fo_pax, fo_ch1, hk_pax, hk_ch1
        nonlocal room, usr


        nonlocal hkdiscrepancy_list, rmplan, room, usr
        nonlocal hkdiscrepancy_list_data, rmplan_data

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.house_status != 0)).order_by(Zimmer.zinr).all():
            hkdiscrepancy_list = Hkdiscrepancy_list()
            hkdiscrepancy_list_data.append(hkdiscrepancy_list)

            hkdiscrepancy_list.zinr = zimmer.zinr
            hkdiscrepancy_list.features = zimmer.features
            hkdiscrepancy_list.etage = zimmer.etage
            hkdiscrepancy_list.bezeich = zimmer.bezeich
            hkdiscrepancy_list.house_status = zimmer.house_status
            hkdiscrepancy_list.zistatus = zimmer.zistatus
            hkdiscrepancy_list.fo_status = substring(zimmer.features, 0, 12)
            hkdiscrepancy_list.hk_status = substring(zimmer.features, 12, 12)
            hkdiscrepancy_list.fo_a = to_int(substring(zimmer.features, 65, 2))
            hkdiscrepancy_list.hk_a = to_int(substring(zimmer.features, 69, 2))
            hkdiscrepancy_list.fo_ch = to_int(substring(zimmer.features, 67, 2))
            hkdiscrepancy_list.hk_ch = to_int(substring(zimmer.features, 71, 2))
            hkdiscrepancy_list.reason = substring(zimmer.features, 33, 32)
            hkdiscrepancy_list.zeit = substring(zimmer.features, 28, 5)

            bediener = get_cache (Bediener, {"userinit": [(eq, trim(substring(zimmer.features, 24, 4)))]})

            if bediener:
                hkdiscrepancy_list.userinit = bediener.userinit
                hkdiscrepancy_list.nr = bediener.nr

    if case_type.lower()  == ("deactivate-disc").lower() :

        # zimmer = get_cache (Zimmer, {"zinr": [(eq, zinno)]})
        zimmer = db_session.query(Zimmer).filter(Zimmer.zinr == zinno).with_for_update().first()
        zimmer.house_status = housestat
        zimmer.features = feat


        pass

    elif case_type.lower()  == ("cr-rmplan").lower() :

        for room in db_session.query(Room).filter(
                 (Room.house_status > 0)).order_by(Room._recid).all():

            usr = get_cache (Bediener, {"userinit": [(eq, substring(room.features, 24, 2))]})
            i = i + 1

            if (i % 2) != 0:
                rmplan = Rmplan()
                rmplan_data.append(rmplan)

                rmplan.nr = i
                rmplan.str = rmplan.str + to_string(room.zinr, "x(6)") + to_string(substring(room.features, 0, 12) , "x(12)") + to_string(substring(room.features, 63, 2) , "x(2)") + to_string(substring(room.features, 65, 2) , "x(2)") + to_string(substring(room.features, 12, 12) , "x(12)") + to_string(substring(room.features, 67, 2) , "x(2)") + to_string(substring(room.features, 69, 2) , "x(2)") + to_string(substring(room.features, 31, 32) , "x(32)")
            else:
                rmplan.str = rmplan.str + to_string(room.zinr, "x(6)") + to_string(substring(room.features, 0, 12) , "x(12)") + to_string(substring(room.features, 63, 2) , "x(2)") + to_string(substring(room.features, 65, 2) , "x(2)") + to_string(substring(room.features, 12, 12) , "x(12)") + to_string(substring(room.features, 67, 2) , "x(2)") + to_string(substring(room.features, 69, 2) , "x(2)") + to_string(substring(room.features, 31, 32) , "x(32)")

    elif case_type.lower()  == ("of-zinr").lower() :

        zimmer = get_cache (Zimmer, {"zinr": [(eq, zinno)]})

        if not zimmer:
            msg_str = translateExtended ("Room not found", lvcarea, "")

        elif zimmer and zimmer.house_status != 0:
            msg_str = translateExtended ("Discrepancy already defined for this room.", lvcarea, "")
        else:

            if zimmer.zistatus <= 2:
                fo_stat = translateExtended ("Vacant", lvcarea, "")
                hk_stat = translateExtended ("Occupied", lvcarea, "")

            elif zimmer.zistatus <= 5 or zimmer.zistatus == 8:
                fo_stat = translateExtended ("Occupied", lvcarea, "")
                hk_stat = ""

            elif zimmer.zistatus == 6:
                fo_stat = translateExtended ("Occupied", lvcarea, "")
                hk_stat = translateExtended ("Out-Of-Order", lvcarea, "")

        if zinno != "":

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag == 1) & (Res_line.zinr == zinno) & (Res_line.resstatus == 6) | (Res_line.resstatus == 13)).order_by(Res_line._recid).all():
                fo_pax = fo_pax + res_line.erwachs + res_line.gratis
                fo_ch1 = fo_ch1 + res_line.kind1

    elif case_type.lower()  == ("of-exit").lower() :

        # zimmer = get_cache (Zimmer, {"zinr": [(eq, zinno)]})
        zimmer = db_session.query(Zimmer).filter(Zimmer.zinr == zinno).with_for_update().first()

        if zimmer:
            pass
            zimmer.house_status = 1
            zimmer.features = " "


            overlay (zimmer.features, 1 ,to_string(fo_stat1))
            overlay (zimmer.features, 13 ,to_string(hk_stat1))
            overlay (zimmer.features, 25 ,to_string(user_init))
            overlay (zimmer.features, 29 ,to_string(get_current_time_in_seconds(), "HH:MM"))
            overlay (zimmer.features, 34 ,to_string(hk_str))
            overlay (zimmer.features, 66 ,to_string(fo_pax))
            overlay (zimmer.features, 68 ,to_string(fo_ch1))
            overlay (zimmer.features, 70 ,to_string(hk_pax))
            overlay (zimmer.features, 72 ,to_string(hk_ch1))
            pass
            pass
    disp_it()

    return generate_output()