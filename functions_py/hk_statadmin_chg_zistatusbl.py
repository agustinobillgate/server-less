#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Bediener, Res_history, Queasy, Res_line, Outorder

bline_list_data, Bline_list = create_model("Bline_list", {"zinr":string, "selected":bool, "bl_recid":int})
om_list_data, Om_list = create_model("Om_list", {"zinr":string, "ind":int})

def hk_statadmin_chg_zistatusbl(bline_list_data:[Bline_list], om_list_data:[Om_list], pvilanguage:int, ci_date:date, chgsort:int, 
                                t_zinr:string, user_init:string, user_nr:int):

    prepare_cache ([Bediener, Res_history, Queasy, Outorder])

    curr_zinr = ""
    curr_stat = ""
    z_list_data = []
    from_stat:string = ""
    to_stat:string = ""
    lvcarea:string = "hk-statadmin"
    stat_list:List[string] = create_empty_list(10,"")
    zimmer = bediener = res_history = queasy = res_line = outorder = None

    z_list = om_list = bline_list = None

    z_list_data, Z_list = create_model("Z_list", {"zinr":string, "setup":int, "zikatnr":int, "etage":int, "zistatus":int, "code":string, "bediener_nr_stat":int, "checkout":bool, "str_reason":string})

    db_session = local_storage.db_session
    t_zinr = t_zinr.strip()

    def generate_output():
        nonlocal curr_zinr, curr_stat, z_list_data, from_stat, to_stat, lvcarea, stat_list, zimmer, bediener, res_history, queasy, res_line, outorder
        nonlocal pvilanguage, ci_date, chgsort, t_zinr, user_init, user_nr


        nonlocal z_list, om_list, bline_list
        nonlocal z_list_data

        return {"bline-list": bline_list_data, "om-list": om_list_data, "curr_zinr": curr_zinr, "curr_stat": curr_stat, "z-list": z_list_data}

    def chg_zistatus():

        nonlocal curr_zinr, curr_stat, z_list_data, from_stat, to_stat, lvcarea, stat_list, zimmer, bediener, res_history, queasy, res_line, outorder
        nonlocal pvilanguage, ci_date, chgsort, t_zinr, user_init, user_nr


        nonlocal z_list, om_list, bline_list
        nonlocal z_list_data

        result:bool = False

        for bline_list in query(bline_list_data, filters=(lambda bline_list: bline_list.selected)):

            # zimmer = get_cache (Zimmer, {"zinr": [(eq, bline_list.zinr)]})
            zimmer = db_session.query(Zimmer).filter(
                     (Zimmer.zinr == bline_list.zinr)).with_for_update().first()
            
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

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Room " + zimmer.zinr +\
                        " Status Changed From " +\
                        from_stat + " to " + to_stat
                res_history.action = "HouseKeeping"


                pass
                pass
            zimmer.bediener_nr_stat = user_nr
            pass

            if zimmer.zistatus == 0:

                # queasy = get_cache (Queasy, {"key": [(eq, 162)],"char1": [(eq, zimmer.zinr)]})
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 162) & (Queasy.char1 == zimmer.zinr)).with_for_update().first()

                if queasy:
                    queasy.number1 = 1
                    queasy.char3 = user_init
                    queasy.number3 = get_current_time_in_seconds()
                    queasy.date3 = get_current_date()


                    pass

            om_list = query(om_list_data, filters=(lambda om_list: om_list.zinr == zimmer.zinr), first=True)

            if om_list.ind != 8:
                om_list.ind = zimmer.zistatus + 1
            pass
            curr_zinr = zimmer.zinr
            curr_stat = stat_list[zimmer.zistatus + 1 - 1]
            bline_list.selected = False
        z_list_data.clear()

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            z_list = Z_list()
            z_list_data.append(z_list)

            buffer_copy(zimmer, z_list)

            if zimmer.zistatus == 2:

                res_line = get_cache (Res_line, {"resstatus": [(eq, 8)],"zinr": [(eq, zimmer.zinr)],"abreise": [(eq, ci_date)]})

                if res_line:
                    z_list.checkout = True

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"betriebsnr": [(le, 2)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)]})

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
    stat_list[6] = translateExtended ("Out-of-Order", lvcarea, "")
    stat_list[7] = translateExtended ("Off-Market", lvcarea, "")
    stat_list[8] = translateExtended ("Do not Disturb", lvcarea, "")
    stat_list[9] = translateExtended ("Out-of-Service", lvcarea, "")

    # zimmer = get_cache (Zimmer, {"zinr": [(eq, t_zinr)]})
    zimmer = db_session.query(Zimmer).filter(
             (Zimmer.zinr == t_zinr)).with_for_update().first()
    chg_zistatus()

    return generate_output()