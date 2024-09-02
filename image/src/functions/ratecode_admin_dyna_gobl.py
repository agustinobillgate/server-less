from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Zimkateg, Queasy, Ratecode, Bediener, Res_history, Counters, Guest, Guest_pr

def ratecode_admin_dyna_gobl(curr_select:str, inp_str:str, user_init:str, drbuff:[Drbuff]):
    error_code = 0
    dynarate_list_list = []
    prcode:str = ""
    bookengid:int = 0
    a:str = ""
    i:int = 0
    zimkateg = queasy = ratecode = bediener = res_history = counters = guest = guest_pr = None

    dynarate_list = drbuff = qsy = bqueasy = qsy170 = None

    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"s_recid":int, "counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str})
    drbuff_list, Drbuff = create_model_like(Dynarate_list)

    Qsy = Queasy
    Bqueasy = Queasy
    Qsy170 = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_code, dynarate_list_list, prcode, bookengid, a, i, zimkateg, queasy, ratecode, bediener, res_history, counters, guest, guest_pr
        nonlocal qsy, bqueasy, qsy170


        nonlocal dynarate_list, drbuff, qsy, bqueasy, qsy170
        nonlocal dynarate_list_list, drbuff_list
        return {"error_code": error_code, "dynaRate-list": dynarate_list_list}

    def fill_dynamic_ratecode(prcode:str, new_flag:bool):

        nonlocal error_code, dynarate_list_list, prcode, bookengid, a, i, zimkateg, queasy, ratecode, bediener, res_history, counters, guest, guest_pr
        nonlocal qsy, bqueasy, qsy170


        nonlocal dynarate_list, drbuff, qsy, bqueasy, qsy170
        nonlocal dynarate_list_list, drbuff_list

        curr_counter:int = 0

        if new_flag:

            counters = db_session.query(Counters).filter(
                    (Counters.counter_no == 50)).first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 50
                counters.counter_bez = "Counter for Dynamic Ratecode"
                counters.counter = 0


            counters.counter = counters.counter + 1

            counters = db_session.query(Counters).first()
            curr_counter = counters.counter
        else:
            curr_counter = drbuff.counter
        ratecode.CODE = prcode
        ratecode.char1[4] = "CN" + to_string(curr_counter) + ";" +\
                "RT" + to_string(drBuff.rmType) + ";" +\
                "WD" + to_string(drBuff.w_day) + ";" +\
                "FR" + to_string(drBuff.fr_room) + ";" +\
                "TR" + to_string(drBuff.to_room) + ";" +\
                "D1" + to_string(drBuff.days1) + ";" +\
                "D2" + to_string(drBuff.days2) + ";" +\
                "RC" + to_string(drBuff.rCode) + ";"


        buffer_copy(drBuff, dynarate_list,except_fields=["drBuff.s_recid","drBuff.rCode"])
        dynaRate_list.s_recid = to_int(ratecode._recid)
        dynaRate_list.rCode = a

        if bookengid != 0:
            update_bookengine_config()

    def update_bookengine_config():

        nonlocal error_code, dynarate_list_list, prcode, bookengid, a, i, zimkateg, queasy, ratecode, bediener, res_history, counters, guest, guest_pr
        nonlocal qsy, bqueasy, qsy170


        nonlocal dynarate_list, drbuff, qsy, bqueasy, qsy170
        nonlocal dynarate_list_list, drbuff_list

        cm_gastno:int = 0
        iftask:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        tokcounter:int = 0
        Qsy = Queasy
        Bqueasy = Queasy
        Qsy170 = Queasy

        qsy = db_session.query(Qsy).filter(
                (Qsy.key == 159) &  (Qsy.number1 == bookengid)).first()

        if qsy:

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == qsy.number2)).first()

            guest_pr = db_session.query(Guest_pr).filter(
                    (Guest_pr.gastnr == guest.gastnr)).first()

            if guest_pr:
                cm_gastno = guest.gastnr
            else:

                return

        guest_pr_obj_list = []
        for guest_pr, bqueasy in db_session.query(Guest_pr, Bqueasy).join(Bqueasy,(Bqueasy.key == 2) &  (Bqueasy.char1 == Guest_pr.CODE) &  (Bqueasy.logi2)).filter(
                (Guest_pr.gastnr == cm_gastno)).all():
            if guest_pr._recid in guest_pr_obj_list:
                continue
            else:
                guest_pr_obj_list.append(guest_pr._recid)

            if prcode == guest_pr.CODE:

                qsy170 = db_session.query(Qsy170).filter(
                        (Qsy170.key == 170) &  (func.lower(Qsy170.char1) == (prcode).lower()) &  (Qsy170.logi1 == False) &  (Qsy170.logi2 == False)).first()
                while None != qsy170:

                    qsy = db_session.query(Qsy).filter(
                            (Qsy._recid == qsy170._recid)).first()

                    if qsy:
                        qsy.logi2 = True

                        qsy = db_session.query(Qsy).first()


                    qsy170 = db_session.query(Qsy170).filter(
                            (Qsy170.key == 170) &  (func.lower(Qsy170.char1) == (prcode).lower()) &  (Qsy170.logi1 == False) &  (Qsy170.logi2 == False)).first()
                break


    if num_entries(inp_str, ";") > 1:
        prcode = entry(0, inp_str, ";")
        bookengid = to_int(entry(1, inp_str, ";"))


    else:
        prcode = inp_str

    if bookengid == 0:
        bookengid = 1

    drbuff = query(drbuff_list, first=True)
    a = drBuff.rcode

    if substring(a, len(a) - 1, 1) == " ":
        a = substring(a, 0, len(a) - 1)

    if drBuff.rmType.lower()  != "*":

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.kurzbez == drBuff.rmType)).first()

        if not zimkateg:
            error_code = 1

            return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (trim (Queasy.char1) == trim(a))).first()

    if not queasy:
        error_code = 2

        return generate_output()

    if drBuff.rmType.lower()  == "*":

        ratecode = db_session.query(Ratecode).filter(
                (trim (Ratecode.CODE) == trim (queasy.char1))).first()
    else:

        ratecode = db_session.query(Ratecode).filter(
                (trim (Ratecode.CODE) == trim (queasy.char1)) &  (Ratecode.zikatnr == zimkateg.zikatnr)).first()

    if not ratecode:
        error_code = 3

        return generate_output()

    if curr_select.lower()  == "add_rate":
        curr_select = "insert"

    if curr_select.lower()  == "insert":
        ratecode = Ratecode()
        db_session.add(ratecode)

        dynarate_list = Dynarate_list()
        dynarate_list_list.append(dynarate_list)

        fill_dynamic_ratecode(prcode, True)

        ratecode = db_session.query(Ratecode).first()


        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Insert Dynamic RateCode, Code: " + prcode


            res_history.action = "RateCode"

            res_history = db_session.query(Res_history).first()


    elif curr_select.lower()  == "chg_rate":

        ratecode = db_session.query(Ratecode).filter(
                (Ratecode._recid == drBuff.s_recid)).first()
        fill_dynamic_ratecode(prcode, False)

        ratecode = db_session.query(Ratecode).first()

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Dynamic RateCode, Code: " + prcode


            res_history.action = "RateCode"

            res_history = db_session.query(Res_history).first()


    return generate_output()