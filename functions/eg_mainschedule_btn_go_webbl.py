#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_action, Eg_maintain, Counters, Eg_mdetail

maintain_data, Maintain = create_model_like(Eg_maintain)
action_data, Action = create_model_like(Eg_action, {"selected":bool})

def eg_mainschedule_btn_go_webbl(maintain_data:[Maintain], action_data:[Action], user_init:string):

    prepare_cache ([Eg_maintain, Counters, Eg_mdetail])

    fl_daily:bool = False
    fl_weekly:bool = False
    fl_monthly:bool = False
    fl_quarter:bool = False
    fl_half_yearly:bool = False
    fl_yearly:bool = False
    a:date = None
    b:date = None
    tdate:date = None
    nr:int = 0
    eg_action = eg_maintain = counters = eg_mdetail = None

    action = maintain = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_daily, fl_weekly, fl_monthly, fl_quarter, fl_half_yearly, fl_yearly, a, b, tdate, nr, eg_action, eg_maintain, counters, eg_mdetail
        nonlocal user_init


        nonlocal action, maintain

        return {"maintain": maintain_data}


    maintain = query(maintain_data, first=True)

    if maintain.typework == 1:
        fl_daily = True

    elif maintain.typework == 2:
        fl_weekly = True

    elif maintain.typework == 3:
        fl_monthly = True

    elif maintain.typework == 4:
        fl_quarter = True

    elif maintain.typework == 5:
        fl_half_yearly = True

    elif maintain.typework == 6:
        fl_yearly = True

    if fl_daily:
        a = maintain.estworkdate
        tdate = a + timedelta(days=360)
        while a <= tdate:

            counters = get_cache (Counters, {"counter_no": [(eq, 38)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 38
                counters.counter_bez = "Counter for maintenance in engineering"
                counters.counter = 0


            counters.counter = counters.counter + 1
            pass
            nr = counters.counter
            eg_maintain = Eg_maintain()
            db_session.add(eg_maintain)

            buffer_copy(maintain, eg_maintain,except_fields=["maintain.maintainnr","maintain.type","maintain.created_date","maintain.estworkdate"])
            eg_maintain.maintainnr = nr
            eg_maintain.type = 1
            eg_maintain.created_date = get_current_date()
            eg_maintain.estworkdate = a


            a = a + timedelta(days=1)

            for action in query(action_data, filters=(lambda action: action.selected)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = nr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    elif fl_weekly:
        a = maintain.estworkdate
        tdate = a + timedelta(days=365)
        while a <= tdate:

            counters = get_cache (Counters, {"counter_no": [(eq, 38)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 38
                counters.counter_bez = "Counter for maintenance in engineering"
                counters.counter = 0


            counters.counter = counters.counter + 1
            pass
            nr = counters.counter
            eg_maintain = Eg_maintain()
            db_session.add(eg_maintain)

            buffer_copy(maintain, eg_maintain,except_fields=["maintain.maintainnr","maintain.type","maintain.created_date","maintain.estworkdate"])
            eg_maintain.maintainnr = nr
            eg_maintain.type = 1
            eg_maintain.created_date = get_current_date()
            eg_maintain.estworkdate = a


            a = a + timedelta(days=7)

            for action in query(action_data, filters=(lambda action: action.selected)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = nr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    elif fl_monthly:
        a = maintain.estworkdate
        tdate = a + timedelta(days=365)
        while a <= tdate:

            counters = get_cache (Counters, {"counter_no": [(eq, 38)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 38
                counters.counter_bez = "Counter for maintenance in engineering"
                counters.counter = 0


            counters.counter = counters.counter + 1
            pass
            nr = counters.counter
            eg_maintain = Eg_maintain()
            db_session.add(eg_maintain)

            buffer_copy(maintain, eg_maintain,except_fields=["maintain.maintainnr","maintain.type","maintain.created_date","maintain.estworkdate"])
            eg_maintain.maintainnr = nr
            eg_maintain.type = 1
            eg_maintain.created_date = get_current_date()
            eg_maintain.estworkdate = a


            a = a + timedelta(days=30)

            for action in query(action_data, filters=(lambda action: action.selected)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = nr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    elif fl_quarter:
        a = maintain.estworkdate
        tdate = a + timedelta(days=365)
        while a <= tdate:

            counters = get_cache (Counters, {"counter_no": [(eq, 38)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 38
                counters.counter_bez = "Counter for maintenance in engineering"
                counters.counter = 0


            counters.counter = counters.counter + 1
            pass
            nr = counters.counter
            eg_maintain = Eg_maintain()
            db_session.add(eg_maintain)

            buffer_copy(maintain, eg_maintain,except_fields=["maintain.maintainnr","maintain.type","maintain.created_date","maintain.estworkdate"])
            eg_maintain.maintainnr = nr
            eg_maintain.type = 1
            eg_maintain.created_date = get_current_date()
            eg_maintain.estworkdate = a


            a = a + timedelta(days=90)

            for action in query(action_data, filters=(lambda action: action.selected)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = nr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    elif fl_half_yearly:
        a = maintain.estworkdate
        tdate = a + timedelta(days=365)
        while a <= tdate:

            counters = get_cache (Counters, {"counter_no": [(eq, 38)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 38
                counters.counter_bez = "Counter for maintenance in engineering"
                counters.counter = 0


            counters.counter = counters.counter + 1
            pass
            nr = counters.counter
            eg_maintain = Eg_maintain()
            db_session.add(eg_maintain)

            buffer_copy(maintain, eg_maintain,except_fields=["maintain.maintainnr","maintain.type","maintain.created_date","maintain.estworkdate"])
            eg_maintain.maintainnr = nr
            eg_maintain.type = 1
            eg_maintain.created_date = get_current_date()
            eg_maintain.estworkdate = a


            a = a + timedelta(days=180)

            for action in query(action_data, filters=(lambda action: action.selected)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = nr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    elif fl_yearly:
        a = maintain.estworkdate
        tdate = a + timedelta(days=365)
        while a <= tdate:

            counters = get_cache (Counters, {"counter_no": [(eq, 38)]})

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 38
                counters.counter_bez = "Counter for maintenance in engineering"
                counters.counter = 0


            counters.counter = counters.counter + 1
            pass
            nr = counters.counter
            eg_maintain = Eg_maintain()
            db_session.add(eg_maintain)

            buffer_copy(maintain, eg_maintain,except_fields=["maintain.maintainnr","maintain.type","maintain.created_date","maintain.estworkdate"])
            eg_maintain.maintainnr = nr
            eg_maintain.type = 1
            eg_maintain.created_date = get_current_date()
            eg_maintain.estworkdate = a


            a = a + timedelta(days=365)

            for action in query(action_data, filters=(lambda action: action.selected)):
                eg_mdetail = Eg_mdetail()
                db_session.add(eg_mdetail)

                eg_mdetail.key = 1
                eg_mdetail.maintainnr = nr
                eg_mdetail.nr = action.actionnr
                eg_mdetail.create_date = get_current_date()
                eg_mdetail.create_time = get_current_time_in_seconds()
                eg_mdetail.create_by = user_init

    return generate_output()