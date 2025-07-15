from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.htplogic import htplogic
from sqlalchemy import func
from models import Kontline, Ratecode, Arrangement, Queasy, Guest_pr, Zimkateg, Guest, Waehrung, Res_line, Zimmer, Reservation, Segment

def find_dyna_ratecodesm(gastno:int, datum:date, rmtype:str, adult:int, child:int, rmrate:decimal, dynacode:str, argtno:int):
    statcode = ""
    markno = 0
    wahrno = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    room_occ:int = 0
    global_occ:bool = False
    i_param439:int = 0
    param486:bool = False
    w_day:int = 0
    tokcounter:int = 0
    argtcounter:int = 0
    iftask:str = ""
    mestoken:str = ""
    mesvalue:str = ""
    mapcode:str = ""
    rsv_globekey:bool = False
    dyna_flag:bool = False
    rmtype_str:str = ""
    zimkateg_zikatnr:int = 0
    currency:str = ""
    roomtype:int = 0
    argt:int = 0
    kontline = ratecode = arrangement = queasy = guest_pr = zimkateg = guest = waehrung = res_line = zimmer = reservation = segment = None

    rcode_list = dynarate_list = kline = buffratecode = None

    rcode_list_list, Rcode_list = create_model("Rcode_list", {"rcode":str})
    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str})

    Kline = create_buffer("Kline",Kontline)
    Buffratecode = create_buffer("Buffratecode",Ratecode)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal statcode, markno, wahrno, wd_array, room_occ, global_occ, i_param439, param486, w_day, tokcounter, argtcounter, iftask, mestoken, mesvalue, mapcode, rsv_globekey, dyna_flag, rmtype_str, zimkateg_zikatnr, currency, roomtype, argt, kontline, ratecode, arrangement, queasy, guest_pr, zimkateg, guest, waehrung, res_line, zimmer, reservation, segment
        nonlocal gastno, datum, rmtype, adult, child, rmrate, dynacode, argtno
        nonlocal kline, buffratecode


        nonlocal rcode_list, dynarate_list, kline, buffratecode
        nonlocal rcode_list_list, dynarate_list_list

        return {"statcode": statcode, "argtno": argtno, "markno": markno, "wahrno": wahrno}

    def find_dyna_rate():

        nonlocal statcode, markno, wahrno, wd_array, room_occ, global_occ, i_param439, param486, w_day, tokcounter, argtcounter, iftask, mestoken, mesvalue, mapcode, rsv_globekey, dyna_flag, rmtype_str, zimkateg_zikatnr, currency, roomtype, argt, kontline, ratecode, arrangement, queasy, guest_pr, zimkateg, guest, waehrung, res_line, zimmer, reservation, segment
        nonlocal gastno, datum, rmtype, adult, child, rmrate, dynacode, argtno
        nonlocal kline, buffratecode


        nonlocal rcode_list, dynarate_list, kline, buffratecode
        nonlocal rcode_list_list, dynarate_list_list

        commission_str:str = ""
        commission_dec:decimal = to_decimal("0.0")
        found_flag:bool = False
        mindiff:decimal = 999999999
        diffrate:decimal = to_decimal("0.0")

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastno)).first()

        if guest:

            if num_entries(guest.steuernr, "|") == 2:
                commission_str = entry(1, guest.steuernr, "|")
                commission_str = replace_str(commission_str, "-", "")
                commission_str = replace_str(commission_str, "%", "")
                commission_str = replace_str(commission_str, ",", ".")
                commission_dec =  to_decimal(to_decimal(commission_str) )

            if commission_dec != 0:
                found_flag = find_secondary_rate()

            if found_flag:

                return

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == dynacode)).order_by(Ratecode._recid).all():
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
            argtcounter = argtcounter + 1

            if argtcounter >= 1:

                buffratecode = db_session.query(Buffratecode).filter(
                         (Buffratecode.code == dynarate_list.rcode)).first()

                if buffratecode:
                    argt = buffratecode.argtnr
                    argtno = buffratecode.argtnr

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*").lower()), first=True)
        global_occ = None != dynarate_list and i_param439 == 1

        if global_occ:

            for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != ("*").lower())):
                dynarate_list_list.remove(dynarate_list)

        else:

            for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != (rmtype_str).lower())):
                dynarate_list_list.remove(dynarate_list)

        found_flag = find_static_occ()

        if found_flag:

            return


    def find_secondary_rate():

        nonlocal statcode, markno, wahrno, wd_array, room_occ, global_occ, i_param439, param486, w_day, argtcounter, iftask, mestoken, mapcode, rsv_globekey, dyna_flag, rmtype_str, zimkateg_zikatnr, currency, roomtype, argt, kontline, ratecode, arrangement, queasy, guest_pr, zimkateg, guest, waehrung, res_line, zimmer, reservation, segment
        nonlocal gastno, datum, rmtype, adult, child, rmrate, dynacode, argtno
        nonlocal kline, buffratecode


        nonlocal rcode_list, dynarate_list, kline, buffratecode
        nonlocal rcode_list_list, dynarate_list_list

        found_flag = False
        tokcounter:int = 0
        mesvalue:str = ""
        mindiff:decimal = 999999999
        diffrate:decimal = to_decimal("0.0")

        def generate_inner_output():
            return (found_flag)

        for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
            mesvalue = entry(tokcounter - 1, queasy.char3, ",")

            if mesvalue != "":
                rcode_list = Rcode_list()
                rcode_list_list.append(rcode_list)

                rcode_list.rcode = mesvalue

        rcode_list = query(rcode_list_list, first=True)

        if not rcode_list:

            return generate_inner_output()
        w_day = wd_array[get_weekday(datum) - 1]


        pass

        for rcode_list in query(rcode_list_list):

            ratecode = db_session.query(Ratecode).filter(
                     (Ratecode.code == rcode_list.rcode) & (Ratecode.zikatnr == zimkateg_zikatnr)).first()

            if ratecode:

                if not arrangement:

                    arrangement = db_session.query(Arrangement).filter(
                             (Arrangement.argtnr == ratecode.argtnr)).first()

                    if arrangement:
                        argtno = arrangement.argtnr

                if wahrno == 0 or markno == 0:

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 18) & (Queasy.number1 == ratecode.marknr)).first()

                    if queasy:

                        waehrung = db_session.query(Waehrung).filter(
                                 (Waehrung.wabkurz == queasy.char3)).first()

                        if waehrung:
                            wahrno = waehrung.waehrungsnr
                            markno = ratecode.marknr

            if arrangement and markno != 0 and wahrno != 0:
                break

        if not zimkateg:

            return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
                found_flag = True

                return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day)).first()

            if ratecode:
                diffrate =  to_decimal(ratecode.zipreis) - to_decimal(rmrate)

                if diffrate < 0:
                    diffrate =  - to_decimal(diffrate)

                if diffrate < mindiff:
                    statcode = ratecode.code
                    mindiff =  to_decimal(diffrate)
                    found_flag = True

        if found_flag:

            return generate_inner_output()

        for rcode_list in query(rcode_list_list):
            mapcode = rcode_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0)).first()

            if ratecode:
                diffrate =  to_decimal(ratecode.zipreis) - to_decimal(rmrate)

                if diffrate < 0:
                    diffrate =  - to_decimal(diffrate)

                if diffrate < mindiff:
                    statcode = ratecode.code
                    mindiff =  to_decimal(diffrate)
                    found_flag = True

        return generate_inner_output()


    def find_static_rate():

        nonlocal statcode, markno, wahrno, wd_array, room_occ, global_occ, i_param439, param486, w_day, tokcounter, argtcounter, iftask, mestoken, mesvalue, mapcode, rsv_globekey, dyna_flag, rmtype_str, zimkateg_zikatnr, currency, roomtype, argt, kontline, ratecode, arrangement, queasy, guest_pr, zimkateg, guest, waehrung, res_line, zimmer, reservation, segment
        nonlocal gastno, datum, rmtype, adult, child, rmrate, dynacode, argtno
        nonlocal kline, buffratecode


        nonlocal rcode_list, dynarate_list, kline, buffratecode
        nonlocal rcode_list_list, dynarate_list_list


        w_day = wd_array[get_weekday(datum) - 1]

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == statcode) & (Ratecode.zikatnr == zimkateg_zikatnr)).order_by(Ratecode._recid).all():

            if not arrangement:

                arrangement = db_session.query(Arrangement).filter(
                         (Arrangement.argtnr == ratecode.argtnr)).first()

                if arrangement:
                    argtno = arrangement.argtnr

            if wahrno == 0 or markno == 0:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == ratecode.marknr)).first()

                if queasy:

                    waehrung = db_session.query(Waehrung).filter(
                             (Waehrung.wabkurz == queasy.char3)).first()

                    if waehrung:
                        wahrno = waehrung.waehrungsnr
                        markno = ratecode.marknr

            if arrangement and markno != 0 and wahrno != 0:
                break


    def find_static_rate2():

        nonlocal statcode, markno, wahrno, wd_array, room_occ, global_occ, i_param439, param486, tokcounter, argtcounter, iftask, mestoken, mesvalue, rsv_globekey, dyna_flag, rmtype_str, zimkateg_zikatnr, currency, roomtype, argt, kontline, ratecode, arrangement, queasy, guest_pr, zimkateg, guest, waehrung, res_line, zimmer, reservation, segment
        nonlocal gastno, datum, rmtype, adult, child, rmrate, dynacode, argtno
        nonlocal kline, buffratecode


        nonlocal rcode_list, dynarate_list, kline, buffratecode
        nonlocal rcode_list_list, dynarate_list_list

        w_day:int = 0
        mapcode:str = ""
        found_flag:bool = False
        mindiff:decimal = 999999999
        diffrate:decimal = to_decimal("0.0")
        w_day = wd_array[get_weekday(datum) - 1]

        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.kurzbez == rmtype)).first()

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.argtnr == argtno)).first()

        for dynarate_list in query(dynarate_list_list):
            mapcode = dynarate_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.erwachs == adult) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.erwachs == adult) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.kind1 == child) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day) & (Ratecode.zipreis == rmrate)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0) & (Ratecode.zipreis == rmrate)).first()

            if ratecode:
                statcode = ratecode.code
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

                return

        for dynarate_list in query(dynarate_list_list):
            mapcode = dynarate_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == w_day)).first()

            if ratecode:
                diffrate =  to_decimal(ratecode.zipreis) - to_decimal(rmrate)

                if diffrate < 0:
                    diffrate =  - to_decimal(diffrate)

                if diffrate < mindiff:
                    statcode = ratecode.code
                    markno = ratecode.marknr
                    argtno = ratecode.argtnr
                    mindiff =  to_decimal(diffrate)
                    found_flag = True

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                if queasy:
                    currency = queasy.char3

                if currency != "":

                    waehrung = db_session.query(Waehrung).filter(
                             (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

                    if waehrung:
                        wahrno = waehrung.waehrungsnr

        if found_flag:

            return

        for dynarate_list in query(dynarate_list_list):
            mapcode = dynarate_list.rcode

            ratecode = db_session.query(Ratecode).filter(
                     (func.lower(Ratecode.code) == (mapcode).lower()) & (Ratecode.zikatnr == zimkateg_zikatnr) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum) & (Ratecode.wday == 0)).first()

            if ratecode:
                diffrate =  to_decimal(ratecode.zipreis) - to_decimal(rmrate)

                if diffrate < 0:
                    diffrate =  - to_decimal(diffrate)

                if diffrate < mindiff:
                    statcode = ratecode.code
                    markno = ratecode.marknr
                    argtno = ratecode.argtnr
                    mindiff =  to_decimal(diffrate)
                    found_flag = True

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                if queasy:
                    currency = queasy.char3

                if currency != "":

                    waehrung = db_session.query(Waehrung).filter(
                             (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

                    if waehrung:
                        wahrno = waehrung.waehrungsnr


    def find_static_occ():

        nonlocal statcode, markno, wahrno, wd_array, room_occ, global_occ, i_param439, param486, w_day, tokcounter, argtcounter, iftask, mestoken, mesvalue, mapcode, rsv_globekey, dyna_flag, rmtype_str, zimkateg_zikatnr, currency, roomtype, argt, kontline, ratecode, arrangement, queasy, guest_pr, zimkateg, guest, waehrung, res_line, zimmer, reservation, segment
        nonlocal gastno, datum, rmtype, adult, child, rmrate, dynacode, argtno
        nonlocal kline, buffratecode


        nonlocal rcode_list, dynarate_list, kline, buffratecode
        nonlocal rcode_list_list, dynarate_list_list

        found_flag = False

        def generate_inner_output():
            return (found_flag)

        w_day = wd_array[get_weekday(datum) - 1]


        room_occ = count_availability(datum, roomtype)
        currency = ""

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.fr_room <= room_occ and dynarate_list.to_room >= room_occ), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.fr_room <= room_occ and dynarate_list.to_room >= room_occ), first=True)

        if dynarate_list:

            if not global_occ:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rCode) & (Queasy.number1 == roomtype) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == datum)).first()
            else:

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 145) & (Queasy.char1 == dynacode) & (Queasy.char2 == dynarate_list.rCode) & (Queasy.number1 == 0) & (Queasy.deci1 == dynarate_list.w_day) & (Queasy.deci2 == dynarate_list.counter) & (Queasy.date1 == datum)).first()

            if queasy:
                dynarate_list.rcode = queasy.char3

            ratecode = db_session.query(Ratecode).filter(
                     (Ratecode.code == dynarate_list.rCode) & (Ratecode.zikatnr == roomtype) & (Ratecode.wday == w_day) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum)).first()

            if not ratecode:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == dynarate_list.rCode) & (Ratecode.zikatnr == roomtype) & (Ratecode.wday == 0) & (Ratecode.startperiode <= datum) & (Ratecode.endperiode >= datum)).first()

            if ratecode:
                statcode = ratecode.code
                markno = ratecode.marknr
                argtno = ratecode.argtnr
                found_flag = True

                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 18) & (Queasy.number1 == markno)).first()

                if queasy:
                    currency = queasy.char3

                if currency != "":

                    waehrung = db_session.query(Waehrung).filter(
                             (func.lower(Waehrung.wabkurz) == (currency).lower())).first()

                    if waehrung:
                        wahrno = waehrung.waehrungsnr

        return generate_inner_output()


    def count_availability(curr_date:date, i_typ:int):

        nonlocal statcode, markno, wahrno, wd_array, room_occ, global_occ, i_param439, param486, w_day, tokcounter, argtcounter, iftask, mestoken, mesvalue, mapcode, rsv_globekey, dyna_flag, rmtype_str, zimkateg_zikatnr, currency, roomtype, argt, kontline, ratecode, arrangement, queasy, guest_pr, zimkateg, guest, waehrung, res_line, zimmer, reservation, segment
        nonlocal gastno, datum, rmtype, adult, child, rmrate, dynacode, argtno
        nonlocal kline, buffratecode


        nonlocal rcode_list, dynarate_list, kline, buffratecode
        nonlocal rcode_list_list, dynarate_list_list

        rm_occ = 0
        vhp_limited:bool = False
        do_it:bool = False
        rm_allot:int = 0

        def generate_inner_output():
            return (rm_occ)

        rm_occ = 0
        rm_allot = 0

        if global_occ:

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.kontstat == 1) & (Kontline.betriebsnr == 1) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                rm_allot = rm_allot + kontline.zimmeranz

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = db_session.query(Reservation).filter(
                             (Reservation.resnr == res_line.resnr)).first()

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0

                if do_it:
                    rm_occ = rm_occ + res_line.zimmeranz

                kline = db_session.query(Kline).filter(
                         (Kline.kontignr == res_line.kontignr) & (Kline.kontstat == 1)).first()

                if kline:

                    kontline = db_session.query(Kontline).filter(
                             (Kontline.kontcode == kline.kontcode) & (Kontline.betriebsnr == 1) & (Kontline.kontstat == 1)).first()

                    if kontline:
                        do_it = True

                        if res_line.zinr != "":

                            zimmer = db_session.query(Zimmer).filter(
                                     (Zimmer.zinr == res_line.zinr)).first()
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = db_session.query(Reservation).filter(
                                     (Reservation.resnr == res_line.resnr)).first()

                            segment = db_session.query(Segment).filter(
                                     (Segment.segmentcode == reservation.segmentcode)).first()
                            do_it = None != segment and segment.vip_level == 0

                        if do_it:
                            rm_allot = rm_allot - res_line.zimmeranz
            rm_occ = rm_occ + rm_allot + 1
        else:

            for kontline in db_session.query(Kontline).filter(
                     (Kontline.kontstat == 1) & (Kontline.betriebsnr == 1) & (Kontline.zikatnr == i_typ) & (curr_date >= Kontline.ankunft) & (curr_date <= Kontline.abreise)).order_by(Kontline._recid).all():
                rm_allot = rm_allot + kontline.zimmeranz

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4) & (Res_line.resstatus != 12) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.zikatnr == i_typ) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & (Res_line.kontignr >= 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
                do_it = True

                if res_line.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()
                    do_it = zimmer.sleeping

                if do_it and vhp_limited:

                    reservation = db_session.query(Reservation).filter(
                             (Reservation.resnr == res_line.resnr)).first()

                    segment = db_session.query(Segment).filter(
                             (Segment.segmentcode == reservation.segmentcode)).first()
                    do_it = None != segment and segment.vip_level == 0

                if do_it:
                    rm_occ = rm_occ + res_line.zimmeranz

                kline = db_session.query(Kline).filter(
                         (Kline.kontignr == res_line.kontignr) & (Kline.kontstat == 1)).first()

                if kline:

                    kontline = db_session.query(Kontline).filter(
                             (Kontline.kontcode == kline.kontcode) & (Kontline.betriebsnr == 1) & (Kontline.kontstat == 1)).first()

                    if kontline:
                        do_it = True

                        if res_line.zinr != "":

                            zimmer = db_session.query(Zimmer).filter(
                                     (Zimmer.zinr == res_line.zinr)).first()
                            do_it = zimmer.sleeping

                        if do_it and vhp_limited:

                            reservation = db_session.query(Reservation).filter(
                                     (Reservation.resnr == res_line.resnr)).first()

                            segment = db_session.query(Segment).filter(
                                     (Segment.segmentcode == reservation.segmentcode)).first()
                            do_it = None != segment and segment.vip_level == 0

                        if do_it:
                            rm_allot = rm_allot - res_line.zimmeranz
            rm_occ = rm_occ + rm_allot + 1

        return generate_inner_output()


    i_param439 = get_output(htpint(439))
    param486 = get_output(htplogic(486))
    argt = argtno

    arrangement = db_session.query(Arrangement).filter(
             (Arrangement.argtnr == argtno) & (not Arrangement.weeksplit)).first()

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 2) & (Queasy.char1 == dynacode)).first()

    if not queasy:

        guest_pr = db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == gastno)).first()

        if guest_pr:

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 2) & (Queasy.char1 == guest_pr.code)).first()

            if queasy:
                dynacode = queasy.char1

            elif not queasy:

                return generate_output()
    dyna_flag = queasy.logi2
    statcode = dynacode

    zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.kurzbez == rmtype)).first()

    if zimkateg:
        rmtype_str = zimkateg.kurzbez
        zimkateg_zikatnr = zimkateg.zikatnr
        roomtype = zimkateg.zikatnr

    if dyna_flag:
        find_dyna_rate()
    else:
        find_static_rate()

    return generate_output()