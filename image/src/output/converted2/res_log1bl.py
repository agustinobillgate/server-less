#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimkateg, Reslin_queasy, Res_line, Reservation

def res_log1bl(pvilanguage:int, from_date:date, mi_inhouse:bool):

    prepare_cache ([Zimkateg, Reslin_queasy, Res_line, Reservation])

    res_log1_list = []
    lvcarea:string = "res-log1"
    zimkateg = reslin_queasy = res_line = reservation = None

    res_log1 = None

    res_log1_list, Res_log1 = create_model("Res_log1", {"flag":int, "resnr":int, "name":string, "ankunft1":date, "ankunft2":date, "abreise1":date, "abreise2":date, "qty1":int, "qty2":int, "adult1":int, "adult2":int, "child1":int, "child2":int, "comp1":int, "comp2":int, "rmcat1":string, "rmcat2":string, "zinr1":string, "zinr2":string, "argt1":string, "argt2":string, "rate1":Decimal, "rate2":Decimal, "fixrate1":string, "fixrate2":string, "name1":string, "name2":string, "id1":string, "id2":string, "date1":date, "date2":date, "zeit":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_log1_list, lvcarea, zimkateg, reslin_queasy, res_line, reservation
        nonlocal pvilanguage, from_date, mi_inhouse


        nonlocal res_log1
        nonlocal res_log1_list

        return {"res-log1": res_log1_list}

    def create_list():

        nonlocal res_log1_list, lvcarea, zimkateg, reslin_queasy, res_line, reservation
        nonlocal pvilanguage, from_date, mi_inhouse


        nonlocal res_log1
        nonlocal res_log1_list

        zimkateg1 = None
        do_it:bool = False
        Zimkateg1 =  create_buffer("Zimkateg1",Zimkateg)
        res_log1_list.clear()

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.betriebsnr == 0) & (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.number1 == 0) & (Reslin_queasy.date1 == None) & (Reslin_queasy.char3 > "") & (Reslin_queasy.deci1 == 0) & (Reslin_queasy.logi1 == False) & (Reslin_queasy.date2 == from_date)).order_by(Reslin_queasy._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, to_int(trim(substring(reslin_queasy.char3, 50, 3))))]})

            zimkateg1 = get_cache (Zimkateg, {"zikatnr": [(eq, to_int(trim(substring(reslin_queasy.char3, 53, 3))))]})

            res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})

            reservation = get_cache (Reservation, {"resnr": [(eq, reslin_queasy.resnr)]})
            do_it = True

            if mi_inhouse and res_line and res_line.active_flag != 1:
                do_it = False

            if do_it:
                res_log1 = Res_log1()
                res_log1_list.append(res_log1)

                res_log1.resnr = reslin_queasy.resnr

                if reservation:
                    res_log1.name = reservation.name

                if matches(reslin_queasy.char3,r"*;*"):
                    res_log1.ankunft1 = date_mdy(entry(0, reslin_queasy.char3, ";"))
                    res_log1.ankunft2 = date_mdy(entry(1, reslin_queasy.char3, ";"))
                    res_log1.abreise1 = date_mdy(entry(2, reslin_queasy.char3, ";"))
                    res_log1.abreise2 = date_mdy(entry(3, reslin_queasy.char3, ";"))
                    res_log1.qty1 = to_int(entry(4, reslin_queasy.char3, ";"))
                    res_log1.qty2 = to_int(entry(5, reslin_queasy.char3, ";"))
                    res_log1.adult1 = to_int(entry(6, reslin_queasy.char3, ";"))
                    res_log1.adult2 = to_int(entry(7, reslin_queasy.char3, ";"))
                    res_log1.child1 = to_int(entry(8, reslin_queasy.char3, ";"))
                    res_log1.child2 = to_int(entry(9, reslin_queasy.char3, ";"))
                    res_log1.comp1 = to_int(entry(10, reslin_queasy.char3, ";"))
                    res_log1.comp2 = to_int(entry(11, reslin_queasy.char3, ";"))
                    res_log1.zinr1 = entry(14, reslin_queasy.char3, ";")
                    res_log1.zinr2 = entry(15, reslin_queasy.char3, ";")
                    res_log1.argt1 = entry(16, reslin_queasy.char3, ";")
                    res_log1.argt2 = entry(17, reslin_queasy.char3, ";")
                    res_log1.rate1 =  to_decimal(to_decimal(entry(18 , reslin_queasy.char3 , ";")) )
                    res_log1.rate2 =  to_decimal(to_decimal(entry(19 , reslin_queasy.char3 , ";")) )
                    res_log1.id1 = entry(20, reslin_queasy.char3, ";")
                    res_log1.id2 = entry(21, reslin_queasy.char3, ";")
                    res_log1.name1 = entry(24, reslin_queasy.char3, ";")
                    res_log1.name2 = entry(25, reslin_queasy.char3, ";")
                    res_log1.fixrate1 = entry(26, reslin_queasy.char3, ";")
                    res_log1.fixrate2 = entry(27, reslin_queasy.char3, ";")

                    if trim(entry(22, reslin_queasy.char3, ";")) == "":
                        res_log1.date1 = None
                    else:
                        res_log1.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))

                    if trim(entry(23, reslin_queasy.char3, ";")) == "":
                        res_log1.date2 = None
                    else:
                        res_log1.date2 = date_mdy(entry(23, reslin_queasy.char3, ";"))

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, to_int(entry(12, reslin_queasy.char3, ";")))]})

                    zimkateg1 = get_cache (Zimkateg, {"zikatnr": [(eq, to_int(entry(13, reslin_queasy.char3, ";")))]})

                    if zimkateg:
                        res_log1.rmcat1 = to_string(zimkateg.kurzbez, "x(6)")

                    if zimkateg1:
                        res_log1.rmcat2 = to_string(zimkateg1.kurzbez, "x(6)")
                else:

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, to_int(trim(substring(reslin_queasy.char3, 50, 3))))]})

                    zimkateg1 = get_cache (Zimkateg, {"zikatnr": [(eq, to_int(trim(substring(reslin_queasy.char3, 53, 3))))]})
                    res_log1.ankunft1 = date_mdy(substring(reslin_queasy.char3, 0, 8))
                    res_log1.ankunft2 = date_mdy(substring(reslin_queasy.char3, 8, 8))
                    res_log1.abreise1 = date_mdy(substring(reslin_queasy.char3, 16, 8))
                    res_log1.abreise2 = date_mdy(substring(reslin_queasy.char3, 24, 8))
                    res_log1.qty1 = to_int(substring(reslin_queasy.char3, 32, 3))
                    res_log1.qty2 = to_int(substring(reslin_queasy.char3, 35, 3))
                    res_log1.adult1 = to_int(substring(reslin_queasy.char3, 38, 2))
                    res_log1.adult2 = to_int(substring(reslin_queasy.char3, 40, 2))
                    res_log1.child1 = to_int(substring(reslin_queasy.char3, 42, 2))
                    res_log1.child2 = to_int(substring(reslin_queasy.char3, 44, 2))
                    res_log1.comp1 = to_int(substring(reslin_queasy.char3, 46, 2))
                    res_log1.comp2 = to_int(substring(reslin_queasy.char3, 48, 2))

                    if zimkateg:
                        res_log1.rmcat1 = to_string(zimkateg.kurzbez, "x(6)")

                    if zimkateg1:
                        res_log1.rmcat2 = to_string(zimkateg1.kurzbez, "x(6)")
                    res_log1.zinr1 = substring(reslin_queasy.char3, 56, 4)
                    res_log1.zinr2 = substring(reslin_queasy.char3, 60, 4)
                    res_log1.argt1 = substring(reslin_queasy.char3, 64, 5)
                    res_log1.argt2 = substring(reslin_queasy.char3, 69, 5)
                    res_log1.rate1 = to_decimal(substring(reslin_queasy.char3, 74, 12))
                    res_log1.rate2 = to_decimal(substring(reslin_queasy.char3, 86, 12))
                    res_log1.id1 = substring(reslin_queasy.char3, 98, 2)
                    res_log1.id2 = substring(reslin_queasy.char3, 100, 2)
                    res_log1.date1 = date_mdy(substring(reslin_queasy.char3, 102, 8))

                    if substring(reslin_queasy.char3, 110, 8) == " ":
                        res_log1.date2 = None
                    else:
                        res_log1.date2 = date_mdy(substring(reslin_queasy.char3, 110, 8))

                    if length(reslin_queasy.char3) > 120:
                        res_log1.name1 = substring(reslin_queasy.char3, 118, 16)
                        res_log1.name2 = substring(reslin_queasy.char3, 134, 16)

                    if length(reslin_queasy.char3) > 151:
                        res_log1.fixrate1 = substring(reslin_queasy.char3, 150, 3)
                        res_log1.fixrate2 = substring(reslin_queasy.char3, 153, 3)
                res_log1.zeit = reslin_queasy.number2

    create_list()

    return generate_output()