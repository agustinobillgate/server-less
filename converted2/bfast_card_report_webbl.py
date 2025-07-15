#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Mealcoup, Res_line, Guest, Arrangement, Argt_line

payload_list_data, Payload_list = create_model("Payload_list", {"room":string, "fdate":date, "tdate":date, "mealtime":string, "lname":string}, {"room": "*"})

def bfast_card_report_webbl(payload_list_data:[Payload_list]):

    prepare_cache ([Htparam, Mealcoup, Res_line, Guest, Arrangement, Argt_line])

    bfast_data_data = []
    getdatanr:int = 0
    i:int = 0
    ii:int = 0
    sumadult:int = 0
    sumcompl:int = 0
    sumchild:int = 0
    sumtotuse:int = 0
    dateval:int = 0
    artgrp_abf:int = 0
    artgrp_lunch:int = 0
    artgrp_dinner:int = 0
    tempresnr:int = 0
    strdayuse:string = ""
    strday:string = ""
    counter:int = 0
    bill_date:date = None
    htparam = mealcoup = res_line = guest = arrangement = argt_line = None

    bfast_data = payload_list = None

    bfast_data_data, Bfast_data = create_model("Bfast_data", {"tdate":date, "roomnr":string, "resnr":int, "guestnr":int, "vip":bool, "nation":string, "guestname":string, "totaladult":int, "totalcompli":int, "totalchild":int, "totaluse":int, "dummychr":string, "arrivaldate":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bfast_data_data, getdatanr, i, ii, sumadult, sumcompl, sumchild, sumtotuse, dateval, artgrp_abf, artgrp_lunch, artgrp_dinner, tempresnr, strdayuse, strday, counter, bill_date, htparam, mealcoup, res_line, guest, arrangement, argt_line


        nonlocal bfast_data, payload_list
        nonlocal bfast_data_data

        return {"bfast-data": bfast_data_data}

    def fill_data(used:int, daycount:int):

        nonlocal bfast_data_data, getdatanr, i, ii, sumadult, sumcompl, sumchild, sumtotuse, dateval, artgrp_abf, artgrp_lunch, artgrp_dinner, tempresnr, strdayuse, strday, counter, bill_date, htparam, mealcoup, res_line, guest, arrangement, argt_line


        nonlocal bfast_data, payload_list
        nonlocal bfast_data_data

        tmpdate:date = None
        totadult:int = 0
        totcompli:int = 0
        totchild:int = 0
        j:int = 0
        tmpstr:string = ""
        tmpint:int = 0
        day_use:date = None
        tmpdate = mealcoup.ankunft + timedelta(days=used)
        day_use = mealcoup.ankunft + timedelta(days=daycount)

        if day_use >= payload_list.fdate and day_use <= payload_list.tdate:

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

                if argt_line.argt_artnr == artgrp_abf and payload_list.mealtime.lower()  == ("Breakfast").lower() :

                    if argt_line.fakt_modus == 3 and (tmpdate - res_line.ankunft == 1):
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis

                    elif argt_line.fakt_modus == 6 and (tmpdate - res_line.ankunft <= argt_line.intervall):
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis

                    elif argt_line.fakt_modus != 3 and argt_line.fakt_modus != 6:
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis
                    for j in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                        if matches(entry(j - 1, res_line.zimmer_wunsch, ";"),r"*ChAge*"):
                            tmpstr = substring(entry(j - 1, res_line.zimmer_wunsch, ";") , 5)
                    for j in range(1,res_line.kind1 + 1) :

                        if j > num_entries(tmpstr, ","):
                            break

                        if to_int(entry(j - 1, tmpstr, ",")) > 12:
                            tmpint = tmpint + 1
                    totadult = totadult + tmpint
                    totchild = res_line.kind1 - tmpint
                    sumadult = sumadult + totadult
                    sumchild = sumchild + totchild
                    sumcompl = sumcompl + totcompli
            bfast_data = Bfast_data()
            bfast_data_data.append(bfast_data)

            bfast_data.tdate = day_use
            bfast_data.roomnr = mealcoup.zinr
            bfast_data.resnr = mealcoup.resnr
            bfast_data.guestnr = guest.gastnr
            bfast_data.guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
            bfast_data.totaladult = totadult
            bfast_data.totalcompli = totcompli
            bfast_data.totalchild = totchild
            bfast_data.totaluse = mealcoup.verbrauch[daycount - 1]
            sumtotuse = sumtotuse + mealcoup.verbrauch[daycount - 1]

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})

    if htparam:
        artgrp_abf = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})

    if htparam:
        artgrp_lunch = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})

    if htparam:
        artgrp_dinner = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        bill_date = htparam.fdate

    payload_list = query(payload_list_data, first=True)

    if payload_list.fdate == None or payload_list.tdate == None:

        for mealcoup in db_session.query(Mealcoup).filter(
                 (Mealcoup.name == payload_list.mealtime) & (matches(Mealcoup.zinr,("*" + payload_list.room + "*")))).order_by(Mealcoup._recid).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == mealcoup.resnr) & (Res_line.zinr == mealcoup.zinr) & (matches(Res_line.name,("*" + payload_list.lname + "*")))).first()

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if not guest:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                getdatanr = 0
                strdayuse = ""
                for ii in range(1,32 + 1) :

                    if mealcoup.verbrauch[ii - 1] != 0:
                        getdatanr = getdatanr + 1
                        strdayuse = strdayuse + to_string(ii) + ";"
                for i in range(1,getdatanr + 1) :
                    dateval = to_int(entry(i - 1, strdayuse, ";"))
                    fill_data(i, dateval)
    else:

        for mealcoup in db_session.query(Mealcoup).filter(
                 (Mealcoup.name == payload_list.mealtime) & (Mealcoup.ankunft <= payload_list.tdate) & (Mealcoup.abreise >= payload_list.fdate) & (matches(Mealcoup.zinr,("*" + payload_list.room + "*")))).order_by(Mealcoup.ankunft.desc()).all():

            res_line = db_session.query(Res_line).filter(
                     (Res_line.resnr == mealcoup.resnr) & (Res_line.zinr == mealcoup.zinr) & (matches(Res_line.name,("*" + payload_list.lname + "*")))).first()

            if res_line:

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if not guest:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
                getdatanr = 0
                strdayuse = ""
                for ii in range(1,32 + 1) :

                    if mealcoup.verbrauch[ii - 1] != 0:
                        getdatanr = getdatanr + 1
                        strdayuse = strdayuse + to_string(ii) + ";"
                for i in range(1,getdatanr + 1) :
                    dateval = to_int(entry(i - 1, strdayuse, ";"))
                    fill_data(i, dateval)

    bfast_data = query(bfast_data_data, first=True)

    if bfast_data:
        bfast_data = Bfast_data()
        bfast_data_data.append(bfast_data)

        bfast_data.roomnr = "T O T A L"
        bfast_data.totaladult = sumadult
        bfast_data.totalcompli = sumcompl
        bfast_data.totalchild = sumchild
        bfast_data.totaluse = sumtotuse

    return generate_output()