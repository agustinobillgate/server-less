#using conversion tools version: 1.0.0.119

# ============================================
# Rulita, 19-11-2025
# - Fixing field rmType -> rmtype
# - Fixing inden else new_flag

# Rulita, 21-11-2025
# - Fixing add data ratecode array char1[4] 
# =============================================
# Rd, 27/11/2025, with_for_update added
# =============================================
from functions.additional_functions import *
from decimal import Decimal
from models import Zimkateg, Queasy, Ratecode, Bediener, Res_history, Counters, Guest, Guest_pr

# Rulita, 21-11-2025
# - Fixing add data ratecode array char1[4]
from sqlalchemy.orm import flag_modified

dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"s_recid":int, "counter":int, "w_day":int, "rmType":string, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rCode":string})
drbuff_data, Drbuff = create_model_like(Dynarate_list)

def ratecode_admin_dyna_gobl(curr_select:string, inp_str:string, user_init:string, drbuff_data:[Drbuff]):

    prepare_cache ([Zimkateg, Ratecode, Bediener, Res_history, Counters, Guest, Guest_pr])

    dynarate_list_data = []
    error_code = 0
    dynarate_list_data = []
    prcode:string = ""
    bookengid:int = 0
    a:string = ""
    i:int = 0
    tmp_rchar1_4:string = ""

    zimkateg = queasy = ratecode = bediener = res_history = counters = guest = guest_pr = None

    dynarate_list = drbuff = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dynarate_list_data, error_code, dynarate_list_data, prcode, bookengid, a, i, zimkateg, queasy, ratecode, bediener, res_history, counters, guest, guest_pr, tmp_rchar1_4
        nonlocal curr_select, inp_str, user_init


        nonlocal dynarate_list, drbuff
        nonlocal dynarate_list_data

        return {"error_code": error_code, "dynaRate-list": dynarate_list_data}

    def fill_dynamic_ratecode(prcode:string, new_flag:bool):

        nonlocal dynarate_list_data, error_code, dynarate_list_data, bookengid, a, i, zimkateg, queasy, bediener, res_history, counters, guest, guest_pr, tmp_rchar1_4
        nonlocal curr_select, inp_str, user_init


        nonlocal dynarate_list, drbuff
        nonlocal dynarate_list_data

        curr_counter:int = 0

        # Rulita, 19-11-2025
        # Fixing inden else new_flag
        if new_flag:

            # counters = get_cache (Counters, {"counter_no": [(eq, 50)]})
            # Rd, 24/11/2025 , Update last counter dengan next_counter_for_update
            counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 50)).with_for_update().first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 50
                counters.counter_bez = "Counter for Dynamic Ratecode"
                counters.counter = 0

            counters.counter = counters.counter + 1
            pass
            curr_counter = counters.counter
        else:
            curr_counter = drbuff.counter

        ratecode.code = prcode
        # Rulita, 21-11-2025
        # - Fixing add data ratecode array char1[4]
        ratecode.char1[4] = "CN" + to_string(curr_counter) + ";" +\
                "RT" + to_string(drbuff.rmType) + ";" +\
                "WD" + to_string(drbuff.w_day) + ";" +\
                "FR" + to_string(drbuff.fr_room) + ";" +\
                "TR" + to_string(drbuff.to_room) + ";" +\
                "D1" + to_string(drbuff.days1) + ";" +\
                "D2" + to_string(drbuff.days2) + ";" +\
                "RC" + to_string(drbuff.rCode) + ";"
        
        flag_modified(ratecode, "char1")
        # End Rulita

        buffer_copy(drbuff, dynarate_list,except_fields=["drbuff.s_recid","drbuff.rCode"])
        dynarate_list.s_recid = to_int(ratecode._recid)
        dynarate_list.rcode = a

        if bookengid != 0:
            update_bookengine_config()


    def update_bookengine_config():

        nonlocal dynarate_list_data, error_code, dynarate_list_data, prcode, bookengid, a, i, zimkateg, queasy, ratecode, bediener, res_history, counters, guest, guest_pr, tmp_rchar1_4
        nonlocal curr_select, inp_str, user_init


        nonlocal dynarate_list, drbuff
        nonlocal dynarate_list_data

        cm_gastno:int = 0
        qsy = None
        bqueasy = None
        qsy170 = None
        iftask:string = ""
        mestoken:string = ""
        mesvalue:string = ""
        tokcounter:int = 0
        Qsy =  create_buffer("Qsy",Queasy)
        Bqueasy =  create_buffer("Bqueasy",Queasy)
        Qsy170 =  create_buffer("Qsy170",Queasy)

        qsy = db_session.query(Qsy).filter(
                 (Qsy.key == 159) & (Qsy.number1 == bookengid)).first()

        if qsy:
            # guest = get_cache (Guest, {"gastnr": [(eq, qsy.number2)]})
            guest = db_session.query(Guest).filter(
                Guest.gastnr == qsy.number2).first()
            if guest:
                guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

                if guest_pr:
                    cm_gastno = guest.gastnr
                else:
                    return
            else:
                    return

        guest_pr_obj_list = {}
        for guest_pr, bqueasy in db_session.query(Guest_pr, Bqueasy).join(Bqueasy,(Bqueasy.key == 2) & (Bqueasy.char1 == Guest_pr.code) & (Bqueasy.logi2)).filter(
                 (Guest_pr.gastnr == cm_gastno)).order_by(Bqueasy.number3.desc(), Bqueasy.deci3.desc()).yield_per(100):
            if guest_pr_obj_list.get(guest_pr._recid):
                continue
            else:
                guest_pr_obj_list[guest_pr._recid] = True

            if prcode == guest_pr.code:

                qsy170 = db_session.query(Qsy170).filter(
                         (Qsy170.key == 170) & (Qsy170.char1 == (prcode).lower()) & (Qsy170.logi1 == False) & (Qsy170.logi2 == False)).first()
                while None != qsy170:

                    qsy = db_session.query(Qsy).filter(
                             (Qsy._recid == qsy170._recid)).with_for_update().first()

                    if qsy:
                        qsy.logi2 = True


                        pass
                        pass

                    curr_recid = qsy170._recid
                    qsy170 = db_session.query(Qsy170).filter(
                             (Qsy170.key == 170) & (Qsy170.char1 == (prcode).lower()) & (Qsy170.logi1 == False) & (Qsy170.logi2 == False) & (Qsy170._recid > curr_recid)).first()
                break

    if num_entries(inp_str, ";") > 1:
        prcode = entry(0, inp_str, ";")
        bookengid = to_int(entry(1, inp_str, ";"))
    else:
        prcode = inp_str

    if bookengid == 0:
        bookengid = 1

    drbuff = query(drbuff_data, first=True)
    a = drbuff.rCode

    if substring(a, length(a) - 1, 1) == " ":
        a = substring(a, 0, length(a) - 1)

    # Rulita, 19-11-2025
    # Fixing field rmType -> rmtype
    if drbuff.rmType != "*" :

        # zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, drbuff.rmType)]})
        zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.kurzbez == drbuff.rmType)).first()

        if not zimkateg:
            error_code = 1

            return generate_output()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 2) & (trim (Queasy.char1) == trim(a))).first()

    if not queasy:
        error_code = 2

        return generate_output()

    # Rulita, 19-11-2025
    # Fixing field rmType -> rmtype
    if drbuff.rmType.lower() == ("*").lower() :

        ratecode = db_session.query(Ratecode).filter(
                 (trim (Ratecode.code) == trim (queasy.char1))).first()
    else:

        ratecode = db_session.query(Ratecode).filter(
                 (trim (Ratecode.code) == trim (queasy.char1)) & (Ratecode.zikatnr == zimkateg.zikatnr)).first()

    if not ratecode:
        error_code = 3

        return generate_output()

    if curr_select.lower()  == ("add-rate").lower() :
        curr_select = "insert"

    if curr_select.lower()  == ("insert").lower() :
        ratecode = Ratecode()
        db_session.add(ratecode)

        dynarate_list = Dynarate_list()
        dynarate_list_data.append(dynarate_list)

        fill_dynamic_ratecode(prcode, True)
        pass
        pass

        # bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        bediener = db_session.query(Bediener).filter(
                 (Bediener.userinit == user_init)).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Insert Dynamic RateCode, Code: " + prcode


            res_history.action = "RateCode"
            pass
            pass

    elif curr_select.lower()  == ("chg-rate").lower() :

        ratecode = get_cache (Ratecode, {"_recid": [(eq, drbuff.s_recid)]})
        fill_dynamic_ratecode(prcode, False)
        pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Dynamic RateCode, Code: " + prcode


            res_history.action = "RateCode"
            pass
            pass

    return generate_output()