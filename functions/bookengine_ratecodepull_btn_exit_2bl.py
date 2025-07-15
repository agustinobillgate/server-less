#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

t_push_list_data, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})

def bookengine_ratecodepull_btn_exit_2bl(t_push_list_data:[T_push_list], bookengid:int, user_init:string, case_type:int):

    prepare_cache ([Bediener, Res_history])

    str:string = ""
    old_str:string = ""
    queasy = bediener = res_history = None

    t_push_list = outlist = bufq = qsy = None

    outlist_data, Outlist = create_model("Outlist", {"key":int, "number1":int, "char1":string})

    Bufq = create_buffer("Bufq",Queasy)
    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, old_str, queasy, bediener, res_history
        nonlocal bookengid, user_init, case_type
        nonlocal bufq, qsy


        nonlocal t_push_list, outlist, bufq, qsy
        nonlocal outlist_data

        return {}


    if case_type == 1:

        for t_push_list in query(t_push_list_data):
            str = ""
            str = t_push_list.rcodevhp + ";" +\
                    t_push_list.rcodebe + ";" +\
                    t_push_list.rmtypevhp + ";" +\
                    t_push_list.rmtypebe + ";" +\
                    t_push_list.argtvhp


            bufq = Queasy()
            db_session.add(bufq)

            bufq.key = 163
            bufq.number1 = bookengid
            bufq.char1 = str


            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Add Pull Mapping RateCode, Booking Engine ID: " + to_string(bookengid) + ", RateCode: " + str
                res_history.action = "Booking Engine"


                pass
                pass
    elif case_type == 2:

        for t_push_list in query(t_push_list_data):
            str = ""
            str = t_push_list.rcodevhp + ";" +\
                    t_push_list.rcodebe + ";" +\
                    t_push_list.rmtypevhp + ";" +\
                    t_push_list.rmtypebe + ";" +\
                    t_push_list.argtvhp

            qsy = db_session.query(Qsy).filter(
                     (Qsy._recid == t_push_list.flag)).first()

            if qsy:
                old_str = qsy.char1
                qsy.char1 = str


                pass
                pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Modify Pull Mapping RateCode, Booking Engine ID: " + to_string(bookengid) + ", From: " + old_str + " To " + str
                res_history.action = "Booking Engine"


                pass
                pass
    elif case_type == 3:

        for t_push_list in query(t_push_list_data):

            qsy = db_session.query(Qsy).filter(
                     (Qsy._recid == t_push_list.flag)).first()

            if qsy:
                db_session.delete(qsy)
                pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Deleted Pull Mapping RateCode, Booking Engine ID: " + to_string(bookengid) + ", RateCode: " + str
            res_history.action = "Booking Engine"


            pass
            pass

    return generate_output()