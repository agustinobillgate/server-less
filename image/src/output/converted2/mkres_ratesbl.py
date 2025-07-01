#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_bonus_nightbl import check_bonus_nightbl
from models import Res_line, Reslin_queasy, Queasy, Htparam, Zimkateg, Segment, Reservation

reslin_list_list, Reslin_list = create_model_like(Res_line)
room_list_list, Room_list = create_model("Room_list", {"avail_flag":bool, "allot_flag":bool, "zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":[int,30], "bezeich":string, "room":[int,30], "coom":[string,30], "rmrate":[Decimal,30], "currency":int, "wabkurz":string, "i_counter":int, "rateflag":bool, "adult":int, "child":int, "prcode":[string,30], "rmcat":string, "argt":string, "rcode":string, "segmentcode":string, "dynarate":bool, "expired":bool, "argt_remark":string, "minstay":int, "maxstay":int, "minadvance":int, "maxadvance":int, "frdate":date, "todate":date, "marknr":int, "datum":[date,30]}, {"sleeping": True, "frdate": None, "todate": None})
res_dynarate_list, Res_dynarate = create_model("Res_dynarate", {"date1":date, "date2":date, "rate":Decimal, "rmcat":string, "argt":string, "prcode":string, "rcode":string, "markno":int, "setup":int, "adult":int, "child":int})

def mkres_ratesbl(from_date:date, user_init:string, chg_zikat:bool, chg_flag:bool, reslin_list_list:[Reslin_list], room_list_list:[Room_list], res_dynarate_list:[Res_dynarate]):

    prepare_cache ([Res_line, Reslin_queasy, Queasy, Htparam, Zimkateg, Segment, Reservation])

    ratecode_bez = ""
    new_segm = ""
    fixed_rate = False
    room_rate = to_decimal("0.0")
    resno:int = 0
    reslinno:int = 0
    ankunft:date = None
    abreise:date = None
    curr_argt:string = ""
    ractive:bool = False
    curr_i:int = 0
    fr_date:date = None
    checkin_date:date = None
    curr_date:date = None
    to_date:date = None
    p_493:bool = False
    cid:string = ""
    cdate:string = " "
    counter:int = 0
    res_line = reslin_queasy = queasy = htparam = zimkateg = segment = reservation = None

    reslin_list = res_dynarate = room_list = t_rqy = r_qsy = bqueasy = None

    t_rqy_list, T_rqy = create_model_like(Reslin_queasy, {"count_i":int})

    R_qsy = create_buffer("R_qsy",Reslin_queasy)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ratecode_bez, new_segm, fixed_rate, room_rate, resno, reslinno, ankunft, abreise, curr_argt, ractive, curr_i, fr_date, checkin_date, curr_date, to_date, p_493, cid, cdate, counter, res_line, reslin_queasy, queasy, htparam, zimkateg, segment, reservation
        nonlocal from_date, user_init, chg_zikat, chg_flag
        nonlocal r_qsy, bqueasy


        nonlocal reslin_list, res_dynarate, room_list, t_rqy, r_qsy, bqueasy
        nonlocal t_rqy_list

        return {"ratecode_bez": ratecode_bez, "new_segm": new_segm, "fixed_rate": fixed_rate, "room_rate": room_rate, "Res-Dynarate": res_dynarate_list}

    def update_qsy171():

        nonlocal ratecode_bez, new_segm, fixed_rate, room_rate, resno, reslinno, ankunft, abreise, curr_argt, ractive, curr_i, fr_date, checkin_date, curr_date, to_date, p_493, cid, cdate, counter, res_line, reslin_queasy, queasy, htparam, zimkateg, segment, reservation
        nonlocal from_date, user_init, chg_zikat, chg_flag
        nonlocal r_qsy, bqueasy


        nonlocal reslin_list, res_dynarate, room_list, t_rqy, r_qsy, bqueasy
        nonlocal t_rqy_list

        qsy = None
        zbuff = None
        upto_date:date = None
        datum:date = None
        start_date:date = None
        i:int = 0
        iftask:string = ""
        origcode:string = ""
        newcode:string = ""
        do_it:bool = False
        cat_flag:bool = False
        roomnr:int = 0
        roomnr1:int = 0
        Qsy =  create_buffer("Qsy",Queasy)
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == ("$origcode$").lower() :
                origcode = substring(iftask, 10)
                return
        for i in range(1,num_entries(reslin_list.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(i - 1, reslin_list.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == ("$origcode$").lower() :
                newcode = substring(iftask, 10)
                return

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if cat_flag and zbuff:
            roomnr = zbuff.typ
            roomnr1 = zimkateg.typ

        elif zbuff:
            roomnr = zbuff.zikatnr
            roomnr1 = zimkateg.zikatnr

        if origcode.lower()  == (newcode).lower()  and res_line.zikatnr == zimkateg.zikatnr:
            pass

        elif origcode != "" or newcode != "":

            if res_line.ankunft == res_line.abreise:
                upto_date = res_line.abreise
            else:
                upto_date = res_line.abreise - timedelta(days=1)

            if res_line.zikatnr != zimkateg.zikatnr:
                for datum in date_range(res_line.ankunft,upto_date) :

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True
                        pass
                        pass

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr1)],"char1": [(eq, newcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True
                        pass
                        pass

            elif res_line.zikatnr == zimkateg.zikatnr and origcode.lower()  != (newcode).lower() :
                for datum in date_range(res_line.ankunft,upto_date) :

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True
                        pass
                        pass

                    queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, datum)],"number1": [(eq, roomnr)],"char1": [(eq, newcode)]})

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:
                        pass
                        queasy.logi2 = True
                        pass
                        pass

    reslin_list = query(reslin_list_list, first=True)

    room_list = query(room_list_list, first=True)
    resno = reslin_list.resnr
    reslinno = reslin_list.reslinnr
    ankunft = reslin_list.ankunft
    abreise = reslin_list.abreise
    curr_argt = reslin_list.arrangement

    if reslin_list.changed != None:
        cid = reslin_list.changed_id
        cdate = to_string(reslin_list.changed)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    checkin_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 493)]})
    p_493 = htparam.flogical


    counter = 1

    for reslin_queasy in db_session.query(Reslin_queasy).filter(
             (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (((Reslin_queasy.date1 >= from_date) & (Reslin_queasy.date1 <= (abreise - timedelta(days=1)))) | ((Reslin_queasy.date1 >= from_date) & (Reslin_queasy.date2 <= (abreise - timedelta(days=1)))))).order_by(Reslin_queasy._recid).all():
        t_rqy = T_rqy()
        t_rqy_list.append(t_rqy)

        t_rqy.key = "ResChanges"
        t_rqy.count_i = counter
        t_rqy.resnr = resno
        t_rqy.reslinnr = reslinno
        t_rqy.date2 = get_current_date()
        t_rqy.number2 = get_current_time_in_seconds()


        t_rqy.char3 = to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("Modify Fixrate FR:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
        counter = counter + 2
        db_session.delete(reslin_queasy)
        pass

    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, room_list.rcode)]})

    if queasy:

        bqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, queasy.char1)]})

        if bqueasy and bqueasy.logi1:
            ratecode_bez = queasy.char1 + " - " + queasy.char2


        else:
            ratecode_bez = queasy.char1 + " - " + queasy.char2

    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.date1 < Reslin_queasy.date2)).order_by(Reslin_queasy._recid).all():
        to_date = reslin_queasy.date2

        r_qsy = get_cache (Reslin_queasy, {"_recid": [(eq, reslin_queasy._recid)]})
        r_qsy.date2 = r_qsy.date1


        pass
        pass
        curr_date = reslin_queasy.date1
        for curr_i in range(2,(to_date - reslin_queasy.date1)  + 1) :
            curr_date = curr_date + timedelta(days=1)


            r_qsy = Reslin_queasy()
            db_session.add(r_qsy)

            buffer_copy(reslin_queasy, r_qsy,except_fields=["date1","date2"])
            r_qsy.date1 = curr_date
            r_qsy.date2 = curr_date


            pass
            pass
    counter = 2
    fixed_rate = True
    fr_date = from_date


    for curr_i in range(1,(abreise - from_date)  + 1) :

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"date1": [(eq, fr_date)],"date2": [(eq, fr_date)]})

        if not reslin_queasy:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "arrangement"
            reslin_queasy.resnr = resno
            reslin_queasy.reslinnr = reslinno
            reslin_queasy.date1 = fr_date
            reslin_queasy.date2 = fr_date
            reslin_queasy.deci1 =  to_decimal(room_list.rmrate[curr_i - 1])
            reslin_queasy.char2 = room_list.prcode[curr_i - 1]
            reslin_queasy.char3 = user_init

            if curr_argt != room_list.argt:
                reslin_queasy.char1 = room_list.argt


            t_rqy = T_rqy()
            t_rqy_list.append(t_rqy)

            t_rqy.key = "ResChanges"
            t_rqy.count_i = counter
            t_rqy.resnr = resno
            t_rqy.reslinnr = reslinno
            t_rqy.date2 = get_current_date()
            t_rqy.number2 = get_current_time_in_seconds()


            t_rqy.char3 = to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("Modify Fixrate TO:") + ";" + to_string(reslin_queasy.date1) + "-" + to_string(reslin_queasy.deci1) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
            counter = counter + 2

        if curr_i == 1:
            room_rate =  to_decimal(reslin_queasy.deci1)
        fr_date = fr_date + timedelta(days=1)

    for t_rqy in query(t_rqy_list, sort_by=[("count_i",False)]):
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        buffer_copy(t_rqy, reslin_queasy)

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, room_list.rmcat)]})

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})
    update_qsy171()
    res_line.zimmer_wunsch = reslin_list.zimmer_wunsch
    res_line.arrangement = reslin_list.arrangement
    res_line.betriebsnr = reslin_list.betriebsnr
    res_line.zipreis =  to_decimal(reslin_list.zipreis)
    res_line.reserve_int = room_list.marknr
    res_line.zikatnr = zimkateg.zikatnr
    res_line.l_zuordnung[0] = zimkateg.zikatnr

    if chg_zikat:
        res_line.zinr = ""
        res_line.setup = 0


    pass
    ractive = True

    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, room_list.rcode)]})

    bqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, queasy.char1)]})

    if bqueasy:
        ractive = not bqueasy.logi1

    if entry(0, queasy.char3, ";") != "" and ractive and ((reslin_list.active_flag == 0) or (reslin_list.active_flag == 1) and (from_date == checkin_date)):

        segment = get_cache (Segment, {"bezeich": [(eq, entry(0, queasy.char3, ";"))]})

        if segment:

            reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})
            reservation.segmentcode = segment.segmentcode
            new_segm = to_string(segment.segmentcode) + " " +\
                    segment.bezeich


            pass

    if room_list.dynarate:

        for res_dynarate in query(res_dynarate_list):

            if res_dynarate.date2 < from_date:
                pass

            elif res_dynarate.date1 < checkin_date and res_dynarate.date2 >= checkin_date:
                res_dynarate.date2 = checkin_date - timedelta(days=1)
            else:
                res_dynarate_list.remove(res_dynarate)
        fixed_rate = True
        fr_date = from_date


        for curr_i in range(1,(abreise - from_date)  + 1) :
            res_dynarate = Res_dynarate()
            res_dynarate_list.append(res_dynarate)

            res_dynarate.date1 = fr_date
            res_dynarate.date2 = fr_date
            res_dynarate.rmcat = room_list.rmcat
            res_dynarate.argt = room_list.argt
            res_dynarate.markno = room_list.marknr
            res_dynarate.adult = room_list.adult
            res_dynarate.child = room_list.child
            res_dynarate.rcode = room_list.rcode
            res_dynarate.prcode = room_list.prcode[curr_i - 1]
            res_dynarate.rate =  to_decimal(room_list.rmrate[curr_i - 1])

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"date1": [(eq, fr_date)],"date2": [(eq, fr_date)]})

            if not reslin_queasy:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "arrangement"
                reslin_queasy.resnr = resno
                reslin_queasy.reslinnr = reslinno
                reslin_queasy.date1 = fr_date
                reslin_queasy.date2 = fr_date
                reslin_queasy.deci1 =  to_decimal(room_list.rmrate[curr_i - 1])
                reslin_queasy.char2 = room_list.prcode[curr_i - 1]
                reslin_queasy.char3 = user_init

                if curr_argt != room_list.argt:
                    pass

            if curr_i == 1:
                room_rate =  to_decimal(reslin_queasy.deci1)
            fr_date = fr_date + timedelta(days=1)
            res_dynarate.rate =  to_decimal(reslin_queasy.deci1)
            reslin_queasy.char1 = room_list.argt

    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno)).order_by(Reslin_queasy._recid).all():

        if reslin_queasy.date2 < reslin_list.ankunft:
            db_session.delete(reslin_queasy)

        elif reslin_queasy.date1 >= reslin_list.abreise:
            db_session.delete(reslin_queasy)

    if reslin_list.active_flag == 0:
        res_dynarate_list = get_output(check_bonus_nightbl(reslin_list.ankunft, reslin_list.abreise, res_dynarate_list))

    return generate_output()