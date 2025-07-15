from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from sqlalchemy import func
from functions.htpdate import htpdate
from functions.calculate_occupied_rooms import calculate_occupied_rooms
from functions.ratecode_rate import ratecode_rate
from models import Ratecode, Queasy, Zimkateg, Guest_pr, Waehrung

def calc_dynarates(frdate:date, todate:date, sm_gastno:int, dynacode:str, roomtype:int, argt:int, adult:int, child:int):
    rate_list_list = []
    argtno:int = 0
    markno:int = 0
    rmtype:int = 0
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

    rate_list = dynarate_list = master_dyna = buff_dynarate = bratecode = bqueasy = rclist = None

    rate_list_list, Rate_list = create_model("Rate_list", {"datum":date, "currency":str, "rmrate":decimal, "updateflag":bool, "rcode":str, "rcmap":str, "room_type":str})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str, "dynacode":str})
    master_dyna_list, Master_dyna = create_model_like(Dynarate_list)
    rclist_list, Rclist = create_model("Rclist", {"rctype":int, "rcname":str})

    Buff_dynarate = Dynarate_list
    buff_dynarate_list = dynarate_list_list

    Bratecode = create_buffer("Bratecode",Ratecode)
    Bqueasy = create_buffer("Bqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_list_list, argtno, markno, rmtype, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, master_dyna, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, master_dyna_list, rclist_list

        return {"rate-list": rate_list_list}

    def create_masterdyna():

        nonlocal rate_list_list, argtno, markno, rmtype, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, master_dyna, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, master_dyna_list, rclist_list

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == RClist.RCname)).order_by(Ratecode._recid).all():

            if re.match(r".*RT" + rmtype_str + r".*",ratecode.char1[4], re.IGNORECASE):
                master_dyna = Master_dyna()
                master_dyna_list.append(master_dyna)

                iftask = ratecode.char1[4]
                for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                    mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                    mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                    if mestoken == "CN":
                        master_dyna.counter = to_int(mesvalue)
                    elif mestoken == "RT":
                        master_dyna.rmtype = mesvalue
                    elif mestoken == "WD":
                        master_dyna.w_day = to_int(mesvalue)
                    elif mestoken == "FR":
                        master_dyna.fr_room = to_int(mesvalue)
                    elif mestoken == "TR":
                        master_dyna.to_room = to_int(mesvalue)
                    elif mestoken == "D1":
                        master_dyna.days1 = to_int(mesvalue)
                    elif mestoken == "D2":
                        master_dyna.days2 = to_int(mesvalue)
                    elif mestoken == "RC":
                        master_dyna.rcode = mesvalue
        currency = ""

        if master_Dyna:

            if roomtype != 0 and argt != 0:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == master_Dyna.rCode) & (Ratecode.zikatnr == roomtype) & (Ratecode.argtnr == argt)).first()
            else:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == master_Dyna.rCode)).first()
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


    def create_dynabuffers(datum:date):

        nonlocal rate_list_list, argtno, markno, rmtype, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, master_dyna, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, master_dyna_list, rclist_list

        use_it:bool = False
        occ_rooms:int = 0
        rate_found:bool = False
        rm_rate:decimal = to_decimal("0.0")
        restricted:bool = False
        kback_flag:bool = False
        ci_date:date = None
        curr_wday:int = 0
        ci_date = get_output(htpdate(87))
        dynarate_list_list.clear()

        for master_dyna in query(master_dyna_list):
            dynarate_list = Dynarate_list()
            dynarate_list_list.append(dynarate_list)

            buffer_copy(master_dyna, dynarate_list)
        curr_wday = get_weekday(datum) - 1

        if curr_wday == 0:
            curr_wday = 7

        for dynarate_list in query(dynarate_list_list):
            occ_rooms = get_output(calculate_occupied_rooms(datum, dynarate_list.rmtype))
            use_it = True

            if dynarate_list.days1 != 0 and (datum - ci_date) <= dynarate_list.days1:
                use_it = False

            if use_it and dynarate_list.days2 != 0 and (datum - ci_date) >= dynarate_list.days2:
                use_it = False

            if use_it and dynarate_list.w_day > 0 and dynarate_list.w_day != curr_wday:
                use_it = False

            if use_it:
                use_it = (dynarate_list.fr_room <= occ_rooms) and (dynarate_list.to_room >= occ_rooms)

            if not use_it:
                dynarate_list_list.remove(dynarate_list)

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == curr_wday and dynarate_list.days1 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == curr_wday and dynarate_list.days2 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == curr_wday), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days2 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == 0), first=True)

        if dynarate_list:

            zimkateg = db_session.query(Zimkateg).filter(
                         (Zimkateg.kurzbez == dynarate_list.rmtype)).first()
            rm_rate =  to_decimal("0")
            mapcode = dynarate_list.rcode

            queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 145) & (Queasy.char1 == dynacode) & (func.lower(Queasy.char2) == (mapcode).lower()) & (Queasy.number1 == zimkateg.zikatnr) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == datum)).first()

            if queasy:
                mapcode = queasy.char3
            rate_found, rm_rate, restricted, kback_flag = get_output(ratecode_rate(False, False, -1, 0, ("!" + mapcode), datum, datum, datum, (datum + 1), markno, argtno, zimkateg.zikatnr, adult, child, 0, 0, wahrno))

            if rate_found:
                rate_list = Rate_list()
                rate_list_list.append(rate_list)

                rate_list.datum = datum
                rate_list.currency = currency
                rate_list.rmrate =  to_decimal(rm_rate)
                rate_list.rcode = mapcode
                rate_list.rcmap = dynacode
                rate_list.room_type = dynarate_list.rmtype


    def create_statbuffers(datum:date):

        nonlocal rate_list_list, argtno, markno, rmtype, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, rmtype_str, global_occ, i_param439, wd_array, ratecode, queasy, zimkateg, guest_pr, waehrung
        nonlocal frdate, todate, sm_gastno, dynacode, roomtype, argt, adult, child
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, master_dyna, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, master_dyna_list, rclist_list

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


    i_param439 = get_output(htpint(439))
    rclist_list.clear()

    zimkateg = db_session.query(Zimkateg).filter(
             (Zimkateg.zikatnr == roomtype)).first()

    if zimkateg:
        rmtype_str = zimkateg.kurzbez

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
    rate_list_list.clear()

    for rclist in query(rclist_list):

        if RClist.RCtype == 1:
            dynacode = RClist.RCname
            create_masterdyna()
            for datum in date_range(frdate,todate) :
                create_dynabuffers(datum)
        elif RClist.RCtype == 2:

            if argt == 0 and roomtype == 0:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == RClist.RCname)).first()
            else:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == RClist.RCname) & (Ratecode.zikatnr == roomtype) & (Ratecode.argtnr == argt)).first()
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