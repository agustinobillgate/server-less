#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bediener, Reservation, Res_history

res_list_data, Res_list = create_model_like(Res_line, {"kurzbez":string, "groupname":string, "join_flag":bool, "mbill_flag":bool, "prev_join":bool, "prev_mbill":bool})

def connect_group_join_itbl(resno:int, selected_resnr:int, user_init:string, res_list_data:[Res_list]):

    prepare_cache ([Res_line, Bediener, Reservation, Res_history])

    res_line = bediener = reservation = res_history = None

    res_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_line, bediener, reservation, res_history
        nonlocal resno, selected_resnr, user_init


        nonlocal res_list

        return {}

    def join_it():

        nonlocal res_line, bediener, reservation, res_history
        nonlocal resno, selected_resnr, user_init


        nonlocal res_list

        rmno:string = ""
        rline = None
        mbuff = None
        Rline =  create_buffer("Rline",Res_line)
        Mbuff =  create_buffer("Mbuff",Reservation)

        res_list = query(res_list_data, first=True)

        for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == selected_resnr) & (Res_line.l_zuordnung[inc_value(4)] == 0)).order_by(Res_line._recid).all():

            # rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
            rline = db_session.query(Res_line).filter(Res_line._recid == res_line._recid).with_for_update().first()
            rline.l_zuordnung[4] = selected_resnr


            pass

        mbuff = get_cache (Reservation, {"resnr": [(eq, selected_resnr)]})

        # reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})
        reservation = db_session.query(Reservation).filter(Reservation.resnr == resno).with_for_update().first()
        reservation.grpflag = mbuff.grpflag
        reservation.groupname = mbuff.groupname
        reservation.verstat = mbuff.verstat


        pass

        for res_list in query(res_list_data, filters=(lambda res_list:(res_list.prev_join != res_list.join_flag) or (res_list.prev_mbill != res_list.mbill_flag))):

            # res_line = get_cache (Res_line, {"resnr": [(eq, res_list.resnr)],"reslinnr": [(eq, res_list.reslinnr)]})
            res_line = db_session.query(Res_line).filter((Res_line.resnr == res_list.resnr) & (Res_line.kontakt_nr == res_list.reslinnr)).with_for_update().first()

            if res_list.join_flag:
                res_line.l_zuordnung[4] = selected_resnr
                res_line.l_zuordnung[1] = 0


            else:
                res_line.l_zuordnung[1] = 2
                res_line.l_zuordnung[4] = 0


            pass

            if (res_list.prev_join != res_list.join_flag):
                res_history = Res_history()
                db_session.add(res_history)


                if res_list.join_flag:
                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Reservation"
                    res_history.aenderung = "resno: " + to_string(resno) +\
                        " rmno: " + res_line.zinr + " " + res_line.name +\
                        " - Connect to Group resno " + to_string(selected_resnr)


                else:
                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.action = "Reservation"
                    res_history.aenderung = "resno: " + to_string(resno) +\
                        " rmno: " + res_line.zinr + " " + res_line.name +\
                        " - Disconnect from Group resno " + to_string(selected_resnr)


                pass
                pass

            for res_line in db_session.query(Res_line).filter(
                         (Res_line.resnr == res_list.resnr) & (Res_line.kontakt_nr == res_list.reslinnr) & (Res_line.l_zuordnung[inc_value(2)] == 1)).order_by(Res_line._recid).all():

                # rline = get_cache (Res_line, {"_recid": [(eq, res_line._recid)]})
                rline = db_session.query(Res_line).filter(Res_line._recid == res_line._recid).with_for_update().first()

                if res_list.join_flag:
                    rline.l_zuordnung[4] = selected_resnr


                else:
                    rline.l_zuordnung[4] = 0
                pass


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    join_it()

    return generate_output()