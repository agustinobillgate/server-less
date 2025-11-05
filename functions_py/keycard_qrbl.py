#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 05/11/2025
# to_int(res_line.code))]}) -> to_int(res_line.code.strip()))}).first() 
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Guest, Zimmer, Reservation, Queasy, Artikel, Guestbook, Nation

def keycard_qrbl(room:string, res_nr:int, reslin_nr:int, checkoutdate:date):

    prepare_cache ([Res_line, Guest, Zimmer, Reservation, Queasy, Artikel, Guestbook, Nation])

    room_status = ""
    res_status = ""
    guest_name = ""
    ci_datetime = None
    co_datetime = None
    type_ofpay = ""
    oth_deposit = to_decimal("0.0")
    key_done = 0
    key_status = ""
    guest_phone = ""
    guest_email = ""
    guest_country = ""
    purpose_stay = ""
    rsv_deposit = to_decimal("0.0")
    rsv_deposit_str = ""
    oth_deposit_str = ""
    img_idcard_data = []
    citime:string = ""
    cotime:string = ""
    cidate:string = ""
    codate:string = ""
    loop_i:int = 0
    mestoken:string = ""
    meskeyword:string = ""
    mesvalue:string = ""
    lvcs:string = ""
    lviresnr:int = 0
    res_line = guest = zimmer = reservation = queasy = artikel = guestbook = nation = None

    img_idcard = None

    img_idcard_data, Img_idcard = create_model("Img_idcard", {"gastnr":int, "zinr":string, "objfile":bytes})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_status, res_status, guest_name, ci_datetime, co_datetime, type_ofpay, oth_deposit, key_done, key_status, guest_phone, guest_email, guest_country, purpose_stay, rsv_deposit, rsv_deposit_str, oth_deposit_str, img_idcard_data, citime, cotime, cidate, codate, loop_i, mestoken, meskeyword, mesvalue, lvcs, lviresnr, res_line, guest, zimmer, reservation, queasy, artikel, guestbook, nation
        nonlocal room, res_nr, reslin_nr, checkoutdate


        nonlocal img_idcard
        nonlocal img_idcard_data

        return {"res_nr": res_nr, "reslin_nr": reslin_nr, "room_status": room_status, "res_status": res_status, "guest_name": guest_name, "ci_datetime": ci_datetime, "co_datetime": co_datetime, "type_ofpay": type_ofpay, "oth_deposit": oth_deposit, "key_done": key_done, "key_status": key_status, "guest_phone": guest_phone, "guest_email": guest_email, "guest_country": guest_country, "purpose_stay": purpose_stay, "rsv_deposit": rsv_deposit, "rsv_deposit_str": rsv_deposit_str, "oth_deposit_str": oth_deposit_str, "img-idcard": img_idcard_data}

    def assign_it():

        nonlocal room_status, res_status, guest_name, ci_datetime, co_datetime, type_ofpay, oth_deposit, key_done, key_status, guest_phone, guest_email, guest_country, purpose_stay, rsv_deposit, rsv_deposit_str, oth_deposit_str, img_idcard_data, citime, cotime, cidate, codate, loop_i, mestoken, meskeyword, mesvalue, lvcs, lviresnr, res_line, guest, zimmer, reservation, queasy, artikel, guestbook, nation
        nonlocal room, res_nr, reslin_nr, checkoutdate


        nonlocal img_idcard
        nonlocal img_idcard_data

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if zimmer.zistatus == 0:
            room_status = "VACANT CLEAN CHECKED"

        elif zimmer.zistatus == 1:
            room_status = "VACANT CLEAN UNCHECKED"

        elif zimmer.zistatus == 2:
            room_status = "VACANT DIRTY"

        elif zimmer.zistatus == 3:
            room_status = "EXPECTED DEPARTURE"

        elif zimmer.zistatus == 4:
            room_status = "OCCUPIED DIRTY"

        elif zimmer.zistatus == 5:
            room_status = "OCCUPIED CLEANED"

        elif zimmer.zistatus == 6:
            room_status = "OUT OF ORDER"

        elif zimmer.zistatus == 7:
            room_status = "OFF MARKET"

        elif zimmer.zistatus == 8:
            room_status = "DO NOT DISTURB"

        if res_line.resstatus == 1:
            res_status = "GUARANTEED RESERVATION"

        elif res_line.resstatus == 2:
            res_status = "6 PM RESERVATION"

        elif res_line.resstatus == 3:
            res_status = "TENTATIVE RESERVATION"

        elif res_line.resstatus == 4:
            res_status = "WAITING LIST RESERVATION"

        elif res_line.resstatus == 5:
            res_status = "ORAL CONFIRM RESERVATION"

        elif res_line.resstatus == 6:
            res_status = "RESIDENT GUEST"

        elif res_line.resstatus == 8:
            res_status = "CHECK OUT GUEST"
        guest_name = guest.anrede1 + "," + guest.vorname1 + " " + guest.name
        guest_name = guest_name.upper()
        citime = to_string(res_line.ankzeit, "HH:MM:SS")
        cotime = to_string(res_line.abreisezeit, "HH:MM:SS")
        cidate = to_string(get_day(res_line.ankunft)) + "-" + to_string(get_month(res_line.ankunft)) + "-" + to_string(get_year(res_line.ankunft))
        codate = to_string(get_day(res_line.abreise)) + "-" + to_string(get_month(res_line.abreise)) + "-" + to_string(get_year(res_line.abreise))
        ci_datetime = to_datetime(cidate + " " + citime)
        co_datetime = to_datetime(codate + " " + cotime)

        if res_line.code != "" and res_line.code.lower()  != ("0").lower() :

            # queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})
            queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})

            if queasy:
                type_ofpay = queasy.char1.upper()
        rsv_deposit =  to_decimal(reservation.depositgef)

        if rsv_deposit != 0:

            artikel = db_session.query(Artikel).filter(
                     (Artikel.departement == 0) & ((Artikel.artart == 2) | (Artikel.artart == 5) | (Artikel.artart == 6) | (Artikel.artart == 7)) & (Artikel.activeflag) & (Artikel.artnr == reservation.zahlkonto)).first()

            if artikel:
                rsv_deposit_str = artikel.bezeich.upper()
        key_done = res_line.betrieb_gast

        if key_done != 0:
            key_status = "DUPLICATE KEY"
        else:
            key_status = "NEW KEY"

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guestbook:
            img_idcard = Img_idcard()
            img_idcard_data.append(img_idcard)

            img_idcard.gastnr = guestbook.gastnr
            img_idcard.zinr = res_line.zinr
            img_idcard.objfile = guestbook.imagefile


        res_nr = res_line.resnr
        reslin_nr = res_line.reslinnr
        guest_phone = guest.mobil_telefon
        guest_email = guest.email_adr
        guest_country = guest.land

        nation = get_cache (Nation, {"kurzbez": [(eq, guest_country)]})

        if nation:
            guest_country = nation.bezeich
        for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
            mestoken = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

            if substring(mestoken, 0, 8) == ("SEGM_PUR").lower() :
                meskeyword = substring(mestoken, 0, 8)
                mesvalue = substring(mestoken, 8, 1)
                return

        if to_int(mesvalue) != 0:

            queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(mesvalue))]})

            if queasy:
                purpose_stay = queasy.char3
        oth_deposit =  to_decimal("0")
        pass
        pass
        pass
        pass
        pass
        pass
        pass
        pass


    if res_nr != 0:

        res_line = get_cache (Res_line, {"resnr": [(eq, res_nr)],"reslinnr": [(eq, reslin_nr)],"zinr": [(eq, room)]})

        if res_line:
            assign_it()
    else:

        res_line = get_cache (Res_line, {"zinr": [(eq, room)],"abreise": [(eq, checkoutdate)]})

        if res_line:
            assign_it()

    return generate_output()