#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Reslin_queasy, Guest, Res_line, Zimkateg

def chgrmrate_report_1bl(fdate:date, tdate:date, resno:int):

    prepare_cache ([Reslin_queasy, Guest, Res_line, Zimkateg])

    res_log_data = []
    akuntf:string = ""
    abreise:string = ""
    date1:string = ""
    date2:date = None
    loopi:int = 0
    str:string = ""
    reslin_queasy = guest = res_line = zimkateg = None

    res_log = breslin = tguest = None

    res_log_data, Res_log = create_model("Res_log", {"his_recid":int, "ankunft1":date, "abreise1":date, "qty1":int, "qty2":int, "adult1":int, "adult2":int, "child1":int, "child2":int, "comp1":int, "comp2":int, "rmcat1":string, "rmcat2":string, "zinr1":string, "zinr2":string, "argt1":string, "argt2":string, "rate1":Decimal, "rate2":Decimal, "fixrate1":string, "fixrate2":string, "name1":string, "name2":string, "id1":string, "id2":string, "date1":date, "date2":date, "zeit":int, "resnr":int, "reslinnr":int, "resstatus":int, "room_cat":string, "rate_code":string, "night_stay":int, "variance":Decimal, "rsv_name":string})

    Breslin = create_buffer("Breslin",Reslin_queasy)
    Tguest = create_buffer("Tguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_log_data, akuntf, abreise, date1, date2, loopi, str, reslin_queasy, guest, res_line, zimkateg
        nonlocal fdate, tdate, resno
        nonlocal breslin, tguest


        nonlocal res_log, breslin, tguest
        nonlocal res_log_data

        return {"res-log": res_log_data}

    def create_list():

        nonlocal res_log_data, akuntf, abreise, date1, date2, loopi, str, reslin_queasy, guest, res_line, zimkateg
        nonlocal fdate, tdate, resno
        nonlocal breslin, tguest


        nonlocal res_log, breslin, tguest
        nonlocal res_log_data

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.date2 <= tdate)).order_by(Reslin_queasy._recid).all():

            if matches(reslin_queasy.char3,r"*;*") and to_decimal(entry(18, reslin_queasy.char3, ";")) != to_decimal(entry(19, reslin_queasy.char3, ";")):
                res_log = Res_log()
                res_log_data.append(res_log)

                res_log.resnr = reslin_queasy.resnr
                res_log.reslinnr = reslin_queasy.reslinnr
                res_log.ankunft1 = date_mdy(to_int(entry(1, entry(0, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(0, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(0, reslin_queasy.char3, ";") , "/"))))
                res_log.abreise1 = date_mdy(to_int(entry(1, entry(2, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(2, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(2, reslin_queasy.char3, ";") , "/"))))
                res_log.zinr1 = entry(14, reslin_queasy.char3, ";")
                res_log.rate1 =  to_decimal(to_decimal(entry(18 , reslin_queasy.char3 , ";")) )
                res_log.rate2 =  to_decimal(to_decimal(entry(19 , reslin_queasy.char3 , ";")) )
                res_log.name1 = entry(24, reslin_queasy.char3, ";")
                res_log.id1 = entry(20, reslin_queasy.char3, ";")
                res_log.id2 = entry(21, reslin_queasy.char3, ";")
                res_log.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))
                res_log.zeit = number2
                res_log.date1 = reslin_queasy.date2
                res_log.variance =  to_decimal(res_log.rate1) - to_decimal(res_log.rate2)
                res_log.night_stay = (res_log.abreise1 - res_log.ankunft1).days

                res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})

                if res_line:
                    res_log.resstatus = res_line.resstatus

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                    if zimkateg:
                        res_log.room_cat = zimkateg.kurzbez


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            res_log.rate_code = substring(str, 6)

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest:
                        res_log.rsv_name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma


                    else:
                        res_log.rsv_name = ""

            elif matches(to_string(entry(24, reslin_queasy.char3, ";")),r"*CHG Fixrate TO*"):

                breslin = db_session.query(Breslin).filter(
                         (Breslin.key == ("ResChanges").lower()) & (Breslin.resnr == reslin_queasy.resnr) & (Breslin.reslinnr == reslin_queasy.reslinnr) & (Breslin.date2 == reslin_queasy.date2) & (matches(to_string(entry(24, Breslin.char3, ";")),"*CHG Fixrate FR*")) & (Breslin.number2 == reslin_queasy.number2)).first()

                if breslin and to_decimal(entry(1, entry(25, reslin_queasy.char3, ";") , "-")) != to_decimal(entry(1, entry(25, breslin.char3, ";") , "-")):
                    res_log = Res_log()
                    res_log_data.append(res_log)

                    res_log.resnr = reslin_queasy.resnr
                    res_log.reslinnr = reslin_queasy.reslinnr
                    res_log.ankunft1 = date_mdy(to_int(entry(1, entry(0, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(0, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(0, reslin_queasy.char3, ";") , "/"))))
                    res_log.abreise1 = date_mdy(to_int(entry(1, entry(2, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(2, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(2, reslin_queasy.char3, ";") , "/"))))
                    res_log.zinr1 = entry(14, reslin_queasy.char3, ";")
                    res_log.rate1 =  to_decimal(to_decimal(entry(1 , entry(25 , breslin.char3 , ";") , "-")) )
                    res_log.rate2 =  to_decimal(to_decimal(entry(1 , entry(25 , reslin_queasy.char3 , ";") , "-")) )
                    res_log.id1 = entry(20, reslin_queasy.char3, ";")
                    res_log.id2 = entry(21, reslin_queasy.char3, ";")
                    res_log.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))
                    res_log.zeit = reslin_queasy.number2
                    res_log.date1 = reslin_queasy.date2
                    res_log.variance =  to_decimal(res_log.rate1) - to_decimal(res_log.rate2)
                    res_log.night_stay = (res_log.abreise1 - res_log.ankunft1).days

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if guest:
                            res_log.name1 = guest.name


                        res_log.resstatus = res_line.resstatus

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            res_log.room_cat = zimkateg.kurzbez


                        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                res_log.rate_code = substring(str, 6)

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if tguest:
                            res_log.rsv_name = tguest.name + ", " + tguest.vorname1 + " " + tguest.anrede1 + tguest.anredefirma


                        else:
                            res_log.rsv_name = ""


    def create_list1():

        nonlocal res_log_data, akuntf, abreise, date1, date2, loopi, str, reslin_queasy, guest, res_line, zimkateg
        nonlocal fdate, tdate, resno
        nonlocal breslin, tguest


        nonlocal res_log, breslin, tguest
        nonlocal res_log_data

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.date2 >= fdate) & (Reslin_queasy.date2 <= tdate) & (Reslin_queasy.resnr == resno)).order_by(Reslin_queasy._recid).all():

            if matches(reslin_queasy.char3,r"*;*") and to_decimal(entry(18, reslin_queasy.char3, ";")) != to_decimal(entry(19, reslin_queasy.char3, ";")):
                res_log = Res_log()
                res_log_data.append(res_log)

                res_log.resnr = reslin_queasy.resnr
                res_log.reslinnr = reslin_queasy.reslinnr
                res_log.ankunft1 = date_mdy(to_int(entry(1, entry(0, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(0, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(0, reslin_queasy.char3, ";") , "/"))))
                res_log.abreise1 = date_mdy(to_int(entry(1, entry(2, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(2, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(2, reslin_queasy.char3, ";") , "/"))))
                res_log.zinr1 = entry(14, reslin_queasy.char3, ";")
                res_log.rate1 =  to_decimal(to_decimal(entry(18 , reslin_queasy.char3 , ";")) )
                res_log.rate2 =  to_decimal(to_decimal(entry(19 , reslin_queasy.char3 , ";")) )
                res_log.name1 = entry(24, reslin_queasy.char3, ";")
                res_log.id1 = entry(20, reslin_queasy.char3, ";")
                res_log.id2 = entry(21, reslin_queasy.char3, ";")
                res_log.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))
                res_log.zeit = number2
                res_log.date1 = reslin_queasy.date2
                res_log.variance =  to_decimal(res_log.rate1) - to_decimal(res_log.rate2)
                res_log.night_stay = (res_log.abreise1 - res_log.ankunft1).days

                res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})

                if res_line:
                    res_log.resstatus = res_line.resstatus

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                    if zimkateg:
                        res_log.room_cat = zimkateg.kurzbez


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            res_log.rate_code = substring(str, 6)

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest:
                        res_log.rsv_name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma


                    else:
                        res_log.rsv_name = ""

            elif matches(to_string(entry(24, reslin_queasy.char3, ";")),r"*CHG Fixrate TO*"):

                breslin = db_session.query(Breslin).filter(
                         (Breslin.key == ("ResChanges").lower()) & (Breslin.resnr == reslin_queasy.resnr) & (Breslin.reslinnr == reslin_queasy.reslinnr) & (Breslin.date2 == reslin_queasy.date2) & (matches(to_string(entry(24, Breslin.char3, ";")),"*CHG Fixrate FR*")) & (Breslin.number2 == reslin_queasy.number2)).first()

                if breslin and to_decimal(entry(1, entry(25, reslin_queasy.char3, ";") , "-")) != to_decimal(entry(1, entry(25, breslin.char3, ";") , "-")):
                    res_log = Res_log()
                    res_log_data.append(res_log)

                    res_log.resnr = reslin_queasy.resnr
                    res_log.reslinnr = reslin_queasy.reslinnr
                    res_log.ankunft1 = date_mdy(to_int(entry(1, entry(0, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(0, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(0, reslin_queasy.char3, ";") , "/"))))
                    res_log.abreise1 = date_mdy(to_int(entry(1, entry(2, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(2, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(2, reslin_queasy.char3, ";") , "/"))))
                    res_log.zinr1 = entry(14, reslin_queasy.char3, ";")
                    res_log.rate1 =  to_decimal(to_decimal(entry(1 , entry(25 , breslin.char3 , ";") , "-")) )
                    res_log.rate2 =  to_decimal(to_decimal(entry(1 , entry(25 , reslin_queasy.char3 , ";") , "-")) )
                    res_log.id1 = entry(20, reslin_queasy.char3, ";")
                    res_log.id2 = entry(21, reslin_queasy.char3, ";")
                    res_log.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))
                    res_log.zeit = reslin_queasy.number2
                    res_log.date1 = reslin_queasy.date2
                    res_log.variance =  to_decimal(res_log.rate1) - to_decimal(res_log.rate2)
                    res_log.night_stay = (res_log.abreise1 - res_log.ankunft1).days

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if guest:
                            res_log.name1 = guest.name


                        res_log.resstatus = res_line.resstatus

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            res_log.room_cat = zimkateg.kurzbez


                        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                res_log.rate_code = substring(str, 6)

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if tguest:
                            res_log.rsv_name = tguest.name + ", " + tguest.vorname1 + " " + tguest.anrede1 + tguest.anredefirma


                        else:
                            res_log.rsv_name = ""


    def create_list2():

        nonlocal res_log_data, akuntf, abreise, date1, date2, loopi, str, reslin_queasy, guest, res_line, zimkateg
        nonlocal fdate, tdate, resno
        nonlocal breslin, tguest


        nonlocal res_log, breslin, tguest
        nonlocal res_log_data

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("ResChanges").lower()) & (Reslin_queasy.resnr == resno)).order_by(Reslin_queasy._recid).all():

            if matches(reslin_queasy.char3,r"*;*") and to_decimal(entry(18, reslin_queasy.char3, ";")) != to_decimal(entry(19, reslin_queasy.char3, ";")):
                res_log = Res_log()
                res_log_data.append(res_log)

                res_log.resnr = reslin_queasy.resnr
                res_log.reslinnr = reslin_queasy.reslinnr
                res_log.ankunft1 = date_mdy(to_int(entry(1, entry(0, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(0, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(0, reslin_queasy.char3, ";") , "/"))))
                res_log.abreise1 = date_mdy(to_int(entry(1, entry(2, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(2, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(2, reslin_queasy.char3, ";") , "/"))))
                res_log.zinr1 = entry(14, reslin_queasy.char3, ";")
                res_log.rate1 =  to_decimal(to_decimal(entry(18 , reslin_queasy.char3 , ";")) )
                res_log.rate2 =  to_decimal(to_decimal(entry(19 , reslin_queasy.char3 , ";")) )
                res_log.name1 = entry(24, reslin_queasy.char3, ";")
                res_log.id1 = entry(20, reslin_queasy.char3, ";")
                res_log.id2 = entry(21, reslin_queasy.char3, ";")
                res_log.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))
                res_log.zeit = number2
                res_log.date1 = reslin_queasy.date2
                res_log.variance =  to_decimal(res_log.rate1) - to_decimal(res_log.rate2)
                res_log.night_stay = (res_log.abreise1 - res_log.ankunft1).days

                res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})

                if res_line:
                    res_log.resstatus = res_line.resstatus

                    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                    if zimkateg:
                        res_log.room_cat = zimkateg.kurzbez


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            res_log.rate_code = substring(str, 6)

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    if guest:
                        res_log.rsv_name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma


                    else:
                        res_log.rsv_name = ""

            elif matches(to_string(entry(24, reslin_queasy.char3, ";")),r"*CHG Fixrate TO*"):

                breslin = db_session.query(Breslin).filter(
                         (Breslin.key == ("ResChanges").lower()) & (Breslin.resnr == reslin_queasy.resnr) & (Breslin.reslinnr == reslin_queasy.reslinnr) & (Breslin.date2 == reslin_queasy.date2) & (matches(to_string(entry(24, Breslin.char3, ";")),"*CHG Fixrate FR*")) & (Breslin.number2 == reslin_queasy.number2)).first()

                if breslin and to_decimal(entry(1, entry(25, reslin_queasy.char3, ";") , "-")) != to_decimal(entry(1, entry(25, breslin.char3, ";") , "-")):
                    res_log = Res_log()
                    res_log_data.append(res_log)

                    res_log.resnr = reslin_queasy.resnr
                    res_log.reslinnr = reslin_queasy.reslinnr
                    res_log.ankunft1 = date_mdy(to_int(entry(1, entry(0, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(0, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(0, reslin_queasy.char3, ";") , "/"))))
                    res_log.abreise1 = date_mdy(to_int(entry(1, entry(2, reslin_queasy.char3, ";") , "/")) , to_int(entry(0, entry(2, reslin_queasy.char3, ";") , "/")) , to_int("20" + timedelta(days=entry(2, entry(2, reslin_queasy.char3, ";") , "/"))))
                    res_log.zinr1 = entry(14, reslin_queasy.char3, ";")
                    res_log.rate1 =  to_decimal(to_decimal(entry(1 , entry(25 , breslin.char3 , ";") , "-")) )
                    res_log.rate2 =  to_decimal(to_decimal(entry(1 , entry(25 , reslin_queasy.char3 , ";") , "-")) )
                    res_log.id1 = entry(20, reslin_queasy.char3, ";")
                    res_log.id2 = entry(21, reslin_queasy.char3, ";")
                    res_log.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))
                    res_log.zeit = reslin_queasy.number2
                    res_log.date1 = reslin_queasy.date2
                    res_log.variance =  to_decimal(res_log.rate1) - to_decimal(res_log.rate2)
                    res_log.night_stay = (res_log.abreise1 - res_log.ankunft1).days

                    res_line = get_cache (Res_line, {"resnr": [(eq, reslin_queasy.resnr)],"reslinnr": [(eq, reslin_queasy.reslinnr)]})

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        if guest:
                            res_log.name1 = guest.name


                        res_log.resstatus = res_line.resstatus

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                        if zimkateg:
                            res_log.room_cat = zimkateg.kurzbez


                        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                res_log.rate_code = substring(str, 6)

                        tguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        if tguest:
                            res_log.rsv_name = tguest.name + ", " + tguest.vorname1 + " " + tguest.anrede1 + tguest.anredefirma


                        else:
                            res_log.rsv_name = ""


    if fdate != None and tdate != None and resno != 0:
        create_list1()

    elif fdate == None and tdate == None and resno != 0:
        create_list2()
    else:
        create_list()

    return generate_output()