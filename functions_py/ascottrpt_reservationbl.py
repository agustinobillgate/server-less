#using conversion tools version: 1.0.0.117
"""_yusufwijasena_22/10/2025
    updated_07/11/2025

    Ticket ID: 698860
        _remark_:   - changed import from functions to functions_py
                    - character_conversionbl not found
                    - fix var declation
                    - changed string to str
                    - fix ("string").lower() to "string"
                    
    Ticket ID: 5C46F2
        _remark_:   - update from ITA: BFC578
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servvat import calc_servvat
# from functions.calc_servtaxesbl import calc_servtaxesbl
# from functions.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
# from functions.character_conversionbl import character_conversionbl
from functions_py.calc_servvat import calc_servvat
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from functions_py.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
from functions_py.character_conversionbl import character_conversionbl
from models import Guest, Reslin_queasy, Queasy, H_artikel, Htparam, Res_line, Zimkateg, Reservation, Sourccod, Segment, Genstat, Zimmer, Nation, Arrangement, Artikel, Mc_guest, Waehrung, Bediener, Bill, Bill_line, H_bill, H_bill_line

data_list_data, Data_list = create_model(
    "Data_list", {
        "confno":str, 
        "arrdate":str, 
        "depdate":str, 
        "roomtype":str, 
        "roomrate":Decimal, 
        "gname":str, 
        "comp":str, 
        "sourcename":str, 
        "memberno":str, 
        "profile":str, 
        "email":str, 
        "totrev":Decimal, 
        "rmrev":Decimal, 
        "fbrev":Decimal,
        "others":Decimal,
        "grossrm":Decimal,
        "grossfb":Decimal,
        "grossothers":Decimal,
        "totgross":Decimal,
        "propid":str,
        "bookdate":str,
        "market":str,
        "bookstatus":str,
        "adult":int,
        "child":int,
        "note":str,
        "guestid":int,
        "rsvid":str,
        "numofguest":int,
        "recordcount":int,
        "grpname":str,
        "companyid":str,
        "canceldate":str,
        "infant":int,
        "createdbyuser":str,
        "createdept":str,
        "modifbyuser":str,
        "modifdept":str,
        "rsvstatus":str,
        "currency":str,
        "reportdate":str,
        "rmno":str,
        "ratecode":str,
        "idcardnum":str,
        "idcardtype":str,
        "connectingrm":str,
        "prevroomnr":str,
        "reward":str,
        "billfbrev":Decimal,
        "grossbillfb":Decimal,
        "billotherrev":Decimal,
        "grossbillother":Decimal,
        "g_title":str,
        "firstname":str,
        "lastname":str,
        "mobile":str,
        "phone":str,
        "postcode":str,
        "fax":str,
        "address1":str,
        "address2":str,
        "city":str,
        "state":str,
        "country":str,
        "nationality":str,
        "birthdate":str,
        "gender":str,
        "actualdate":str,
        "ratecode_bez":str,
        "roomtype_bez":str,
        "market_bez":str,
        "occflag":str,
        "company__crm":str,
        "travelagent__crm":str,
        "travelagentid":str,
        "rateelement":str,
        "flag":str,
        "datum":str,
        "account":str,
        "sharerno":str,
        "guest_crm":str,
        "hear_code":str,
        "come_code":str,
        "eligble_miles":str,
        "legacy_rsvid":str,
        "legacy_guestid":str,
        "legacy_rigid":str,
        "exch_rate":str,
        "ragent_crm":str,
        "travelagent_func":str,
        "rms_companyname":str,
        "rms_travelagent":str,
        "rms_relocation":str,
        "relocation_agent":str,
        "modify_date":str,
        "rms_search":str,
        "fname":str,
        "timestamp":str,
        "inserted":str,
        "sourceprofile":str,
        "groupid":str,
        "membership":str,
        "parent_rsvid":str,
        "total_rates":str
        }
    )        

# def ascottrpt_reservationbl(datum:date, propid:string, data_list_data:[Data_list]):
def ascottrpt_reservationbl(datum:date, propid:str, data_list_data:Data_list):

    prepare_cache ([Guest, Queasy, H_artikel, Htparam, Res_line, Zimkateg, Reservation, Sourccod, Segment, Genstat, Zimmer, Nation, Arrangement, Artikel, Mc_guest, Waehrung, Bediener, Bill, Bill_line, H_bill, H_bill_line])

    data_count = 0
    birthdate = ""
    str_rsv = ""
    contcode = ""
    lastrmno = ""
    rstat = ""
    reslinnr_str = ""
    i:int = 0
    loop_i:int = 0
    curr_i:int = 0
    datacount:int = 0
    billno:int = 0
    cancel_loop:int = 0
    billflag:bool = False
    do_it:bool = False
    resv_date:date = None
    rsv_date:date = None
    to_date:date = None
    datum1:date = None
    afterdatum1:date = None
    flodging = to_decimal("0.0")
    lodging = to_decimal("0.0")
    breakfast = to_decimal("0.0")
    lunch = to_decimal("0.0")
    dinner = to_decimal("0.0")
    others = to_decimal("0.0")
    rmrate = to_decimal("0.0")
    net_vat = to_decimal("0.0")
    net_service = to_decimal("0.0")
    vat = to_decimal("0.0")
    service = to_decimal("0.0")
    t_rmrev = to_decimal("0.0")
    t_fbrev = to_decimal("0.0")
    t_others = to_decimal("0.0")
    betragvalue = to_decimal("0.0")
    grossbetrag = to_decimal("0.0")
    newbetrag = to_decimal("0.0")
    totalfb = to_decimal("0.0")
    totgrossfb = to_decimal("0.0")
    totalother = to_decimal("0.0")
    totgrossother = to_decimal("0.0")
    longcharoutput = ""
    ci_date = ""
    co_date = ""
    arrtime = ""
    deptime = ""
    co_date_abreise = ""
    actualdatum = ""
    serv1 = to_decimal("0.0")
    serv2 = to_decimal("0.0")
    vat2 = to_decimal("0.0")
    vat3 = to_decimal("0.0")
    vat4 = to_decimal("0.0")
    fact = to_decimal("0.0")
    fact1 = to_decimal("0.0")
    fact2 = to_decimal("0.0")
    vat1 = to_decimal("0.0")
    service1 = to_decimal("0.0")
    bill_date:date = None
    todate:date = None
    curr_time:int = 0
    counter:int = 0
    guest = reslin_queasy = queasy = h_artikel = htparam = res_line = zimkateg = reservation = sourccod = segment = genstat = zimmer = nation = arrangement = artikel = mc_guest = waehrung = bediener = bill = bill_line = h_bill = h_bill_line = None

    data_list = gmember = gcomp = rqueasy = qsy19 = qsy2 = buffart = datalist = qsy231 = qsy289 = t_datalist = None

    Gmember = create_buffer("Gmember",Guest)
    Gcomp = create_buffer("Gcomp",Guest)
    Rqueasy = create_buffer("Rqueasy",Reslin_queasy)
    Qsy19 = create_buffer("Qsy19",Queasy)
    Qsy2 = create_buffer("Qsy2",Queasy)
    Buffart = create_buffer("Buffart",H_artikel)
    Datalist = Data_list
    datalist_data = data_list_data

    Qsy231 = create_buffer("Qsy231",Queasy)
    Qsy289 = create_buffer("Qsy289",Queasy)
    T_datalist = Data_list
    t_datalist_data = data_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        return {
            "data_count": data_count, 
            "data-list": data_list_data
            }

    def add__months(pdate:date, pmonths:int):
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        iyear:int = 0
        imonth:int = 0
        iday:int = 0
        inewyear:int = 0
        inewmonth:int = 0
        imaxday:int = 0
        dnewdate:date 
        iyear = get_year(pdate)
        imonth = get_month(pdate)
        iday = get_day(pdate)
        inewmonth = imonth + pmonths
        inewyear = iyear + truncate((inewmonth - 1) / 12, 0)
        inewmonth = ((inewmonth - 1) % 12) + 1

        if inewmonth == 2:

            if (inewyear % 4 == 0 and inewyear % 100 != 0) or (inewyear % 400 == 0):
                imaxday = 29
            else:
                imaxday = 28
        elif inewmonth == 4:
            imaxday = 30
        elif inewmonth == 6:
            imaxday = 30
        elif inewmonth == 9:
            imaxday = 30
        elif inewmonth == 11:
            imaxday = 30
        else:
            imaxday = 31

        if iday > imaxday:
            iday = imaxday
        dnewdate = date_mdy(inewmonth, iday, inewyear)
        return dnewdate

    def find_last_roomnumber(resno:int, guestno:int):
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        rmno = ""
        resdate:date 
        resbuff = None

        def generate_inner_output():
            return (rmno)

        Resbuff =  create_buffer("Resbuff",Res_line)
        rmno = "NULL"
        resdate = date_mdy(1, 1, 1970)

        for resbuff in db_session.query(Resbuff).filter(
                (Resbuff.gastnrmember == guestno) & (Resbuff.resnr != resno) & (Resbuff.resstatus == 8)).order_by(Resbuff._recid).all():

            if resbuff.abreise > resdate:
                resdate = resbuff.abreise
                rmno = resbuff.zinr

        return generate_inner_output()

    def deduct_taxes(department:str, artnum:int, billingdate:date, servicecode:int, mwstcode:int, inp_betrag:Decimal):
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        out_betrag = to_decimal("0.0")

        def generate_inner_output():
            return (out_betrag)

        service, vat = get_output(calc_servvat(department, artnum, billingdate, servicecode, mwstcode))
        out_betrag = to_decimal(round(to_decimal(inp_betrag / (1 + service + vat)) , 2))

        return generate_inner_output()

    def generate_tabledata(casetyp:str):
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        curr_3month:date = None
        bsegment = None
        Bsegment =  create_buffer("Bsegment",Segment)

        # if session_date_format() == ("dmy").lower() :
        if session_date_format() == "dmy" :
            resv_date = date_mdy(substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 0, 2))

        # elif session_date_format() == ("mdy").lower() :
        elif session_date_format() == "mdy" :
            resv_date = date_mdy(substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2) + "/" + substring(res_line.reserve_char, 0, 2))
        else:
            resv_date = date_mdy(substring(res_line.reserve_char, 0, 8))

        if get_year(resv_date) > get_year(get_current_date()):
            resv_date = date_mdy(substring(res_line.reserve_char, 0, 2) + "/" + substring(res_line.reserve_char, 3, 2) + "/" + substring(res_line.reserve_char, 6, 2))
            
        actualdatum = to_string(get_year(datum1) , "9999") + "-" + to_string(get_month(datum1) , "99") + "-" + to_string(get_day(datum1) , "99")
        do_it = True

        # if casetyp.lower()  == ("CheckedOut").lower() :
        if casetyp.lower()  == "checkedout" :
            genstat = get_cache (Genstat, {
                "resnr": [(eq, res_line.resnr)],
                "res_int[0]": [(eq, res_line.reslinnr)],
                "datum": [(eq, res_line.abreise - timedelta(days=1))]})

            if genstat:
                if genstat.resstatus == 13:
                    do_it = False
            else:
                genstat = get_cache (Genstat, {
                    "resnr": [(eq, res_line.resnr)],
                    "res_int[0]": [(eq, res_line.reslinnr)],
                    "datum": [(eq, res_line.ankunft)]})

                if genstat:
                    if genstat.resstatus == 13:
                        do_it = False

        if length(to_string(res_line.reslinnr)) <= 3:
            reslinnr_str = to_string(res_line.reslinnr, "999")

        elif length(to_string(res_line.reslinnr)) == 4:
            reslinnr_str = to_string(res_line.reslinnr, "9999")

        elif length(to_string(res_line.reslinnr)) == 5:
            reslinnr_str = to_string(res_line.reslinnr, "99999")

        if ((datum1 >= datum - timedelta(days=90) and datum1 <= datum + timedelta(days=730)) or casetyp.lower()  == ("CheckedOut").lower()) and res_line.resstatus != 99 and res_line.resstatus != 12 and res_line.l_zuordnung[2] == 0 and do_it:
            data_list = query(data_list_data, filters=(lambda data_list: data_list.rsvid == to_string(res_line.resnr) + reslinnr_str and entry(0, data_list.actualdate, " ") == (actualdatum).lower()), first=True)

            # if not data_list or casetyp.lower()  == ("Cancel").lower() :
            if not data_list or casetyp.lower()  == "cancel" :
                datacount = datacount + 1
                data_list = Data_list()
                data_list_data.append(data_list)

                data_list.confno = propid + "-" + to_string(res_line.resnr) + reslinnr_str
                data_list.roomrate =  to_decimal(res_line.zipreis)
                data_list.sourcename = sourccod.bezeich
                data_list.market = segment.bezeich
                data_list.profile = propid + "-" + to_string(gmember.gastnr)
                data_list.propid = propid
                data_list.gname = gmember.vorname1 + " " + gmember.name + "," + gmember.anrede1
                data_list.adult = res_line.erwachs
                data_list.child = res_line.kind1
                data_list.infant = res_line.kind2
                data_list.guestid = gmember.gastnr
                data_list.rsvid = to_string(res_line.resnr) + reslinnr_str
                data_list.numofguest = res_line.erwachs + res_line.kind1 + res_line.kind2
                data_list.reward = "NULL"
                data_list.roomtype = zimkateg.kurzbez
                data_list.roomtype_bez = zimkateg.bezeichnung
                data_list.recordcount = datacount
                data_list.occflag = "1"
                data_list.account = "-"
                data_list.sharerno = "-"

                if casetyp.lower()  == "checkedout"  or casetyp.lower()  == "inhouse"  or casetyp.lower()  == "guaranteed"  or casetyp.lower()  == "cancel" :
                    data_list.flag = "ACT"

                elif casetyp.lower()  == "forecast" :
                    data_list.flag = "BOB"

                if casetyp.lower()  == "checkedout"  or casetyp.lower()  == "inhouse"  or casetyp.lower()  == "guaranteed"  or casetyp.lower()  == "cancel" :
                    if datum1 >= (datum - timedelta(days=90)) and datum1 < datum:
                        data_list.flag = "HST"

                ci_date = to_string(get_year(res_line.ankunft) , "9999") + to_string(get_month(res_line.ankunft) , "99") + to_string(get_day(res_line.ankunft) , "99")
                data_list.datum = to_string(get_year(datum1) , "9999") + to_string(get_month(datum1) , "99") + to_string(get_day(datum1) , "99")

                if segment.bemerkung != "":
                    data_list.market_bez = segment.bemerkung
                else:
                    data_list.market_bez = "NULL"

                if gmember.vorname1 != "" and gmember.vorname1 != None:
                    data_list.firstname = gmember.vorname1
                else:
                    data_list.firstname = "NULL"

                if gmember.name != "" and gmember.name != None:
                    data_list.lastname = gmember.name
                else:
                    data_list.lastname = "NULL"

                if gmember.anrede1 != "" and gmember.anrede1 != None:
                    data_list.g_title = gmember.anrede1
                else:
                    data_list.g_title = "NULL"

                if gmember.adresse1 != "" and gmember.adresse1 != None:
                    data_list.address1 = gmember.adresse1
                else:
                    data_list.address1 = "NULL"
                data_list.address1 = replace_str(data_list.address1, chr_unicode(44) , " ")

                if gmember.adresse2 != "" and gmember.adresse2 != None:
                    data_list.address2 = gmember.adresse2
                else:
                    data_list.address2 = "NULL"
                data_list.address2 = replace_str(data_list.address2, chr_unicode(44) , " ")

                if gmember.mobil_telefon != "" and gmember.mobil_telefon != None:
                    data_list.mobile = gmember.mobil_telefon
                else:
                    data_list.mobile = "NULL"

                if gmember.telefon != "" and gmember.telefon != None:
                    data_list.phone = gmember.telefon
                else:
                    data_list.phone = "NULL"

                if gmember.plz != "" and gmember.plz != None:
                    data_list.postcode = gmember.plz
                else:
                    data_list.postcode = "NULL"

                if gmember.fax != "" and gmember.fax != None:
                    data_list.fax = gmember.fax
                else:
                    data_list.fax = "NULL"

                if gmember.wohnort != "" and gmember.wohnort != None:
                    data_list.city = gmember.wohnort
                else:
                    data_list.city = "NULL"

                if gmember.geburt_ort2 != "" and gmember.geburt_ort2 != None:
                    data_list.state = gmember.geburt_ort2
                else:
                    data_list.state = "NULL"

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

                if nation:
                    data_list.nationality = nation.bezeich
                    data_list.country = nation.bezeich

                else:
                    data_list.nationality = "NULL"
                    data_list.country = "NULL"

                if gmember.geburtdatum1 == None:
                    birthdate = "NULL"
                else:
                    if get_year(gmember.geburtdatum1) >= (get_year(get_current_date()) - 100) and get_year(gmember.geburtdatum1) <= get_year(get_current_date()):
                        birthdate = to_string(get_year(gmember.geburtdatum1) , "9999") + "-" + to_string(get_month(gmember.geburtdatum1) , "99") + "-" + to_string(get_day(gmember.geburtdatum1) , "99")
                    else:
                        birthdate = "NULL"
                        
                data_list.birthdate = birthdate

                if gmember.geschlecht.lower()  == "m" :
                    data_list.gender = "Male"

                elif gmember.geschlecht.lower()  == "f" :
                    data_list.gender = "Female"
                else:
                    data_list.gender = "NULL"

                if datum < res_line.abreise:
                    genstat = get_cache (Genstat, {
                        "resnr": [(eq, res_line.resnr)],
                        "res_int[0]": [(eq, res_line.reslinnr)],
                        "datum": [(eq, datum1)]})

                    if genstat:
                        rstat = get_resstatus("genstat", genstat.resstatus)
                        data_list.rsvstatus = rstat
                    else:
                        rstat = get_resstatus("resline", res_line.resstatus)
                        data_list.rsvstatus = rstat
                else:
                    rstat = get_resstatus("resline", res_line.resstatus)
                    data_list.rsvstatus = rstat

                if casetyp.lower()  == "cancel" :
                    data_list.rsvstatus = "Cancelled"

                elif casetyp.lower()  == "guaranteed" :
                    data_list.rsvstatus = "Guaranteed"
                data_list.gname = replace_str(data_list.gname, chr_unicode(35) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(42) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(47) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(34) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(44) , " ")

                if res_line.bemerk != "":
                    data_list.note = res_line.bemerk
                    data_list.note = replace_str(data_list.note, chr_unicode(4) , " ")
                    data_list.note = replace_str(data_list.note, chr_unicode(10) , " ")
                    data_list.note = replace_str(data_list.note, chr_unicode(13) , " ")
                    data_list.note = replace_str(data_list.note, chr_unicode(32) , " ")
                    data_list.note = replace_str(data_list.note, chr_unicode(34) , "")
                    data_list.note = replace_str(data_list.note, chr_unicode(39) , "")
                    data_list.note = replace_str(data_list.note, chr_unicode(92) , chr_unicode(47))
                    data_list.note = replace_str(data_list.note, chr_unicode(35) , "")
                    data_list.note = replace_str(data_list.note, chr_unicode(42) , "")
                    data_list.note = replace_str(data_list.note, chr_unicode(47) , "")
                    data_list.note = replace_str(data_list.note, chr_unicode(44) , " ")
                else:
                    data_list.note = "NULL"

                if gmember.email_adr != "":
                    data_list.email = gmember.email_adr
                    data_list.email = replace_str(data_list.email, chr_unicode(10) , " ")
                    data_list.email = replace_str(data_list.email, chr_unicode(13) , " ")
                    data_list.email = replace_str(data_list.email, chr_unicode(34) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(39) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(92) , chr_unicode(47))
                    data_list.email = replace_str(data_list.email, chr_unicode(35) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(42) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(47) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(44) , " ")
                else:
                    data_list.email = "NULL"

                if res_line.resstatus != 9:
                    data_list.bookstatus = "BOOKING"

                elif res_line.resstatus == 9 or res_line.resstatus == 10:
                    data_list.bookstatus = "CANCEL"
                data_list.canceldate = "-"

                if res_line.cancelled != None:
                    data_list.canceldate = to_string(get_year(res_line.cancelled) , "9999") + "-" + to_string(get_month(res_line.cancelled) , "99") + "-" + to_string(get_day(res_line.cancelled) , "99") # update ITA: BFC578
                data_list.modify_date = "NULL"

                if res_line.changed != None:
                    data_list.modify_date = to_string(get_year(res_line.changed) , "9999") + "-" + to_string(get_month(res_line.changed) , "99") + "-" + to_string(get_day(res_line.changed) , "99")
                rsv_date = reservation.resdat

                if rsv_date != None:
                    data_list.bookdate = to_string(get_year(rsv_date) , "9999") + to_string(get_month(rsv_date) , "99") + to_string(get_day(rsv_date) , "99")
                else:
                    data_list.bookdate = "-"
                data_list.actualdate = to_string(get_year(datum1) , "9999") + "-" + to_string(get_month(datum1) , "99") + "-" + to_string(get_day(datum1) , "99") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
                
                t_rmrev =  to_decimal("0")
                t_fbrev =  to_decimal("0")
                t_others =  to_decimal("0")
                lodging =  to_decimal("0")
                breakfast =  to_decimal("0")
                lunch =  to_decimal("0")
                dinner =  to_decimal("0")
                others =  to_decimal("0")

                if datum1 <= datum:
                    genstat = get_cache (Genstat, {
                        "datum": [(eq, datum1)],
                        "resnr": [(eq, res_line.resnr)],
                        "res_int[0]": [(eq, res_line.reslinnr)]})

                    if genstat:
                        arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

                        artikel = get_cache (Artikel, {
                            "artnr": [(eq, arrangement.argt_artikelnr)],
                            "departement": [(eq, 0)]})

                        if artikel:
                            serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                            lodging =  to_decimal(genstat.logis)
                            breakfast =  to_decimal(genstat.res_deci[1])
                            lunch =  to_decimal(genstat.res_deci[2])
                            dinner =  to_decimal(genstat.res_deci[3])
                            others =  to_decimal(genstat.res_deci[4])

                            bsegment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                            if bsegment:
                                data_list.market = bsegment.bezeich

                                if segment.bemerkung != "":
                                    data_list.market_bez = bsegment.bemerkung
                                else:
                                    data_list.market_bez = "NULL"
                else:
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum1, curr_i, datum))

                if lodging > 0:
                    if lodging > 0:
                        t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging)

                    if breakfast > 0 or lunch > 0 or dinner > 0:
                        t_fbrev =  to_decimal(t_fbrev) + to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)

                    if others > 0:
                        t_others =  to_decimal(t_others) + to_decimal(others)
                        
                data_list.rmrev = to_decimal(round(t_rmrev , 2))
                data_list.fbrev = to_decimal(round(t_fbrev , 2))
                data_list.others = to_decimal(round(t_others , 2))
                data_list.totrev =  to_decimal(data_list.rmrev) + to_decimal(data_list.fbrev) + to_decimal(data_list.others)
                data_list.grossrm = to_decimal(round(t_rmrev * (1 + vat1 + vat2 + serv1) , 2))
                data_list.grossfb = to_decimal(round(t_fbrev * (1 + vat1 + vat2 + serv1) , 2))
                data_list.grossothers = to_decimal(round(t_others * (1 + vat1 + vat2 + serv1) , 2))
                data_list.totgross =  to_decimal(data_list.grossrm) + to_decimal(data_list.grossfb) + to_decimal(data_list.grossothers)
                data_list.reportdate = to_string(get_year(datum) , "9999") + "-" +\
                        to_string(get_month(datum) , "99") + "-" +\
                        to_string(get_day(datum) , "99") + " " +\
                        to_string(get_current_time_in_seconds(), "HH:MM:SS")

                if res_line.ankunft != None:
                    ci_date = to_string(get_year(res_line.ankunft) , "9999") + to_string(get_month(res_line.ankunft) , "99") + to_string(get_day(res_line.ankunft) , "99")
                else:
                    ci_date = ""

                if res_line.abreise != None:
                    co_date = to_string(get_year(res_line.abreise) , "9999") + to_string(get_month(res_line.abreise) , "99") + to_string(get_day(res_line.abreise) , "99")
                else:
                    co_date = ""
                afterdatum1 = datum1 + timedelta(days=1)
                actualdatum = to_string(get_year(afterdatum1) , "9999") + "-" + to_string(get_month(afterdatum1) , "99") + "-" + to_string(get_day(afterdatum1) , "99")

                if res_line.ankzeit != 0:
                    arrtime = to_string(res_line.ankzeit, "HH:MM:SS")
                else:
                    arrtime = "00:00:00"

                if res_line.abreisezeit != 0:
                    deptime = to_string(res_line.abreisezeit, "HH:MM:SS")
                else:
                    deptime = "00:00:00"
                    
                data_list.arrdate = ci_date
                data_list.depdate = co_date
                data_list.comp = "-"
                data_list.company__crm = "-"
                data_list.travelagent__crm = "-"
                data_list.companyid = "-"
                data_list.travelagentid = "-"
                data_list.travelagent_func = "-"
                data_list.sourceprofile = "-"
                data_list.hear_code = "-"
                data_list.come_code = "-"
                data_list.eligble_miles = "-"
                data_list.legacy_rigid = "-"
                data_list.membership = "-"
                data_list.exch_rate = "-"
                data_list.parent_rsvid = "-"
                data_list.ragent_crm = "-"
                data_list.rms_companyname = "-"
                data_list.rms_travelagent = "-"
                data_list.rms_relocation = "-"
                data_list.relocation_agent = "-"
                data_list.rms_search = "-"
                data_list.total_rates = "-"
                data_list.fname = "-"
                data_list.timestamp = "-"
                data_list.inserted = "-"

                gcomp = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                if gcomp:
                    data_list.comp = gcomp.name + ", " + gcomp.anredefirma

                    if gcomp.karteityp == 1:
                        data_list.companyid = to_string(gcomp.gastnr)

                    elif gcomp.karteityp == 2:
                        data_list.travelagentid = to_string(gcomp.gastnr)

                    qsy231 = get_cache (Queasy, {
                        "key": [(eq, 231)],
                        "number1": [(eq, gcomp.gastnr)]})

                    if qsy231:
                        if gcomp.karteityp == 1:
                            data_list.company__crm = qsy231.char1

                        elif gcomp.karteityp == 2:
                            data_list.travelagent__crm = qsy231.char1
                data_list.comp = replace_str(data_list.comp, chr_unicode(44) , " ")

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == gmember.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                if mc_guest:
                    data_list.memberno = mc_guest.cardnum
                else:
                    data_list.memberno = "NULL"

                if data_list.memberno.lower()  == "null" :
                    data_list.guest_crm = "-"

                else:
                    data_list.guest_crm = data_list.memberno

                if reservation.groupname != "":
                    data_list.grpname = reservation.groupname
                else:
                    data_list.grpname = "-"
                data_list.grpname = replace_str(data_list.grpname, chr_unicode(44) , " ")
                data_list.groupid = "-"

                if data_list.companyid != "":
                    data_list.groupid = data_list.companyid
                data_list.currency = "NULL"

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    data_list.currency = waehrung.wabkurz
                data_list.createdbyuser = "-"
                data_list.createdept = "-"

                bediener = get_cache (Bediener, {"nr": [(eq, to_int(reservation.useridanlage))]})

                if bediener:
                    qsy19 = get_cache (Queasy, {
                        "key": [(eq, 19)],
                        "number1": [(eq, bediener.user_group)]})

                    if qsy19:
                        data_list.createdbyuser = bediener.username
                        data_list.createdept = qsy19.char3
                data_list.modifbyuser = "-"
                data_list.modifdept = "-"

                bediener = get_cache (Bediener, {"nr": [(eq, to_int(res_line.changed_id))]})

                if bediener:
                    qsy19 = get_cache (Queasy, {
                        "key": [(eq, 19)],
                        "number1": [(eq, bediener.user_group)]})

                    if qsy19:
                        data_list.modifbyuser = bediener.username
                        data_list.modifdept = qsy19.char3

                if res_line.zinr != "":
                    data_list.rmno = res_line.zinr
                else:
                    data_list.rmno = "-"
                contcode = "-"
                
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str_rsv = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str_rsv, 0, 6) == "$code$" :
                        contcode = substring(str_rsv, 6)
                data_list.ratecode = contcode

                if contcode.lower()  != "-" :

                    qsy2 = get_cache (Queasy, {
                        "key": [(eq, 2)],
                        "char1": [(eq, contcode)]})

                    if qsy2:
                        ratecode_bez = qsy2.char2
                    else:
                        ratecode_bez = "-"
                else:
                    ratecode_bez = "-"

                qsy289 = get_cache (Queasy, {
                    "key": [(eq, 289)],
                    "char1": [(eq, data_list.ratecode)]})

                if qsy289:
                    data_list.rateelement = qsy289.char2

                else:
                    data_list.rateelement = "NULL"

                if gmember.geburt_ort1 != "":
                    data_list.idcardtype = gmember.geburt_ort1
                else:
                    data_list.idcardtype = "NULL"

                if data_list.idcardtype.lower()  == "null" :
                    data_list.legacy_rsvid = "-"

                else:
                    data_list.legacy_rsvid = data_list.idcardtype

                if gmember.ausweis_nr1 != "":
                    data_list.idcardnum = gmember.ausweis_nr1
                else:
                    data_list.idcardnum = "NULL"

                if data_list.idcardnum.lower()  == "null" :
                    data_list.legacy_guestid = "-"

                else:
                    data_list.legacy_guestid = data_list.idcardnum

                data_list.prevroomnr = "-"
                lastrmno = find_last_roomnumber(res_line.resnr, res_line.gastnrmember)
                data_list.prevroomnr = lastrmno
                data_list.connectingrm = "-"

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if zimmer:
                    if zimmer.verbindung[0] != "":
                        data_list.connectingrm = zimmer.verbindung[0]

                bill = get_cache (Bill, {
                    "resnr": [(eq, res_line.resnr)],
                    "reslinnr": [(eq, res_line.reslinnr)]})

                if bill:
                    for bill_line in db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == bill.rechnr) & (Bill_line.betrag > 0) & (Bill_line.artnr != 99)).order_by(Bill_line._recid).all():

                        artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)]})

                        if artikel:
                            if artikel.umsatzart == 4:
                                betragvalue = deduct_taxes(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code, bill_line.betrag)
                                data_list.billotherrev =  to_decimal(data_list.billotherrev) + to_decimal(betragvalue)
                                data_list.grossbillother =  to_decimal(data_list.grossbillother) + to_decimal(bill_line.betrag)

                            elif artikel.umsatzart == 5 or artikel.umsatzart == 6 or (artikel.artart == 1 and artikel.umsatzart == 0):
                                betragvalue = deduct_taxes(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code, bill_line.betrag)

                                if bill_line.betrag == betragvalue:
                                    billflag = False
                                    for i in range(1,length(bill_line.bezeich)  + 1) :
                                        if substring(bill_line.bezeich, i - 1, 1) == "*" :
                                            billno = to_int(substring(bill_line.bezeich, i + 1 - 1, length(bill_line.bezeich)))
                                            i = 999
                                            billflag = True

                                    if billflag :
                                        betragvalue =  to_decimal("0")
                                        grossbetrag =  to_decimal("0")

                                        h_bill = get_cache (H_bill, {
                                            "rechnr": [(eq, billno)],
                                            "resnr": [(eq, bill.resnr)],
                                            "reslinnr": [(eq, bill.reslinnr)]})

                                        for h_bill_line in db_session.query(H_bill_line).filter(
                                                (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == bill_line.bill_datum) & (H_bill_line.departement == bill_line.departement)).order_by(H_bill_line._recid).all():
                                            if h_bill_line.epreis > 0:
                                                buffart = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)]})

                                                if buffart:
                                                    newbetrag = deduct_taxes(buffart.departement, buffart.artnr, bill_line.bill_datum, buffart.service_code, buffart.mwst_code, h_bill_line.betrag)
                                                betragvalue =  to_decimal(betragvalue) + to_decimal(newbetrag)
                                                grossbetrag =  to_decimal(grossbetrag) + to_decimal(h_bill_line.betrag)
                                                
                                data_list.billfbrev =  to_decimal(data_list.billfbrev) + to_decimal(betragvalue)
                                data_list.grossbillfb =  to_decimal(data_list.grossbillfb) + to_decimal(grossbetrag)

                if data_list.rsvstatus.lower()  == "cancelled"  or data_list.rsvstatus.lower()  == "noshow" :
                    data_list.occflag = "0"
                    data_list.roomrate =  to_decimal("0")
                    data_list.totrev =  to_decimal("0")
                    data_list.rmrev =  to_decimal("0")
                    data_list.fbrev =  to_decimal("0")
                    data_list.others =  to_decimal("0")
                    data_list.grossrm =  to_decimal("0")
                    data_list.grossfb =  to_decimal("0")
                    data_list.grossothers =  to_decimal("0")
                    data_list.totgross =  to_decimal("0")
                    data_list.billfbrev =  to_decimal("0")
                    data_list.grossbillfb =  to_decimal("0")
                    data_list.billotherrev =  to_decimal("0")
                    data_list.grossbillother =  to_decimal("0")


                co_date_abreise = to_string(get_year(res_line.abreise) , "9999") + "-" + to_string(get_month(res_line.abreise) , "99") + "-" + to_string(get_day(res_line.abreise) , "99")
                verifynullvalues()

                if actualdatum.lower()  == (co_date_abreise).lower() :
                    genstat = get_cache (Genstat, {
                        "resnr": [(eq, res_line.resnr)],
                        "res_int[0]": [(eq, res_line.reslinnr)],
                        "datum": [(eq, datum)],
                        "res_date[0]": [(lt, Genstat.datum)],
                        "res_date[1]": [(eq, genstat.datum)],
                        "resstatus": [(eq, 8)]})

                    if not genstat:
                        datacount = datacount + 1
                        datalist = Datalist()
                        datalist_data.append(datalist)

                        buffer_copy(data_list, datalist)
                        datalist.arrdate = data_list.arrdate
                        datalist.depdate = data_list.depdate
                        datalist.actualdate = data_list.depdate
                        datalist.occflag = "0"
                        datalist.roomrate =  to_decimal("0")
                        datalist.totrev =  to_decimal("0")
                        datalist.rmrev =  to_decimal("0")
                        datalist.fbrev =  to_decimal("0")
                        datalist.others =  to_decimal("0")
                        datalist.grossrm =  to_decimal("0")
                        datalist.grossfb =  to_decimal("0")
                        datalist.grossothers =  to_decimal("0")
                        datalist.totgross =  to_decimal("0")
                        datalist.billfbrev =  to_decimal("0")
                        datalist.grossbillfb =  to_decimal("0")
                        datalist.billotherrev =  to_decimal("0")
                        datalist.grossbillother =  to_decimal("0")

                    else:
                        datacount = datacount + 1
                        datalist = Datalist()
                        datalist_data.append(datalist)

                        buffer_copy(data_list, datalist)
                        data_list.actualdate = to_string(get_year(genstat.datum) , "9999") + "-" + to_string(get_month(genstat.datum) , "99") + "-" + to_string(get_day(genstat.datum) , "99") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")

                if data_list.rsvstatus.lower()  == "checkedout"  and (res_line.ankunft > datum or res_line.abreise > datum):
                    data_list_data.remove(data_list)
                    datacount = datacount - 1

    def generate_tabledata2():
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        curr_3month:date 
        bsegment = None
        Bsegment =  create_buffer("Bsegment",Segment)
        actualdatum = to_string(get_year(datum1) , "9999") + "-" + to_string(get_month(datum1) , "99") + "-" + to_string(get_day(datum1) , "99")
        do_it = True

        if length(to_string(genstat.res_int[0])) <= 3:
            reslinnr_str = to_string(genstat.res_int[0], "999")

        elif length(to_string(genstat.res_int[0])) == 4:
            reslinnr_str = to_string(genstat.res_int[0], "9999")

        elif length(to_string(genstat.res_int[0])) == 5:
            reslinnr_str = to_string(genstat.res_int[0], "99999")

        if do_it:
            data_list = query(data_list_data, filters=(lambda data_list: data_list.rsvid == to_string(genstat.resnr) + reslinnr_str and entry(0, data_list.actualdate, " ") == (actualdatum).lower()), first=True)

            if not data_list:
                datacount = datacount + 1
                data_list = Data_list()
                data_list_data.append(data_list)

                data_list.confno = propid + "-" + to_string(genstat.resnr) + reslinnr_str
                data_list.roomrate =  to_decimal(genstat.zipreis)
                data_list.sourcename = sourccod.bezeich
                data_list.market = segment.bezeich
                data_list.profile = propid + "-" + to_string(gmember.gastnr)
                data_list.propid = propid
                data_list.gname = gmember.vorname1 + " " + gmember.name + "," + gmember.anrede1
                data_list.adult = genstat.erwachs
                data_list.child = genstat.kind1
                data_list.infant = genstat.kind2
                data_list.guestid = gmember.gastnr
                data_list.rsvid = to_string(genstat.resnr) + reslinnr_str
                data_list.numofguest = genstat.erwachs + genstat.kind1 + genstat.kind2
                data_list.reward = "NULL"
                data_list.roomtype = zimkateg.kurzbez
                data_list.roomtype_bez = zimkateg.bezeichnung
                data_list.recordcount = datacount
                data_list.occflag = "1"
                data_list.account = "-"
                data_list.sharerno = "-"
                data_list.flag = "HST"

                ci_date = to_string(get_year(genstat.res_date[0]) , "9999") + to_string(get_month(genstat.res_date[0]) , "99") + to_string(get_day(genstat.res_date[0]) , "99")
                data_list.datum = to_string(get_year(datum1) , "9999") +\
                        to_string(get_month(datum1) , "99") +\
                        to_string(get_day(datum1) , "99")

                if segment.bemerkung != "":
                    data_list.market_bez = segment.bemerkung
                else:
                    data_list.market_bez = "NULL"

                if gmember.vorname1 != "" and gmember.vorname1 != None:
                    data_list.firstname = gmember.vorname1
                else:
                    data_list.firstname = "NULL"

                if gmember.name != "" and gmember.name != None:
                    data_list.lastname = gmember.name
                else:
                    data_list.lastname = "NULL"

                if gmember.anrede1 != "" and gmember.anrede1 != None:
                    data_list.g_title = gmember.anrede1
                else:
                    data_list.g_title = "NULL"

                if gmember.adresse1 != "" and gmember.adresse1 != None:
                    data_list.address1 = gmember.adresse1
                else:
                    data_list.address1 = "NULL"
                data_list.address1 = replace_str(data_list.address1, chr_unicode(44) , " ")

                if gmember.adresse2 != "" and gmember.adresse2 != None:
                    data_list.address2 = gmember.adresse2
                else:
                    data_list.address2 = "NULL"
                data_list.address2 = replace_str(data_list.address2, chr_unicode(44) , " ")

                if gmember.mobil_telefon != "" and gmember.mobil_telefon != None:
                    data_list.mobile = gmember.mobil_telefon
                else:
                    data_list.mobile = "NULL"

                if gmember.telefon != "" and gmember.telefon != None:
                    data_list.phone = gmember.telefon
                else:
                    data_list.phone = "NULL"

                if gmember.plz != "" and gmember.plz != None:
                    data_list.postcode = gmember.plz
                else:
                    data_list.postcode = "NULL"

                if gmember.fax != "" and gmember.fax != None:
                    data_list.fax = gmember.fax
                else:
                    data_list.fax = "NULL"

                if gmember.wohnort != "" and gmember.wohnort != None:
                    data_list.city = gmember.wohnort
                else:
                    data_list.city = "NULL"

                if gmember.geburt_ort2 != "" and gmember.geburt_ort2 != None:
                    data_list.state = gmember.geburt_ort2
                else:
                    data_list.state = "NULL"

                nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation1)]})

                if nation:
                    data_list.nationality = nation.bezeich
                    data_list.country = nation.bezeich

                else:
                    data_list.nationality = "NULL"
                    data_list.country = "NULL"

                if gmember.geburtdatum1 == None:
                    birthdate = "NULL"
                else:
                    if get_year(gmember.geburtdatum1) >= (get_year(get_current_date()) - 100) and get_year(gmember.geburtdatum1) <= get_year(get_current_date()):
                        birthdate = to_string(get_year(gmember.geburtdatum1) , "9999") + "-" + to_string(get_month(gmember.geburtdatum1) , "99") + "-" + to_string(get_day(gmember.geburtdatum1) , "99")
                    else:
                        birthdate = "NULL"
                data_list.birthdate = birthdate

                if gmember.geschlecht.lower()  == "m" :
                    data_list.gender = "Male"

                elif gmember.geschlecht.lower()  == "f" :
                    data_list.gender = "Female"
                else:
                    data_list.gender = "NULL"
                rstat = get_resstatus("genstat", genstat.resstatus)
                data_list.rsvstatus = rstat
                data_list.gname = replace_str(data_list.gname, chr_unicode(35) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(42) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(47) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(34) , "")
                data_list.gname = replace_str(data_list.gname, chr_unicode(44) , " ")
                data_list.note = "NULL"

                if gmember.email_adr != "":
                    data_list.email = gmember.email_adr
                    data_list.email = replace_str(data_list.email, chr_unicode(10) , " ")
                    data_list.email = replace_str(data_list.email, chr_unicode(13) , " ")
                    data_list.email = replace_str(data_list.email, chr_unicode(34) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(39) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(92) , chr_unicode(47))
                    data_list.email = replace_str(data_list.email, chr_unicode(35) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(42) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(47) , "")
                    data_list.email = replace_str(data_list.email, chr_unicode(44) , " ")
                else:
                    data_list.email = "NULL"
                data_list.canceldate = "-"
                data_list.modify_date = "NULL"


                rsv_date = reservation.resdat

                if rsv_date is not None:
                    data_list.bookdate = to_string(get_year(rsv_date) , "9999") + to_string(get_month(rsv_date) , "99") + to_string(get_day(rsv_date) , "99") # update ITA: BFC578
                else:
                    data_list.bookdate = "-"
                data_list.actualdate = to_string(get_year(datum1) , "9999") + "-" + to_string(get_month(datum1) , "99") + "-" + to_string(get_day(datum1) , "99") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
                t_rmrev =  to_decimal("0")
                t_fbrev =  to_decimal("0")
                t_others =  to_decimal("0")
                lodging =  to_decimal("0")
                breakfast =  to_decimal("0")
                lunch =  to_decimal("0")
                dinner =  to_decimal("0")
                others =  to_decimal("0")

                arrangement = get_cache (
                    Arrangement, {"arrangement": [(eq, genstat.argt)]})

                artikel = get_cache (Artikel, {
                    "artnr": [(eq, arrangement.argt_artikelnr)],
                    "departement": [(eq, 0)]})

                if artikel:
                    serv1, vat1, vat2, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))
                    lodging =  to_decimal(genstat.logis)
                    breakfast =  to_decimal(genstat.res_deci[1])
                    lunch =  to_decimal(genstat.res_deci[2])
                    dinner =  to_decimal(genstat.res_deci[3])
                    others =  to_decimal(genstat.res_deci[4])

                    bsegment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                    if bsegment:
                        data_list.market = bsegment.bezeich

                        if segment.bemerkung != "":
                            data_list.market_bez = bsegment.bemerkung
                        else:
                            data_list.market_bez = "NULL"

                if lodging > 0:
                    if lodging > 0:
                        t_rmrev =  to_decimal(t_rmrev) + to_decimal(lodging)

                    if breakfast > 0 or lunch > 0 or dinner > 0:
                        t_fbrev =  to_decimal(t_fbrev) + to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)

                    if others > 0:
                        t_others =  to_decimal(t_others) + to_decimal(others)
                        
                data_list.rmrev = to_decimal(round(t_rmrev , 2))
                data_list.fbrev = to_decimal(round(t_fbrev , 2))
                data_list.others = to_decimal(round(t_others , 2))
                data_list.totrev =  to_decimal(data_list.rmrev) + to_decimal(data_list.fbrev) + to_decimal(data_list.others)
                data_list.grossrm = to_decimal(round(t_rmrev * (1 + vat1 + vat2 + serv1) , 2))
                data_list.grossfb = to_decimal(round(t_fbrev * (1 + vat1 + vat2 + serv1) , 2))
                data_list.grossothers = to_decimal(round(t_others * (1 + vat1 + vat2 + serv1) , 2))
                data_list.totgross =  to_decimal(data_list.grossrm) + to_decimal(data_list.grossfb) + to_decimal(data_list.grossothers)
                data_list.reportdate = to_string(get_year(datum) , "9999") + "-" +\
                        to_string(get_month(datum) , "99") + "-" +\
                        to_string(get_day(datum) , "99") + " " +\
                        to_string(get_current_time_in_seconds(), "HH:MM:SS")

                if genstat.res_date[0] != None:
                    ci_date = to_string(get_year(genstat.res_date[0]) , "9999") + to_string(get_month(genstat.res_date[0]) , "99") + to_string(get_day(genstat.res_date[0]) , "99")
                else:
                    ci_date = ""

                if genstat.res_date[1] != None:
                    co_date = to_string(get_year(genstat.res_date[1]) , "9999") + to_string(get_month(genstat.res_date[1]) , "99") + to_string(get_day(genstat.res_date[1]) , "99")
                else:
                    co_date = ""
                afterdatum1 = datum1 + timedelta(days=1)
                actualdatum = to_string(get_year(afterdatum1) , "9999") + "-" + to_string(get_month(afterdatum1) , "99") + "-" + to_string(get_day(afterdatum1) , "99")
                arrtime = "00:00:00"
                deptime = "00:00:00"

                data_list.arrdate = ci_date
                data_list.depdate = co_date
                data_list.comp = "-"
                data_list.company__crm = "-"
                data_list.travelagent__crm = "-"
                data_list.companyid = "-"
                data_list.travelagentid = "-"
                data_list.travelagent_func = "-"
                data_list.sourceprofile = "-"
                data_list.hear_code = "-"
                data_list.come_code = "-"
                data_list.eligble_miles = "-"
                data_list.legacy_rigid = "-"
                data_list.membership = "-"
                data_list.exch_rate = "-"
                data_list.parent_rsvid = "-"
                data_list.ragent_crm = "-"
                data_list.rms_companyname = "-"
                data_list.rms_travelagent = "-"
                data_list.rms_relocation = "-"
                data_list.relocation_agent = "-"
                data_list.rms_search = "-"
                data_list.total_rates = "-"
                data_list.fname = "-"
                data_list.timestamp = "-"
                data_list.inserted = "-"

                gcomp = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

                if gcomp:
                    data_list.comp = gcomp.name + ", " + gcomp.anredefirma

                    if gcomp.karteityp == 1:
                        data_list.companyid = to_string(gcomp.gastnr)

                    elif gcomp.karteityp == 2:
                        data_list.travelagentid = to_string(gcomp.gastnr)

                    qsy231 = get_cache (Queasy, {
                        "key": [(eq, 231)],
                        "number1": [(eq, gcomp.gastnr)]})

                    if qsy231:
                        if gcomp.karteityp == 1:
                            data_list.company__crm = qsy231.char1

                        elif gcomp.karteityp == 2:
                            data_list.travelagent__crm = qsy231.char1
                data_list.comp = replace_str(data_list.comp, chr_unicode(44) , " ")

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.gastnr == gmember.gastnr) & (Mc_guest.cardnum != "") & (Mc_guest.activeflag)).first()

                if mc_guest:
                    data_list.memberno = mc_guest.cardnum
                else:
                    data_list.memberno = "NULL"

                if data_list.memberno.lower()  == "null" :
                    data_list.guest_crm = "-"

                else:
                    data_list.guest_crm = data_list.memberno

                if reservation.groupname != "":
                    data_list.grpname = reservation.groupname
                else:
                    data_list.grpname = "-"
                data_list.grpname = replace_str(data_list.grpname, chr_unicode(44) , " ")
                data_list.groupid = "-"

                if data_list.companyid != "":
                    data_list.groupid = data_list.companyid
                data_list.currency = "NULL"

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})

                if waehrung:
                    data_list.currency = waehrung.wabkurz
                data_list.createdbyuser = "-"
                data_list.createdept = "-"

                bediener = get_cache (Bediener, {"nr": [(eq, to_int(reservation.useridanlage))]})

                if bediener:
                    qsy19 = get_cache (Queasy, {
                        "key": [(eq, 19)],
                        "number1": [(eq, bediener.user_group)]})

                    if qsy19:
                        data_list.createdbyuser = bediener.username
                        data_list.createdept = qsy19.char3
                data_list.modifbyuser = "-"
                data_list.modifdept = "-"

                if genstat.zinr != "":
                    data_list.rmno = genstat.zinr
                else:
                    data_list.rmno = "-"
                contcode = "-"
                for loop_i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
                    str_rsv = entry(loop_i - 1, genstat.res_char[1], ";")

                    if substring(str_rsv, 0, 6) == "$code$" :
                        contcode = substring(str_rsv, 6)
                data_list.ratecode = contcode

                if contcode.lower()  != ("-").lower() :
                    qsy2 = get_cache (Queasy, {
                        "key": [(eq, 2)],
                        "char1": [(eq, contcode)]})

                    if qsy2:
                        ratecode_bez = qsy2.char2
                    else:
                        ratecode_bez = "-"
                else:
                    ratecode_bez = "-"

                qsy289 = get_cache (Queasy, {
                    "key": [(eq, 289)],
                    "char1": [(eq, data_list.ratecode)]})

                if qsy289:
                    data_list.rateelement = qsy289.char2

                else:
                    data_list.rateelement = "NULL"

                if gmember.geburt_ort1 != "":
                    data_list.idcardtype = gmember.geburt_ort1
                else:
                    data_list.idcardtype = "NULL"

                if data_list.idcardtype.lower()  == "null" :
                    data_list.legacy_rsvid = "-"

                else:
                    data_list.legacy_rsvid = data_list.idcardtype

                if gmember.ausweis_nr1 != "":
                    data_list.idcardnum = gmember.ausweis_nr1
                else:
                    data_list.idcardnum = "NULL"

                if data_list.idcardnum.lower()  == "null" :
                    data_list.legacy_guestid = "-"

                else:
                    data_list.legacy_guestid = data_list.idcardnum

                data_list.prevroomnr = "-"
                lastrmno = find_last_roomnumber(genstat.resnr, genstat.gastnrmember)
                data_list.prevroomnr = lastrmno
                data_list.connectingrm = "-"

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

                if zimmer:
                    if zimmer.verbindung[0] != "":
                        data_list.connectingrm = zimmer.verbindung[0]

                bill = get_cache (Bill, {
                    "resnr": [(eq, genstat.resnr)],
                    "reslinnr": [(eq, genstat.res_int[0])]})

                if bill:
                    for bill_line in db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == bill.rechnr) & (Bill_line.betrag > 0) & (Bill_line.artnr != 99)).order_by(Bill_line._recid).all():
                        artikel = get_cache (Artikel, {"artnr": [(eq, bill_line.artnr)]})

                        if artikel:
                            if artikel.umsatzart == 4:
                                betragvalue = deduct_taxes(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code, bill_line.betrag)
                                data_list.billotherrev =  to_decimal(data_list.billotherrev) + to_decimal(betragvalue)
                                data_list.grossbillother =  to_decimal(data_list.grossbillother) + to_decimal(bill_line.betrag)

                            elif artikel.umsatzart == 5 or artikel.umsatzart == 6 or (artikel.artart == 1 and artikel.umsatzart == 0):
                                betragvalue = deduct_taxes(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code, bill_line.betrag)

                                if bill_line.betrag == betragvalue:
                                    billflag = False
                                    for i in range(1,length(bill_line.bezeich)  + 1) :
                                        if substring(bill_line.bezeich, i - 1, 1) == ("*").lower() :
                                            billno = to_int(substring(bill_line.bezeich, i + 1 - 1, length(bill_line.bezeich)))
                                            i = 999
                                            billflag = True

                                    if billflag :
                                        betragvalue =  to_decimal("0")
                                        grossbetrag =  to_decimal("0")

                                        h_bill = get_cache (H_bill, {
                                            "rechnr": [(eq, billno)],
                                            "resnr": [(eq, bill.resnr)],
                                            "reslinnr": [(eq, bill.reslinnr)]})

                                        for h_bill_line in db_session.query(H_bill_line).filter(
                                                (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == bill_line.bill_datum) & (H_bill_line.departement == bill_line.departement)).order_by(H_bill_line._recid).all():
                                            if h_bill_line.epreis > 0:
                                                buffart = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)]})

                                                if buffart:
                                                    newbetrag = deduct_taxes(buffart.departement, buffart.artnr, bill_line.bill_datum, buffart.service_code, buffart.mwst_code, h_bill_line.betrag)
                                                betragvalue =  to_decimal(betragvalue) + to_decimal(newbetrag)
                                                grossbetrag =  to_decimal(grossbetrag) + to_decimal(h_bill_line.betrag)
                                                
                                data_list.billfbrev =  to_decimal(data_list.billfbrev) + to_decimal(betragvalue)
                                data_list.grossbillfb =  to_decimal(data_list.grossbillfb) + to_decimal(grossbetrag)
                                
                co_date_abreise = to_string(get_year(genstat.res_date[1]) , "9999") + "-" + to_string(get_month(genstat.res_date[1]) , "99") + "-" + to_string(get_day(genstat.res_date[1]) , "99")
                verifynullvalues()


    def get_resstatus(ttype:string, stat:int):
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        out_stat = ""

        def generate_inner_output():
            return (out_stat)

        if ttype.lower()  == "resline" :
            if stat == 1 or stat == 2 or stat == 5:
                out_stat = "Guaranteed"

            elif stat == 3 or stat == 4:
                out_stat = "Tentative"

            elif stat == 6:
                out_stat = "InHouse"

            elif stat == 8:
                out_stat = "CheckedOut"

            elif stat == 9:
                out_stat = "Cancelled"

            elif stat == 10:
                out_stat = "NoShow"

            elif stat == 11:
                out_stat = "RoomSharer"

            elif stat == 12:
                out_stat = "AddBill"

            elif stat == 13:
                out_stat = "InHouseRoomSharer"

            elif stat == 99:
                out_stat = "Deleted"
                
            else:
                out_stat = "Undefined"

        elif ttype.lower()  == "genstat" :
            if stat == 6 or stat == 8:
                out_stat = "InHouse"
            elif stat == 13:
                out_stat = "InHouseRoomSharer"
            else:
                out_stat = "Undefined"

        return generate_inner_output()


    def verifynullvalues():
        nonlocal data_count, birthdate, str_rsv, contcode, lastrmno, rstat, reslinnr_str, i, loop_i, curr_i, datacount, billno, cancel_loop, billflag, do_it, resv_date, rsv_date, to_date, datum1, afterdatum1, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service, t_rmrev, t_fbrev, t_others, betragvalue, grossbetrag, newbetrag, totalfb, totgrossfb, totalother, totgrossother, longcharoutput, ci_date, co_date, arrtime, deptime, co_date_abreise, actualdatum, serv1, serv2, vat2, vat3, vat4, fact, fact1, fact2, vat1, service1, bill_date, todate, curr_time, counter, guest, reslin_queasy, queasy, h_artikel, htparam, res_line, zimkateg, reservation, sourccod, segment, genstat, zimmer, nation, arrangement, artikel, mc_guest, waehrung, bediener, bill, bill_line, h_bill, h_bill_line
        nonlocal datum, propid
        nonlocal gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist
        nonlocal data_list, gmember, gcomp, rqueasy, qsy19, qsy2, buffart, datalist, qsy231, qsy289, t_datalist

        if data_list.confno == "":
            data_list.confno = "NULL"

        if data_list.arrdate == "":
            data_list.arrdate = "NULL"

        if data_list.depdate == "":
            data_list.depdate = "NULL"

        if data_list.roomtype == "":
            data_list.roomtype = "NULL"

        if data_list.gname == "":
            data_list.gname = "NULL"

        if data_list.comp == "":
            data_list.comp = "NULL"

        if data_list.sourcename == "":
            data_list.sourcename = "NULL"

        if data_list.memberno == "":
            data_list.memberno = "NULL"

        if data_list.profile == "":
            data_list.profile = "NULL"

        if data_list.email == "":
            data_list.email = "NULL"

        if data_list.propid == "":
            data_list.propid = "NULL"

        if data_list.bookdate == "":
            data_list.bookdate = "NULL"

        if data_list.market == "":
            data_list.market = "NULL"

        if data_list.bookstatus == "":
            data_list.bookstatus = "NULL"

        if data_list.note == "" or data_list.note == None:
            data_list.note = "NULL"

        if data_list.rsvid == "":
            data_list.rsvid = "NULL"

        if data_list.grpname == "":
            data_list.grpname = "NULL"

        if data_list.canceldate == "":
            data_list.canceldate = "NULL"

        if data_list.createdbyuser == "":
            data_list.createdbyuser = "NULL"

        if data_list.createdept == "":
            data_list.createdept = "NULL"

        if data_list.modifbyuser == "":
            data_list.modifbyuser = "NULL"

        if data_list.modifdept == "":
            data_list.modifdept = "NULL"

        if data_list.rsvstatus == "":
            data_list.rsvstatus = "NULL"

        if data_list.currency == "":
            data_list.currency = "NULL"

        if data_list.reportdate == "":
            data_list.reportdate = "NULL"

        if data_list.rmno == "":
            data_list.rmno = "NULL"

        if data_list.ratecode == "":
            data_list.ratecode = "NULL"

        if data_list.idcardnum == "":
            data_list.idcardnum = "NULL"

        if data_list.idcardtype == "":
            data_list.idcardtype = "NULL"

        if data_list.connectingrm == "":
            data_list.connectingrm = "-"

        if data_list.prevroomnr == "":
            data_list.prevroomnr = "-"

        if data_list.reward == "":
            data_list.reward = "NULL"

        if data_list.g_title == "":
            data_list.g_title = "NULL"

        if data_list.firstname == "":
            data_list.firstname = "NULL"

        if data_list.lastname == "":
            data_list.lastname = "NULL"

        if data_list.mobile == "":
            data_list.mobile = "NULL"

        if data_list.phone == "":
            data_list.phone = "NULL"

        if data_list.postcode == "":
            data_list.postcode = "NULL"

        if data_list.fax == "":
            data_list.fax = "NULL"

        if data_list.address1 == "":
            data_list.address1 = "NULL"

        if data_list.address2 == "":
            data_list.address2 = "NULL"

        if data_list.city == "":
            data_list.city = "NULL"

        if data_list.state == "":
            data_list.state = "NULL"

        if data_list.country == "":
            data_list.country = "NULL"

        if data_list.nationality == "":
            data_list.nationality = "NULL"

        if data_list.birthdate == "":
            data_list.birthdate = "NULL"

        if data_list.gender == "":
            data_list.gender = "NULL"

        if data_list.actualdate == "":
            data_list.actualdate = "NULL"

        if data_list.ratecode_bez == "":
            data_list.ratecode_bez = "NULL"

        if data_list.roomtype_bez == "":
            data_list.roomtype_bez = "NULL"

        if data_list.market_bez == "":
            data_list.market_bez = "NULL"

        if data_list.company__crm == "" or data_list.company__crm == None:
            data_list.company__crm = "NULL"

        if data_list.travelagent__crm == "" or data_list.travelagent__crm == None:
            data_list.travelagent__crm = "NULL"

        if data_list.firstname.lower()  != "null" :
            data_list.firstname, longcharoutput = get_output(character_conversionbl(data_list.firstname, ""))

        if data_list.lastname.lower()  != "null" :
            data_list.lastname, longcharoutput = get_output(character_conversionbl(data_list.lastname, ""))

        if data_list.gname.lower()  != "null" :
            data_list.gname, longcharoutput = get_output(character_conversionbl(data_list.gname, ""))

        if data_list.address1.lower()  != "null" :
            data_list.address1, longcharoutput = get_output(character_conversionbl(data_list.address1, ""))

        if data_list.address2.lower()  != "null" :
            data_list.address2, longcharoutput = get_output(character_conversionbl(data_list.address2, ""))

        if data_list.note.lower()  != "null" :
            data_list.note, longcharoutput = get_output(character_conversionbl(data_list.note, ""))

        if data_list.email.lower()  != "null" :
            data_list.email, longcharoutput = get_output(character_conversionbl(data_list.email, ""))

        if data_list.ratecode_bez.lower()  != "null" :
            data_list.ratecode_bez, longcharoutput = get_output(character_conversionbl(data_list.ratecode_bez, ""))

        if data_list.idcardnum.lower()  != "null" :
            data_list.idcardnum, longcharoutput = get_output(character_conversionbl(data_list.idcardnum, ""))

        if data_list.idcardtype.lower()  != "null" :
            data_list.idcardtype, longcharoutput = get_output(character_conversionbl(data_list.idcardtype, ""))

        if data_list.comp.lower()  != "null" :
            data_list.comp, longcharoutput = get_output(character_conversionbl(data_list.comp, ""))

    todate = datum + timedelta(days=730)
    curr_time = get_current_time_in_seconds()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        bill_date = htparam.fdate

    curr_time = get_current_time_in_seconds()

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resstatus <= 13) & (Res_line.resstatus != 4) & (Res_line.resstatus != 8) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.active_flag == 0) & (Res_line.ankunft <= todate) & (Res_line.abreise >= datum) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
        curr_i = 0

        if reservation.resdat <= datum:
            if res_line.ankunft == res_line.abreise:
                to_date = res_line.abreise
            else:
                to_date = res_line.abreise - timedelta(days=1)
            for datum1 in date_range(res_line.ankunft,to_date) :
                curr_i = curr_i + 1
                generate_tabledata("Forecast")
    curr_time = get_current_time_in_seconds()

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.abreise == datum) & (Res_line.resstatus != 12) & (Res_line.abreise < todate)).order_by(Res_line._recid).all():
        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

        if res_line.ankunft == res_line.abreise:
            to_date = res_line.abreise
        else:
            if res_line.abreise > datum:
                to_date = datum - timedelta(days=1)
            else:
                to_date = res_line.abreise - timedelta(days=1)
        curr_i = 0
        for datum1 in date_range(res_line.ankunft,to_date) :
            curr_i = curr_i + 1
            generate_tabledata("CheckedOut")
    curr_time = get_current_time_in_seconds()

    for res_line in db_session.query(Res_line).filter(
            (((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.ankunft == datum)) | ((Res_line.resstatus == 8) & (Res_line.active_flag == 2) & (Res_line.ankunft == datum) & (Res_line.abreise == datum)) | ((Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 12) & (Res_line.resstatus != 10) & (Res_line.ankunft == datum) & (datum < bill_date)) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.resstatus != 12) & (Res_line.ankunft < todate)).order_by(Res_line._recid).all():
        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

        if res_line.ankunft == res_line.abreise:
            to_date = res_line.abreise
        else:
            to_date = res_line.abreise - timedelta(days=1)
        curr_i = 0
        for datum1 in date_range(res_line.ankunft,datum) :
            curr_i = curr_i + 1
            generate_tabledata("InHouse")
    curr_time = get_current_time_in_seconds()

    for reservation in db_session.query(Reservation).filter(
            (Reservation.resdat == datum)).order_by(Reservation._recid).all():
        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == reservation.resnr) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line._recid).all():
            gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            if res_line.ankunft == res_line.abreise:
                to_date = res_line.abreise
            else:
                to_date = res_line.abreise - timedelta(days=1)
            curr_i = 0
            for datum1 in date_range(res_line.ankunft,to_date) :
                curr_i = curr_i + 1

                if res_line.resstatus != 9 and res_line.cancelled != datum:
                    generate_tabledata("Guaranteed")
    curr_time = get_current_time_in_seconds()

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resstatus == 9) & (Res_line.cancelled == datum) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

        segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})
        curr_i = 1
        for cancel_loop in range(1,res_line.zimmeranz + 1) :
            datum1 = datum
            generate_tabledata("Cancel")
    curr_time = get_current_time_in_seconds()

    for data_list in query(data_list_data, filters=(lambda data_list: data_list.entry(0, data_list.arrdate, " ") == entry(0, data_list.depdate, " ") and data_list.rmno.lower()  != "null")):

        t_datalist = query(t_datalist_data, filters=(lambda t_datalist: t_datalist.rmno == data_list.rmno and entry(0, t_datalist.arrdate, " ") == entry(0, data_list.arrdate, " ") and t_datalist.guestid != data_list.guestid), first=True)

        if t_datalist:
            genstat = get_cache (Genstat, {
                "datum": [(eq, date_mdy(to_int(entry(1, entry(0, t_datalist.arrdate, " ") , "-")) , to_int(entry(2, entry(0, t_datalist.arrdate, " ") , "-")) , to_int(entry(0, entry(0, t_datalist.arrdate, " ") , "-"))))],
                "zinr": [(eq, t_datalist.rmno)],
                "gastnrmember": [(ne, t_datalist.guestid)]})

            if not genstat:
                data_list_data.remove(data_list)

    for data_list in query(data_list_data, filters=(lambda data_list: data_list.entry(0, data_list.arrdate, " ") == entry(0, data_list.depdate, " ") and data_list.rmno.lower()  != "null")):
        genstat = get_cache (Genstat, {
            "datum": [(eq, date_mdy(to_int(entry(1, entry(0, data_list.arrdate, " ") , "-")) , to_int(entry(2, entry(0, data_list.arrdate, " ") , "-")) , to_int(entry(0, entry(0, data_list.arrdate, " ") , "-"))))],
            "zinr": [(eq, data_list.rmno)]})

        if not genstat:
            data_list_data.remove(data_list)

    for zimmer in db_session.query(Zimmer).filter(
            (Zimmer.sleeping == False)).order_by(Zimmer._recid).all():

        data_list = query(data_list_data, filters=(lambda data_list: data_list.rmno == zimmer.zinr and data_list.rsvstatus.lower()  == "inhouse"  and entry(0, data_list.actualdate, " ") == to_string(get_year(datum) , "9999") + "-" + to_string(get_month(datum) , "99") + "-" + to_string(get_day(datum) , "99") and data_list.rmrev == 0), first=True)
        while None != data_list:
            data_list.occflag = "0"

            data_list = query(data_list_data, filters=(lambda data_list: data_list.rmno == zimmer.zinr and data_list.rsvstatus.lower()  == "inhouse"  and entry(0, data_list.actualdate, " ") == to_string(get_year(datum) , "9999") + "-" + to_string(get_month(datum) , "99") + "-" + to_string(get_day(datum) , "99") and data_list.rmrev == 0), next=True)

    for data_list in query(data_list_data, sort_by=[("recordcount",True)]):
        data_count = data_list.recordcount
        break

    return generate_output()