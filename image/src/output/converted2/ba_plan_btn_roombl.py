#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_reser, Bk_func, Bk_raum, Bediener, Res_history

def ba_plan_btn_roombl(resnr:int, reslinnr:int, chg_room:string, user_init:string, chg_table:string):

    prepare_cache ([Bk_reser, Bk_func, Bk_raum, Bediener, Res_history])

    room_desc1:string = ""
    room_desc2:string = ""
    bk_reser = bk_func = bk_raum = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_desc1, room_desc2, bk_reser, bk_func, bk_raum, bediener, res_history
        nonlocal resnr, reslinnr, chg_room, user_init, chg_table

        return {}


    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)],"veran_resnr": [(eq, reslinnr)]})

    if bk_reser:
        pass
        bk_reser.raum = chg_room
        pass

        bk_func = get_cache (Bk_func, {"veran_nr": [(eq, bk_reser.veran_nr)],"veran_seite": [(eq, bk_reser.veran_seite)]})

        if bk_func:

            bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_func.raeume[0])]})

            if bk_raum:
                room_desc1 = bk_raum.bezeich

            bk_raum = get_cache (Bk_raum, {"raum": [(eq, chg_room)]})

            if bk_raum:
                room_desc2 = bk_raum.bezeich

            if bk_func.tischform[0] == "":

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Room Changes From " + room_desc1 +\
                        " To " + room_desc2 + " Table Setup From Not Defined" +\
                        " To " + chg_table
                res_history.action = "Banquet"


                pass
                pass
            else:

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Room Changes From " + bk_func.raeume[0] +\
                        " To " + chg_room + " Table Setup From " + bk_func.tischform[0] +\
                        " To " + chg_table
                res_history.action = "Banquet"


                pass
                pass
            pass
            bk_func.raeume[0] = chg_room
            bk_func.tischform[0] = chg_table
            pass
            pass
        pass

    return generate_output()