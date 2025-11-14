#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.get_room_breakdown import get_room_breakdown
from functions.ghs_get_room_breakdownbl import ghs_get_room_breakdownbl
from models import Guest, Res_line, Htparam, Paramtext, Interface, Reservation, Zimkateg, Waehrung, Sourccod, Segment, Reslin_queasy, Fixleist, Artikel

def if_crm_centralized_3bl(casetype:string, paramflag:string, notthisflag:string):

    prepare_cache ([Guest, Res_line, Htparam, Paramtext, Reservation, Zimkateg, Waehrung, Sourccod, Segment, Reslin_queasy, Fixleist, Artikel])

    if_resnr = 0
    if_reslinnr = 0
    t_resline_data = []
    t_rate_data = []
    t_guest_data = []
    art_list_data = []
    ci_date:date = None
    loop_i:int = 0
    loop_count:int = 0
    str:string = ""
    contcode:string = ""
    out_str:string = ""
    datum:date = get_current_date()
    datum1:date = None
    to_date:date = None
    curr_i:int = 0
    datum2:date = None
    add_it:bool = False
    argt_rate:Decimal = to_decimal("0.0")
    delta:int = 0
    start_date:date = None
    co_date:date = None
    departement:string = ""
    artikelnr:string = ""
    i:int = 0
    htl_code:string = ""
    htl_name:string = ""
    flodging:Decimal = to_decimal("0.0")
    lodging:Decimal = to_decimal("0.0")
    breakfast:Decimal = to_decimal("0.0")
    lunch:Decimal = to_decimal("0.0")
    dinner:Decimal = to_decimal("0.0")
    others:Decimal = to_decimal("0.0")
    rmrate:Decimal = to_decimal("0.0")
    net_vat:Decimal = to_decimal("0.0")
    net_service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    totvat:Decimal = to_decimal("0.0")
    totlodg:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    t_rmrev:Decimal = to_decimal("0.0")
    t_fbrev:Decimal = to_decimal("0.0")
    t_other:Decimal = to_decimal("0.0")
    t_fbrev_tax:Decimal = to_decimal("0.0")
    t_other_tax:Decimal = to_decimal("0.0")
    serv1:Decimal = to_decimal("0.0")
    vat1:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact1:Decimal = to_decimal("0.0")
    guest = res_line = htparam = paramtext = interface = reservation = zimkateg = waehrung = sourccod = segment = reslin_queasy = fixleist = artikel = None

    t_resline = t_guest = t_rate = art_list = bufguest = bufres_line = bufguest2 = None

    t_resline_data, T_resline = create_model("T_resline", {"recid1":int, "res_status":string, "booksource":string, "createdate":date, "resnr":int, "reslinnr":int, "roomtypecode":string, "rateplancode":string, "unitnumber":int, "currency":string, "adult":int, "child":int, "startdate":date, "enddate":date, "hotelcode":string, "hotelname":string, "mainrsvcomment":string, "remark":string, "booker_id":int, "bookerfirstname":string, "bookerlastname":string, "bookergender":string, "bookertitle":string, "bookerphone":string, "bookeremail":string, "bookeraddress1":string, "bookeraddress2":string, "bookeraddress3":string, "bookercity":string, "bookerpostalcode":string, "bookerstate":string, "bookercountry":string, "bookernation":string, "bookerbirthdate":string, "bookercitizenid":string, "flight1":string, "eta":string, "flight2":string, "etd":string, "room_number":string, "ci_time":string, "co_time":string, "segment":string})
    t_guest_data, T_guest = create_model("T_guest", {"recid1":int, "resnr":int, "reslinnr":int, "guest_id":int, "guest_title":string, "firstname":string, "lastname":string, "gender":string, "phonenum":string, "mobilenum":string, "email":string, "addresstype":string, "address1":string, "address2":string, "address3":string, "city":string, "postalcode":string, "state":string, "country":string, "primary_guest":int, "birthdate":string, "nationality":string, "citizenid":string})
    t_rate_data, T_rate = create_model("T_rate", {"recid1":int, "resnr":int, "reslinnr":int, "effectivedate":date, "expiredate":date, "unitmultiplier":int, "aftertax":Decimal, "tax_percent":Decimal, "totalaftertax":Decimal, "totaltax_amount":Decimal, "lodging":Decimal, "fb_amount":Decimal, "fb_amount_tax":Decimal, "other_amount":Decimal, "other_amount_tax":Decimal})
    art_list_data, Art_list = create_model("Art_list", {"recid1":int, "resnr":int, "reslinnr":int, "bezeich":string, "price":Decimal, "qty":int, "artnr":string})

    Bufguest = create_buffer("Bufguest",Guest)
    Bufres_line = create_buffer("Bufres_line",Res_line)
    Bufguest2 = create_buffer("Bufguest2",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal if_resnr, if_reslinnr, t_resline_data, t_rate_data, t_guest_data, art_list_data, ci_date, loop_i, loop_count, str, contcode, out_str, datum, datum1, to_date, curr_i, datum2, add_it, argt_rate, delta, start_date, co_date, departement, artikelnr, i, htl_code, htl_name, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, totvat, totlodg, service, t_rmrev, t_fbrev, t_other, t_fbrev_tax, t_other_tax, serv1, vat1, vat2, fact1, guest, res_line, htparam, paramtext, interface, reservation, zimkateg, waehrung, sourccod, segment, reslin_queasy, fixleist, artikel
        nonlocal casetype, paramflag, notthisflag
        nonlocal bufguest, bufres_line, bufguest2


        nonlocal t_resline, t_guest, t_rate, art_list, bufguest, bufres_line, bufguest2
        nonlocal t_resline_data, t_guest_data, t_rate_data, art_list_data

        return {"if_resnr": if_resnr, "if_reslinnr": if_reslinnr, "t-resline": t_resline_data, "t-rate": t_rate_data, "t-guest": t_guest_data, "art-list": art_list_data}

    def decode_string(in_str:string):

        nonlocal if_resnr, if_reslinnr, t_resline_data, t_rate_data, t_guest_data, art_list_data, ci_date, loop_i, loop_count, str, contcode, out_str, datum, datum1, to_date, curr_i, datum2, add_it, argt_rate, delta, start_date, co_date, departement, artikelnr, i, htl_code, htl_name, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, totvat, totlodg, service, t_rmrev, t_fbrev, t_other, t_fbrev_tax, t_other_tax, serv1, vat1, vat2, fact1, guest, res_line, htparam, paramtext, interface, reservation, zimkateg, waehrung, sourccod, segment, reslin_queasy, fixleist, artikel
        nonlocal casetype, paramflag, notthisflag
        nonlocal bufguest, bufres_line, bufguest2


        nonlocal t_resline, t_guest, t_rate, art_list, bufguest, bufres_line, bufguest2
        nonlocal t_resline_data, t_guest_data, t_rate_data, art_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        in_str = paramtext.ptexte
        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext:
        out_str = decode_string(paramtext.ptexte)
        htl_code = out_str

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 240)]})

    if paramtext:
        out_str = decode_string(paramtext.ptexte)
        htl_name = out_str

    if casetype.lower()  == ("new").lower() :

        interface = db_session.query(Interface).filter(
                 (Interface.key == 10) & (not_(matches(Interface.nebenstelle,"*" + paramflag + "*"))) & (not_(matches(Interface.nebenstelle,"*" + notthisflag + "*"))) & (matches((Interface.parameters,"*insert*"))) | (matches(Interface.parameters,"*qci*"))) | (matches(Interface.parameters,"*new*")) | (matches(Interface.parameters,"*split*")) & (not_(matches(Interface.parameters,"*|init*"))).order_by(Interface._recid.desc()).first()

        if interface:

            res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)],"resstatus": [(ne, 11),(ne, 13)],"l_zuordnung[2]": [(eq, 0)]})

            if res_line:
                if_resnr = res_line.resnr
                if_reslinnr = res_line.reslinnr

                bufguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
                    t_guest.resnr = res_line.resnr
                    t_guest.reslinnr = res_line.reslinnr
                    t_guest.guest_id = bufguest.gastnr
                    t_guest.guest_title = bufguest.anrede1
                    t_guest.firstname = bufguest.vorname1
                    t_guest.lastname = bufguest.name
                    t_guest.gender = bufguest.geschlecht
                    t_guest.phonenum = bufguest.telefon
                    t_guest.mobilenum = bufguest.mobil_telefon
                    t_guest.email = bufguest.email_adr
                    t_guest.city = bufguest.wohnort
                    t_guest.country = bufguest.land
                    t_guest.primary_guest = 1
                    t_guest.nationality = bufguest.nation1
                    t_guest.citizenid = bufguest.ausweis_nr1

                    if bufguest.geburtdatum1 != None:
                        t_guest.birthdate = to_string(bufguest.geburtdatum1)

                    if bufguest.adresse1 != None:
                        t_guest.address1 = bufguest.adresse1

                    if bufguest.adresse2 != None:
                        t_guest.address2 = bufguest.adresse2

                    if bufguest.adresse3 != None:
                        t_guest.address3 = bufguest.adresse3

                    if bufguest.plz != None:
                        t_guest.postalcode = bufguest.plz

                    if bufguest.geburt_ort2 != None:
                        t_guest.state = bufguest.geburt_ort2
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(60) , "")
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(62) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(60) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(62) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(60) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(62) , "")

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = res_line.bemerk
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(42) , " ")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(60) , "")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(62) , "")

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(60) , "")
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(62) , "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        t_resline.segment = to_string(segment.Bezeich)

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                if waehrung:
                    t_resline.currency = waehrung.wabkurz

                if guest:
                    t_resline.booker_id = guest.gastnr
                    t_resline.bookerfirstname = guest.vorname1
                    t_resline.bookerlastname = guest.name
                    t_resline.bookergender = guest.geschlecht
                    t_resline.bookertitle = guest.anrede1
                    t_resline.bookerphone = guest.telefon
                    t_resline.bookeremail = guest.email_adr
                    t_resline.bookercity = guest.wohnort
                    t_resline.bookercountry = guest.land
                    t_resline.bookernation = guest.nation1
                    t_resline.bookercitizenid = guest.ausweis_nr1

                    if guest.geburtdatum1 != None:
                        t_resline.bookerbirthdate = to_string(guest.geburtdatum1)

                    if guest.adresse1 != None:
                        t_resline.bookeraddress1 = guest.adresse1

                    if guest.adresse2 != None:
                        t_resline.bookeraddress2 = guest.adresse2

                    if guest.adresse3 != None:
                        t_resline.bookeraddress3 = guest.adresse3

                    if guest.plz != None:
                        t_resline.bookerpostalcode = guest.plz

                    if guest.geburt_ort2 != None:
                        t_resline.bookerstate = guest.geburt_ort2
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(60) , "")
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(62) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(60) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(62) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(60) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(62) , "")

                if res_line.resstatus == 1:
                    t_resline.res_status = "Guaranteed"

                elif res_line.resstatus == 2:
                    t_resline.res_status = "6PM"

                elif res_line.resstatus == 3:
                    t_resline.res_status = "Tentative"

                elif res_line.resstatus == 4:
                    t_resline.res_status = "WaitList"

                elif res_line.resstatus == 5:
                    t_resline.res_status = "OralConfirm"

                elif res_line.resstatus == 6:
                    t_resline.res_status = "Inhouse"

                elif res_line.resstatus == 8:
                    t_resline.res_status = "CheckedOut"

                elif res_line.resstatus == 9:
                    t_resline.res_status = "Cancelled"

                elif res_line.resstatus == 10:
                    t_resline.res_status = "NoShow"

                elif res_line.resstatus == 11:
                    t_resline.res_status = "RoomSharer"

                elif res_line.resstatus == 12:
                    t_resline.res_status = "AddBill"

                elif res_line.resstatus == 13:
                    t_resline.res_status = "Inhouse(RoomSharer)"

                elif res_line.resstatus == 99:
                    t_resline.res_status = "Deleted"

                if res_line.ankunft == res_line.abreise:
                    to_date = res_line.abreise
                else:
                    to_date = res_line.abreise - timedelta(days=1)
                for datum1 in date_range(res_line.ankunft,to_date) :
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat =  to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                for datum in date_range(res_line.ankunft,datum2) :
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum, 1, datum2))
                    t_fbrev = ( to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_fbrev_tax =  to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)
                    t_other =  to_decimal(others) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_other_tax =  to_decimal(others)
                    lodging = ( to_decimal(rmrate) - to_decimal(breakfast) - to_decimal(lunch) - to_decimal(dinner) - to_decimal(others)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.unitmultiplier = 1
                        t_rate.aftertax = to_decimal(round(reslin_queasy.deci1 , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))
                    else:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.aftertax = to_decimal(round(res_line.zipreis , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.unitmultiplier = 1
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft,co_date) :
                    argt_rate =  to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if res_line.ankunft == datum2:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum2) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum2 + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - res_line.ankunft

                                if delta < 0:
                                    delta = 0
                            start_date = res_line.ankunft + timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:

                            art_list = query(art_list_data, filters=(lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.resnr = res_line.resnr
                            art_list.reslinnr = res_line.reslinnr
                            art_list.bezeich = artikel.bezeich
                            art_list.price =  to_decimal(art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                pass
                db_session.delete(interface)
                pass

    elif casetype.lower()  == ("update").lower() :

        interface = db_session.query(Interface).filter(
                 (Interface.key == 10) & (not_(matches(Interface.nebenstelle,"*" + paramflag + "*"))) & (not_(matches(Interface.nebenstelle,"*" + notthisflag + "*"))) & (matches((Interface.parameters,"*modify*"))) | (matches(Interface.parameters,"*checkin*"))) | (matches(Interface.parameters,"*checkout*")) & (not_(matches(Interface.parameters,"*|init*"))).order_by(Interface._recid.desc()).first()

        if interface:

            res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)],"resstatus": [(ne, 11),(ne, 13)],"l_zuordnung[2]": [(eq, 0)]})

            if res_line:
                if_resnr = res_line.resnr
                if_reslinnr = res_line.reslinnr

                bufguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
                    t_guest.resnr = res_line.resnr
                    t_guest.reslinnr = res_line.reslinnr
                    t_guest.guest_id = bufguest.gastnr
                    t_guest.guest_title = bufguest.anrede1
                    t_guest.firstname = bufguest.vorname1
                    t_guest.lastname = bufguest.name
                    t_guest.gender = bufguest.geschlecht
                    t_guest.phonenum = bufguest.telefon
                    t_guest.mobilenum = bufguest.mobil_telefon
                    t_guest.email = bufguest.email_adr
                    t_guest.city = bufguest.wohnort
                    t_guest.country = bufguest.land
                    t_guest.primary_guest = 1
                    t_guest.nationality = bufguest.nation1
                    t_guest.citizenid = bufguest.ausweis_nr1

                    if bufguest.geburtdatum1 != None:
                        t_guest.birthdate = to_string(bufguest.geburtdatum1)

                    if bufguest.adresse1 != None:
                        t_guest.address1 = bufguest.adresse1

                    if bufguest.adresse2 != None:
                        t_guest.address2 = bufguest.adresse2

                    if bufguest.adresse3 != None:
                        t_guest.address3 = bufguest.adresse3

                    if bufguest.plz != None:
                        t_guest.postalcode = bufguest.plz

                    if bufguest.geburt_ort2 != None:
                        t_guest.state = bufguest.geburt_ort2
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(60) , "")
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(62) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(60) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(62) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(60) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(62) , "")

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = res_line.bemerk
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(42) , " ")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(60) , "")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(62) , "")

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(60) , "")
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(62) , "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        t_resline.segment = to_string(segment.Bezeich)

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                if waehrung:
                    t_resline.currency = waehrung.wabkurz

                if guest:
                    t_resline.booker_id = guest.gastnr
                    t_resline.bookerfirstname = guest.vorname1
                    t_resline.bookerlastname = guest.name
                    t_resline.bookergender = guest.geschlecht
                    t_resline.bookertitle = guest.anrede1
                    t_resline.bookerphone = guest.telefon
                    t_resline.bookeremail = guest.email_adr
                    t_resline.bookercity = guest.wohnort
                    t_resline.bookercountry = guest.land
                    t_resline.bookernation = guest.nation1
                    t_resline.bookercitizenid = guest.ausweis_nr1

                    if guest.geburtdatum1 != None:
                        t_resline.bookerbirthdate = to_string(guest.geburtdatum1)

                    if guest.adresse1 != None:
                        t_resline.bookeraddress1 = guest.adresse1

                    if guest.adresse2 != None:
                        t_resline.bookeraddress2 = guest.adresse2

                    if guest.adresse3 != None:
                        t_resline.bookeraddress3 = guest.adresse3

                    if guest.plz != None:
                        t_resline.bookerpostalcode = guest.plz

                    if guest.geburt_ort2 != None:
                        t_resline.bookerstate = guest.geburt_ort2
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(60) , "")
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(62) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(60) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(62) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(60) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(62) , "")

                if res_line.resstatus == 1:
                    t_resline.res_status = "Guaranteed"

                elif res_line.resstatus == 2:
                    t_resline.res_status = "6PM"

                elif res_line.resstatus == 3:
                    t_resline.res_status = "Tentative"

                elif res_line.resstatus == 4:
                    t_resline.res_status = "WaitList"

                elif res_line.resstatus == 5:
                    t_resline.res_status = "OralConfirm"

                elif res_line.resstatus == 6:
                    t_resline.res_status = "Inhouse"

                elif res_line.resstatus == 8:
                    t_resline.res_status = "CheckedOut"

                elif res_line.resstatus == 9:
                    t_resline.res_status = "Cancelled"

                elif res_line.resstatus == 10:
                    t_resline.res_status = "NoShow"

                elif res_line.resstatus == 11:
                    t_resline.res_status = "RoomSharer"

                elif res_line.resstatus == 12:
                    t_resline.res_status = "AddBill"

                elif res_line.resstatus == 13:
                    t_resline.res_status = "Inhouse(RoomSharer)"

                elif res_line.resstatus == 99:
                    t_resline.res_status = "Deleted"

                if res_line.ankunft == res_line.abreise:
                    to_date = res_line.abreise
                else:
                    to_date = res_line.abreise - timedelta(days=1)
                for datum1 in date_range(res_line.ankunft,to_date) :
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat =  to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                for datum in date_range(res_line.ankunft,datum2) :
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum, 2, datum2))
                    t_fbrev = ( to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_fbrev_tax =  to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)
                    t_other =  to_decimal(others) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_other_tax =  to_decimal(others)
                    lodging = ( to_decimal(rmrate) - to_decimal(breakfast) - to_decimal(lunch) - to_decimal(dinner) - to_decimal(others)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.unitmultiplier = 1
                        t_rate.aftertax = to_decimal(round(reslin_queasy.deci1 , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))
                    else:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.aftertax = to_decimal(round(res_line.zipreis , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.unitmultiplier = 1
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft,co_date) :
                    argt_rate =  to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if res_line.ankunft == datum2:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum2) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum2 + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - res_line.ankunft

                                if delta < 0:
                                    delta = 0
                            start_date = res_line.ankunft + timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:

                            art_list = query(art_list_data, filters=(lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.resnr = res_line.resnr
                            art_list.reslinnr = res_line.reslinnr
                            art_list.bezeich = artikel.bezeich
                            art_list.price =  to_decimal(art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                pass
                db_session.delete(interface)
                pass

    elif casetype.lower()  == ("cancel").lower() :

        interface = db_session.query(Interface).filter(
                 (Interface.key == 10) & (not_(matches(Interface.nebenstelle,"*" + paramflag + "*"))) & (not_(matches(Interface.nebenstelle,"*" + notthisflag + "*"))) & (matches((Interface.parameters,"*cancel*"))) | (matches(Interface.parameters,"*delete*"))) & (not_(matches(Interface.parameters,"*|init*"))).order_by(Interface._recid.desc()).first()

        if interface:

            res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)]})

            if res_line:
                if_resnr = res_line.resnr
                if_reslinnr = res_line.reslinnr

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(60) , "")
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(62) , "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                if res_line.resstatus == 1:
                    t_resline.res_status = "Guaranteed"

                elif res_line.resstatus == 2:
                    t_resline.res_status = "6PM"

                elif res_line.resstatus == 3:
                    t_resline.res_status = "Tentative"

                elif res_line.resstatus == 4:
                    t_resline.res_status = "WaitList"

                elif res_line.resstatus == 5:
                    t_resline.res_status = "OralConfirm"

                elif res_line.resstatus == 6:
                    t_resline.res_status = "Inhouse"

                elif res_line.resstatus == 8:
                    t_resline.res_status = "CheckedOut"

                elif res_line.resstatus == 9:
                    t_resline.res_status = "Cancelled"

                elif res_line.resstatus == 10:
                    t_resline.res_status = "NoShow"

                elif res_line.resstatus == 11:
                    t_resline.res_status = "RoomSharer"

                elif res_line.resstatus == 12:
                    t_resline.res_status = "AddBill"

                elif res_line.resstatus == 13:
                    t_resline.res_status = "Inhouse(RoomSharer)"

                elif res_line.resstatus == 99:
                    t_resline.res_status = "Deleted"

    elif casetype.lower()  == ("new-initial").lower() :

        for interface in db_session.query(Interface).filter(
                 (Interface.key == 10) & (not_(matches(Interface.nebenstelle,"*" + paramflag + "*"))) & (not_(matches(Interface.nebenstelle,"*" + notthisflag + "*"))) & (matches((Interface.parameters,"*new|init*")))).order_by(intdate, int_time).all():
            loop_count = loop_count + 1

            if loop_count > 5:
                break

            res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)],"resstatus": [(ne, 11),(ne, 13)],"l_zuordnung[2]": [(eq, 0)]})

            if res_line:
                if_resnr = res_line.resnr
                if_reslinnr = res_line.reslinnr

                bufguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
                    t_guest.resnr = res_line.resnr
                    t_guest.reslinnr = res_line.reslinnr
                    t_guest.guest_id = bufguest.gastnr
                    t_guest.guest_title = bufguest.anrede1
                    t_guest.firstname = bufguest.vorname1
                    t_guest.lastname = bufguest.name
                    t_guest.gender = bufguest.geschlecht
                    t_guest.phonenum = bufguest.telefon
                    t_guest.mobilenum = bufguest.mobil_telefon
                    t_guest.email = bufguest.email_adr
                    t_guest.city = bufguest.wohnort
                    t_guest.country = bufguest.land
                    t_guest.primary_guest = 1
                    t_guest.nationality = bufguest.nation1
                    t_guest.citizenid = bufguest.ausweis_nr1

                    if bufguest.geburtdatum1 != None:
                        t_guest.birthdate = to_string(bufguest.geburtdatum1)

                    if bufguest.adresse1 != None:
                        t_guest.address1 = bufguest.adresse1

                    if bufguest.adresse2 != None:
                        t_guest.address2 = bufguest.adresse2

                    if bufguest.adresse3 != None:
                        t_guest.address3 = bufguest.adresse3

                    if bufguest.plz != None:
                        t_guest.postalcode = bufguest.plz

                    if bufguest.geburt_ort2 != None:
                        t_guest.state = bufguest.geburt_ort2
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(60) , "")
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(62) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(60) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(62) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(60) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(62) , "")

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = res_line.bemerk
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(42) , " ")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(60) , "")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(62) , "")

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(60) , "")
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(62) , "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        t_resline.segment = to_string(segment.Bezeich)

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                if waehrung:
                    t_resline.currency = waehrung.wabkurz

                if guest:
                    t_resline.booker_id = guest.gastnr
                    t_resline.bookerfirstname = guest.vorname1
                    t_resline.bookerlastname = guest.name
                    t_resline.bookergender = guest.geschlecht
                    t_resline.bookertitle = guest.anrede1
                    t_resline.bookerphone = guest.telefon
                    t_resline.bookeremail = guest.email_adr
                    t_resline.bookercity = guest.wohnort
                    t_resline.bookercountry = guest.land
                    t_resline.bookernation = guest.nation1
                    t_resline.bookercitizenid = guest.ausweis_nr1

                    if guest.geburtdatum1 != None:
                        t_resline.bookerbirthdate = to_string(guest.geburtdatum1)

                    if guest.adresse1 != None:
                        t_resline.bookeraddress1 = guest.adresse1

                    if guest.adresse2 != None:
                        t_resline.bookeraddress2 = guest.adresse2

                    if guest.adresse3 != None:
                        t_resline.bookeraddress3 = guest.adresse3

                    if guest.plz != None:
                        t_resline.bookerpostalcode = guest.plz

                    if guest.geburt_ort2 != None:
                        t_resline.bookerstate = guest.geburt_ort2
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(60) , "")
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(62) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(60) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(62) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(60) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(62) , "")

                if res_line.resstatus == 1:
                    t_resline.res_status = "Guaranteed"

                elif res_line.resstatus == 2:
                    t_resline.res_status = "6PM"

                elif res_line.resstatus == 3:
                    t_resline.res_status = "Tentative"

                elif res_line.resstatus == 4:
                    t_resline.res_status = "WaitList"

                elif res_line.resstatus == 5:
                    t_resline.res_status = "OralConfirm"

                elif res_line.resstatus == 6:
                    t_resline.res_status = "Inhouse"

                elif res_line.resstatus == 8:
                    t_resline.res_status = "CheckedOut"

                elif res_line.resstatus == 9:
                    t_resline.res_status = "Cancelled"

                elif res_line.resstatus == 10:
                    t_resline.res_status = "NoShow"

                elif res_line.resstatus == 11:
                    t_resline.res_status = "RoomSharer"

                elif res_line.resstatus == 12:
                    t_resline.res_status = "AddBill"

                elif res_line.resstatus == 13:
                    t_resline.res_status = "Inhouse(RoomSharer)"

                elif res_line.resstatus == 99:
                    t_resline.res_status = "Deleted"

                if res_line.ankunft == res_line.abreise:
                    to_date = res_line.abreise
                else:
                    to_date = res_line.abreise - timedelta(days=1)
                for datum1 in date_range(res_line.ankunft,to_date) :
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat =  to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                for datum in date_range(res_line.ankunft,datum2) :
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum, 1, datum2))
                    t_fbrev = ( to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_fbrev_tax =  to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)
                    t_other =  to_decimal(others) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_other_tax =  to_decimal(others)
                    lodging = ( to_decimal(rmrate) - to_decimal(breakfast) - to_decimal(lunch) - to_decimal(dinner) - to_decimal(others)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.unitmultiplier = 1
                        t_rate.aftertax = to_decimal(round(reslin_queasy.deci1 , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))
                    else:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.aftertax = to_decimal(round(res_line.zipreis , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.unitmultiplier = 1
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft,co_date) :
                    argt_rate =  to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if res_line.ankunft == datum2:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum2) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum2 + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - res_line.ankunft

                                if delta < 0:
                                    delta = 0
                            start_date = res_line.ankunft + timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:

                            art_list = query(art_list_data, filters=(lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.resnr = res_line.resnr
                            art_list.reslinnr = res_line.reslinnr
                            art_list.bezeich = artikel.bezeich
                            art_list.price =  to_decimal(art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                db_session.delete(interface)
                pass

    elif casetype.lower()  == ("update-initial").lower() :

        for interface in db_session.query(Interface).filter(
                 (Interface.key == 10) & (not_(matches(Interface.nebenstelle,"*" + paramflag + "*"))) & (not_(matches(Interface.nebenstelle,"*" + notthisflag + "*"))) & (matches((Interface.parameters,"*modify|init*")))).order_by(intdate, int_time).all():
            loop_count = loop_count + 1

            if loop_count > 5:
                break

            res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)],"resstatus": [(ne, 11),(ne, 13)],"l_zuordnung[2]": [(eq, 0)]})

            if res_line:
                if_resnr = res_line.resnr
                if_reslinnr = res_line.reslinnr

                bufguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
                    t_guest.resnr = res_line.resnr
                    t_guest.reslinnr = res_line.reslinnr
                    t_guest.guest_id = bufguest.gastnr
                    t_guest.guest_title = bufguest.anrede1
                    t_guest.firstname = bufguest.vorname1
                    t_guest.lastname = bufguest.name
                    t_guest.gender = bufguest.geschlecht
                    t_guest.phonenum = bufguest.telefon
                    t_guest.mobilenum = bufguest.mobil_telefon
                    t_guest.email = bufguest.email_adr
                    t_guest.city = bufguest.wohnort
                    t_guest.country = bufguest.land
                    t_guest.primary_guest = 1
                    t_guest.nationality = bufguest.nation1
                    t_guest.citizenid = bufguest.ausweis_nr1

                    if bufguest.geburtdatum1 != None:
                        t_guest.birthdate = to_string(bufguest.geburtdatum1)

                    if bufguest.adresse1 != None:
                        t_guest.address1 = bufguest.adresse1

                    if bufguest.adresse2 != None:
                        t_guest.address2 = bufguest.adresse2

                    if bufguest.adresse3 != None:
                        t_guest.address3 = bufguest.adresse3

                    if bufguest.plz != None:
                        t_guest.postalcode = bufguest.plz

                    if bufguest.geburt_ort2 != None:
                        t_guest.state = bufguest.geburt_ort2
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(60) , "")
                    t_guest.address1 = replace_str(t_guest.address1, chr_unicode(62) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(60) , "")
                    t_guest.address2 = replace_str(t_guest.address2, chr_unicode(62) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(60) , "")
                    t_guest.address3 = replace_str(t_guest.address3, chr_unicode(62) , "")

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = res_line.bemerk
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(42) , " ")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(60) , "")
                t_resline.remark = replace_str(t_resline.remark, chr_unicode(62) , "")

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(60) , "")
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(62) , "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                    segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                    if segment:
                        t_resline.segment = to_string(segment.Bezeich)

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                if waehrung:
                    t_resline.currency = waehrung.wabkurz

                if guest:
                    t_resline.booker_id = guest.gastnr
                    t_resline.bookerfirstname = guest.vorname1
                    t_resline.bookerlastname = guest.name
                    t_resline.bookergender = guest.geschlecht
                    t_resline.bookertitle = guest.anrede1
                    t_resline.bookerphone = guest.telefon
                    t_resline.bookeremail = guest.email_adr
                    t_resline.bookercity = guest.wohnort
                    t_resline.bookercountry = guest.land
                    t_resline.bookernation = guest.nation1
                    t_resline.bookercitizenid = guest.ausweis_nr1

                    if guest.geburtdatum1 != None:
                        t_resline.bookerbirthdate = to_string(guest.geburtdatum1)

                    if guest.adresse1 != None:
                        t_resline.bookeraddress1 = guest.adresse1

                    if guest.adresse2 != None:
                        t_resline.bookeraddress2 = guest.adresse2

                    if guest.adresse3 != None:
                        t_resline.bookeraddress3 = guest.adresse3

                    if guest.plz != None:
                        t_resline.bookerpostalcode = guest.plz

                    if guest.geburt_ort2 != None:
                        t_resline.bookerstate = guest.geburt_ort2
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(60) , "")
                    t_resline.bookeraddress1 = replace_str(t_resline.bookeraddress1, chr_unicode(62) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(60) , "")
                    t_resline.bookeraddress2 = replace_str(t_resline.bookeraddress2, chr_unicode(62) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(60) , "")
                    t_resline.bookeraddress3 = replace_str(t_resline.bookeraddress3, chr_unicode(62) , "")

                if res_line.resstatus == 1:
                    t_resline.res_status = "Guaranteed"

                elif res_line.resstatus == 2:
                    t_resline.res_status = "6PM"

                elif res_line.resstatus == 3:
                    t_resline.res_status = "Tentative"

                elif res_line.resstatus == 4:
                    t_resline.res_status = "WaitList"

                elif res_line.resstatus == 5:
                    t_resline.res_status = "OralConfirm"

                elif res_line.resstatus == 6:
                    t_resline.res_status = "Inhouse"

                elif res_line.resstatus == 8:
                    t_resline.res_status = "CheckedOut"

                elif res_line.resstatus == 9:
                    t_resline.res_status = "Cancelled"

                elif res_line.resstatus == 10:
                    t_resline.res_status = "NoShow"

                elif res_line.resstatus == 11:
                    t_resline.res_status = "RoomSharer"

                elif res_line.resstatus == 12:
                    t_resline.res_status = "AddBill"

                elif res_line.resstatus == 13:
                    t_resline.res_status = "Inhouse(RoomSharer)"

                elif res_line.resstatus == 99:
                    t_resline.res_status = "Deleted"

                if res_line.ankunft == res_line.abreise:
                    to_date = res_line.abreise
                else:
                    to_date = res_line.abreise - timedelta(days=1)
                for datum1 in date_range(res_line.ankunft,to_date) :
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat =  to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                for datum in date_range(res_line.ankunft,datum2) :
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, service = get_output(ghs_get_room_breakdownbl(res_line._recid, datum, 2, datum2))
                    t_fbrev = ( to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_fbrev_tax =  to_decimal(breakfast) + to_decimal(lunch) + to_decimal(dinner)
                    t_other =  to_decimal(others) / to_decimal((1) + to_decimal(vat) + to_decimal(service))
                    t_other_tax =  to_decimal(others)
                    lodging = ( to_decimal(rmrate) - to_decimal(breakfast) - to_decimal(lunch) - to_decimal(dinner) - to_decimal(others)) / to_decimal((1) + to_decimal(vat) + to_decimal(service))

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

                    if reslin_queasy:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.unitmultiplier = 1
                        t_rate.aftertax = to_decimal(round(reslin_queasy.deci1 , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))
                    else:
                        t_rate = T_rate()
                        t_rate_data.append(t_rate)

                        t_rate.recid1 = interface._recid
                        t_rate.resnr = res_line.resnr
                        t_rate.reslinnr = res_line.reslinnr
                        t_rate.effectivedate = datum
                        t_rate.expiredate = datum
                        t_rate.aftertax = to_decimal(round(res_line.zipreis , 2))
                        t_rate.totaltax_amount = to_decimal(round(totvat , 2))
                        t_rate.unitmultiplier = 1
                        t_rate.totalaftertax = to_decimal(round(t_rate.aftertax * t_rate.unitmultiplier , 2))
                        t_rate.lodging = to_decimal(round(lodging , 2))
                        t_rate.fb_amount = to_decimal(round(t_fbrev , 2))
                        t_rate.fb_amount_tax = to_decimal(round(t_fbrev_tax , 2))
                        t_rate.other_amount = to_decimal(round(t_other , 2))
                        t_rate.other_amount_tax = to_decimal(round(t_other_tax , 2))

                        if t_rate.totaltax_amount != 0:
                            t_rate.tax_percent = to_decimal(round(t_rate.totalaftertax / t_rate.totaltax_amount , 2))

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft,co_date) :
                    argt_rate =  to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                             (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate =  to_decimal("0")

                        if fixleist.sequenz == 1:
                            add_it = True

                        elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                            if res_line.ankunft == datum2:
                                add_it = True

                        elif fixleist.sequenz == 4 and get_day(datum2) == 1:
                            add_it = True

                        elif fixleist.sequenz == 5 and get_day(datum2 + 1) == 1:
                            add_it = True

                        elif fixleist.sequenz == 6:

                            if fixleist.lfakt == None:
                                delta = 0
                            else:
                                delta = fixleist.lfakt - res_line.ankunft

                                if delta < 0:
                                    delta = 0
                            start_date = res_line.ankunft + timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache (Artikel, {"artnr": [(eq, fixleist.artnr)],"departement": [(eq, fixleist.departement)]})
                            argt_rate =  to_decimal(fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:

                            art_list = query(art_list_data, filters=(lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.resnr = res_line.resnr
                            art_list.reslinnr = res_line.reslinnr
                            art_list.bezeich = artikel.bezeich
                            art_list.price =  to_decimal(art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                db_session.delete(interface)
                pass

    elif casetype.lower()  == ("cancel-initial").lower() :

        for interface in db_session.query(Interface).filter(
                 (Interface.key == 10) & (not_(matches(Interface.nebenstelle,"*" + paramflag + "*"))) & (not_(matches(Interface.nebenstelle,"*" + notthisflag + "*"))) & (matches((Interface.parameters,"*cancel|init*")))).order_by(intdate, int_time).all():
            loop_count = loop_count + 1

            if loop_count > 5:
                break

            res_line = get_cache (Res_line, {"resnr": [(eq, interface.resnr)],"reslinnr": [(eq, interface.reslinnr)]})

            if res_line:
                if_resnr = res_line.resnr
                if_reslinnr = res_line.reslinnr

                reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
                for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(60) , "")
                    t_resline.mainrsvcomment = replace_str(t_resline.mainrsvcomment, chr_unicode(62) , "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                if res_line.resstatus == 1:
                    t_resline.res_status = "Guaranteed"

                elif res_line.resstatus == 2:
                    t_resline.res_status = "6PM"

                elif res_line.resstatus == 3:
                    t_resline.res_status = "Tentative"

                elif res_line.resstatus == 4:
                    t_resline.res_status = "WaitList"

                elif res_line.resstatus == 5:
                    t_resline.res_status = "OralConfirm"

                elif res_line.resstatus == 6:
                    t_resline.res_status = "Inhouse"

                elif res_line.resstatus == 8:
                    t_resline.res_status = "CheckedOut"

                elif res_line.resstatus == 9:
                    t_resline.res_status = "Cancelled"

                elif res_line.resstatus == 10:
                    t_resline.res_status = "NoShow"

                elif res_line.resstatus == 11:
                    t_resline.res_status = "RoomSharer"

                elif res_line.resstatus == 12:
                    t_resline.res_status = "AddBill"

                elif res_line.resstatus == 13:
                    t_resline.res_status = "Inhouse(RoomSharer)"

                elif res_line.resstatus == 99:
                    t_resline.res_status = "Deleted"

    for t_resline in query(t_resline_data):

        if t_resline.bookercity == None:
            t_resline.bookercity = ""

        if t_resline.remark == None:
            t_resline.remark = ""

    return generate_output()