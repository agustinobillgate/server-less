#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 31/10/2025
# Ticket:F6D79E
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.ratecode_rate import ratecode_rate
from functions.calculate_occupied_roomsbl import calculate_occupied_roomsbl
from sqlalchemy import func
from models import Ratecode, Queasy, Htparam, Zimkateg, Guest_pr, Waehrung, Segment, Arrangement, Res_line

created_list_data, Created_list = create_model("Created_list", {"ratecode":string, "marknr":int, "rmcateg":int, "argtno":int, "statcode":[string,300], "rmrate":[Decimal,300]})

def available_rates_cldbl(frdate:date, todate:date, i_zikatnr:int, i_counter:int, adult_child_str:string, ind_gastno:int, created_list_data:[Created_list]):

    prepare_cache ([Ratecode, Queasy, Htparam, Zimkateg, Guest_pr, Waehrung, Segment, Arrangement, Res_line])

    rate_list_data = []
    adult:int = 0
    child:int = 0
    rooms:int = 1
    inp_resnr:int = 0
    inp_reslinnr:int = 0
    rmtype:int = 0
    argtno:int = 0
    markno:int = 0
    wahrno:int = 0
    tokcounter:int = 0
    iftask:string = ""
    mestoken:string = ""
    mesvalue:string = ""
    currency:string = ""
    mapcode:string = ""
    datum:date = None
    ankunft:date = None
    dynacode:string = ""
    rmtype_str:string = ""
    curr_i:int = 0
    curr_date:date = None
    rm_rate:Decimal = to_decimal("0.0")
    rate_found:bool = False
    restricted:bool = False
    kback_flag:bool = False
    global_occ:bool = False
    dd:int = 0
    mm:int = 0
    yyyy:int = 0
    ci_date:date = None
    co_date:date = None
    map_code:string = ""
    use_it:bool = False
    w_day:int = 0
    occ_rooms:int = 0
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    occ_room_array:List[int] = create_empty_list(300,0)
    not_found_flag:bool = False
    do_it:bool = False
    rate_created:bool = False
    allotment_ok:bool = False
    calc_rm:bool = False
    doit:bool = False
    curr_time:int = 0
    ratecode = queasy = htparam = zimkateg = guest_pr = waehrung = segment = arrangement = res_line = None

    created_list = rate_list = dynarate_list = selected_ratelist = buff_rlist = buff_dynarate = bratecode = bqueasy = qsy18 = ratebuff = dynabuff = pqueasy = None

    rate_list_data, Rate_list = create_model("Rate_list", {"ratecode":string, "segmentcode":string, "dynaflag":bool, "expired":bool, "room_type":int, "argtno":int, "statcode":[string,300], "rmrate":[Decimal,300], "minstay":int, "maxstay":int, "minadvance":int, "maxadvance":int, "frdate":date, "todate":date, "adult":int, "child":int, "currency":int, "wabkurz":string, "occ_rooms":int, "marknr":int, "i_counter":int}, {"frdate": None, "todate": None})
    dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"counter":int, "w_day":int, "rmtype":string, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":string, "dynacode":string})
    selected_ratelist_data, Selected_ratelist = create_model("Selected_ratelist", {"ratecode":string, "marknr":int, "argtno":int, "adult":int, "child":int, "minstay":int, "maxstay":int})

    Buff_rlist = Rate_list
    buff_rlist_data = rate_list_data

    Buff_dynarate = Dynarate_list
    buff_dynarate_data = dynarate_list_data

    Bratecode = create_buffer("Bratecode",Ratecode)
    Bqueasy = create_buffer("Bqueasy",Queasy)
    Qsy18 = create_buffer("Qsy18",Queasy)
    Ratebuff = create_buffer("Ratebuff",Ratecode)
    Dynabuff = Dynarate_list
    dynabuff_data = dynarate_list_data

    Pqueasy = create_buffer("Pqueasy",Queasy)


    db_session = local_storage.db_session

    adult_child_str = adult_child_str.strip()

    def generate_output():
        nonlocal rate_list_data, adult, child, rooms, inp_resnr, inp_reslinnr, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, ankunft, dynacode, rmtype_str, curr_i, curr_date, rm_rate, rate_found, restricted, kback_flag, global_occ, dd, mm, yyyy, ci_date, co_date, map_code, use_it, w_day, occ_rooms, wd_array, occ_room_array, not_found_flag, do_it, rate_created, allotment_ok, calc_rm, doit, curr_time, ratecode, queasy, htparam, zimkateg, guest_pr, waehrung, segment, arrangement, res_line
        nonlocal frdate, todate, i_zikatnr, i_counter, adult_child_str, ind_gastno
        nonlocal buff_rlist, buff_dynarate, bratecode, bqueasy, qsy18, ratebuff, dynabuff, pqueasy


        nonlocal created_list, rate_list, dynarate_list, selected_ratelist, buff_rlist, buff_dynarate, bratecode, bqueasy, qsy18, ratebuff, dynabuff, pqueasy
        nonlocal rate_list_data, dynarate_list_data, selected_ratelist_data

        return {"ind_gastno": ind_gastno, "created-list": created_list_data, "rate-list": rate_list_data}

    def check_allotment(origcode:string, statcode:string, curr_date:date):

        nonlocal rate_list_data, adult, child, rooms, inp_resnr, inp_reslinnr, rmtype, argtno, markno, wahrno, tokcounter, iftask, mestoken, mesvalue, currency, mapcode, datum, ankunft, dynacode, rmtype_str, rm_rate, rate_found, restricted, kback_flag, global_occ, dd, mm, yyyy, ci_date, co_date, map_code, use_it, w_day, occ_rooms, wd_array, occ_room_array, not_found_flag, do_it, rate_created, allotment_ok, calc_rm, doit, curr_time, ratecode, queasy, htparam, zimkateg, guest_pr, waehrung, segment, arrangement, res_line
        nonlocal frdate, todate, i_zikatnr, i_counter, adult_child_str, ind_gastno
        nonlocal buff_rlist, buff_dynarate, bratecode, bqueasy, qsy18, ratebuff, dynabuff, pqueasy


        nonlocal created_list, rate_list, dynarate_list, selected_ratelist, buff_rlist, buff_dynarate, bratecode, bqueasy, qsy18, ratebuff, dynabuff, pqueasy
        nonlocal rate_list_data, dynarate_list_data, selected_ratelist_data

        allotment_ok = True
        occ_room:int = 0
        allotment:int = 0
        curr_i:int = 0
        rline_origcode:string = ""
        str:string = ""
        ratecode_found:bool = False
        doit_flag:bool = False
        zbuff = None

        def generate_inner_output():
            return (allotment_ok)

        Zbuff =  create_buffer("Zbuff",Zimkateg)

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rate_list.room_type)]})

        if zimkateg.typ == 0:

            ratecode = get_cache (Ratecode, {"code": [(eq, statcode)],"zikatnr": [(eq, rate_list.room_type)],"argtnr": [(eq, rate_list.argtno)],"startperiode": [(le, curr_date)],"endperiode": [(ge, curr_date)],"num1[0]": [(gt, 0)]})
            ratecode_found = None != ratecode

            if ratecode_found:
                allotment = ratecode.num1[0]
            else:

                ratecode_obj_list = {}
                ratecode = Ratecode()
                zbuff = Zimkateg()
                for ratecode.code, ratecode.zikatnr, ratecode.argtnr, ratecode.erwachs, ratecode.kind1, ratecode.marknr, ratecode.char1, ratecode._recid, zbuff.typ, zbuff.zikatnr, zbuff.kurzbez, zbuff._recid in db_session.query(Ratecode.code, Ratecode.zikatnr, Ratecode.argtnr, Ratecode.erwachs, Ratecode.kind1, Ratecode.marknr, Ratecode.char1, Ratecode._recid, Zbuff.typ, Zbuff.zikatnr, Zbuff.kurzbez, Zbuff._recid).join(Zbuff,(Zbuff.zikatnr == Ratecode.zikatnr) & (Zbuff.typ == zimkateg.typ)).filter(
                         (func.lower(Ratecode.code) == (statcode).lower()) & (Ratecode.zikatnr == rate_list.room_type) & (Ratecode.argtnr == rate_list.argtno) & (Ratecode.startperiode <= curr_date) & (Ratecode.endperiode >= curr_date) & (Ratecode.num1[inc_value(0)] > 0)).order_by(Ratecode._recid).all():
                    if ratecode_obj_list.get(ratecode._recid):
                        continue
                    else:
                        ratecode_obj_list[ratecode._recid] = True


                    ratecode_found = True
                    allotment = ratecode.num1[0]

                    break

        if not (allotment > 0):

            return generate_inner_output()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnr == ind_gastno) & (Res_line.active_flag <= 1) & (Res_line.ankunft <= curr_date) & (Res_line.abreise > curr_date) & ((Res_line.resstatus <= 6) & (Res_line.resstatus != 3) & (Res_line.resstatus != 4)) & (matches(Res_line.zimmer_wunsch,("*$origcode$*")))).order_by(Res_line._recid).all():
            doit_flag = (res_line.resnr != inp_resnr) or (res_line.reslinnr != inp_reslinnr)

            if doit_flag  and zimkateg.typ == 0:

                if res_line.zikatnr != zimkateg.zikatnr:
                    doit_flag = False
            else:

                zbuff = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                if zbuff.typ != zimkateg.typ:
                    doit_flag = False

            if doit_flag:

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

                if arrangement.argtnr != rate_list.argtno:
                    doit_flag = False

            if doit_flag:
                for curr_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(curr_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 10).lower() == ("$origcode$") :
                        rline_origcode = substring(str, 10)

                        if rline_origcode.lower()  == (origcode).lower() :
                            occ_room = occ_room + res_line.zimmeranz
                        break

        if (occ_room + rooms) > allotment:
            allotment_ok = False

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 459)]})

    if htparam:
        calc_rm = htparam.flogical

    if ind_gastno == 0:
        ind_gastno = get_output(htpint(123))

        if ind_gastno == 0:

            return generate_output()
    adult_child_str = substring(adult_child_str, 2)
    adult = to_int(entry(0, adult_child_str, ","))
    child = to_int(entry(1, adult_child_str, ","))

    if num_entries(adult_child_str, ",") > 2:
        i_counter = i_counter * 100
        mm = to_int(substring(entry(2, adult_child_str, ",") , 0, 2))
        dd = to_int(substring(entry(2, adult_child_str, ",") , 2, 2))
        yyyy = to_int(substring(entry(2, adult_child_str, ",") , 4, 4))
        co_date = date_mdy(mm, dd, yyyy) + timedelta(days=1)

        if todate > co_date:
            todate = co_date

    if num_entries(adult_child_str, ",") > 3:
        rooms = to_int(entry(3, adult_child_str, ","))
        inp_resnr = to_int(entry(4, adult_child_str, ","))
        inp_reslinnr = to_int(entry(5, adult_child_str, ","))

    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, i_zikatnr)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    if frdate == ci_date:
        ankunft = ci_date
    else:
        ankunft = frdate + timedelta(days=2)

    guest_pr_obj_list = {}
    guest_pr = Guest_pr()
    bqueasy = Queasy()
    for guest_pr.code, guest_pr._recid, bqueasy.char3, bqueasy._recid, bqueasy.char1, bqueasy.number1, bqueasy.number2, bqueasy.deci2, bqueasy.number3, bqueasy.deci3, bqueasy.date1, bqueasy.date2, bqueasy.logi1 in db_session.query(Guest_pr.code, Guest_pr._recid, Bqueasy.char3, Bqueasy._recid, Bqueasy.char1, Bqueasy.number1, Bqueasy.number2, Bqueasy.deci2, Bqueasy.number3, Bqueasy.deci3, Bqueasy.date1, Bqueasy.date2, Bqueasy.logi1).join(Bqueasy,(Bqueasy.key == 2) & (Bqueasy.char1 == Guest_pr.code)).filter(
             (Guest_pr.gastnr == ind_gastno)).order_by(Bqueasy.logi2, Bqueasy.number3.desc(), Bqueasy.deci3.desc()).all():
        if guest_pr_obj_list.get(guest_pr._recid):
            continue
        else:
            guest_pr_obj_list[guest_pr._recid] = True


        curr_time = get_current_time_in_seconds()

        # if bqueasy.number3 > (ankunft - timedelta(days=ci_date)):
        if bqueasy.number3 > (ankunft - ci_date).days:
            pass

        # elif bqueasy.deci3 > 0 and bqueasy.deci3 < (ankunft - timedelta(days=ci_date)):
        elif bqueasy.deci3 > 0 and bqueasy.deci3 < (ankunft - ci_date).days:
            pass

        elif not bqueasy.logi2:
            doit = True

            pqueasy = get_cache (Queasy, {"key": [(eq, 264)],"char1": [(eq, bqueasy.char1)]})

            if pqueasy:
                doit = not pqueasy.logi1

            if doit:

                for bratecode in db_session.query(Bratecode).filter(
                         (Bratecode.code == trim(guest_pr.code)) & (Bratecode.zikatnr == i_zikatnr) & (Bratecode.erwachs == adult) & (Bratecode.kind1 == child) & (not_ (Bratecode.startperiode > todate)) & (not_ (Bratecode.endperiode < frdate))).order_by(Bratecode.wday.desc(), Bratecode.erwachs, Bratecode.startperiode).all():
                    do_it = True

                    if bqueasy.number3 != 0:

                        buff_rlist = query(buff_rlist_data, filters=(lambda buff_rlist: buff_rlist.rateCode != bratecode.code and buff_rlist.room_type == bratecode.zikatnr and buff_rlist.argtno == bratecode.argtnr and buff_rlist.adult == bratecode.erwachs and buff_rlist.child == bratecode.kind1 and buff_rlist.marknr == bratecode.marknr), first=True)
                        do_it = not None != buff_rlist

                    if do_it:

                        rate_list = query(rate_list_data, filters=(lambda rate_list: rate_list.rateCode == bratecode.code and rate_list.room_type == bratecode.zikatnr and rate_list.argtno == bratecode.argtnr and rate_list.adult == bratecode.erwachs and rate_list.child == bratecode.kind1 and rate_list.marknr == bratecode.marknr), first=True)

                        if not rate_list:

                            qsy18 = get_cache (Queasy, {"key": [(eq, 18)],"number1": [(eq, bratecode.marknr)]})

                            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, qsy18.char3)]})
                            rate_list = Rate_list()
                            rate_list_data.append(rate_list)

                            i_counter = i_counter + 1
                            rate_list.i_counter = i_counter
                            rate_list.ratecode = bratecode.code
                            rate_list.room_type = bratecode.zikatnr
                            rate_list.argtno = bratecode.argtnr
                            rate_list.adult = bratecode.erwachs
                            rate_list.child = bratecode.kind1
                            rate_list.marknr = bratecode.marknr
                            rate_list.currency = bqueasy.number1
                            rate_list.minstay = bqueasy.number2
                            rate_list.maxstay = bqueasy.deci2
                            rate_list.minadvance = bqueasy.number3
                            rate_list.maxadvance = bqueasy.deci3
                            rate_list.frdate = bqueasy.date1
                            rate_list.todate = bqueasy.date2
                            rate_list.wabkurz = waehrung.wabkurz

                            if bqueasy.char3 != "":

                                segment = get_cache (Segment, {"bezeich": [(eq, bqueasy.char3)]})

                                if segment:
                                    rate_list.segmentcode = to_string(segment.segmentcode) + " " + segment.bezeich

                            if bqueasy.date1 != None and (ci_date < bqueasy.date1):
                                rate_list.expired = True

                            if bqueasy.date2 != None and (ci_date > bqueasy.date2):
                                rate_list.expired = True
                        curr_i = 0

                        if not rate_list.expired:
                            for curr_date in (frdate - todate).days :
                                curr_i = curr_i + 1
                                allotment_ok = True

                                if allotment_ok:
                                    rate_found, rm_rate, restricted, kback_flag = get_output(ratecode_rate(False, False, 0, 1, ("!" + bqueasy.char1), ci_date, curr_date, curr_date, curr_date, rate_list.marknr, rate_list.argtno, i_zikatnr, rate_list.adult, rate_list.child, 0, 0, rate_list.currency))

                                if rate_found:
                                    rate_list.rmrate[curr_i - 1] = rm_rate
                                    rate_list.statcode[curr_i - 1] = bqueasy.char1


                                else:
                                    rate_list.rmrate[curr_i - 1] = -0.001

        elif bqueasy.logi2:
            dynarate_list_data.clear()

            for bratecode in db_session.query(Bratecode).filter(
                     (Bratecode.code == guest_pr.code)).order_by(Bratecode._recid).all():
                dynarate_list = Dynarate_list()
                dynarate_list_data.append(dynarate_list)

                dynarate_list.dynacode = bratecode.code
                iftask = bratecode.char1[4]


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
                        dynarate_list.rcode = trim(mesvalue)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 439)]})

            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*")), first=True)
            global_occ = None != dynarate_list and htparam.finteger == 1

            if global_occ:

                for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != ("*"))):
                    dynarate_list_data.remove(dynarate_list)

            else:

                for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype != zimkateg.kurzbez)):
                    dynarate_list_data.remove(dynarate_list)


            for dynarate_list in query(dynarate_list_data):

                bratecode_obj_list = {}
                bratecode = Ratecode()
                arrangement = Arrangement()
                for bratecode.code, bratecode.zikatnr, bratecode.argtnr, bratecode.erwachs, bratecode.kind1, bratecode.marknr, bratecode.char1, bratecode._recid, arrangement.argtnr, arrangement._recid in db_session.query(Bratecode.code, Bratecode.zikatnr, Bratecode.argtnr, Bratecode.erwachs, Bratecode.kind1, Bratecode.marknr, Bratecode.char1, Bratecode._recid, Arrangement.argtnr, Arrangement._recid).join(Arrangement,(Arrangement.argtnr == Bratecode.argtnr)).filter(
                         (Bratecode.code == dynarate_list.rcode) & (Bratecode.zikatnr == i_zikatnr) & (Bratecode.erwachs == adult) & (Bratecode.kind1 == child) & (not_ (Bratecode.startperiode > todate)) & (not_ (Bratecode.endperiode < frdate))).order_by(Bratecode.wday, Arrangement.arrangement, Bratecode.erwachs, Bratecode.startperiode).all():
                    if bratecode_obj_list.get(bratecode._recid):
                        continue
                    else:
                        bratecode_obj_list[bratecode._recid] = True

                    buff_rlist = query(buff_rlist_data, filters=(lambda buff_rlist: buff_rlist.rateCode == guest_pr.code and buff_rlist.room_type == bratecode.zikatnr and buff_rlist.argtno == bratecode.argtnr and buff_rlist.adult == bratecode.erwachs and buff_rlist.child == bratecode.kind1 and buff_rlist.marknr == bratecode.marknr), first=True)
                    do_it = not None != buff_rlist

                    if do_it:

                        rate_list = query(rate_list_data, filters=(lambda rate_list: rate_list.rateCode == guest_pr.code and rate_list.room_type == i_zikatnr and rate_list.argtno == bratecode.argtnr and rate_list.adult == bratecode.erwachs and rate_list.child == bratecode.kind1), first=True)

                        if not rate_list:

                            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, bqueasy.number1)]})
                            rate_list = Rate_list()
                            rate_list_data.append(rate_list)

                            i_counter = i_counter + 1
                            rate_list.i_counter = i_counter
                            rate_list.ratecode = guest_pr.code
                            rate_list.dynaflag = True
                            rate_list.room_type = i_zikatnr
                            rate_list.argtno = bratecode.argtnr
                            rate_list.adult = bratecode.erwachs
                            rate_list.child = bratecode.kind1
                            rate_list.marknr = bratecode.marknr
                            rate_list.currency = bqueasy.number1
                            rate_list.minstay = bqueasy.number2
                            rate_list.maxstay = bqueasy.deci2
                            rate_list.minadvance = bqueasy.number3
                            rate_list.maxadvance = bqueasy.deci3
                            rate_list.frdate = bqueasy.date1
                            rate_list.todate = bqueasy.date2
                            rate_list.wabkurz = waehrung.wabkurz

                            if bqueasy.char3 != "":

                                segment = get_cache (Segment, {"bezeich": [(eq, bqueasy.char3)]})

                                if segment:
                                    rate_list.segmentcode = to_string(segment.segmentcode) + " " + segment.bezeich

                            if bqueasy.date1 != None and bqueasy.date2 != None and ((ci_date < bqueasy.date1) or (ci_date > bqueasy.date2)):
                                rate_list.expired = True

            if zimkateg.typ > 0:

                for rate_list in query(rate_list_data):

                    created_list = query(created_list_data, filters=(lambda created_list: created_list.rateCode == rate_list.rateCode and created_list.marknr == rate_list.marknr and created_list.rmcateg == zimkateg.typ and created_list.argtno == rate_list.argtno), first=True)

                    if created_list:
                        rate_created = True
                        rate_list.i_counter = - rate_list.i_counter


                        for curr_i in range(1,300 + 1) :
                            rate_list.rmrate[curr_i - 1] = created_list.rmRate[curr_i - 1]
                            rate_list.statcode[curr_i - 1] = created_list.statcode[curr_i - 1]


            if calc_rm :
                rate_created = False

            rate_list = query(rate_list_data, first=True)

            if rate_list and not rate_created:
                curr_i = 0
                for curr_date in (frdate - todate).days :
                    curr_i = curr_i + 1
                    w_day = wd_array[get_weekday(curr_date) - 1]


                    occ_rooms = get_output(calculate_occupied_roomsbl(curr_date, zimkateg.kurzbez, global_occ))
                    occ_room_array[curr_i - 1] = occ_rooms

                    dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == w_day and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and (dynarate_list.fr_room <= occ_rooms) and (dynarate_list.to_room >= occ_rooms)), first=True)

                    if not dynarate_list:

                        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and (dynarate_list.fr_room <= occ_rooms) and (dynarate_list.to_room >= occ_rooms)), first=True)

                    if dynarate_list:
                        mapcode = dynarate_list.strip()

                        if not global_occ:

                            queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, guest_pr.code)],"char2": [(eq, mapcode)],"number1": [(eq, i_zikatnr)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, curr_date)]})
                        else:

                            queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, guest_pr.code)],"char2": [(eq, mapcode)],"number1": [(eq, 0)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, curr_date)]})

                        if queasy:
                            mapcode = queasy.char3

                        for rate_list in query(rate_list_data, filters=(lambda rate_list: rate_list.dynaflag  and rate_list.rateCode == guest_pr.code)):
                            rate_found = check_allotment(bqueasy.char1, mapcode, curr_date)

                            if rate_found:
                                rate_found, rm_rate, restricted, kback_flag = get_output(ratecode_rate(False, False, 0, 1, ("!" + mapcode), ci_date, curr_date, curr_date, curr_date, rate_list.marknr, rate_list.argtno, i_zikatnr, rate_list.adult, rate_list.child, 0, 0, rate_list.currency))

                            if rate_found:
                                rate_list.rmrate[curr_i - 1] = rm_rate
                                rate_list.statcode[curr_i - 1] = mapcode


                            else:
                                rate_list.rmrate[curr_i - 1] = -0.001

                                if dynarate_list.w_day != 0:
                                    not_found_flag = True


                curr_i = 0

                if not_found_flag:
                    for curr_date in (frdate - todate).days :
                        curr_i = curr_i + 1
                        occ_rooms = occ_room_array[curr_i - 1]

                        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.w_day == 0 and dynarate_list.days1 == 0 and dynarate_list.days2 == 0 and (dynarate_list.fr_room <= occ_rooms) and (dynarate_list.to_room >= occ_rooms)), first=True)

                        if dynarate_list:
                            mapcode = dynarate_list.rcode

                            if not global_occ:

                                queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, guest_pr.code)],"char2": [(eq, mapcode)],"number1": [(eq, i_zikatnr)],"deci1": [(eq, 0)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, curr_date)]})
                            else:

                                queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, guest_pr.code)],"char2": [(eq, mapcode)],"number1": [(eq, 0)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, curr_date)]})

                            if queasy:
                                mapcode = queasy.char3

                            for rate_list in query(rate_list_data, filters=(lambda rate_list: rate_list.dynaflag  and rate_list.rateCode == guest_pr.code)):

                                if rate_list.rmRate[curr_i - 1] == 0:
                                    rate_found, rm_rate, restricted, kback_flag = get_output(ratecode_rate(False, False, 0, 1, ("!" + mapcode), ci_date, curr_date, curr_date, curr_date, rate_list.marknr, rate_list.argtno, i_zikatnr, rate_list.adult, rate_list.child, 0, 0, rate_list.currency))

                                    if rate_found:
                                        rate_list.rmrate[curr_i - 1] = rm_rate
                                        rate_list.statcode[curr_i - 1] = mapcode

    for rate_list in query(rate_list_data, filters=(lambda rate_list: rate_list.minadvance > 0), sort_by=[("minadvance",True)]):

        selected_ratelist = query(selected_ratelist_data, filters=(lambda selected_ratelist: selected_ratelist.marknr == rate_list.marknr and selected_ratelist.argtno == rate_list.argtno and selected_ratelist.adult == rate_list.adult and selected_ratelist.child == rate_list.child and selected_ratelist.minstay == rate_list.minstay and selected_ratelist.maxstay == rate_list.maxstay), first=True)

        if not selected_ratelist:
            selected_ratelist = Selected_ratelist()
            selected_ratelist_data.append(selected_ratelist)

            selected_ratelist.marknr = rate_list.marknr
            selected_ratelist.argtno = rate_list.argtno
            selected_ratelist.adult = rate_list.adult
            selected_ratelist.child = rate_list.child
            selected_ratelist.minstay = rate_list.minstay
            selected_ratelist.maxstay = rate_list.maxstay


        else:
            rate_list_data.remove(rate_list)

    if zimkateg.typ > 0:

        for rate_list in query(rate_list_data, filters=(lambda rate_list: rate_list.dynaflag)):

            if rate_list.i_counter < 0:
                rate_list.i_counter = - rate_list.i_counter
            else:
                created_list = Created_list()
                created_list_data.append(created_list)

                buffer_copy(rate_list, created_list)
                created_list.rmcateg = zimkateg.typ


    return generate_output()