#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rd, 13/11/2025
# Create queasy: 161
# Rd, 27/11/2025, with_for_update added
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

t_push_list_data, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})

def bookengine_ratecodepush_btn_exit_1bl(t_push_list_data:[T_push_list], bookengid:int, user_init:string):

    prepare_cache ([Bediener, Res_history])

    str:string = ""
    i:int = 0
    queasy = bediener = res_history = None

    t_push_list = outlist = bufq = qsy = None

    outlist_data, Outlist = create_model("Outlist", {"key":int, "number1":int, "char1":string})

    Bufq = create_buffer("Bufq",Queasy)
    Qsy = create_buffer("Qsy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, i, queasy, bediener, res_history
        nonlocal bookengid, user_init
        nonlocal bufq, qsy


        nonlocal t_push_list, outlist, bufq, qsy
        nonlocal outlist_data

        return {}


    queasy = get_cache (Queasy, {"key": [(eq, 161)],"number1": [(eq, bookengid)]})
    while None != queasy :
        outlist = Outlist()
        outlist_data.append(outlist)

        outlist.key = 161
        outlist.number1 = queasy.number1
        outlist.char1 = queasy.char1

        qsy = db_session.query(Qsy).filter(
                 (Qsy._recid == queasy._recid)).with_for_update().first()

        if qsy:
            db_session.delete(qsy)
            pass

        curr_recid = queasy._recid
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 161) & (Queasy.number1 == bookengid) & (Queasy._recid > curr_recid)).first()

    for t_push_list in query(t_push_list_data):
        str = t_push_list.rcodevhp + ";" + t_push_list.rcodebe + ";" + t_push_list.rmtypevhp + ";" + t_push_list.rmtypebe + ";" + t_push_list.argtvhp
        bufq = Queasy()
        db_session.add(bufq)

        bufq.key = 161
        bufq.number1 = bookengid
        bufq.char1 = str
        pass

        for outlist in query(outlist_data, filters=(lambda outlist: outlist.key == 161 and outlist.number1 == bookengid)):

            if outlist.char1.lower()  != (str).lower() :

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Push RateCode, Booking Engine ID: " + to_string(bookengid) + ", RateCode: " + str
                    res_history.action = "Booking Engine"


                    pass
                    pass

    return generate_output()