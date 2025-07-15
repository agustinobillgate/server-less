from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpdate import htpdate
from functions.ratecode_rate import ratecode_rate
from models import Ratecode, Queasy, Guest_pr, Waehrung, Zimkateg, Res_line

def calc_dynaratesrtd(frdate:date, todate:date, sm_gastno:int):
    rate_list_list = []
    dynacode:str = ""
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
    ratecode = queasy = guest_pr = waehrung = zimkateg = res_line = None

    rate_list = dynarate_list = buff_dynarate = bratecode = bqueasy = rclist = None

    rate_list_list, Rate_list = create_model("Rate_list", {"datum":date, "currency":str, "rmrate":decimal, "updateflag":bool, "occ_rooms":int, "rcode":str, "rcmap":str, "room_type":str, "argtno":int, "adult":int, "child":int})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str, "adult":int, "child":int})
    rclist_list, Rclist = create_model("Rclist", {"rctype":int, "rcname":str})

    Buff_dynarate = Dynarate_list
    buff_dynarate_list = dynarate_list_list

    Bratecode = create_buffer("Bratecode",Ratecode)
    Bqueasy = create_buffer("Bqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rate_list_list, dynacode, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, ratecode, queasy, guest_pr, waehrung, zimkateg, res_line
        nonlocal frdate, todate, sm_gastno
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, rclist_list

        return {"rate-list": rate_list_list}

    def create_masterdyna():

        nonlocal rate_list_list, dynacode, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, ratecode, queasy, guest_pr, waehrung, zimkateg, res_line
        nonlocal frdate, todate, sm_gastno
        nonlocal buff_dynarate, bratecode, bqueasy


        nonlocal rate_list, dynarate_list, buff_dynarate, bratecode, bqueasy, rclist
        nonlocal rate_list_list, dynarate_list_list, rclist_list

        buf_ratecode = None
        Buf_ratecode =  create_buffer("Buf_ratecode",Ratecode)

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

                    buf_ratecode = db_session.query(Buf_ratecode).filter(
                             (Buf_ratecode.code == mesvalue)).first()
                    dynarate_list.adult = buf_ratecode.erwachs
                    dynarate_list.child = buf_ratecode.kind1
                    dynarate_list.rcode = mesvalue
        currency = ""

        if dynarate_list:

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

            zimkateg = db_session.query(Zimkateg).filter(
                     (Zimkateg.kurzbez == dynarate_list.rmtype)).first()


    def create_dynabuffers():

        nonlocal rate_list_list, dynacode, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, rmtype_str, ratecode, queasy, guest_pr, waehrung, zimkateg, res_line
        nonlocal frdate, todate, sm_gastno
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

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.zikatnr == zimkateg.zikatnr)).order_by(Res_line._recid).all():

            if res_line.ankunft >= frdate:
                datum1 = res_line.ankunft
            else:
                datum1 = frdate

            if res_line.abreise <= todate:
                datum2 = res_line.abreise - timedelta(days=1)
            else:
                datum2 = todate
            for datum in date_range(datum1,datum2) :

                rate_list = query(rate_list_list, filters=(lambda rate_list: rate_list.datum == datum), first=True)

                if rate_list:
                    rate_list.occ_rooms = rate_list.occ_rooms + res_line.zimmeranz

        for rate_list in query(rate_list_list):
            curr_wday = get_weekday(rate_list.datum) - 1

            if curr_wday == 0:
                curr_wday = 7

            for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.dynarate_list.rmtype == zimkateg.kurzbez), sort_by=[("w_day",True)]):
                use_it = True

                if dynarate_list.days1 != 0 and (rate_list.datum - ci_date) <= dynarate_list.days1:
                    use_it = False

                if use_it and dynarate_list.days2 != 0 and (rate_list.datum - ci_date) >= dynarate_list.days2:
                    use_it = False

                if use_it:

                    if dynarate_list.w_day == curr_wday and (dynarate_list.fr_room <= rate_list.occ_rooms) and (dynarate_list.to_room >= rate_list.occ_rooms):
                        rate_list.rcode = dynarate_list.rcode
                        rate_list.rcmap = dynacode
                        rate_list.adult = dynarate_list.adult
                        rate_list.child = dynarate_list.child

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rcode) & (Queasy.number1 == zimkateg.zikatnr) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == rate_list.datum)).first()

                        if queasy:
                            rate_list.rcode = queasy.char3
                            rate_list.adult = dynarate_list.adult
                            rate_list.child = dynarate_list.child


                        break

                    elif dynarate_list.w_day == 0 and (dynarate_list.fr_room <= rate_list.occ_rooms and dynarate_list.to_room >= rate_list.occ_rooms):
                        rate_list.rcode = dynarate_list.rcode
                        rate_list.rcmap = dynacode
                        rate_list.adult = dynarate_list.adult
                        rate_list.child = dynarate_list.child

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rcode) & (Queasy.number1 == zimkateg.zikatnr) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == rate_list.datum)).first()

                        if queasy:
                            rate_list.rcode = queasy.char3
                            rate_list.adult = dynarate_list.adult
                            rate_list.child = dynarate_list.child


                        break

        for rate_list in query(rate_list_list):
            rate_found, rm_rate, restricted, kback_flag = get_output(ratecode_rate(False, False, -1, 0, ("!" + rate_list.rcode), rate_list.datum, rate_list.datum, rate_list.datum, (rate_list.datum + 1), markno, argtno, zimkateg.zikatnr, rate_list.adult, rate_list.child, 0, 0, wahrno))

            if rate_found:
                rate_list.currency = currency
                rate_list.rmrate =  to_decimal(rm_rate)


            else:
                rate_list_list.remove(rate_list)

        for rate_list in query(rate_list_list, filters=(lambda rate_list: rate_list.rmRate == 0)):
            rate_list_list.remove(rate_list)

    rate_list_list.clear()
    for datum in date_range(frdate,todate) :
        rate_list = Rate_list()
        rate_list_list.append(rate_list)

        rate_list.datum = datum


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

    for rclist in query(rclist_list):

        if RClist.RCtype == 1:
            dynacode = RClist.RCname
            create_masterdyna()
            create_dynabuffers()

    return generate_output()