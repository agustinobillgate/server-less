#using conversion tools version: 1.0.0.117
"""_yusufwijasena_22-10-2025

    TicketID: 698860
        _remark_:   - changed import from functions to functions_py
                    - character_conversionbl not found
                    - fix var declation
                    - changed string to str
                    - fix UPPER to substring().upper()
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
# from functions.calc_servtaxesbl import calc_servtaxesbl
# from functions.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
# from functions.calc_servvat import calc_servvat
# from functions.character_conversionbl import character_conversionbl
from functions_py.calc_servtaxesbl import calc_servtaxesbl
from functions_py.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
from functions_py.calc_servvat import calc_servvat
from functions_py.character_conversionbl import character_conversionbl
from models import Guest, H_artikel, Queasy, Htparam, Hoteldpt, Genstat, Reservation, Res_line, Bill, Zimkateg, Sourccod, Segment, Waehrung, Arrangement, Artikel, H_bill, H_bill_line, Bill_line

crm_data_data, Crm_data = create_model(
    "Crm_data", {
        "resid":str, 
        "guestid":int, 
        "ota_bookingid":str, 
        "salutation":str, 
        "firstname":str, 
        "lastname":str, 
        "email":str,
        "dob":str,
        "idcard_type":str,
        "idcard_num":str,
        "phonenumber":str,
        "arrdate":str,
        "depdate":str,
        "nights":int,
        "res_status":str,
        "ratecode":str,
        "roomtype":str,
        "zinr":str,
        "booksource":str,
        "marketsegment":str,
        "roomprice":Decimal,
        "taxes":Decimal,
        "currency":str,
        "countrycode":str,
        "nationcode":str,
        "otacode":str,
        "otaname":str,
        "propid":str,
        "confno":str,
        "recordcount":int,
        "gdpr_flag":str,
        "marketing":str,
        "newsletter":str,
        "occupation":str,
        "vip":bool,
        "city":str,
        "gender":str,
        "billfbrev":Decimal,
        "grossbillfb":Decimal,
        "billotherrev":Decimal,
        "grossbillother":Decimal,
        "profilecreated":str,
        "crm__id":str,
        "address":str,
        "outletname":str,
        "rateelement":str,
        "rig":str,
        "billno":str
        }
    )

def ascottrpt_crmbl(fdate:date, tdate:date, propid:str, rig:str, crm_data_data:Crm_data):

    prepare_cache ([Guest, H_artikel, Queasy, Htparam, Hoteldpt, Genstat, Reservation, Res_line, Bill, Zimkateg, Sourccod, Segment, Waehrung, Arrangement, Artikel, H_bill, H_bill_line, Bill_line])

    crm_count = 0
    tempdate:date 
    p_87:date 
    datum1:date 
    tdate1:date 
    tdate2:date 
    arrmonth = ""
    depmonth = ""
    dobmonth = ""
    arrmonthint:int = 0
    depmonthint:int = 0
    loop_i:int = 0
    str = ""
    contcode = ""
    service = to_decimal("0.0")
    serv = to_decimal("0.0")
    vat = to_decimal("0.0")
    vat1 = to_decimal("0.0")
    fact1 = to_decimal("0.0")
    tax_included:bool = False
    calc_nights:bool = False
    gdprflag = ""
    marketingflag = ""
    newsletterflag = ""
    vouchernum = ""
    deptname = "NULL"
    count1:int = 0
    betragvalue = to_decimal("0.0")
    grossbetrag = to_decimal("0.0")
    newbetrag = to_decimal("0.0")
    billflag:bool = False
    flag_artnr:bool = False
    billno:int = 0
    totalfb = to_decimal("0.0")
    totgrossfb = to_decimal("0.0")
    totalother = to_decimal("0.0")
    totgrossother = to_decimal("0.0")
    flodging = to_decimal("0.0")
    lodging = to_decimal("0.0")
    breakfast = to_decimal("0.0")
    lunch = to_decimal("0.0")
    dinner = to_decimal("0.0")
    others = to_decimal("0.0")
    rmrate = to_decimal("0.0")
    net_vat = to_decimal("0.0")
    net_service = to_decimal("0.0")
    totrevincl = to_decimal("0.0")
    totrevexcl = to_decimal("0.0")
    totfbincl = to_decimal("0.0")
    totfbexcl = to_decimal("0.0")
    tototherincl = to_decimal("0.0")
    tototherexcl = to_decimal("0.0")
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    vipflag = ""
    longcharoutput = ""
    guest = h_artikel = queasy = htparam = hoteldpt = genstat = reservation = res_line = bill = zimkateg = sourccod = segment = waehrung = arrangement = artikel = h_bill = h_bill_line = bill_line = None

    crm_data = guest_ota = buffart = qsy231 = qsy289 = None

    Guest_ota = create_buffer("Guest_ota",Guest)
    Buffart = create_buffer("Buffart",H_artikel)
    Qsy231 = create_buffer("Qsy231",Queasy)
    Qsy289 = create_buffer("Qsy289",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        return {"crm-data": crm_data_data, "crm_count": crm_count}

    def assign_genstat_values(genstat_casetyp:int):
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        calc_nights = False

        crm_data = query(crm_data_data, filters=(lambda crm_data: crm_data.resid == to_string(genstat.resnr) + to_string(genstat.res_int[0], "999")), first=True)

        if not crm_data:
            arrmonth = month_tostring(get_month(genstat.res_date[0]))
            depmonth = month_tostring(get_month(genstat.res_date[1]))
            gdprflag = "NO"
            marketingflag = "NO"
            newsletterflag = "NO"
            vouchernum = "NULL"
            # for loop_i in range(1,num_entries(genstat.res_char[1], ";") - 1 + 1) :
            for loop_i in range(1,num_entries(genstat.res_char[1], ";")) :
                str = entry(loop_i - 1, genstat.res_char[1], ";")

                # if substring(str, 0, 7) == ("voucher").lower() :
                #     vouchernum = substring(str, 7)

                # if substring(str, 0, 6) == ("$CODE$").lower() :
                #     contcode = substring(str, 6)

                # if substring(str, 0, 4) == ("GDPR").lower() :
                #     gdprflag = UPPER (substring(str, 4))

                # if substring(str, 0, 9) == ("MARKETING").lower() :
                #     marketingflag = UPPER (substring(str, 9))

                # if substring(str, 0, 10) == ("NEWSLETTER").lower() :
                #     newsletterflag = UPPER (substring(str, 10))
                if substring(str, 0, 7) == "voucher" :
                    vouchernum = substring(str, 7)

                if substring(str, 0, 6) == "$code$" :
                    contcode = substring(str, 6)

                if substring(str, 0, 4) == "gdpr" :
                    gdprflag = substring(str, 4).upper()

                if substring(str, 0, 9) == "marketing" :
                    marketingflag = substring(str, 9).upper()

                if substring(str, 0, 10) == "newsletter" :
                    newsletterflag = substring(str, 10).upper()
                    
            count1 = count1 + 1
            crm_data = Crm_data()
            crm_data_data.append(crm_data)

            crm_data.propid = propid
            crm_data.rig = rig
            crm_data.confno = to_string(genstat.resnr) + to_string(genstat.res_int[0], "999")
            crm_data.resid = to_string(genstat.resnr) + to_string(genstat.res_int[0], "999")
            crm_data.arrdate = to_string(get_day(genstat.res_date[0]) , "99") + "/" + to_string(get_month(genstat.res_date[0]) , "99") + "/" + to_string(get_year(genstat.res_date[0]) , "9999")
            crm_data.depdate = to_string(get_day(genstat.res_date[1]) , "99") + "/" + to_string(get_month(genstat.res_date[1]) , "99") + "/" + to_string(get_year(genstat.res_date[1]) , "9999")
            crm_data.nights = (genstat.res_date[1] - genstat.res_date[0]).days
            crm_data.zinr = genstat.zinr
            crm_data.recordcount = count1
            crm_data.outletname = deptname

            if genstat_casetyp == 1:
                if genstat.resstatus == 1 or genstat.resstatus == 2 or genstat.resstatus == 3 or genstat.resstatus == 4 or genstat.resstatus == 5 or genstat.resstatus == 11:
                    crm_data.res_status = "Reserved"

                elif genstat.resstatus == 6 or genstat.resstatus == 12 or genstat.resstatus == 13:
                    crm_data.res_status = "InHouse"

                elif genstat.resstatus == 8:
                    crm_data.res_status = "CheckedOut"

                elif genstat.resstatus == 9:
                    crm_data.res_status = "Cancelled"

                elif genstat.resstatus == 10:
                    crm_data.res_status = "NoShow"
                else:
                    crm_data.res_status = "Undefined-" + to_string(genstat.resstatus)

                res_line = get_cache (Res_line, {
                    "resnr": [(eq, genstat.resnr)],
                    "reslinnr": [(eq, genstat.res_int[0])]})

                if res_line:
                    gdprflag = "NO"
                    marketingflag = "NO"
                    newsletterflag = "NO"
                    # for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";")) :
                        str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                        # if substring(str, 0, 7) == ("voucher").lower() :
                        #     vouchernum = substring(str, 7)

                        # if substring(str, 0, 6) == ("$CODE$").lower() :
                        #     contcode = substring(str, 6)

                        # if substring(str, 0, 4) == ("GDPR").lower() :
                        #     gdprflag = UPPER (substring(str, 4))

                        # if substring(str, 0, 9) == ("MARKETING").lower() :
                        #     marketingflag = UPPER (substring(str, 9))

                        # if substring(str, 0, 10) == ("NEWSLETTER").lower() :
                        #     newsletterflag = UPPER (substring(str, 10))
                        if substring(str, 0, 7) == "voucher" :
                            vouchernum = substring(str, 7)

                        if substring(str, 0, 6) == "$code$" :
                            contcode = substring(str, 6)

                        if substring(str, 0, 4) == "gdpr" :
                            gdprflag = substring(str, 4).upper()

                        if substring(str, 0, 9) == "marketing" :
                            marketingflag = substring(str, 9).upper()

                        if substring(str, 0, 10) == "newsletter" :
                            newsletterflag = substring(str, 10).upper()

                bill = get_cache (Bill, {
                    "resnr": [(eq, genstat.resnr)],
                    "parent_nr": [(eq, genstat.res_int[0])]})

                if bill:
                    crm_data.billno = to_string(bill.rechnr)

            else:
                if res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 3 or res_line.resstatus == 4 or res_line.resstatus == 5 or res_line.resstatus == 11:
                    crm_data.res_status = "Reserved"

                elif res_line.resstatus == 6 or res_line.resstatus == 12 or res_line.resstatus == 13:
                    crm_data.res_status = "InHouse"

                elif res_line.resstatus == 8:
                    crm_data.res_status = "CheckedOut"

                elif res_line.resstatus == 9:
                    crm_data.res_status = "Cancelled"

                elif res_line.resstatus == 10:
                    crm_data.res_status = "NoShow"
                else:
                    crm_data.res_status = "Undefined-" + to_string(res_line.resstatus)
                arrmonth = month_tostring(get_month(res_line.ankunft))
                depmonth = month_tostring(get_month(res_line.abreise))
                crm_data.arrdate = to_string(get_day(res_line.ankunft) , "99") + "/" + to_string(get_month(res_line.ankunft) , "99") + "/" + to_string(get_year(res_line.ankunft) , "9999")
                crm_data.depdate = to_string(get_day(res_line.abreise) , "99") + "/" + to_string(get_month(res_line.abreise) , "99") + "/" + to_string(get_year(res_line.abreise) , "9999")
                crm_data.nights = (res_line.abreise - res_line.ankunft).days
                gdprflag = "NO"
                marketingflag = "NO"
                newsletterflag = "NO"
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    # if substring(str, 0, 7) == ("voucher").lower() :
                    #     vouchernum = substring(str, 7)

                    # if substring(str, 0, 6) == ("$CODE$").lower() :
                    #     contcode = substring(str, 6)

                    # if substring(str, 0, 4) == ("GDPR").lower() :
                    #     gdprflag = UPPER (substring(str, 4))

                    # if substring(str, 0, 9) == ("MARKETING").lower() :
                    #     marketingflag = UPPER (substring(str, 9))

                    # if substring(str, 0, 10) == ("NEWSLETTER").lower() :
                    #     newsletterflag = UPPER (substring(str, 10))
                    if substring(str, 0, 7) == "voucher" :
                        vouchernum = substring(str, 7)

                    if substring(str, 0, 6) == "$code$" :
                        contcode = substring(str, 6)

                    if substring(str, 0, 4) == "gdpr" :
                        gdprflag = substring(str, 4).upper()

                    if substring(str, 0, 9) == "marketing" :
                        marketingflag = substring(str, 9).upper()

                    if substring(str, 0, 10) == "newsletter" :
                        newsletterflag = substring(str, 10).upper()

                bill = get_cache (Bill, {
                    "resnr": [(eq, res_line.resnr)],
                    "parent_nr": [(eq, res_line.resnr)]})

                if bill:
                    crm_data.billno = to_string(bill.rechnr)

            crm_data.gdpr_flag = gdprflag
            crm_data.marketing = marketingflag
            crm_data.newsletter = newsletterflag
            crm_data.ota_bookingid = vouchernum

            if contcode != "":
                crm_data.ratecode = contcode

                qsy289 = get_cache (Queasy, {
                    "key": [(eq, 289)],
                    "char1": [(eq, crm_data.ratecode)]})

                if qsy289:
                    crm_data.rateelement = qsy289.char2

            else:
                crm_data.ratecode = "NULL"
                crm_data.rateelement = "NULL"

            guest = get_cache (Guest, {"gastnr": [(eq, genstat.gastnrmember)]})

            if guest:
                dobmonth = month_tostring(get_month(guest.geburtdatum1))

                if guest.geburtdatum1 != None:

                    if get_year(guest.geburtdatum1) >= (get_year(get_current_date()) - 100) and get_year(guest.geburtdatum1) <= get_year(get_current_date()):
                        crm_data.dob = to_string(get_day(guest.geburtdatum1)) + "-" + dobmonth + "-" + to_string(get_year(guest.geburtdatum1) , "9999")
                    else:
                        crm_data.dob = "NULL"
                else:
                    crm_data.dob = "NULL"

                if guest.vorname1 != "":
                    crm_data.firstname = guest.vorname1
                else:
                    crm_data.firstname = "NULL"

                if guest.name != "":
                    crm_data.lastname = guest.name
                else:
                    crm_data.lastname = "NULL"

                if guest.anrede1 != "":
                    crm_data.salutation = guest.anrede1
                else:
                    crm_data.salutation = "NULL"
                    
                crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(34) , "")
                crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(35) , "")
                crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(42) , "")
                crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(47) , "")
                crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(34) , "")
                crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(35) , "")
                crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(42) , "")
                crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(47) , "")

                if guest.email_adr != "":
                    crm_data.email = guest.email_adr
                    crm_data.email = replace_str(crm_data.email, chr_unicode(10) , " ")
                    crm_data.email = replace_str(crm_data.email, chr_unicode(13) , " ")
                    crm_data.email = replace_str(crm_data.email, chr_unicode(34) , "")
                    crm_data.email = replace_str(crm_data.email, chr_unicode(39) , "")
                    crm_data.email = replace_str(crm_data.email, chr_unicode(92) , chr_unicode(47))
                    crm_data.email = replace_str(crm_data.email, chr_unicode(35) , "")
                    crm_data.email = replace_str(crm_data.email, chr_unicode(42) , "")
                    crm_data.email = replace_str(crm_data.email, chr_unicode(47) , "")
                else:
                    crm_data.email = "NULL"

                if guest.geburt_ort1 != "":
                    crm_data.idcard_type = guest.geburt_ort1
                else:
                    crm_data.idcard_type = "NULL"

                if guest.ausweis_nr1 != "":
                    crm_data.idcard_num = guest.ausweis_nr1
                else:
                    crm_data.idcard_num = "NULL"

                # if guest.geschlecht.lower()  == ("M").lower() :
                #     crm_data.gender = "Male"

                # elif guest.geschlecht.lower()  == ("F").lower() :
                #     crm_data.gender = "Female"
                if guest.geschlecht.lower()  == "m" :
                    crm_data.gender = "Male"

                elif guest.geschlecht.lower()  == "f" :
                    crm_data.gender = "Female"
                else:
                    crm_data.gender = "NULL"

                if guest.wohnort != "":
                    crm_data.city = guest.wohnort
                else:
                    crm_data.city = "NULL"

                if guest.land != "":
                    crm_data.countrycode = guest.land
                else:
                    crm_data.countrycode = "NULL"

                if guest.nation1 != "":
                    crm_data.nationcode = guest.nation1
                else:
                    crm_data.nationcode = "NULL"

                if guest.beruf != "":
                    crm_data.occupation = guest.beruf
                else:
                    crm_data.occupation = "NULL"

                if guest.mobil_telefon != "":
                    crm_data.phonenumber = guest.mobil_telefon

                elif guest.mobil_telefon == "" and guest.telefon != "":
                    crm_data.phonenumber = guest.telefon
                else:
                    crm_data.phonenumber = "NULL"
                    
                crm_data.guestid = guest.gastnr
                crm_data.profilecreated = to_string(get_year(guest.anlage_datum) , "9999") + "-" + to_string(get_month(guest.anlage_datum) , "99") + "-" + to_string(get_day(guest.anlage_datum) , "99") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
                crm_data.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
                
            crm_data.crm__id = "NULL"

            guest_ota = get_cache (Guest, {"gastnr": [(eq, genstat.gastnr)]})

            if guest_ota:
                if guest_ota.karteityp == 2:
                    crm_data.otaname = guest_ota.name
                    crm_data.otacode = trim(entry(0, guest_ota.steuernr, "|"))

                    if crm_data.otacode == "":
                        crm_data.otacode = "NULL"
                else:
                    crm_data.otaname = "NULL"
                    crm_data.otacode = "NULL"

                qsy231 = get_cache (Queasy, {
                    "key": [(eq, 231)],
                    "number1": [(eq, guest_ota.gastnr)]})

                if qsy231:
                    crm_data.crm__id = qsy231.char1

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, genstat.zikatnr)]})

            if zimkateg:
                crm_data.roomtype = zimkateg.kurzbez

            reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

            if reservation:

                sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                if sourccod:
                    crm_data.booksource = sourccod.bezeich
                else:
                    crm_data.booksource = "NULL"

                # if reservation.vesrdepot != "" and crm_data.ota_bookingid.lower()  == ("NULL").lower() :
                if reservation.vesrdepot != "" and crm_data.ota_bookingid.lower()  == "null" :
                    crm_data.ota_bookingid = reservation.vesrdepot

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    crm_data.marketsegment = segment.bezeich
                else:
                    crm_data.marketsegment = "NULL"

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, genstat.wahrungsnr)]})

            if waehrung:
                crm_data.currency = waehrung.wabkurz

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

            if arrangement:
                artikel = get_cache (Artikel, {
                    "artnr": [(eq, arrangement.argt_artikelnr)],
                    "departement": [(eq, 0)]})

                if artikel:
                    serv, vat, vat1, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                if tax_included:
                    crm_data.roomprice =  to_decimal(genstat.logis)
                    crm_data.billfbrev =  to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                    crm_data.grossbillfb = to_decimal(round((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) * (1 + serv + vat + vat1) , 0))
                    crm_data.billotherrev =  to_decimal(genstat.res_deci[4])
                    crm_data.grossbillother = to_decimal(round(genstat.res_deci[4] * (1 + serv + vat + vat1) , 0))
                    crm_data.taxes = (to_decimal((round(to_decimal(genstat.logis) * (1 + serv + vat + vat1) , 0)) - genstat.logis) + (crm_data.grossbillfb - crm_data.billfbrev) + (crm_data.grossbillother - crm_data.billotherrev))
                else:
                    crm_data.roomprice = to_decimal(round(to_decimal(genstat.logis) / (1 + serv + vat + vat1) , 0))
                    crm_data.billfbrev = to_decimal(round((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / (1 + serv + vat + vat1) , 0))
                    crm_data.grossbillfb =  to_decimal(genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                    crm_data.billotherrev = to_decimal(round(genstat.res_deci[4] / (1 + serv + vat + vat1) , 0))
                    crm_data.grossbillother =  to_decimal(genstat.res_deci[4])
                    crm_data.taxes = (to_decimal(genstat.logis - (round(to_decimal(genstat.logis) / (1 + serv + vat + vat1) , 0))) + (crm_data.grossbillfb - crm_data.billfbrev) + (crm_data.grossbillother - crm_data.billotherrev))

            res_line = get_cache (Res_line, {
                "resnr": [(eq, genstat.resnr)],
                "reslinnr": [(eq, genstat.res_int[0])]})

            if res_line:
                if res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9:
                    vipflag = "V"

            if vipflag.lower()  == "v" :
                crm_data.vip = True
            else:
                crm_data.vip = False
        else:
            if genstat_casetyp == 1:
                arrmonth = month_tostring(get_month(genstat.res_date[0]))
                depmonth = month_tostring(get_month(genstat.res_date[1]))
                arrmonthint = string_tomonthint(entry(1, crm_data.depdate, "-"))
                depmonthint = string_tomonthint(entry(1, crm_data.depdate, "-"))
                tempdate = date_mdy(arrmonthint, to_int(entry(0, crm_data.arrdate, "/")) , to_int(entry(2, crm_data.arrdate, "/")))
                tdate1 = tempdate

                if genstat.res_date[0] < tempdate:
                    tdate1 = genstat.res_date[0]
                    calc_nights = True
                    crm_data.arrdate = to_string(get_day(genstat.res_date[0]) , "99") + "/" + to_string(get_month(genstat.res_date[0]) , "99") + "/" + to_string(get_year(genstat.res_date[0]) , "9999")
                tempdate = date_mdy(depmonthint, to_int(entry(0, crm_data.depdate, "/")) , to_int(entry(2, crm_data.depdate, "/")))
                tdate2 = tempdate

                if genstat.res_date[1] > tempdate:
                    tdate2 = genstat.res_date[1]
                    calc_nights = True
                    crm_data.depdate = to_string(get_day(genstat.res_date[1]) , "99") + "/" + to_string(get_month(genstat.res_date[1]) , "99") + "/" + to_string(get_year(genstat.res_date[1]) , "9999")

                if calc_nights:
                    crm_data.nights = (tdate2 - tdate1).days
                calc_nights = False

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, genstat.argt)]})

            if arrangement:
                artikel = get_cache (Artikel, {
                    "artnr": [(eq, arrangement.argt_artikelnr)],
                    "departement": [(eq, 0)]})

                if artikel:
                    serv, vat, vat1, fact1 = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, genstat.datum))

                if tax_included:
                    crm_data.roomprice =  to_decimal(crm_data.roomprice + genstat.logis)
                    crm_data.billfbrev =  to_decimal(crm_data.billfbrev + genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                    crm_data.grossbillfb = to_decimal(crm_data.grossbillfb + round((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) * (1 + serv + vat + vat1) , 0))
                    crm_data.billotherrev =  to_decimal(crm_data.billotherrev + genstat.res_deci[4])
                    crm_data.grossbillother = to_decimal(crm_data.grossbillother + round(genstat.res_deci[4] * (1 + serv + vat + vat1) , 0))
                    crm_data.taxes = to_decimal(crm_data.taxes + ((round(to_decimal(genstat.logis) * (1 + serv + vat + vat1) , 0)) - genstat.logis) + ((round((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) * (1 + serv + vat + vat1) , 0)) - (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])) + ((round(genstat.res_deci[4] * (1 + serv + vat + vat1) , 0)) - (genstat.res_deci[4])))
                else:
                    crm_data.roomprice = to_decimal(crm_data.roomprice + round(to_decimal(genstat.logis) / (1 + serv + vat + vat1) , 0))
                    crm_data.billfbrev = to_decimal(crm_data.billfbrev + round((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) / (1 + serv + vat + vat1) , 0))
                    crm_data.grossbillfb =  to_decimal(crm_data.grossbillfb + genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])
                    crm_data.billotherrev = to_decimal(crm_data.billotherrev + round(genstat.res_deci[4] / (1 + serv + vat + vat1) , 0))
                    crm_data.grossbillother =  to_decimal(crm_data.grossbillother + genstat.res_deci[4])
                    crm_data.taxes = to_decimal(crm_data.taxes + ((genstat.logis - (round(to_decimal(genstat.logis) / (1 + serv + vat + vat1) , 0)))) + ((round((genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3]) * (1 + serv + vat + vat1) , 0)) - (genstat.res_deci[1] + genstat.res_deci[2] + genstat.res_deci[3])) + ((round(genstat.res_deci[4] * (1 + serv + vat + vat1) , 0)) - (genstat.res_deci[4])))

            reservation = get_cache (Reservation, {"resnr": [(eq, genstat.resnr)]})

            if reservation:
                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    crm_data.marketsegment = segment.bezeich
                else:
                    crm_data.marketsegment = "NULL"
        verifynullvalues()


    def assign_resline_values(rsvstat:string):
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        calc_nights = False
        arrmonth = month_tostring(get_month(res_line.ankunft))
        depmonth = month_tostring(get_month(res_line.abreise))
        gdprflag = "NO"
        marketingflag = "NO"
        newsletterflag = "NO"
        vouchernum = "NULL"
        for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

            # if substring(str, 0, 7) == ("voucher").lower() :
            #     vouchernum = substring(str, 7)

            # if substring(str, 0, 6) == ("$CODE$").lower() :
            #     contcode = substring(str, 6)

            # if substring(str, 0, 4) == ("GDPR").lower() :
            #     gdprflag = UPPER (substring(str, 4))

            # if substring(str, 0, 9) == ("MARKETING").lower() :
            #     marketingflag = UPPER (substring(str, 9))

            # if substring(str, 0, 10) == ("NEWSLETTER").lower() :
            #     newsletterflag = UPPER (substring(str, 10))
            if substring(str, 0, 7) == "voucher" :
                vouchernum = substring(str, 7)

            if substring(str, 0, 6) == "$code$" :
                contcode = substring(str, 6)

            if substring(str, 0, 4) == "gdpr" :
                gdprflag = substring(str, 4).upper()

            if substring(str, 0, 9) == "marketing" :
                marketingflag = substring(str, 9).upper()

            if substring(str, 0, 10) == "newsletter" :
                newsletterflag = substring(str, 10).upper()
                
        count1 = count1 + 1
        crm_data = Crm_data()
        crm_data_data.append(crm_data)

        crm_data.propid = propid
        crm_data.rig = rig
        crm_data.confno = to_string(res_line.resnr + res_line.reslinnr, "999")
        crm_data.resid = to_string(res_line.resnr + res_line.reslinnr, "999")
        crm_data.arrdate = to_string(get_day(res_line.ankunft) , "99") + "/" + to_string(get_month(res_line.ankunft) , "99") + "/" + to_string(get_year(res_line.ankunft) , "9999")
        crm_data.depdate = to_string(get_day(res_line.abreise) , "99") + "/" + to_string(get_month(res_line.abreise) , "99") + "/" + to_string(get_year(res_line.abreise) , "9999")
        crm_data.nights = (res_line.abreise - res_line.ankunft).days
        crm_data.zinr = res_line.zinr
        crm_data.recordcount = count1
        crm_data.gdpr_flag = gdprflag
        crm_data.marketing = marketingflag
        crm_data.newsletter = newsletterflag
        crm_data.ota_bookingid = vouchernum
        crm_data.outletname = deptname

        if res_line.resstatus == 1 or res_line.resstatus == 2 or res_line.resstatus == 3 or res_line.resstatus == 4 or res_line.resstatus == 5 or res_line.resstatus == 11:
            crm_data.res_status = "Reserved"

        elif res_line.resstatus == 6 or res_line.resstatus == 12 or res_line.resstatus == 13:
            crm_data.res_status = "InHouse"

        elif res_line.resstatus == 8:
            crm_data.res_status = "CheckedOut"

        elif res_line.resstatus == 9:
            crm_data.res_status = "Cancelled"

        elif res_line.resstatus == 10:
            crm_data.res_status = "NoShow"
        else:
            crm_data.res_status = "Undefined-" + to_string(res_line.resstatus)

        if rsvstat != "":
            crm_data.res_status = rsvstat

        if contcode != "":
            crm_data.ratecode = contcode

            qsy289 = get_cache (Queasy, {
                "key": [(eq, 289)],
                "char1": [(eq, crm_data.ratecode)]})

            if qsy289:
                crm_data.rateelement = qsy289.char2


        else:
            crm_data.ratecode = "NULL"
            crm_data.rateelement = "NULL"

        bill = get_cache (Bill, {
            "resnr": [(eq, res_line.resnr)],
            "parent_nr": [(eq, res_line.resnr)]})

        if bill:
            crm_data.billno = to_string(bill.rechnr)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            dobmonth = month_tostring(get_month(guest.geburtdatum1))

            if guest.geburtdatum1 != None:
                if get_year(guest.geburtdatum1) >= (get_year(get_current_date()) - 100) and get_year(guest.geburtdatum1) <= get_year(get_current_date()):
                    crm_data.dob = to_string(get_day(guest.geburtdatum1) , "99") + "-" + dobmonth + "-" + to_string(get_year(guest.geburtdatum1) , "9999")
                else:
                    crm_data.dob = "NULL"
            else:
                crm_data.dob = "NULL"

            if guest.vorname1 != "":
                crm_data.firstname = guest.vorname1
            else:
                crm_data.firstname = "NULL"

            if guest.name != "":
                crm_data.lastname = guest.name
            else:
                crm_data.lastname = "NULL"

            if guest.anrede1 != "":
                crm_data.salutation = guest.anrede1
            else:
                crm_data.salutation = "NULL"
                
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(34) , "")
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(35) , "")
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(42) , "")
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(47) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(34) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(35) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(42) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(47) , "")

            if guest.email_adr != "":
                crm_data.email = guest.email_adr
                crm_data.email = replace_str(crm_data.email, chr_unicode(10) , " ")
                crm_data.email = replace_str(crm_data.email, chr_unicode(13) , " ")
                crm_data.email = replace_str(crm_data.email, chr_unicode(34) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(39) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(92) , chr_unicode(47))
                crm_data.email = replace_str(crm_data.email, chr_unicode(35) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(42) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(47) , "")
            else:
                crm_data.email = "NULL"

            if guest.geburt_ort1 != "":
                crm_data.idcard_type = guest.geburt_ort1
            else:
                crm_data.idcard_type = "NULL"

            if guest.ausweis_nr1 != "":
                crm_data.idcard_num = guest.ausweis_nr1
            else:
                crm_data.idcard_num = "NULL"

            if guest.geschlecht.lower()  == "m" :
                crm_data.gender = "Male"

            elif guest.geschlecht.lower()  == "f" :
                crm_data.gender = "Female"
            else:
                crm_data.gender = "NULL"

            if guest.wohnort != "":
                crm_data.city = guest.wohnort
            else:
                crm_data.city = "NULL"

            if guest.land != "":
                crm_data.countrycode = guest.land
            else:
                crm_data.countrycode = "NULL"

            if guest.nation1 != "":
                crm_data.nationcode = guest.nation1
            else:
                crm_data.nationcode = "NULL"

            if guest.beruf != "":
                crm_data.occupation = guest.beruf
            else:
                crm_data.occupation = "NULL"

            if guest.mobil_telefon != "":
                crm_data.phonenumber = guest.mobil_telefon

            elif guest.mobil_telefon == "" and guest.telefon != "":
                crm_data.phonenumber = guest.telefon
            else:
                crm_data.phonenumber = "NULL"
                
            crm_data.guestid = guest.gastnr
            crm_data.profilecreated = to_string(get_year(guest.anlage_datum) , "9999") + "-" + to_string(get_month(guest.anlage_datum) , "99") + "-" + to_string(get_day(guest.anlage_datum) , "99") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
            crm_data.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
        crm_data.crm__id = "NULL"

        guest_ota = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        if guest_ota:
            if guest_ota.karteityp == 2:
                crm_data.otaname = guest_ota.name
                crm_data.otacode = trim(entry(0, guest_ota.steuernr, "|"))

                if crm_data.otacode == "":
                    crm_data.otacode = "NULL"
            else:
                crm_data.otaname = "NULL"
                crm_data.otacode = "NULL"

            qsy231 = get_cache (Queasy, {
                "key": [(eq, 231)],
                "number1": [(eq, guest_ota.gastnr)]})

            if qsy231:
                crm_data.crm__id = qsy231.char1

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            crm_data.roomtype = zimkateg.kurzbez

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if reservation:
            sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

            if sourccod:
                crm_data.booksource = sourccod.bezeich
            else:
                crm_data.booksource = "NULL"

            if reservation.vesrdepot != "" and crm_data.ota_bookingid.lower()  == "null" :
                crm_data.ota_bookingid = reservation.vesrdepot

            genstat = get_cache (Genstat, {"datum": [(eq, fdate)],"resnr": [(eq, reservation.resnr)]})

            if genstat:
                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    crm_data.marketsegment = segment.bezeich
                else:
                    crm_data.marketsegment = "NULL"
            else:
                crm_data.marketsegment = "NULL"

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if waehrung:
            crm_data.currency = waehrung.wabkurz
            
        totrevincl =  to_decimal("0")
        totrevexcl =  to_decimal("0")
        totfbincl =  to_decimal("0")
        totfbexcl =  to_decimal("0")
        tototherincl =  to_decimal("0")
        tototherexcl =  to_decimal("0")
        
        for datum1 in date_range(res_line.ankunft,res_line.abreise - 1) :
            lodging =  to_decimal("0")
            breakfast =  to_decimal("0")
            lunch =  to_decimal("0")
            dinner =  to_decimal("0")
            others =  to_decimal("0")
            vat =  to_decimal("0")
            serv =  to_decimal("0")

            flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, serv = get_output(ghs_get_room_breakdownbl(res_line._recid, datum1, 1, fdate))
            
            totrevincl =  to_decimal(totrevincl + lodging)
            totrevexcl =  to_decimal(totrevexcl + (lodging / (to_decimal(1) + vat + serv)))
            totfbincl =  to_decimal(totfbincl + breakfast + lunch + dinner)
            totfbexcl =  to_decimal(totfbexcl + ((breakfast + lunch + dinner) / (to_decimal(1) + vat + serv)))
            tototherincl =  to_decimal(tototherincl + others)
            tototherexcl =  to_decimal(tototherexcl + (others / (to_decimal(1) + vat + serv)))
            
        crm_data.roomprice = to_decimal(round(totrevexcl , 0))
        crm_data.billfbrev = to_decimal(round(totfbexcl , 0))
        crm_data.grossbillfb = to_decimal(round(totfbincl , 0))
        crm_data.billotherrev = to_decimal(round(tototherexcl , 0))
        crm_data.grossbillother = to_decimal(round(tototherincl , 0))
        crm_data.taxes = to_decimal(round(totrevincl , 0) - round(totrevexcl , 0) + (crm_data.grossbillfb - crm_data.billfbrev) + (crm_data.grossbillother - crm_data.billotherrev))

        if res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9:
            vipflag = "V"

        if vipflag.lower()  == "v" :
            crm_data.vip = True
        else:
            crm_data.vip = False
        verifynullvalues()


    def string_tomonthint(inmonth:string):
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        outmonth = 0

        def generate_inner_output():
            return (outmonth)

        if inmonth.lower()  == "jan" :
            outmonth = 1

        elif inmonth.lower()  == "feb" :
            outmonth = 2

        elif inmonth.lower()  == "mar" :
            outmonth = 3

        elif inmonth.lower()  == "apr" :
            outmonth = 4

        elif inmonth.lower()  == "may" :
            outmonth = 5

        elif inmonth.lower()  == "jun" :
            outmonth = 6

        elif inmonth.lower()  == "jul" :
            outmonth = 7

        elif inmonth.lower()  == "aug" :
            outmonth = 8

        elif inmonth.lower()  == "sep" :
            outmonth = 9

        elif inmonth.lower()  == "oct" :
            outmonth = 10

        elif inmonth.lower()  == "nov" :
            outmonth = 11

        elif inmonth.lower()  == "dec" :
            outmonth = 12

        return generate_inner_output()

    def month_tostring(inpmonth:int):
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        strmonth = ""

        def generate_inner_output():
            return (strmonth)

        if inpmonth == 1:
            strmonth = "Jan"

        elif inpmonth == 2:
            strmonth = "Feb"

        elif inpmonth == 3:
            strmonth = "Mar"

        elif inpmonth == 4:
            strmonth = "Apr"

        elif inpmonth == 5:
            strmonth = "May"

        elif inpmonth == 6:
            strmonth = "Jun"

        elif inpmonth == 7:
            strmonth = "Jul"

        elif inpmonth == 8:
            strmonth = "Aug"

        elif inpmonth == 9:
            strmonth = "Sep"

        elif inpmonth == 10:
            strmonth = "Oct"

        elif inpmonth == 11:
            strmonth = "Nov"

        elif inpmonth == 12:
            strmonth = "Dec"

        return generate_inner_output()

    def deduct_taxes(department:string, artnum:int, billingdate:date, servicecode:int, mwstcode:int, inp_betrag:Decimal):
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        out_betrag = to_decimal("0.0")

        def generate_inner_output():
            return (out_betrag)

        service, vat = get_output(calc_servvat(department, artnum, billingdate, servicecode, mwstcode))
        out_betrag = to_decimal(round(to_decimal(inp_betrag / (1 + service + vat)) , 2))

        return generate_inner_output()

    def verifynullvalues():
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289


        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        if crm_data.resid == None:
            crm_data.resid = "NULL"

        if crm_data.guestid == None:
            crm_data.guestid = 0

        if crm_data.ota_bookingid == None:
            crm_data.ota_bookingid = "NULL"

        if crm_data.salutation == None:
            crm_data.salutation = "NULL"

        if crm_data.firstname == None:
            crm_data.firstname = "NULL"

        if crm_data.lastname == None:
            crm_data.lastname = "NULL"

        if crm_data.email == None:
            crm_data.email = "NULL"

        if crm_data.dob == None:
            crm_data.dob = "NULL"

        if crm_data.idcard_type == None:
            crm_data.idcard_type = "NULL"

        if crm_data.idcard_num == None:
            crm_data.idcard_num = "NULL"

        if crm_data.phonenumber == None:
            crm_data.phonenumber = "NULL"

        if crm_data.arrdate == None:
            crm_data.arrdate = "NULL"

        if crm_data.depdate == None:
            crm_data.depdate = "NULL"

        if crm_data.nights == None:
            crm_data.nights = 0

        if crm_data.res_status == None:
            crm_data.res_status = "NULL"

        if crm_data.ratecode == None:
            crm_data.ratecode = "NULL"

        if crm_data.roomtype == None:
            crm_data.roomtype = "NULL"

        if crm_data.zinr == None:
            crm_data.zinr = "NULL"

        if crm_data.booksource == None:
            crm_data.booksource = "NULL"

        if crm_data.marketsegment == None:
            crm_data.marketsegment = "NULL"

        if crm_data.roomprice == None:
            crm_data.roomprice =  to_decimal("0")

        if crm_data.taxes == None:
            crm_data.taxes =  to_decimal("0")

        if crm_data.currency == None:
            crm_data.currency = "NULL"

        if crm_data.countrycode == None:
            crm_data.countrycode = "NULL"

        if crm_data.nationcode == None:
            crm_data.nationcode = "NULL"

        if crm_data.otacode == None:
            crm_data.otacode = "NULL"

        if crm_data.otaname == None:
            crm_data.otaname = "NULL"

        if crm_data.propid == None:
            crm_data.propid = "NULL"

        if crm_data.confno == None:
            crm_data.confno = "NULL"

        if crm_data.recordcount == None:
            crm_data.recordcount = 0

        if crm_data.gdpr_flag == None:
            crm_data.gdpr_flag = "NULL"

        if crm_data.marketing == None:
            crm_data.marketing = "NULL"

        if crm_data.newsletter == None:
            crm_data.newsletter = "NULL"

        if crm_data.occupation == None:
            crm_data.occupation = "NULL"

        if crm_data.vip == None:
            crm_data.vip = False

        if crm_data.city == None:
            crm_data.city = "NULL"

        if crm_data.gender == None:
            crm_data.gender = "NULL"

        if crm_data.billfbrev == None:
            crm_data.billfbrev =  to_decimal("0")

        if crm_data.grossbillfb == None:
            crm_data.grossbillfb =  to_decimal("0")

        if crm_data.billotherrev == None:
            crm_data.billotherrev =  to_decimal("0")

        if crm_data.grossbillother == None:
            crm_data.grossbillother =  to_decimal("0")

        if crm_data.profilecreated == None:
            crm_data.profilecreated = "NULL"

        if crm_data.address == None:
            crm_data.address = "NULL"

        if crm_data.firstname.lower()  != "null" :
            crm_data.firstname, longcharoutput = get_output(character_conversionbl(crm_data.firstname, ""))

        if crm_data.lastname.lower()  != "null" :
            crm_data.lastname, longcharoutput = get_output(character_conversionbl(crm_data.lastname, ""))

        if crm_data.email.lower()  != "null" :
            crm_data.email, longcharoutput = get_output(character_conversionbl(crm_data.email, ""))


    def create_bill_list(bill_rechnr:int, bill_name:string, bill_guestid:int, bill_gastid2:int, bill_dept:int, bdate:date):
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        fname = ""
        lname = ""
        count1 = count1 + 1
        crm_data = Crm_data()
        crm_data_data.append(crm_data)

        crm_data.resid = "NULL"
        crm_data.guestid = 0
        crm_data.ota_bookingid = "NULL"
        crm_data.salutation = "NULL"
        crm_data.firstname = "NULL"
        crm_data.lastname = "NULL"
        crm_data.email = "NULL"
        crm_data.dob = "NULL"
        crm_data.idcard_type = "NULL"
        crm_data.idcard_num = "NULL"
        crm_data.phonenumber = "NULL"
        crm_data.arrdate = to_string(get_day(bdate) , "99") + "/" + to_string(get_month(bdate) , "99") + "/" + to_string(get_year(bdate) , "9999")
        crm_data.depdate = "NULL"
        crm_data.nights = 0
        crm_data.res_status = "NONSTAY"
        crm_data.ratecode = "NULL"
        crm_data.roomtype = "NULL"
        crm_data.zinr = "NULL"
        crm_data.booksource = "NULL"
        crm_data.marketsegment = "NULL"
        crm_data.roomprice =  to_decimal("0")
        crm_data.taxes =  to_decimal("0")
        crm_data.currency = "NULL"
        crm_data.countrycode = "NULL"
        crm_data.nationcode = "NULL"
        crm_data.otacode = "NULL"
        crm_data.otaname = "NULL"
        crm_data.propid = propid
        crm_data.confno = to_string(bill_rechnr)
        crm_data.recordcount = count1
        crm_data.gdpr_flag = "NULL"
        crm_data.marketing = "NULL"
        crm_data.newsletter = "NULL"
        crm_data.occupation = "NULL"
        crm_data.vip = False
        crm_data.city = "NULL"
        crm_data.gender = "NULL"
        crm_data.billfbrev =  to_decimal(totalfb)
        crm_data.grossbillfb =  to_decimal(totgrossfb)
        crm_data.billotherrev =  to_decimal(totalother)
        crm_data.grossbillother =  to_decimal(totgrossother)
        crm_data.profilecreated = "NULL"
        crm_data.address = "NULL"
        crm_data.outletname = "NULL"
        crm_data.billno = "NULL"
        crm_data.rateelement = "NULL"
        crm_data.rig = rig

        res_line = get_cache (Res_line, {
            "resnr": [(eq, bill_guestid)],
            "reslinnr": [(eq, bill_gastid2)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        crm_data.lastname = bill_name

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, bill_dept)]})

        if hoteldpt:
            crm_data.outletname = hoteldpt.depart

        if guest:
            dobmonth = month_tostring(get_month(guest.geburtdatum1))

            if guest.geburtdatum1 != None:

                if get_year(guest.geburtdatum1) >= (get_year(get_current_date()) - 100) and get_year(guest.geburtdatum1) <= get_year(get_current_date()):
                    crm_data.dob = to_string(get_day(guest.geburtdatum1)) + "-" + dobmonth + "-" + to_string(get_year(guest.geburtdatum1) , "9999")
                else:
                    crm_data.dob = "NULL"
            else:
                crm_data.dob = "NULL"

            if guest.vorname1 != "":
                crm_data.firstname = guest.vorname1
            else:
                crm_data.firstname = "NULL"

            if guest.name != "":
                crm_data.lastname = guest.name
            else:
                crm_data.lastname = "NULL"

            if guest.anrede1 != "":
                crm_data.salutation = guest.anrede1
            else:
                crm_data.salutation = "NULL"
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(34) , "")
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(35) , "")
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(42) , "")
            crm_data.firstname = replace_str(crm_data.firstname, chr_unicode(47) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(34) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(35) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(42) , "")
            crm_data.lastname = replace_str(crm_data.lastname, chr_unicode(47) , "")

            if guest.email_adr != "":
                crm_data.email = guest.email_adr
                crm_data.email = replace_str(crm_data.email, chr_unicode(10) , " ")
                crm_data.email = replace_str(crm_data.email, chr_unicode(13) , " ")
                crm_data.email = replace_str(crm_data.email, chr_unicode(34) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(39) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(92) , chr_unicode(47))
                crm_data.email = replace_str(crm_data.email, chr_unicode(35) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(42) , "")
                crm_data.email = replace_str(crm_data.email, chr_unicode(47) , "")
            else:
                crm_data.email = "NULL"

            if guest.geburt_ort1 != "":
                crm_data.idcard_type = guest.geburt_ort1
            else:
                crm_data.idcard_type = "NULL"

            if guest.ausweis_nr1 != "":
                crm_data.idcard_num = guest.ausweis_nr1
            else:
                crm_data.idcard_num = "NULL"

            if guest.geschlecht.lower()  == "m" :
                crm_data.gender = "Male"

            elif guest.geschlecht.lower()  == "f" :
                crm_data.gender = "Female"
            else:
                crm_data.gender = "NULL"

            if guest.wohnort != "":
                crm_data.city = guest.wohnort
            else:
                crm_data.city = "NULL"

            if guest.land != "":
                crm_data.countrycode = guest.land
            else:
                crm_data.countrycode = "NULL"

            if guest.nation1 != "":
                crm_data.nationcode = guest.nation1
            else:
                crm_data.nationcode = "NULL"

            if guest.beruf != "":
                crm_data.occupation = guest.beruf
            else:
                crm_data.occupation = "NULL"

            if guest.mobil_telefon != "":
                crm_data.phonenumber = guest.mobil_telefon

            elif guest.mobil_telefon == "" and guest.telefon != "":
                crm_data.phonenumber = guest.telefon
            else:
                crm_data.phonenumber = "NULL"
            crm_data.guestid = guest.gastnr
            crm_data.profilecreated = to_string(get_year(guest.anlage_datum) , "9999") + "-" + to_string(get_month(guest.anlage_datum) , "99") + "-" + to_string(get_day(guest.anlage_datum) , "99") + " " + to_string(get_current_time_in_seconds(), "HH:MM:SS")
            crm_data.address = guest.adresse1 + " " + guest.adresse2 + " " + guest.adresse3
        verifynullvalues()

    def pos_nonstay_bill():
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        for h_bill in db_session.query(H_bill).filter(
                (H_bill.rechnr > 0) & (H_bill.flag == 1)).order_by(H_bill._recid).all():
            totalfb =  to_decimal("0")
            totgrossfb =  to_decimal("0")
            totalother =  to_decimal("0")
            totgrossother =  to_decimal("0")
            flag_artnr = False

            for h_bill_line in db_session.query(H_bill_line).filter(
                    (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == fdate) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():

                h_artikel = get_cache (H_artikel, {"artnr": [(eq, h_bill_line.artnr)],"artart": [(eq, 0)],"departement": [(eq, h_bill_line.departement)]})

                if h_artikel:
                    if h_artikel.artart == 11 or h_artikel.artart == 12:
                        flag_artnr = True

            if flag_artnr == False:
                for h_bill_line in db_session.query(H_bill_line).filter(
                        (H_bill_line.rechnr == h_bill.rechnr) & (H_bill_line.bill_datum == fdate) & (H_bill_line.departement == h_bill.departement)).order_by(H_bill_line._recid).all():
                    billflag = False
                    for loop_i in range(1,length(h_bill_line.bezeich)  + 1) :
                        if substring(h_bill_line.bezeich, loop_i - 1, 1) == "*" :
                            loop_i = 999
                            billflag = True

                    if not billflag:
                        h_artikel = get_cache (H_artikel, {
                            "artnr": [(eq, h_bill_line.artnr)],
                            "artart": [(eq, 0)],
                            "departement": [(eq, h_bill_line.departement)]})

                        if h_artikel:
                            artikel = get_cache (Artikel, {
                                "artnr": [(eq, h_artikel.artnrfront)],
                                "departement": [(eq, h_artikel.departement)]})

                            if artikel:
                                betragvalue = deduct_taxes(h_artikel.departement, h_artikel.artnr, h_bill_line.bill_datum, h_artikel.service_code, h_artikel.mwst_code, h_bill_line.betrag)

                                if artikel.umsatzart == 4:
                                    totalother =  to_decimal(totalother + betragvalue)
                                    totgrossother =  to_decimal(totgrossother + h_bill_line.betrag)

                                elif artikel.umsatzart == 5 or artikel.umsatzart == 6:
                                    totalfb =  to_decimal(totalfb + betragvalue)
                                    totgrossfb =  to_decimal(totgrossfb + h_bill_line.betrag)

            if totalfb > 0 or totgrossfb > 0 or totalother > 0 or totgrossother > 0:
                crm_data = query(crm_data_data, filters=(lambda crm_data: crm_data.num_entries(crm_data.confno) == 3 and to_int(entry(2, crm_data.confno, "-")) == h_bill_line.rechnr), first=True)

                if crm_data:
                    crm_data.billfbrev =  to_decimal(crm_data.billfbrev + totalfb)
                    crm_data.grossbillfb =  to_decimal(crm_data.grossbillfb + totgrossfb)
                    crm_data.billotherrev =  to_decimal(crm_data.billotherrev + totalother)
                    crm_data.grossbillother =  to_decimal(crm_data.grossbillother + totgrossother)
                else:
                    h_bill_line = get_cache (H_bill_line, {"rechnr": [(eq, h_bill.rechnr)]})

                    if h_bill_line:
                        create_bill_list(h_bill.rechnr, h_bill.bilname, h_bill.resnr, h_bill.reslinnr, h_bill.departement, h_bill_line.bill_datum)


    def gen_nonstay_guestbill():
        nonlocal crm_count, tempdate, p_87, datum1, tdate1, tdate2, arrmonth, depmonth, dobmonth, arrmonthint, depmonthint, loop_i, str, contcode, service, serv, vat, vat1, fact1, tax_included, calc_nights, gdprflag, marketingflag, newsletterflag, vouchernum, deptname, count1, betragvalue, grossbetrag, newbetrag, billflag, flag_artnr, billno, totalfb, totgrossfb, totalother, totgrossother, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, totrevincl, totrevexcl, totfbincl, totfbexcl, tototherincl, tototherexcl, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipflag, longcharoutput, guest, h_artikel, queasy, htparam, hoteldpt, genstat, reservation, res_line, bill, zimkateg, sourccod, segment, waehrung, arrangement, artikel, h_bill, h_bill_line, bill_line
        nonlocal fdate, tdate, propid, rig
        nonlocal guest_ota, buffart, qsy231, qsy289
        nonlocal crm_data, guest_ota, buffart, qsy231, qsy289

        for bill in db_session.query(Bill).filter(
                
                (Bill.rechnr != 0) & (Bill.flag == 1) & (Bill.resnr == 0) & (Bill.billtyp == 0) & (Bill.datum == fdate)).order_by(Bill.rechnr).all():
            totalfb =  to_decimal("0")
            totgrossfb =  to_decimal("0")
            totalother =  to_decimal("0")
            totgrossother =  to_decimal("0")

            for bill_line in db_session.query(Bill_line).filter(
                    (Bill_line.rechnr == bill.rechnr) & (Bill_line.artnr != 99) & (Bill_line.betrag > 0)).order_by(Bill_line._recid).all():

                artikel = get_cache (Artikel, {
                    "artnr": [(eq, bill_line.artnr)],
                    "departement": [(eq, bill_line.departement)]})

                if artikel:
                    if artikel.umsatzart == 4:
                        betragvalue = deduct_taxes(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code, bill_line.betrag)
                        totalother =  to_decimal(totalother + betragvalue)
                        totgrossother =  to_decimal(totgrossother + bill_line.betrag)

                    elif artikel.umsatzart == 5 or artikel.umsatzart == 6 or (artikel.artart == 1 and artikel.umsatzart == 0):
                        grossbetrag =  to_decimal(bill_line.betrag)
                        betragvalue = deduct_taxes(artikel.departement, artikel.artnr, bill_line.bill_datum, artikel.service_code, artikel.mwst_code, bill_line.betrag)
                        billflag = False
                        for loop_i in range(1,length(bill_line.bezeich)  + 1) :

                            if substring(bill_line.bezeich, loop_i - 1, 1) == "*" :
                                billno = to_int(substring(bill_line.bezeich, loop_i + 1 - 1, length(bill_line.bezeich)))
                                loop_i = 999
                                billflag = True

                        if billflag :
                            betragvalue =  to_decimal("0")
                            grossbetrag =  to_decimal("0")
                        totalfb =  to_decimal(totalfb + betragvalue)
                        totgrossfb =  to_decimal(totgrossfb + grossbetrag)

            if totalfb > 0 or totalother > 0:

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill.rechnr)]})

                if bill_line:
                    create_bill_list(bill.rechnr, bill.bilname, bill.gastnr, 0, 0, bill_line.bill_datum)
        pos_nonstay_bill()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
    tax_included = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    p_87 = htparam.fdate

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, 0)]})

    if hoteldpt:
        deptname = hoteldpt.depart

    for genstat in db_session.query(Genstat).filter(
            ((Genstat.resstatus == 6) | (Genstat.resstatus == 8)) & (Genstat.datum == fdate)).order_by(Genstat._recid).all():
        assign_genstat_values(1)

    for reservation in db_session.query(Reservation).filter(
            (Reservation.resdat == fdate)).order_by(Reservation._recid).all():

        for res_line in db_session.query(Res_line).filter(
                (Res_line.resnr == reservation.resnr) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line._recid).all():
            assign_resline_values("Reserved")

    for res_line in db_session.query(Res_line).filter(
            (((Res_line.resstatus == 8) & (Res_line.ankunft != Res_line.abreise))) & (Res_line.ankunft <= fdate) & (Res_line.abreise >= tdate) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.abreise <= tdate)).order_by(Res_line._recid).all():

        if fdate < p_87:
            for genstat in db_session.query(Genstat).filter(
                    (Genstat.resnr == res_line.resnr) & (Genstat.res_int[inc_value(0)] == res_line.reslinnr)).order_by(Genstat._recid).all():
                assign_genstat_values(2)
        else:
            assign_resline_values("")

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resstatus == 9) & (Res_line.cancelled == fdate) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
        assign_resline_values("Cancelled")

    for res_line in db_session.query(Res_line).filter(
            (Res_line.resstatus == 10) & (Res_line.ankunft == fdate) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
        assign_resline_values("NoShow")
    gen_nonstay_guestbill()

    for crm_data in query(crm_data_data, sort_by=[("recordcount",True)]):
        crm_count = crm_data.recordcount
        break

    return generate_output()