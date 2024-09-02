from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from sqlalchemy import func
from functions.calculate_occupied_roomsbl import calculate_occupied_roomsbl
from functions.ratecode_rate import ratecode_rate
from models import Reslin_queasy, Queasy, Zimkateg, Res_line, Ratecode

def res_dyna_rmrate(resno:int, reslinno:int, markno:int, adult:int, child1:int, child2:int, wahrno:int, argtnr:int, rmtype:str, ankunft:date, abreise:date, prcode:str, user_init:str, res_exrate:decimal, ebdisc_flag:bool, kbdisc_flag:bool):
    created = False
    zipreis = 0
    datum:date = None
    to_date:date = None
    ci_date:date = None
    rate_found:bool = False
    kback_flag:bool = False
    restricted_rate:bool = False
    rm_rate:decimal = 0
    mapcode:str = ""
    w_day:int = 0
    global_occ:bool = False
    i_param439:int = 0
    arrival_date:date = None
    wd_array:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    reslin_queasy = queasy = zimkateg = res_line = ratecode = None

    dynarate_list = r_qsy = n_qsy = dybuff = None

    dynarate_list_list, Dynarate_list = create_model("Dynarate_list", {"s_recid":int, "counter":int, "w_day":int, "rmtype":str, "fr_room":int, "to_room":int, "days1":int, "days2":int, "rcode":str})
    r_qsy_list, R_qsy = create_model_like(Reslin_queasy)
    n_qsy_list, N_qsy = create_model_like(Reslin_queasy)

    Dybuff = Dynarate_list
    dybuff_list = dynarate_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal created, zipreis, datum, to_date, ci_date, rate_found, kback_flag, restricted_rate, rm_rate, mapcode, w_day, global_occ, i_param439, arrival_date, wd_array, reslin_queasy, queasy, zimkateg, res_line, ratecode
        nonlocal dybuff


        nonlocal dynarate_list, r_qsy, n_qsy, dybuff
        nonlocal dynarate_list_list, r_qsy_list, n_qsy_list
        return {"created": created, "zipreis": zipreis}

    def create_dynamic_fixrates():

        nonlocal created, zipreis, datum, to_date, ci_date, rate_found, kback_flag, restricted_rate, rm_rate, mapcode, w_day, global_occ, i_param439, arrival_date, wd_array, reslin_queasy, queasy, zimkateg, res_line, ratecode
        nonlocal dybuff


        nonlocal dynarate_list, r_qsy, n_qsy, dybuff
        nonlocal dynarate_list_list, r_qsy_list, n_qsy_list

        for r_qsy in query(r_qsy_list):
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            buffer_copy(r_qsy, reslin_queasy)
            created = True

    def create_buffers(datum:date):

        nonlocal created, zipreis, datum, to_date, ci_date, rate_found, kback_flag, restricted_rate, rm_rate, mapcode, w_day, global_occ, i_param439, arrival_date, wd_array, reslin_queasy, queasy, zimkateg, res_line, ratecode
        nonlocal dybuff


        nonlocal dynarate_list, r_qsy, n_qsy, dybuff
        nonlocal dynarate_list_list, r_qsy_list, n_qsy_list

        use_it:bool = False
        tokcounter:int = 0
        iftask:str = ""
        mestoken:str = ""
        mesvalue:str = ""
        occ_rooms:int = 0
        Dybuff = Dynarate_list
        w_day = wd_array[get_weekday(datum) - 1]


        dynaRate_list_list.clear()

        for ratecode in db_session.query(Ratecode).filter(
                (func.lower(Ratecode.code) == (prcode).lower())).all():
            dynarate_list = Dynarate_list()
            dynarate_list_list.append(dynarate_list)

            iftask = ratecode.char1[4]
            for tokcounter in range(1,num_entries(iftask, ";") - 1 + 1) :
                mestoken = substring(entry(tokcounter - 1, iftask, ";") , 0, 2)
                mesvalue = substring(entry(tokcounter - 1, iftask, ";") , 2)

                if mestoken == "CN":
                    dynarate_list.counter = to_int(mesvalue)
                elif mestoken == "RT":
                    dynaRate_list.rmtype = mesvalue
                elif mestoken == "WD":
                    dynarate_list.w_day = to_int(mesvalue)
                elif mestoken == "FR":
                    dynaRate_list.fr_room = to_int(mesvalue)
                elif mestoken == "TR":
                    dynaRate_list.to_room = to_int(mesvalue)
                elif mestoken == "D1":
                    dynaRate_list.days1 = to_int(mesvalue)
                elif mestoken == "D2":
                    dynaRate_list.days2 = to_int(mesvalue)
                elif mestoken == "RC":
                    dynaRate_list.rCode = mesvalue

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (Queasy.char1 == prcode)).first()

    if not queasy:

        return generate_output()

    if not queasy.logi2:

        return generate_output()

    if ankunft == abreise:
        to_date = ankunft
    else:
        to_date = abreise - 1
    arrival_date = ankunft

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.kurzbez == rmtype)).first()
    ci_date = get_output(htpdate(87))
    i_param439 = get_output(htpint(439))

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

    if res_line and res_line.active_flag == 1:
        arrival_date = ci_date
    for datum in range(ankunft,to_date + 1) :
        create_buffers(datum)
    create_dynamic_fixrates()

    dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynarate_list.rmtype.lower()  == "*"), first=True)
    global_occ = None != dynarate_list and i_param439 == 1

    if global_occ:

        for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list :dynarate_list.rmtype.lower()  != "*")):
            dynarate_list_list.remove(dynarate_list)

    else:

        for dynarate_list in query(dynarate_list_list, filters=(lambda dynarate_list :dynarate_list.rmtype != rmtype)):
            dynarate_list_list.remove(dynarate_list)

    occ_rooms = get_output(calculate_occupied_roomsbl(datum, rmtype, global_occ))

    if occ_rooms == 0:

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.fr_room == 0), first=True)

        if not dynaRate_list:
            occ_rooms = 1

    for dynarate_list in query(dynarate_list_list):
        use_it = True

        if dynaRate_list.days1 != 0 and (ankunft - ci_date) <= dynaRate_list.days1:
            use_it = False

        if use_it and dynaRate_list.days2 != 0 and (ankunft - ci_date) >= dynaRate_list.days2:
            use_it = False

        if use_it:
            use_it = (dynaRate_list.fr_room <= occ_rooms) and (dynaRate_list.to_room >= occ_rooms)

        if not use_it:
            dynarate_list_list.remove(dynarate_list)
        else:

            if (dynaRate_list.days1 != 0) or (dynaRate_list.days2 != 0):

                for dybuff in query(dybuff_list, filters=(lambda dybuff :dybuff.days1 == 0 and dybuff.days2 == 0 and (dybuff.rmtype == dynaRate_list.rmtype) and (dybuff.fr_room <= occ_rooms) and (dybuff.to_room >= occ_rooms))):
                    dybuff_list.remove(dybuff)


            if dynaRate_list.w_day > 0:

                for dybuff in query(dybuff_list, filters=(lambda dybuff :dybuff.w_day == 0 and (dybuff.rmtype == dynaRate_list.rmtype) and (dybuff.fr_room <= occ_rooms) and (dybuff.to_room >= occ_rooms))):
                    dybuff_list.remove(dybuff)


    dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.w_day == w_day and dynaRate_list.days1 != 0), first=True)

    if not dynaRate_list:

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.w_day == w_day and dynaRate_list.days2 != 0), first=True)

    if not dynaRate_list:

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.w_day == w_day), first=True)

    if not dynaRate_list:

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.w_day == 0 and dynaRate_list.days1 != 0), first=True)

    if not dynaRate_list:

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.w_day == 0 and dynaRate_list.days2 != 0), first=True)

    if not dynaRate_list:

        dynarate_list = query(dynarate_list_list, filters=(lambda dynarate_list :dynaRate_list.w_day == 0), first=True)

    if dynaRate_list:
        mapcode = dynaRate_list.rcode

        if global_occ:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 145) &  (func.lower(Queasy.char1) == (prcode).lower()) &  (func.lower(Queasy.char2) == (mapcode).lower()) &  (Queasy.number1 == 0) &  (Queasy.deci1 == dynarate_list.w_day) &  (Queasy.deci2 == dynarate_list.counter) &  (Queasy.date1 == datum)).first()
        else:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 145) &  (func.lower(Queasy.char1) == (prcode).lower()) &  (func.lower(Queasy.char2) == (mapcode).lower()) &  (Queasy.number1 == zimkateg.zikatnr) &  (Queasy.deci1 == dynarate_list.w_day) &  (Queasy.deci2 == dynarate_list.counter) &  (Queasy.date1 == datum)).first()

        if queasy:
            mapcode = queasy.char3
        rate_found, rm_rate, restricted_rate, kback_flag = get_output(ratecode_rate(ebdisc_flag, kbdisc_flag, resno, reslinno, ("!" + mapcode), ci_date, datum, ankunft, abreise, markno, argtnr, zimkateg.zikatnr, adult, child1, child2, res_exrate, wahrno))
        r_qsy = R_qsy()
        r_qsy_list.append(r_qsy)

        r_qsy.key = "arrangement"
        r_qsy.resnr = resno
        r_qsy.reslinnr = reslinno
        r_qsy.date1 = datum
        r_qsy.date2 = datum
        r_qsy.deci1 = rm_rate
        r_qsy.char2 = mapcode
        r_qsy.char3 = user_init

        if datum == arrival_date:
            zipreis = rm_rate

    return generate_output()