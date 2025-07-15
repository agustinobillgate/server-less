#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Zimkateg, Bediener, Res_history

rate_list1_data, Rate_list1 = create_model("Rate_list1", {"origcode":string, "counter":int, "w_day":int, "rooms":string, "rcode":[string,31]})

def update_dynaratecode2_update_ratecodebl(rate_list1_data:[Rate_list1], avail_room:string, chg_wday:int, from_date:date, f_date:date, to_date:date, inp_str:string, contrate_value:string, rmtype:string, user_init:string):

    prepare_cache ([Queasy, Zimkateg, Bediener, Res_history])

    inp_zikatnr:int = 0
    currcode:string = ""
    bookengid:int = 0
    lastrcode:string = ""
    queasy = zimkateg = bediener = res_history = None

    rate_list1 = buf_rate_list1 = buffqueasy = None

    Buf_rate_list1 = Rate_list1
    buf_rate_list1_data = rate_list1_data

    Buffqueasy = create_buffer("Buffqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal inp_zikatnr, currcode, bookengid, lastrcode, queasy, zimkateg, bediener, res_history
        nonlocal rate_list1_data, avail_room, chg_wday, from_date, f_date, to_date, inp_str, contrate_value, rmtype, user_init
        nonlocal buf_rate_list1, buffqueasy


        nonlocal rate_list1, buf_rate_list1, buffqueasy

        return {}

    def update_ratecode():

        nonlocal inp_zikatnr, currcode, bookengid, lastrcode, queasy, zimkateg, bediener, res_history
        nonlocal rate_list1_data, avail_room, chg_wday, from_date, f_date, to_date, inp_str, contrate_value, rmtype, user_init
        nonlocal buf_rate_list1, buffqueasy


        nonlocal rate_list1, buf_rate_list1, buffqueasy

        curr_date:date = None
        curr_i:int = 0
        current_counter:int = 1
        prev_ratecode:string = ""
        avail_queasy:bool = False
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 209) & (Queasy.char1 == (currcode).lower())).order_by(Queasy.deci3.desc()).yield_per(100):
            current_counter = queasy.deci3 + 1
            break

        if avail_room.lower()  != ("ALL").lower() :

            for rate_list1 in query(rate_list1_data, filters=(lambda rate_list1: rate_list1.rooms.lower()  == (avail_room).lower()  and rate_list1.w_day == chg_wday)):
                curr_i = (from_date - f_date).days
                for curr_date in date_range(from_date,to_date) :
                    curr_i = curr_i + 1

                    if rate_list1.origcode.lower()  == (contrate_value).lower() :

                        queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, currcode)],"char2": [(eq, rate_list1.origcode)],"number1": [(eq, inp_zikatnr)],"deci1": [(eq, rate_list1.w_day)],"deci2": [(eq, rate_list1.counter)],"date1": [(eq, curr_date)]})

                        if queasy:
                            qbuff = Queasy()
                            db_session.add(qbuff)

                            buffer_copy(queasy, qbuff,except_fields=["KEY"])
                            qbuff.key = 209
                            qbuff.deci3 =  to_decimal(current_counter)


                            pass
                            db_session.delete(queasy)

                    elif rate_list1.rcode[curr_i - 1] != None:

                        if user_init != "":

                            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                            buffqueasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, currcode)],"char2": [(eq, rate_list1.origcode)],"number1": [(eq, inp_zikatnr)],"deci1": [(eq, rate_list1.w_day)],"deci2": [(eq, rate_list1.counter)],"date1": [(eq, curr_date)]})

                            if buffqueasy:
                                lastrcode = buffqueasy.char3
                            res_history = Res_history()
                            db_session.add(res_history)

                            res_history.nr = bediener.nr
                            res_history.datum = get_current_date()
                            res_history.zeit = get_current_time_in_seconds()
                            res_history.action = "UpdateDynaRateCode"
                            res_history.aenderung = "RateCode: " + currcode + ", Occupancy: " + rate_list1.rooms + " Date: " + to_string(get_year(curr_date) , "9999") + to_string(get_month(curr_date) , "99") +\
                                    to_string(get_day(curr_date) , "99") + "," + lastrcode + " ChangeTo " + contrate_value


                        queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, currcode)],"char2": [(eq, rate_list1.origcode)],"number1": [(eq, inp_zikatnr)],"deci1": [(eq, rate_list1.w_day)],"deci2": [(eq, rate_list1.counter)],"date1": [(eq, curr_date)]})

                        if not queasy:
                            prev_ratecode = rate_list1.origcode
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 145
                            queasy.char1 = currcode
                            queasy.char2 = rate_list1.origcode
                            queasy.deci2 =  to_decimal(rate_list1.counter)
                            queasy.number1 = inp_zikatnr
                            queasy.deci1 =  to_decimal(rate_list1.w_day)
                            queasy.date1 = curr_date


                        else:
                            prev_ratecode = queasy.char3
                        queasy.char3 = contrate_value
                        queasy.number2 = bediener.nr
                        queasy.number3 = get_current_time_in_seconds()
                        queasy.date2 = get_current_date()

                        buf_rate_list1 = query(buf_rate_list1_data, filters=(lambda buf_rate_list1: buf_rate_list1._recid == rate_list1._recid), first=True)
                        buf_rate_list1.rcode[curr_i - 1] = contrate_value
                        pass
                        qbuff = Queasy()
                        db_session.add(qbuff)

                        buffer_copy(queasy, qbuff,except_fields=["KEY"])
                        qbuff.key = 209
                        qbuff.char3 = prev_ratecode
                        qbuff.deci3 =  to_decimal(current_counter)


                        pass

        else:

            for rate_list1 in query(rate_list1_data, filters=(lambda rate_list1: rate_list1.w_day == chg_wday)):
                curr_i = (from_date - f_date).days
                for curr_date in date_range(from_date,to_date) :
                    curr_i = curr_i + 1

                    if rate_list1.origcode.lower()  == (contrate_value).lower() :

                        queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, currcode)],"char2": [(eq, rate_list1.origcode)],"number1": [(eq, inp_zikatnr)],"deci1": [(eq, rate_list1.w_day)],"deci2": [(eq, rate_list1.counter)],"date1": [(eq, curr_date)]})

                        if queasy:
                            qbuff = Queasy()
                            db_session.add(qbuff)

                            buffer_copy(queasy, qbuff,except_fields=["KEY"])
                            qbuff.key = 209
                            qbuff.deci3 =  to_decimal(current_counter)


                            pass
                            db_session.delete(queasy)

                    elif rate_list1.rcode[curr_i - 1] != None:

                        if user_init != "":

                            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                            buffqueasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, currcode)],"char2": [(eq, rate_list1.origcode)],"number1": [(eq, inp_zikatnr)],"deci1": [(eq, rate_list1.w_day)],"deci2": [(eq, rate_list1.counter)],"date1": [(eq, curr_date)]})

                            if buffqueasy:
                                lastrcode = buffqueasy.char3
                            res_history = Res_history()
                            db_session.add(res_history)

                            res_history.nr = bediener.nr
                            res_history.datum = get_current_date()
                            res_history.zeit = get_current_time_in_seconds()
                            res_history.action = "UpdateDynaRateCode"
                            res_history.aenderung = "RateCode: " + currcode + ", Occupancy: ALL, Date: " + to_string(get_year(curr_date) , "9999") + to_string(get_month(curr_date) , "99") +\
                                    to_string(get_day(curr_date) , "99") + "," + lastrcode + " ChangeTo " + contrate_value

                        queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, currcode)],"char2": [(eq, rate_list1.origcode)],"number1": [(eq, inp_zikatnr)],"deci1": [(eq, rate_list1.w_day)],"deci2": [(eq, rate_list1.counter)],"date1": [(eq, curr_date)]})

                        if not queasy:
                            prev_ratecode = rate_list1.origcode
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 145
                            queasy.char1 = currcode
                            queasy.char2 = rate_list1.origcode
                            queasy.number1 = inp_zikatnr
                            queasy.deci1 =  to_decimal(rate_list1.w_day)
                            queasy.deci2 =  to_decimal(rate_list1.counter)
                            queasy.date1 = curr_date


                        else:
                            prev_ratecode = queasy.char3
                        queasy.char3 = contrate_value
                        queasy.number2 = bediener.nr
                        queasy.number3 = get_current_time_in_seconds()
                        queasy.date2 = get_current_date()

                        buf_rate_list1 = query(buf_rate_list1_data, filters=(lambda buf_rate_list1: buf_rate_list1._recid == rate_list1._recid), first=True)
                        buf_rate_list1.rcode[curr_i - 1] = contrate_value
                        pass
                        qbuff = Queasy()
                        db_session.add(qbuff)

                        buffer_copy(queasy, qbuff,except_fields=["KEY"])
                        qbuff.key = 209
                        qbuff.char3 = prev_ratecode
                        qbuff.deci3 =  to_decimal(current_counter)


                        pass

    def update_bookengine_config():

        nonlocal inp_zikatnr, currcode, bookengid, lastrcode, queasy, zimkateg, bediener, res_history
        nonlocal rate_list1_data, avail_room, chg_wday, from_date, f_date, to_date, inp_str, contrate_value, rmtype, user_init
        nonlocal buf_rate_list1, buffqueasy


        nonlocal rate_list1, buf_rate_list1, buffqueasy

        cm_gastno:int = 0
        qsy = None
        bqueasy = None
        datum:date = None
        iftask:string = ""
        mestoken:string = ""
        mesvalue:string = ""
        tokcounter:int = 0
        Qsy =  create_buffer("Qsy",Queasy)
        Bqueasy =  create_buffer("Bqueasy",Queasy)
        for datum in date_range(from_date,to_date) :

            qsy = get_cache (Queasy, {"key": [(eq, 170)],"date1": [(eq, datum)],"char1": [(eq, currcode)],"logi1": [(eq, False)],"logi2": [(eq, False)]})
            while None != qsy:

                bqueasy = get_cache (Queasy, {"_recid": [(eq, qsy._recid)]})

                if bqueasy:
                    bqueasy.logi2 = True


                    pass
                    pass

                curr_recid = qsy._recid
                qsy = db_session.query(Qsy).filter(
                         (Qsy.key == 170) & (Qsy.date1 == datum) & (Qsy.char1 == (currcode).lower()) & (Qsy.logi1 == False) & (Qsy.logi2 == False) & (Qsy._recid > curr_recid)).first()


    if num_entries(inp_str, ";") > 1:
        currcode = entry(0, inp_str, ";")
        bookengid = to_int(entry(1, inp_str, ";"))


    else:
        currcode = inp_str

    if bookengid == 0:
        bookengid = 1

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})

    if zimkateg:
        inp_zikatnr = zimkateg.zikatnr

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    update_ratecode()

    if bookengid != 0:
        update_bookengine_config()

    return generate_output()