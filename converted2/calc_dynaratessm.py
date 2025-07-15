from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from sqlalchemy import func
from functions.htpdate import htpdate
from functions.calculate_occupied_roomsbl import calculate_occupied_roomsbl
from functions.ratecode_rate import ratecode_rate
from functions.calculate_occupied_rooms import calculate_occupied_rooms
from models import Ratecode, Queasy, Zimkateg, Guest_pr, Waehrung

def calc_dynaratessm(frdate:date, todate:date, sm_gastno:int, dynacode:str, roomtype:int, argt:int, adult:int, child:int):
    rate_list_list = []
    rmtype:int = 2
    argtno:int = 0
    markno:int = 0
    wahrno:int = 0
    tokcounter:int = 0
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    currency:str = ""
    mapcode:str = ""
    datum:date = None
    rmtype_str:str = ""
    global_occ:bool = False
    i_param439:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    ratecode = queasy = zimkateg = guest_pr = waehrung = None

    rate_list = dynarate_list = buff_dynarate = bratecode = bqueasy = rclist = None

    rate_list_list, Rate_list = create_model("Rate_list", {"datum":date, "currency":str, "rmrate":decimal, "updateflag":bool, "occ_rooms":int, "rcode":str, "rcmap":str, "room_type":str, "argtno":int})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str})
    rclist_list, Rclist = create_model("Rclist", {"rctype":int, "rcname":str})

    Buff_dynarate = Dynarate_list
    buff_dynarate_list = dynarate_list_list

    Bratecode = create_buffer("Bratecode",Ratecode)
    Bqueasy = create_buffer("Bqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_list_list, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, rclist_list

        return {"rate-list": rate_list_list}

    def create_masterdyna():

        nonlocal rate_list_list, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, rclist_list

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == RClist.RCname)).order_by(Ratecode._recid).all():
            dynarate_list = Dynarate_list()
            dynarate_list_list.append(dynarate_list)

            iftask = ratecode.char1[4]
            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                if mestoken == "CN":
                    dynarate_list.counter = to_int(mesvalue)
                elif mestoken == "RT":
                    dynarate_list.rmtype = mesvalue
                elif mestoken == "WD":
                    dynarate_list.w_day = to_int(mesvalue)
                elif mestoken == "FR":
                    dynarate_list.fr_room = to_int(mesvalue)
                elif mestoken == "TR":
                    dynarate_list.to_room = to_int(mesvalue)
                elif mestoken == "D1":
                    dynarate_list.days1 = to_int(mesvalue)
                elif mestoken == "D2":
                    dynarate_list.days2 = to_int(mesvalue)
                elif mestoken == "RC":
                    dynarate_list.rcode = mesvalue

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*").lower()), first=True)
        global_occ = None != dynarate_list and i_param439 == 1

        if global_occ:

            for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != ("*").lower())):
                dynarate_list_list.remove(dynarate_list)

        else:

            for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != (rmtype_str).lower())):
                dynarate_list_list.remove(dynarate_list)

        currency = ""

        dynarate_list = query(dynarate_list_list, first=True)

        if dynarate_list:

            if roomtype != 0 and argt != 0:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == dynarate_list.rCode) & (Ratecode.zikatnr == roomtype) & (Ratecode.argtnr == argt)).first()
            else:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == dynarate_list.rCode)).first()

            if ratecode:
                markno = ratecode.marknr
                argtno = ratecode.argtnr

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                if queasy:
                    currency = queasy.char3

                if currency != "":

                    waehrung = db_session.query(Waehrung).filter(
                             (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

                    if waehrung:
                        wahrno = waehrung.waehrungsnr


    def create_dynabuffers():

        nonlocal rate_list_list, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, rclist_list

        use_it:bool = False
        occ_rooms:int = 0
        rate_found:bool = False
        rm_rate:decimal = to_decimal("0.0")
        restricted:bool = False
        kback_flag:bool = False
        ci_date:date = None
        curr_wday:int = 0
        datum1:date = None
        datum2:date = None
        ci_date = get_output(htpdate(87))

        for rate_list in query(rate_list_list):
            rate_list.occ_rooms = get_output(calculate_occupied_roomsbl(rate_list.datum, rmtype_str, global_occ))
            curr_wday = wd_array[get_weekday(rate_list.datum) - 1]

            for dynarate_list in query(dynarate_list_list, sort_by=[("w_day",True)]):
                use_it = True

                if dynarate_list.days1 != 0 and (rate_list.datum - ci_date) <= dynarate_list.days1:
                    use_it = False

                if use_it and dynarate_list.days2 != 0 and (rate_list.datum - ci_date) >= dynarate_list.days2:
                    use_it = False

                if use_it:

                    if dynarate_list.w_day == curr_wday and (dynarate_list.fr_room <= rate_list.occ_rooms) and (dynarate_list.to_room >= rate_list.occ_rooms):
                        rate_list.rcode = dynarate_list.rcode
                        rate_list.rcmap = dynacode

                        if global_occ:

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rcode) & (Queasy.number1 == 0) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == rate_list.datum)).first()
                        else:

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rcode) & (Queasy.number1 == zimkateg.zikatnr) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == rate_list.datum)).first()

                        if queasy:
                            rate_list.rcode = queasy.char3
                        break

                    elif dynarate_list.w_day == 0 and (dynarate_list.fr_room <= rate_list.occ_rooms and dynarate_list.to_room >= rate_list.occ_rooms):
                        rate_list.rcode = dynarate_list.rcode
                        rate_list.rcmap = dynacode

                        if global_occ:

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rcode) & (Queasy.number1 == 0) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == rate_list.datum)).first()
                        else:

                            queasy = db_session.query(Queasy).filter(
                                     (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rcode) & (Queasy.number1 == zimkateg.zikatnr) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == rate_list.datum)).first()

                        if queasy:
                            rate_list.rcode = queasy.char3
                        break

        for rate_list in query(rate_list_list):
            rate_found, rm_rate, restricted, kback_flag = get_output(ratecode_rate(False, False, -1, 0, ("!" + rate_list.rcode), rate_list.datum, rate_list.datum, rate_list.datum, (rate_list.datum + 1), markno, argtno, zimkateg.zikatnr, adult, child, 0, 0, wahrno))

            if rate_found:
                rate_list.currency = currency
                rate_list.rmrate =  to_decimal(rm_rate)


            else:
                rate_list_list.remove(rate_list)

        for rate_list in query(rate_list_list, filters=(lambda rate_list: rate_list.rmRate == 0)):
            rate_list_list.remove(rate_list)


    def create_statbuffers(datum:date):

        nonlocal rate_list_list, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, rclist_list

        occ_rooms:int = 0
        rate_found:bool = False
        rm_rate:decimal = to_decimal("0.0")
        restricted:bool = False
        kback_flag:bool = False

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == rmtype)).first()
        occ_rooms = get_output(calculate_occupied_rooms(datum, zimkateg.kurzbez))
        rm_rate =  to_decimal("0")
        rate_found, rm_rate, restricted, kback_flag = get_output(ratecode_rate(False, False, -1, 0, ("!" + RClist.RCname), datum, datum, datum, (datum + 1), markno, argtno, zimkateg.zikatnr, adult, child, 0, 0, wahrno))

        if rate_found:
            rate_list = Rate_list()
            rate_list_list.append(rate_list)

            rate_list.datum = datum
            rate_list.currency = currency
            rate_list.rmrate =  to_decimal(rm_rate)
            rate_list.rcode = RClist.RCname
            rate_list.rcmap = RClist.RCname
            rate_list.room_type = zimkateg.kurzbez

        for rate_list in query(rate_list_list, filters=(lambda rate_list: rate_list.rmRate == 0)):
            rate_list_list.remove(rate_list)

    i_param439 = get_output(htpint(439))

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.zikatnr == roomtype)).first()

    if zimkateg:
        rmtype_str = zimkateg.kurzbez
    rate_list_list.clear()
    for datum in date_range(frdate,todate) :
        rate_list = Rate_list()
        rate_list_list.append(rate_list)

        rate_list.datum = datum
        rate_list.room_type = rmtype_str


    rclist_list.clear()

    for guest_pr in db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == sm_gastno)).order_by(Guest_pr._recid).all():

        bratecode = db_session.query(Bratecode).filter(
                 (Bratecode.code == guest_pr.code)).first()

        if bratecode:
            rclist = Rclist()
            rclist_list.append(rclist)


            bqueasy = db_session.query(Bqueasy).filter(
                     (Bqueasy.key == 2) & (Bqueasy.char1 == bratecode.code)).first()

            if bqueasy and bqueasy.logi2:
                rclist.rctype = 1
                rclist.rcname = bratecode.code

            if bqueasy and not bqueasy.logi2:
                rclist.rctype = 2
                rclist.rcname = bratecode.code


            pass

    if dynacode != "":

        for rclist in query(rclist_list, filters=(lambda rclist: rclist.RClist.RCname.lower()  != (dynacode).lower())):
            rclist_list.remove(rclist)

    for rclist in query(rclist_list):

        if RClist.RCtype == 1:
            dynacode = RClist.RCname
            create_masterdyna()
            create_dynabuffers()
        elif RClist.RCtype == 2:

            if argt == 0 and roomtype == 0:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == RClist.RCname)).first()
            else:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == RClist.RCname) & (Ratecode.zikatnr == roomtype) & (Ratecode.argtnr == argt)).first()

            if ratecode:
                markno = ratecode.marknr
                argtno = ratecode.argtnr
                rmtype = ratecode.zikatnr

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                if queasy:
                    currency = queasy.char3

                if currency != "":

                    waehrung = db_session.query(Waehrung).filter(
                             (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

                    if waehrung:
                        wahrno = waehrung.waehrungsnr
                for datum in date_range(frdate,todate) :
                    create_statbuffers(datum)

    return generate_output()