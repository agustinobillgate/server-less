from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zimmer, Bediener, Res_history, Queasy, Res_line, Outorder

z_list_list, Z_list = create_model("Z_list", {"zinr":str, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":str, "bediener_nr_stat":int, "checkout":bool, "str_reason":str})
om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})
bline_list_list, Bline_list = create_model("Bline_list", {"zinr":str, "selected":bool, "bl_recid":int})

def hk_statadmin_chg_zistatusbl(bline_list:[Bline_list], om_list:[Om_list], pvilanguage:int, ci_date:date, chgsort:int, t_zinr:str, user_init:str, user_nr:int):
    curr_zinr = ""
    curr_stat = ""
    z_list_list = []
    from_stat:str = ""
    to_stat:str = ""
    lvcarea:str = "hk_statadmin"
    stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", ""]
    zimmer = bediener = res_history = queasy = res_line = outorder = None

    z_list = om_list = bline_list = None

    
    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_zinr, curr_stat, from_stat, to_stat, lvcarea, stat_list, zimmer, bediener, res_history, queasy, res_line, outorder


        nonlocal z_list, om_list, bline_list
        global z_list_list, om_list_list, bline_list_list
        return {"curr_zinr": curr_zinr, "curr_stat": curr_stat, "z-list": z_list_list}

    def chg_zistatus():

        nonlocal curr_zinr, curr_stat, from_stat, to_stat, lvcarea, stat_list, zimmer, bediener, res_history, queasy, res_line, outorder


        nonlocal z_list, om_list, bline_list
        global z_list_list, om_list_list, bline_list_list

        result:bool = False

        for bline_list in query(bline_list_list, filters=(lambda bline_list :bline_list.selected)):

            zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == bline_list.zinr)).first()
            from_stat = to_string(zimmer.zistatus) + " " + stat_list[zimmer.zistatus + 1 - 1]

            if chgsort == 8:
                zimmer.zistatus = 8
            else:

                if chgsort == 3 and (zimmer.zistatus <= 1 or zimmer.zistatus == 5) and zimmer.personal :
                    zimmer.personal = False

                if (zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 2):
                    zimmer.zistatus = chgsort - 1

                elif zimmer.zistatus == 4 and chgsort == 1:
                    zimmer.zistatus = 5

                elif zimmer.zistatus == 5 and chgsort == 3:
                    zimmer.zistatus = 4

                elif zimmer.zistatus == 8:
                    zimmer.zistatus = 4
                to_stat = to_string(zimmer.zistatus) + " " + stat_list[zimmer.zistatus + 1 - 1]

                bediener = db_session.query(Bediener).filter(
                            (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Room " + zimmer.zinr +\
                        " Status Changed From " +\
                        from_stat + " to " + to_stat
                res_history.action = "HouseKeeping"

                res_history = db_session.query(Res_history).first()

            zimmer.bediener_nr_stat = user_nr

            zimmer = db_session.query(Zimmer).first()

            if zimmer.zistatus == 0:

                queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 162) &  (Queasy.char1 == zimmer.zinr)).first()

                if queasy:
                    queasy.number1 = 1
                    queasy.char3 = user_init
                    queasy.number3 = get_current_time_in_seconds()
                    queasy.date3 = get_current_date()

                    queasy = db_session.query(Queasy).first()


            om_list = query(om_list_list, filters=(lambda om_list :om_list.zinr == zimmer.zinr), first=True)

            if om_list.ind != 8:
                om_list.ind = zimmer.zistatus + 1

            zimmer = db_session.query(Zimmer).first()
            curr_zinr = zimmer.zinr
            curr_stat = stat_list[zistatus + 1 - 1]
            bline_list.selected = False
        z_list_list.clear()

        for zimmer in db_session.query(Zimmer).all():
            z_list = Z_list()
            z_list_list.append(z_list)

            buffer_copy(zimmer, z_list)

            if zimmer.zistatus == 2:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resstatus == 8) &  (Res_line.zinr == zimmer.zinr) &  (Res_line.abreise == ci_date)).first()

                if res_line:
                    z_list.checkout = True

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr <= 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).first()

            if outorder:
                z_list.str_reason = entry(0, outorder.gespgrund, "$")


            else:
                z_list.str_reason = " "


    stat_list[0] = translateExtended ("Vacant Clean Checked", lvcarea, "")
    stat_list[1] = translateExtended ("Vacant Clean Unchecked", lvcarea, "")
    stat_list[2] = translateExtended ("Vacant Dirty", lvcarea, "")
    stat_list[3] = translateExtended ("Expected Departure", lvcarea, "")
    stat_list[4] = translateExtended ("Occupied Dirty", lvcarea, "")
    stat_list[5] = translateExtended ("Occupied Cleaned", lvcarea, "")
    stat_list[6] = translateExtended ("Out_of_Order", lvcarea, "")
    stat_list[7] = translateExtended ("Off_Market", lvcarea, "")
    stat_list[8] = translateExtended ("Do not Disturb", lvcarea, "")
    stat_list[9] = translateExtended ("Out_of_Service", lvcarea, "")

    zimmer = db_session.query(Zimmer).filter(
            (func.lower(Zimmer.zinr) == (t_zinr).lower())).first()
    chg_zistatus()

    return generate_output()