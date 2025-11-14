# using conversion tools version: 1.0.0.119
"""_summary_

    Ticket ID: 62BADE
        _remark_:   - fix python indentation
                    - add import from function_py
                    - fix order_by(intdate, int_time) to (Interface.intdate, Interface.int_time)
                    - fix buffer buffzim
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
# from functions.get_room_breakdown import get_room_breakdown
from functions_py.get_room_breakdown import get_room_breakdown
from models import Zimkateg, Guest, Res_line, Htparam, Paramtext, Interface, Reservation, Waehrung, Sourccod, Reslin_queasy, Fixleist, Artikel


def if_lodgiq_send_rsvbl(casetype: str):

    prepare_cache([Zimkateg, Guest, Res_line, Htparam, Paramtext, Reservation, Waehrung, Sourccod, Reslin_queasy, Fixleist, Artikel])

    t_resline_data = []
    t_rate_data = []
    t_guest_data = []
    art_list_data = []
    ci_date: date = None
    loop_i: int = 0
    str = ""
    contcode = ""
    out_str = ""
    datum: date = get_current_date()
    datum1: date = None
    to_date: date = None
    curr_i: int = 0
    datum2: date = None
    add_it: bool = False
    argt_rate: Decimal = to_decimal("0.0")
    delta: int = 0
    start_date: date = None
    co_date: date = None
    departement = ""
    artikelnr = ""
    i: int = 0
    htl_code = ""
    htl_name = ""
    flodging: Decimal = to_decimal("0.0")
    lodging: Decimal = to_decimal("0.0")
    breakfast: Decimal = to_decimal("0.0")
    lunch: Decimal = to_decimal("0.0")
    dinner: Decimal = to_decimal("0.0")
    others: Decimal = to_decimal("0.0")
    rmrate: Decimal = to_decimal("0.0")
    net_vat: Decimal = to_decimal("0.0")
    net_service: Decimal = to_decimal("0.0")
    vat: Decimal = to_decimal("0.0")
    totvat: Decimal = to_decimal("0.0")
    service: Decimal = to_decimal("0.0")
    t_rmrev: Decimal = to_decimal("0.0")
    t_fbrev: Decimal = to_decimal("0.0")
    t_others: Decimal = to_decimal("0.0")
    icount: int = 0
    datecounter: int = 0
    temp_rate: Decimal = to_decimal("0.0")
    zimkateg = guest = res_line = htparam = paramtext = interface = reservation = waehrung = sourccod = reslin_queasy = fixleist = artikel = None

    t_resline = t_guest = t_rate = art_list = temp_reslin_queasy = buffzim = bufguest = bufres_line = bufguest2 = None

    t_resline_data, T_resline = create_model(
        "T_resline",
        {
            "recid1": int,
            "res_status": str,
            "booksource": str,
            "createdate": date,
            "resnr": int,
            "reslinnr": int,
            "resid": str,
            "roomtypecode": str,
            "rateplancode": str,
            "unitnumber": int,
            "currency": str,
            "adult": int,
            "child": int,
            "startdate": date,
            "enddate": date,
            "hotelcode": str,
            "hotelname": str,
            "mainrsvcomment": str,
            "remark": str,
            "booker_id": int,
            "bookerfirstname": str,
            "bookerlastname": str,
            "bookergender": str,
            "bookertitle": str,
            "bookerphone": str,
            "bookeremail": str,
            "bookeraddress1": str,
            "bookeraddress2": str,
            "bookeraddress3": str,
            "bookercity": str,
            "bookerpostalcode": str,
            "bookerstate": str,
            "bookercountry": str,
            "bookernation": str,
            "bookerbirthdate": str,
            "bookercitizenid": str,
            "flight1": str,
            "eta": str,
            "flight2": str,
            "etd": str,
            "room_number": str,
            "ci_time": str,
            "co_time": str,
            "rtc": str
        })
    t_guest_data, T_guest = create_model(
        "T_guest",
        {
            "recid1": int,
            "gtype": int,
            "guest_id": int,
            "guest_title": str,
            "firstname": str,
            "lastname": str,
            "gender": str,
            "phonenum": str,
            "mobilenum": str,
            "email": str,
            "addresstype": str,
            "address1": str,
            "address2": str,
            "address3": str,
            "city": str,
            "postalcode": str,
            "state": str,
            "country": str,
            "primary_guest": int,
            "birthdate": str,
            "nationality": str,
            "citizenid": str
        })
    t_rate_data, T_rate = create_model(
        "T_rate",
        {
            "recid1": int,
            "effectivedate": date,
            "expiredate": date,
            "unitmultiplier": int,
            "aftertax": Decimal,
            "tax_percent": Decimal,
            "totalaftertax": Decimal,
            "totaltax_amount": Decimal
        })
    art_list_data, Art_list = create_model(
        "Art_list",
        {
            "recid1": int,
            "bezeich": str,
            "price": Decimal,
            "qty": int,
            "artnr": str
        })
    temp_reslin_queasy_data, Temp_reslin_queasy = create_model(
        "Temp_reslin_queasy",
        {
            "resnr": int,
            "reslinnr": int,
            "number2": int
        })

    buffzim = create_buffer("Buffzim", Zimkateg)
    Bufguest = create_buffer("Bufguest", Guest)
    Bufres_line = create_buffer("Bufres_line", Res_line)
    Bufguest2 = create_buffer("Bufguest2", Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_resline_data, t_rate_data, t_guest_data, art_list_data, ci_date, loop_i, str, contcode, out_str, datum, datum1, to_date, curr_i, datum2, add_it, argt_rate, delta, start_date, co_date, departement, artikelnr, i, htl_code, htl_name, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, totvat, service, t_rmrev, t_fbrev, t_others, icount, datecounter, temp_rate, zimkateg, guest, res_line, htparam, paramtext, interface, reservation, waehrung, sourccod, reslin_queasy, fixleist, artikel
        nonlocal casetype
        nonlocal buffzim, bufguest, bufres_line, bufguest2
        nonlocal t_resline, t_guest, t_rate, art_list, temp_reslin_queasy, buffzim, bufguest, bufres_line, bufguest2
        nonlocal t_resline_data, t_guest_data, t_rate_data, art_list_data, temp_reslin_queasy_data

        return {
            "t-resline": t_resline_data,
            "t-rate": t_rate_data,
            "t-guest": t_guest_data,
            "art-list": art_list_data
        }

    def decode_string(in_str: string):
        nonlocal t_resline_data, t_rate_data, t_guest_data, art_list_data, ci_date, loop_i, str, contcode, out_str, datum, datum1, to_date, curr_i, datum2, add_it, argt_rate, delta, start_date, co_date, departement, artikelnr, i, htl_code, htl_name, flodging, lodging, breakfast, lunch, dinner, others, rmrate, net_vat, net_service, vat, totvat, service, t_rmrev, t_fbrev, t_others, icount, datecounter, temp_rate, zimkateg, guest, res_line, htparam, paramtext, interface, reservation, waehrung, sourccod, reslin_queasy, fixleist, artikel
        nonlocal casetype
        nonlocal buffzim, bufguest, bufres_line, bufguest2
        nonlocal t_resline, t_guest, t_rate, art_list, temp_reslin_queasy, buffzim, bufguest, bufres_line, bufguest2
        nonlocal t_resline_data, t_guest_data, t_rate_data, art_list_data, temp_reslin_queasy_data

        out_str = ""
        s = ""
        j: int = 0
        len_: int = 0

        def generate_inner_output():
            return (out_str)

        in_str = paramtext.ptexte
        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1, length(s) + 1):
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    icount = 1

    htparam = get_cache(Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    paramtext = get_cache(Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext:
        out_str = decode_string(paramtext.ptexte)
        htl_code = out_str

    paramtext = get_cache(Paramtext, {"txtnr": [(eq, 240)]})

    if paramtext:
        out_str = decode_string(paramtext.ptexte)
        htl_name = out_str

    for t_resline in query(t_resline_data):
        t_resline_data.remove(t_resline)
        pass

    for t_rate in query(t_rate_data):
        t_rate_data.remove(t_rate)
        pass

    for t_guest in query(t_guest_data):
        t_guest_data.remove(t_guest)
        pass

    for art_list in query(art_list_data):
        art_list_data.remove(art_list)
        pass

    if casetype.lower() == "new-initial":
        for interface in db_session.query(Interface).filter(
                # (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$LODGIQ$*"))) & (matches((Interface.parameters, "*new|init*")))).order_by(intdate, int_time).all():
                (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$LODGIQ$*"))) & (matches((Interface.parameters, "*new|init*")))).order_by(Interface.intdate, Interface.int_time).all():

            res_line = get_cache(Res_line, {"resnr": [(eq, interface.resnr)], "reslinnr": [(
                eq, interface.reslinnr)], "resstatus": [(ne, 11), (ne, 13)], "l_zuordnung[2]": [(eq, 0)]})

            if res_line:
                bufguest = get_cache(
                    Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
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

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache(
                    Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache(
                    Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1, num_entries(res_line.zimmer_wunsch, ";") - 1 + 1):
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$"):
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.resid = to_string(
                    res_line.resnr) + to_string(res_line.reslinnr, "999")
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name

                if length(t_resline.remark) >= 500:
                    t_resline.remark = substring(res_line.bemerk, 0, 495)
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(60), "")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(62), "")

                if reservation:

                    if length(t_resline.mainrsvcomment) >= 500:
                        t_resline.mainrsvcomment = substring(
                            t_resline.mainrsvcomment, 0, 495)
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(60), "")
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(62), "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache(
                        Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez
                    t_resline.rtc = zimkateg.kurzbez

                if waehrung:
                    if matches(waehrung.bezeich, r"*RUPIAH*") and waehrung.wabkurz.lower() != "idr":
                        t_resline.currency = "IDR"

                    else:
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
                        t_resline.bookerbirthdate = to_string(
                            guest.geburtdatum1)

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
                for datum1 in date_range(res_line.ankunft, to_date):
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(
                        get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat = to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                temp_rate = to_decimal("0")

                for datum in date_range(res_line.ankunft, datum2):

                    reslin_queasy = get_cache(Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(
                        eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, datum)], "date2": [(ge, datum)]})

                    if reslin_queasy:

                        if temp_rate != reslin_queasy.deci1 or reslin_queasy.deci1 == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(reslin_queasy.deci1, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(reslin_queasy.deci1)
                    
                    else:
                        if temp_rate != res_line.zipreis or res_line.zipreis == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(res_line.zipreis, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(res_line.zipreis)

                for bufres_line in db_session.query(Bufres_line).filter(
                        (Bufres_line.resnr == res_line.resnr) & (Bufres_line.kontakt_nr == res_line.reslinnr) & (Bufres_line.resstatus == 11) & (Bufres_line.l_zuordnung[inc_value(2)] == 0)).order_by(Bufres_line._recid).all():

                    bufguest = get_cache(
                        Guest, {"gastnr": [(eq, bufres_line.gastnrmember)]})

                    if bufguest:
                        t_guest = T_guest()
                        t_guest_data.append(t_guest)

                        t_guest.recid1 = interface._recid
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
                        t_guest.primary_guest = 0
                        t_guest.nationality = bufguest.nation1
                        t_guest.citizenid = bufguest.ausweis_nr1

                        if bufguest.geburtdatum1 != None:
                            t_guest.birthdate = to_string(
                                bufguest.geburtdatum1)

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

                        if bufguest.karteityp == 0:
                            t_guest.addresstype = "1"

                        elif bufguest.karteityp == 1:
                            t_guest.addresstype = "2"

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft, co_date):
                    argt_rate = to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                            (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate = to_decimal("0")

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
                            start_date = res_line.ankunft + \
                                timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:

                            artikel = get_cache(Artikel, {"artnr": [(eq, fixleist.artnr)], "departement": [
                                                (eq, fixleist.departement)]})
                            argt_rate = to_decimal(
                                fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:

                            art_list = query(art_list_data, filters=(
                                lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.bezeich = artikel.bezeich
                            art_list.price = to_decimal(
                                art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(
                                artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                db_session.delete(interface)
            icount = icount + 1

            if icount == 26:

                return generate_output()

    elif casetype.lower() == "modify-initial":
        for interface in db_session.query(Interface).filter(
                (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$LODGIQ$*"))) & (matches((Interface.parameters, "*modify|init*")))).order_by(Interface.intdate, Interface.int_time).all():

            res_line = get_cache(Res_line, {"resnr": [(eq, interface.resnr)], "reslinnr": [(
                eq, interface.reslinnr)], "resstatus": [(ne, 11), (ne, 13)], "l_zuordnung[2]": [(eq, 0)]})

            if res_line:

                bufguest = get_cache(
                    Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
                    t_guest.gtype = bufguest.karteityp
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

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache(
                    Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                buffzim = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache(
                    Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1, num_entries(res_line.zimmer_wunsch, ";") - 1 + 1):
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == "$CODE$":
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.resid = to_string(
                    res_line.resnr) + to_string(res_line.reslinnr, "999")
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.remark = res_line.bemerk
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(60), "")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(62), "")

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(60), "")
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(62), "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache(
                        Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                # if buffZim:
                #     t_resline.rtc = buffZim.kurzbez
                if buffzim:
                    t_resline.rtc = buffzim.kurzbez

                if waehrung:
                    if matches(waehrung.bezeich, r"*RUPIAH*") and waehrung.wabkurz.lower() != "idr":
                        t_resline.currency = "IDR"

                    else:
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
                        t_resline.bookerbirthdate = to_string(
                            guest.geburtdatum1)

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
                for datum1 in date_range(res_line.ankunft, to_date):
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(
                        get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat = to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                temp_rate = to_decimal("0")

                for datum in date_range(res_line.ankunft, datum2):
                    reslin_queasy = get_cache(Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(
                        eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, datum)], "date2": [(ge, datum)]})

                    if reslin_queasy:
                        if temp_rate != reslin_queasy.deci1 or reslin_queasy.deci1 == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(reslin_queasy.deci1, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(reslin_queasy.deci1)
                    
                    else:
                        if temp_rate != res_line.zipreis or res_line.zipreis == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(res_line.zipreis, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(res_line.zipreis)

                for bufres_line in db_session.query(Bufres_line).filter(
                        (Bufres_line.resnr == res_line.resnr) & (Bufres_line.kontakt_nr == res_line.reslinnr) & (Bufres_line.resstatus == 11) & (Bufres_line.l_zuordnung[inc_value(2)] == 0)).order_by(Bufres_line._recid).all():
                    bufguest = get_cache(
                        Guest, {"gastnr": [(eq, bufres_line.gastnrmember)]})

                    if bufguest:
                        t_guest = T_guest()
                        t_guest_data.append(t_guest)

                        t_guest.recid1 = interface._recid
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
                        t_guest.primary_guest = 0
                        t_guest.nationality = bufguest.nation1
                        t_guest.citizenid = bufguest.ausweis_nr1

                        if bufguest.geburtdatum1 != None:
                            t_guest.birthdate = to_string(
                                bufguest.geburtdatum1)

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

                        if bufguest.karteityp == 0:
                            t_guest.addresstype = "1"

                        elif bufguest.karteityp == 1:
                            t_guest.addresstype = "2"

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft, co_date):
                    argt_rate = to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                            (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate = to_decimal("0")

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
                            start_date = res_line.ankunft + \
                                timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:
                            artikel = get_cache(Artikel, {"artnr": [(eq, fixleist.artnr)], "departement": [
                                                (eq, fixleist.departement)]})
                            argt_rate = to_decimal(
                                fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:
                            art_list = query(art_list_data, filters=(
                                lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.bezeich = artikel.bezeich
                            art_list.price = to_decimal(
                                art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(
                                artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                db_session.delete(interface)
            icount = icount + 1

            if icount == 26:
                return generate_output()

    elif casetype.lower() == "cancel-initial":
        for interface in db_session.query(Interface).filter(
                (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$IDEASV3$*"))) & (matches((Interface.parameters, "*cancel|init*")))).order_by(Interface.intdate, Interface.int_time).all():
            res_line = get_cache(Res_line, {"resnr": [(eq, interface.resnr)], "reslinnr": [(eq, interface.reslinnr)]})

            if res_line:
                reservation = get_cache(
                    Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache(
                    Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1, num_entries(res_line.zimmer_wunsch, ";") - 1 + 1):
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$"):
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.resid = to_string(
                    res_line.resnr) + to_string(res_line.reslinnr, "999")
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(60), "")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(62), "")
                t_resline.rateplancode = contcode

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(60), "")
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(62), "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache(
                        Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez
                    t_resline.rtc = zimkateg.kurzbez

                if waehrung:
                    if matches(waehrung.bezeich, r"*RUPIAH*") and waehrung.wabkurz.lower() != "idr":
                        t_resline.currency = "IDR"

                    else:
                        t_resline.currency = waehrung.wabkurz

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
                for datum1 in date_range(res_line.ankunft, to_date):
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(
                        get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat = to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                temp_rate = to_decimal("0")

                for datum in date_range(res_line.ankunft, datum2):
                    reslin_queasy = get_cache(Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(
                        eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, datum)], "date2": [(ge, datum)]})

                    if reslin_queasy:
                        if temp_rate != reslin_queasy.deci1 or reslin_queasy.deci1 == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(reslin_queasy.deci1, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(reslin_queasy.deci1)
                    
                    else:
                        if temp_rate != res_line.zipreis or res_line.zipreis == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(res_line.zipreis, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(res_line.zipreis)

            elif not res_line:
                db_session.delete(interface)
            icount = icount + 1

            if icount == 26:
                return generate_output()

    elif casetype.lower() == "new":
        interface = db_session.query(Interface).filter(
            (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$IDEASV3$*"))) & (matches((Interface.parameters, "*insert*"))) | (matches(Interface.parameters, "*qci*"))) | (matches(Interface.parameters, "*new*")) | (matches(Interface.parameters, "*split*")).first()
        
        while interface is not None:
            res_line = get_cache(Res_line, {"resnr": [(eq, interface.resnr)], "reslinnr": [(
                eq, interface.reslinnr)], "resstatus": [(ne, 11), (ne, 13)], "l_zuordnung[2]": [(eq, 0)]})

            if res_line:
                bufguest = get_cache(
                    Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
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

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache(
                    Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache(
                    Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1, num_entries(res_line.zimmer_wunsch, ";") - 1 + 1):
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower():
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.resid = to_string(
                    res_line.resnr) + to_string(res_line.reslinnr, "999")
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.remark = res_line.bemerk
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(60), "")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(62), "")

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(60), "")
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(62), "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache(
                        Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez
                    t_resline.rtc = zimkateg.kurzbez

                if waehrung:
                    if matches(waehrung.bezeich, r"*RUPIAH*") and waehrung.wabkurz.lower() != "idr":
                        t_resline.currency = "IDR"

                    else:
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
                        t_resline.bookerbirthdate = to_string(
                            guest.geburtdatum1)

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
                for datum1 in date_range(res_line.ankunft, to_date):
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(
                        get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat = to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                temp_rate = to_decimal("0")

                for datum in date_range(res_line.ankunft, datum2):
                    reslin_queasy = get_cache(Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(
                        eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, datum)], "date2": [(ge, datum)]})

                    if reslin_queasy:
                        if temp_rate != reslin_queasy.deci1 or reslin_queasy.deci1 == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(reslin_queasy.deci1, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(reslin_queasy.deci1)
                    
                    else:
                        if temp_rate != res_line.zipreis or res_line.zipreis == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(res_line.zipreis, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(res_line.zipreis)

                for bufres_line in db_session.query(Bufres_line).filter(
                        (Bufres_line.resnr == res_line.resnr) & (Bufres_line.kontakt_nr == res_line.reslinnr) & (Bufres_line.resstatus == 11) & (Bufres_line.l_zuordnung[inc_value(2)] == 0)).order_by(Bufres_line._recid).all():
                    bufguest = get_cache(
                        Guest, {"gastnr": [(eq, bufres_line.gastnrmember)]})

                    if bufguest:
                        t_guest = T_guest()
                        t_guest_data.append(t_guest)

                        t_guest.recid1 = interface._recid
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
                        t_guest.primary_guest = 0
                        t_guest.nationality = bufguest.nation1
                        t_guest.citizenid = bufguest.ausweis_nr1

                        if bufguest.geburtdatum1 != None:
                            t_guest.birthdate = to_string(
                                bufguest.geburtdatum1)

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

                        if bufguest.karteityp == 0:
                            t_guest.addresstype = "1"

                        elif bufguest.karteityp == 1:
                            t_guest.addresstype = "2"

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft, co_date):
                    argt_rate = to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                            (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate = to_decimal("0")

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
                            start_date = res_line.ankunft + \
                                timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:
                            artikel = get_cache(Artikel, {"artnr": [(eq, fixleist.artnr)], "departement": [
                                                (eq, fixleist.departement)]})
                            argt_rate = to_decimal(
                                fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:
                            art_list = query(art_list_data, filters=(
                                lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.bezeich = artikel.bezeich
                            art_list.price = to_decimal(
                                art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(
                                artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                db_session.delete(interface)
            icount = icount + 1

            if icount == 6:
                return generate_output()

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$IDEASV3$*"))) & (matches((Interface.parameters, "*insert*"))) | (matches(Interface.parameters, "*qci*"))) | (matches(Interface.parameters, "*new*")) | (matches(Interface.parameters, "*split*")) & (Interface._recid > curr_recid).first()

    elif casetype.lower() == "update":
        interface = db_session.query(Interface).filter(
            (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$IDEASV3$*"))) & (matches((Interface.parameters, "*modify*"))) | (matches(Interface.parameters, "*checkin*"))) | (matches(Interface.parameters, "*checkout*")).first()
        while interface is not None:
            res_line = get_cache(Res_line, {"resnr": [(eq, interface.resnr)], "reslinnr": [(
                eq, interface.reslinnr)], "resstatus": [(ne, 11), (ne, 13)], "l_zuordnung[2]": [(eq, 0)]})

            if res_line:
                bufguest = get_cache(
                    Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bufguest:
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    t_guest.recid1 = interface._recid
                    t_guest.gtype = bufguest.karteityp
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

                    if bufguest.karteityp == 0:
                        t_guest.addresstype = "1"

                    elif bufguest.karteityp == 1:
                        t_guest.addresstype = "2"

                reservation = get_cache(
                    Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                buffzim = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.l_zuordnung[0])]})

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache(
                    Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1, num_entries(res_line.zimmer_wunsch, ";") - 1 + 1):
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower():
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.resid = to_string(
                    res_line.resnr) + to_string(res_line.reslinnr, "999")
                t_resline.unitnumber = res_line.zimmeranz
                t_resline.rateplancode = contcode
                t_resline.adult = res_line.erwachs
                t_resline.child = res_line.kind1
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.remark = res_line.bemerk
                t_resline.flight1 = substring(res_line.flight_nr, 0, 6)
                t_resline.eta = substring(res_line.flight_nr, 6, 5)
                t_resline.flight2 = substring(res_line.flight_nr, 11, 6)
                t_resline.etd = substring(res_line.flight_nr, 17, 5)
                t_resline.room_number = res_line.zinr
                t_resline.ci_time = to_string(res_line.ankzeit, "HH:MM:SS")
                t_resline.co_time = to_string(res_line.abreisezeit, "HH:MM:SS")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(60), "")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(62), "")

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(60), "")
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(62), "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache(
                        Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez

                if buffzim:
                    t_resline.rtc = buffzim.kurzbez

                if waehrung:
                    if matches(waehrung.bezeich, r"*RUPIAH*") and waehrung.wabkurz.lower() != "idr":
                        t_resline.currency = "IDR"

                    else:
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
                        t_resline.bookerbirthdate = to_string(
                            guest.geburtdatum1)

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
                for datum1 in date_range(res_line.ankunft, to_date):
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(
                        get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat = to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                temp_rate = to_decimal("0")

                for datum in date_range(res_line.ankunft, datum2):
                    reslin_queasy = get_cache(Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(
                        eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, datum)], "date2": [(ge, datum)]})

                    if reslin_queasy:
                        if temp_rate != reslin_queasy.deci1 or reslin_queasy.deci1 == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(reslin_queasy.deci1, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(reslin_queasy.deci1)
                    
                    else:
                        if temp_rate != res_line.zipreis or res_line.zipreis == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(res_line.zipreis, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(res_line.zipreis)

                for bufres_line in db_session.query(Bufres_line).filter(
                        (Bufres_line.resnr == res_line.resnr) & (Bufres_line.kontakt_nr == res_line.reslinnr) & (Bufres_line.resstatus == 11) & (Bufres_line.l_zuordnung[inc_value(2)] == 0)).order_by(Bufres_line._recid).all():
                    bufguest = get_cache(
                        Guest, {"gastnr": [(eq, bufres_line.gastnrmember)]})

                    if bufguest:
                        t_guest = T_guest()
                        t_guest_data.append(t_guest)

                        t_guest.recid1 = interface._recid
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
                        t_guest.primary_guest = 0
                        t_guest.nationality = bufguest.nation1
                        t_guest.citizenid = bufguest.ausweis_nr1

                        if bufguest.geburtdatum1 != None:
                            t_guest.birthdate = to_string(
                                bufguest.geburtdatum1)

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

                        if bufguest.karteityp == 0:
                            t_guest.addresstype = "1"

                        elif bufguest.karteityp == 1:
                            t_guest.addresstype = "2"

                if res_line.abreise > res_line.ankunft:
                    co_date = res_line.abreise - timedelta(days=1)
                else:
                    co_date = res_line.abreise
                for datum2 in date_range(res_line.ankunft, co_date):
                    argt_rate = to_decimal("0")

                    for fixleist in db_session.query(Fixleist).filter(
                            (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                        add_it = False
                        argt_rate = to_decimal("0")

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
                            start_date = res_line.ankunft + \
                                timedelta(days=delta)

                            if (res_line.abreise - start_date) < fixleist.dekade:
                                start_date = res_line.ankunft

                            if datum2 <= (start_date + timedelta(days=(fixleist.dekade - 1))):
                                add_it = True

                            if datum2 < start_date:
                                add_it = False

                        if add_it:
                            artikel = get_cache(Artikel, {"artnr": [(eq, fixleist.artnr)], "departement": [
                                                (eq, fixleist.departement)]})
                            argt_rate = to_decimal(
                                fixleist.betrag) * to_decimal(fixleist.number)

                        if argt_rate != 0:
                            art_list = query(art_list_data, filters=(
                                lambda art_list: art_list.bezeich == artikel.bezeich), first=True)

                            if not art_list:
                                art_list = Art_list()
                                art_list_data.append(art_list)

                            art_list.recid1 = interface._recid
                            art_list.bezeich = artikel.bezeich
                            art_list.price = to_decimal(
                                art_list.price) + to_decimal(argt_rate)
                            art_list.qty = fixleist.number
                            art_list.artnr = to_string(
                                artikel.departement, "999") + to_string(artikel.artnr, "9999")

            elif not res_line:
                db_session.delete(interface)
            icount = icount + 1

            if icount == 6:
                return generate_output()

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$IDEASV3$*"))) & (matches((Interface.parameters, "*modify*"))) | (matches(Interface.parameters, "*checkin*"))) | (matches(Interface.parameters, "*checkout*")) & (Interface._recid > curr_recid).first()

    elif casetype.lower() == ("cancel").lower():

        interface = db_session.query(Interface).filter(
            (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$IDEASV3$*"))) & (matches((Interface.parameters, "*cancel*"))) | (matches(Interface.parameters, "*delete*"))).first()
        while interface is not None:
            res_line = get_cache(Res_line, {"resnr": [(eq, interface.resnr)], "reslinnr": [(eq, interface.reslinnr)]})

            if res_line:
                reservation = get_cache(
                    Reservation, {"resnr": [(eq, res_line.resnr)]})

                zimkateg = get_cache(
                    Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

                waehrung = get_cache(
                    Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                guest = get_cache(
                    Guest, {"gastnr": [(eq, reservation.gastnr)]})
                for loop_i in range(1, num_entries(res_line.zimmer_wunsch, ";") - 1 + 1):
                    str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$"):
                        contcode = substring(str, 6)
                t_resline = T_resline()
                t_resline_data.append(t_resline)

                t_resline.recid1 = interface._recid
                t_resline.resnr = res_line.resnr
                t_resline.reslinnr = res_line.reslinnr
                t_resline.resid = to_string(
                    res_line.resnr) + to_string(res_line.reslinnr, "999")
                t_resline.startdate = res_line.ankunft
                t_resline.enddate = res_line.abreise
                t_resline.hotelcode = htl_code
                t_resline.hotelname = htl_name
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(60), "")
                t_resline.remark = replace_str(
                    t_resline.remark, chr_unicode(62), "")
                t_resline.rateplancode = contcode

                if reservation:
                    t_resline.mainrsvcomment = reservation.bemerk
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(60), "")
                    t_resline.mainrsvcomment = replace_str(
                        t_resline.mainrsvcomment, chr_unicode(62), "")

                    if reservation.resdat != None:
                        t_resline.createdate = reservation.resdat

                    sourccod = get_cache(
                        Sourccod, {"source_code": [(eq, reservation.resart)]})

                    if sourccod:
                        t_resline.booksource = sourccod.bezeich

                if zimkateg:
                    t_resline.roomtypecode = zimkateg.kurzbez
                    t_resline.rtc = zimkateg.kurzbez

                if waehrung:
                    if matches(waehrung.bezeich, r"*RUPIAH*") and waehrung.wabkurz.lower() != "idr":
                        t_resline.currency = "IDR"

                    else:
                        t_resline.currency = waehrung.wabkurz

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
                for datum1 in date_range(res_line.ankunft, to_date):
                    curr_i = curr_i + 1
                    flodging, lodging, breakfast, lunch, dinner, others, rmrate, vat, service = get_output(
                        get_room_breakdown(res_line._recid, datum1, curr_i, datum))
                    totvat = to_decimal(totvat) + to_decimal(vat)

                if res_line.ankunft != res_line.abreise:
                    datum2 = res_line.abreise - timedelta(days=1)
                else:
                    datum2 = res_line.abreise
                temp_rate = to_decimal("0")

                for datum in date_range(res_line.ankunft, datum2):
                    reslin_queasy = get_cache(Reslin_queasy, {"key": [(eq, "arrangement")], "resnr": [(
                        eq, res_line.resnr)], "reslinnr": [(eq, res_line.reslinnr)], "date1": [(le, datum)], "date2": [(ge, datum)]})

                    if reslin_queasy:
                        if temp_rate != reslin_queasy.deci1 or reslin_queasy.deci1 == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(reslin_queasy.deci1, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(reslin_queasy.deci1)
                    
                    else:
                        if temp_rate != res_line.zipreis or res_line.zipreis == 0:
                            t_rate = T_rate()
                            t_rate_data.append(t_rate)

                            t_rate.recid1 = interface._recid
                            t_rate.unitmultiplier = 1
                            t_rate.aftertax = to_decimal(
                                round(res_line.zipreis, 2))
                            t_rate.totaltax_amount = to_decimal(
                                round(totvat, 2))
                            t_rate.totalaftertax = to_decimal(
                                round(t_rate.aftertax * t_rate.unitmultiplier, 2))

                            if t_rate.totaltax_amount != 0:
                                t_rate.tax_percent = to_decimal(
                                    round(t_rate.totalaftertax / t_rate.totaltax_amount, 2))

                            if res_line.ankunft != res_line.abreise:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum + timedelta(days=1)

                            else:
                                t_rate.effectivedate = datum
                                t_rate.expiredate = datum

                        else:
                            t_rate.expiredate = datum + timedelta(days=1)

                        temp_rate = to_decimal(res_line.zipreis)

            elif not res_line:
                db_session.delete(interface)
            icount = icount + 1

            if icount == 6:
                return generate_output()

            curr_recid = interface._recid
            interface = db_session.query(Interface).filter(
                (Interface.key == 10) & (not_(matches(Interface.nebenstelle, "*$IDEASV3$*"))) & (matches((Interface.parameters, "*cancel*"))) | (matches(Interface.parameters, "*delete*"))) & (Interface._recid > curr_recid).first()

    return generate_output()
