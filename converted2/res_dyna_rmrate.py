#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from functions.calculate_occupied_roomsbl import calculate_occupied_roomsbl
from functions.ratecode_rate import ratecode_rate
from models import Reslin_queasy, Queasy, Zimkateg, Res_line, Ratecode

def res_dyna_rmrate(resno:int, reslinno:int, markno:int, adult:int, child1:int, child2:int, wahrno:int, argtnr:int, rmtype:string, ankunft:date, abreise:date, prcode:string, user_init:string, res_exrate:Decimal, ebdisc_flag:bool, kbdisc_flag:bool):

    prepare_cache ([Queasy, Zimkateg, Res_line, Ratecode])

    created = False
    zipreis = None
    datum:date = None
    to_date:date = None
    ci_date:date = None
    rate_found:bool = False
    kback_flag:bool = False
    restricted_rate:bool = False
    rm_rate:Decimal = to_decimal("0.0")
    mapcode:string = ""
    w_day:int = 0
    global_occ:bool = False
    i_param439:int = 0
    arrival_date:date = None
    wd_array:List[int] = [7, 1, 2, 3, 4, 5, 6, 7]
    reslin_queasy = queasy = zimkateg = res_line = ratecode = None

    dynarate_list = r_qsy = n_qsy = dybuff = None

    dynarate_list_data, Dynarate_list = create_model("Dynarate_list", {"s_recid":int, "counter":int, "w_day":int, "rmtype":string, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":string})
    r_qsy_data, R_qsy = create_model_like(Reslin_queasy)
    n_qsy_data, N_qsy = create_model_like(Reslin_queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, zipreis, datum, to_date, ci_date, rate_found, kback_flag, restricted_rate, rm_rate, mapcode, w_day, global_occ, i_param439, arrival_date, wd_array, reslin_queasy, queasy, zimkateg, res_line, ratecode
        nonlocal resno, reslinno, markno, adult, child1, child2, wahrno, argtnr, rmtype, ankunft, abreise, prcode, user_init, res_exrate, ebdisc_flag, kbdisc_flag


        nonlocal dynarate_list, r_qsy, n_qsy, dybuff
        nonlocal dynarate_list_data, r_qsy_data, n_qsy_data

        return {"created": created, "zipreis": zipreis}

    def create_dynamic_fixrates():

        nonlocal created, zipreis, datum, to_date, ci_date, rate_found, kback_flag, restricted_rate, rm_rate, mapcode, w_day, global_occ, i_param439, arrival_date, wd_array, reslin_queasy, queasy, zimkateg, res_line, ratecode
        nonlocal resno, reslinno, markno, adult, child1, child2, wahrno, argtnr, rmtype, ankunft, abreise, prcode, user_init, res_exrate, ebdisc_flag, kbdisc_flag


        nonlocal dynarate_list, r_qsy, n_qsy, dybuff
        nonlocal dynarate_list_data, r_qsy_data, n_qsy_data

        for r_qsy in query(r_qsy_data, sort_by=[("date1",False)]):
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            buffer_copy(r_qsy, reslin_queasy)
            created = True


    def create_buffers(datum:date):

        nonlocal created, zipreis, to_date, ci_date, rate_found, kback_flag, restricted_rate, rm_rate, mapcode, w_day, global_occ, i_param439, arrival_date, wd_array, reslin_queasy, queasy, zimkateg, res_line, ratecode
        nonlocal resno, reslinno, markno, adult, child1, child2, wahrno, argtnr, rmtype, ankunft, abreise, prcode, user_init, res_exrate, ebdisc_flag, kbdisc_flag


        nonlocal dynarate_list, r_qsy, n_qsy, dybuff
        nonlocal dynarate_list_data, r_qsy_data, n_qsy_data

        use_it:bool = False
        tokcounter:int = 0
        iftask:string = ""
        mestoken:string = ""
        mesvalue:string = ""
        occ_rooms:int = 0
        Dybuff = Dynarate_list
        dybuff_data = dynarate_list_data
        w_day = wd_array[get_weekday(datum) - 1]


        dynarate_list_data.clear()

        for ratecode in db_session.query(Ratecode).filter(
                 (Ratecode.code == (prcode).lower())).order_by(Ratecode._recid).all():
            dynarate_list = Dynarate_list()
            dynarate_list_data.append(dynarate_list)

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

        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  == ("*").lower()), first=True)
        global_occ = None != dynarate_list and i_param439 == 1

        if global_occ:

            for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype.lower()  != ("*").lower())):
                dynarate_list_data.remove(dynarate_list)

        else:

            for dynarate_list in query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.rmtype != rmtype)):
                dynarate_list_data.remove(dynarate_list)

        occ_rooms = get_output(calculate_occupied_roomsbl(datum, rmtype, global_occ))

        if occ_rooms == 0:

            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.fr_room == 0), first=True)

            if not dynarate_list:
                occ_rooms = 1

        for dynarate_list in query(dynarate_list_data, sort_by=[("w_day",True)]):
            use_it = True

            if dynarate_list.days1 != 0 and (ankunft - ci_date) <= dynarate_list.days1:
                use_it = False

            if use_it and dynarate_list.days2 != 0 and (ankunft - ci_date) >= dynarate_list.days2:
                use_it = False

            if use_it:
                use_it = (dynarate_list.fr_room <= occ_rooms) and (dynarate_list.to_room >= occ_rooms)

            if not use_it:
                dynarate_list_data.remove(dynarate_list)
            else:

                if (dynarate_list.days1 != 0) or (dynarate_list.days2 != 0):

                    for dybuff in query(dybuff_data, filters=(lambda dybuff: dybuff.days1 == 0 and dybuff.days2 == 0 and (dybuff.rmtype == dynarate_list.rmtype) and (dybuff.fr_room <= occ_rooms) and (dybuff.to_room >= occ_rooms))):
                        dybuff_data.remove(dybuff)


                if dynarate_list.w_day > 0:

                    for dybuff in query(dybuff_data, filters=(lambda dybuff: dybuff.w_day == 0 and (dybuff.rmtype == dynarate_list.rmtype) and (dybuff.fr_room <= occ_rooms) and (dybuff.to_room >= occ_rooms))):
                        dybuff_data.remove(dybuff)


        dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.w_day == w_day and dynarate_list.days1 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.w_day == w_day and dynarate_list.days2 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.w_day == w_day), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.w_day == 0 and dynarate_list.days1 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.w_day == 0 and dynarate_list.days2 != 0), first=True)

        if not dynarate_list:

            dynarate_list = query(dynarate_list_data, filters=(lambda dynarate_list: dynarate_list.dynarate_list.w_day == 0), first=True)

        if dynarate_list:
            mapcode = dynarate_list.rcode

            if global_occ:

                queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, prcode)],"char2": [(eq, mapcode)],"number1": [(eq, 0)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, datum)]})
            else:

                queasy = get_cache (Queasy, {"key": [(eq, 145)],"char1": [(eq, prcode)],"char2": [(eq, mapcode)],"number1": [(eq, zimkateg.zikatnr)],"deci1": [(eq, dynarate_list.w_day)],"deci2": [(eq, dynarate_list.counter)],"date1": [(eq, datum)]})

            if queasy:
                mapcode = queasy.char3
            rate_found, rm_rate, restricted_rate, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resno, reslinno, ("!" + mapcode), ci_date, datum, ankunft, abreise, markno, argtnr, zimkateg.zikatnr, adult, child1, child2, res_exrate, wahrno))
            r_qsy = R_qsy()
            r_qsy_data.append(r_qsy)

            r_qsy.key = "arrangement"
            r_qsy.resnr = resno
            r_qsy.reslinnr = reslinno
            r_qsy.date1 = datum
            r_qsy.date2 = datum
            r_qsy.deci1 =  to_decimal(rm_rate)
            r_qsy.char2 = mapcode
            r_qsy.char3 = user_init

            if datum == arrival_date:
                zipreis =  to_decimal(rm_rate)


    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, prcode)]})

    if not queasy:

        return generate_output()

    if not queasy.logi2:

        return generate_output()

    if ankunft == abreise:
        to_date = ankunft
    else:
        to_date = abreise - timedelta(days=1)
    arrival_date = ankunft

    zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, rmtype)]})
    ci_date = get_output(htpdate(87))
    i_param439 = get_output(htpint(439))

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

    if res_line and res_line.active_flag == 1:
        arrival_date = ci_date
    for datum in date_range(ankunft,to_date) :
        create_buffers(datum)
    create_dynamic_fixrates()

    return generate_output()