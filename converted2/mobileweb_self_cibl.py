#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.search_reservationbl import search_reservationbl
from functions.iproom_assignmentbl import iproom_assignmentbl
from models import Res_line, Queasy, Guestbook, Waehrung, Guest, Interface, Reservation, Zimmer

def mobileweb_self_cibl(co_date:date, book_code:string, ch_name:string, early_ci:bool, max_room:int, citime:string, groupflag:bool):

    prepare_cache ([Res_line, Queasy, Waehrung, Guest, Reservation])

    mess_result = ""
    arrival_guestlist_data = []
    delete_it:int = 0
    err_code:int = 0
    ercode:int = 0
    i:int = 0
    tmp_char:string = ""
    ci_time:string = ""
    depo_bal:Decimal = to_decimal("0.0")
    res_flag:bool = False
    res_line = queasy = guestbook = waehrung = guest = interface = reservation = zimmer = None

    arrival_guest = arrival_guestlist = buff_resline = None

    arrival_guest_data, Arrival_guest = create_model("Arrival_guest", {"i_counter":int, "gastno":int, "resnr":int, "reslinnr":int, "gast":string, "ci":date, "co":date, "rmtype":string, "zinr":string, "argt":string, "adult":string, "child":string, "rmtype_str":string, "room_sharer":bool, "pre_checkin":bool, "argt_str":string, "preference":string, "new_zinr":bool, "zikatnr":int, "l_selected":bool, "kontakt_nr":int, "room_stat":int, "res_status":int})
    arrival_guestlist_data, Arrival_guestlist = create_model("Arrival_guestlist", {"i_counter":int, "gastno":int, "resnr":int, "reslinnr":int, "gast":string, "ci":date, "co":date, "rmtype":string, "zinr":string, "argt":string, "adult":string, "child":string, "rmtype_str":string, "room_sharer":bool, "pre_checkin":bool, "argt_str":string, "preference":string, "new_zinr":bool, "zikatnr":int, "l_selected":bool, "kontakt_nr":int, "guest_email":string, "guest_phnumber":string, "guest_nation":string, "guest_country":string, "guest_region":string, "room_preference":string, "purposeofstay":string, "room_status":string, "image_flag":string, "currency_usage":string, "key_generated":bool, "preauth_flag":bool, "res_status":string, "ifdata_sent":bool, "param_broadcast":string, "wifi_password":string, "payment_method":string, "payment_status":string, "payment_channel":string, "transid_merchant":string, "vehicle_number":string, "smoking_room":bool, "amount_depo":Decimal, "depo_paid1":Decimal, "depo_paid2":Decimal, "depo_balance":Decimal})

    Buff_resline = create_buffer("Buff_resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, arrival_guestlist_data, delete_it, err_code, ercode, i, tmp_char, ci_time, depo_bal, res_flag, res_line, queasy, guestbook, waehrung, guest, interface, reservation, zimmer
        nonlocal co_date, book_code, ch_name, early_ci, max_room, citime, groupflag
        nonlocal buff_resline


        nonlocal arrival_guest, arrival_guestlist, buff_resline
        nonlocal arrival_guest_data, arrival_guestlist_data

        return {"mess_result": mess_result, "arrival-guestlist": arrival_guestlist_data}


    if co_date == None:
        mess_result = "99 - CheckOut Date Is Mandatory!"

        return generate_output()

    if citime == "" or citime == None:
        mess_result = "99 - CheckIn Time Is Mandatory! - HH:MM"

        return generate_output()

    if length(citime) != 5:
        mess_result = "99 - CheckIn Time Format Is Invalid, should be [HH:MM]"

        return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 8)],"number2": [(eq, 11)]})

    if queasy:

        if queasy.logi1 :
            ci_time = queasy.char3

            if citime.lower()  < (ci_time).lower() :
                mess_result = "9 - To Early For CheckIn your time is under of earliest checkin time at : " + ci_time + ", Please Go to Front-Desk!"

                return generate_output()
        else:

            queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 8)],"number2": [(eq, 2)]})

            if queasy:
                ci_time = queasy.char3
            else:
                ci_time = "13:00"

            if citime.lower()  < (ci_time).lower() :
                mess_result = "9 - Early CheckIn Not Possible in MCI, Please Go to Front-Desk!"

                return generate_output()
    delete_it, ercode, arrival_guest_data = get_output(search_reservationbl(co_date, book_code, ch_name, early_ci, 1, citime, groupflag))

    if delete_it == 5:
        mess_result = "5 - Group CheckIn Not Possible in MCI, Please Go to Front-Desk!"

        return generate_output()

    if delete_it == 2:
        mess_result = "2 - Reservation Not Splitted Yet, CheckIn Not Possible in MCI, Please Go to Front-Desk!"

        return generate_output()

    arrival_guest = query(arrival_guest_data, first=True)

    if not arrival_guest:
        mess_result = "1 - Reservation Not Found"

        return generate_output()
    arrival_guest_data, err_code = get_output(iproom_assignmentbl(arrival_guest_data))

    if err_code == 1:
        mess_result = "01 - Room Not Available or Occupied with other reservation, Please Go to Front-Desk!"

    if err_code == 2:
        mess_result = "02 - Room Status still not available, Please Go to Front-Desk!"

    if err_code == 0 and delete_it == 0:
        mess_result = "0 - Find Reservation Success With Room Assignment!"

    for arrival_guest in query(arrival_guest_data):
        arrival_guestlist = Arrival_guestlist()
        arrival_guestlist_data.append(arrival_guestlist)

        arrival_guestlist.i_counter = arrival_guest.i_counter
        arrival_guestlist.gastno = arrival_guest.gastno
        arrival_guestlist.resnr = arrival_guest.resnr
        arrival_guestlist.reslinnr = arrival_guest.reslinnr
        arrival_guestlist.gast = arrival_guest.gast
        arrival_guestlist.ci = arrival_guest.ci
        arrival_guestlist.co = arrival_guest.co
        arrival_guestlist.rmtype = arrival_guest.rmtype
        arrival_guestlist.zinr = arrival_guest.zinr
        arrival_guestlist.argt = arrival_guest.argt
        arrival_guestlist.adult = arrival_guest.adult
        arrival_guestlist.child = arrival_guest.child
        arrival_guestlist.rmtype_str = arrival_guest.rmtype_str
        arrival_guestlist.room_sharer = arrival_guest.room_sharer
        arrival_guestlist.pre_checkin = arrival_guest.pre_checkin
        arrival_guestlist.argt_str = arrival_guest.argt_str
        arrival_guestlist.preference = arrival_guest.preference
        arrival_guestlist.new_zinr = arrival_guest.new_zinr
        arrival_guestlist.zikatnr = arrival_guest.zikatnr
        arrival_guestlist.l_selected = arrival_guest.l_selected
        arrival_guestlist.kontakt_nr = arrival_guest.kontakt_nr

        if arrival_guest.room_stat == 0:
            arrival_guestlist.room_status = "0 Ready To Checkin"

        if arrival_guest.room_stat == 1:
            arrival_guestlist.room_status = "1 Room Already ASSIGN or Overlapping"

        if arrival_guest.room_stat == 2:
            arrival_guestlist.room_status = "2 Room Status Not Ready To Checkin"

        if arrival_guest.room_stat == 3:
            arrival_guestlist.room_status = "3 Room With Type Selected Not Available"

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, arrival_guest.gastno)]})

        if guestbook:
            arrival_guestlist.image_flag = "0 image id already exist"
        else:
            arrival_guestlist.image_flag = "1 image id still empty"

        res_line = get_cache (Res_line, {"resnr": [(eq, arrival_guestlist.resnr)],"reslinnr": [(eq, arrival_guestlist.reslinnr)]})

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
        arrival_guestlist.currency_usage = waehrung.wabkurz

        if res_line.betrieb_gast != 0:
            arrival_guestlist.key_generated = True

        if arrival_guest.res_status == 0:
            arrival_guestlist.res_status = "0 - Guest Not Checkin"
        else:
            arrival_guestlist.res_status = "1 - Guest Already Checkin"

    for arrival_guestlist in query(arrival_guestlist_data):

        guest = get_cache (Guest, {"gastnr": [(eq, arrival_guestlist.gastno)]})

        res_line = get_cache (Res_line, {"resnr": [(eq, arrival_guestlist.resnr)],"reslinnr": [(eq, arrival_guestlist.reslinnr)]})
        arrival_guestlist.guest_email = guest.email_adr
        arrival_guestlist.guest_phnumber = guest.mobil_telefon
        arrival_guestlist.guest_nation = guest.nation1
        arrival_guestlist.guest_country = guest.land
        arrival_guestlist.guest_region = guest.geburt_ort2


        for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
            tmp_char = entry(i - 1, res_line.zimmer_wunsch, ";")

            if matches(tmp_char,r"*ROOMREF*"):
                arrival_guestlist.room_preference = entry(3, tmp_char, "|")
                arrival_guestlist.room_preference = entry(1, room_preference, "=")

            if matches(tmp_char,r"*SEGM_PUR*"):
                arrival_guestlist.purposeofstay = substring(tmp_char, 8, 1)

                queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(arrival_guestlist.purposeofstay))]})

                if queasy:
                    arrival_guestlist.purposeofstay = queasy.char3

            if matches(tmp_char,r"*VN=*"):
                arrival_guestlist.vehicle_number = entry(1, tmp_char, "=")

        interface = get_cache (Interface, {"key": [(eq, 50)],"resnr": [(eq, arrival_guestlist.resnr)],"reslinnr": [(eq, arrival_guestlist.reslinnr)]})

        if interface:
            arrival_guestlist.ifdata_sent = True

        queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 8)],"number2": [(eq, 12)]})

        if queasy:

            if queasy.logi1 :
                arrival_guestlist.wifi_password = guest.name

        queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, arrival_guestlist.resnr)],"number2": [(eq, arrival_guestlist.reslinnr)]})

        if queasy:
            arrival_guestlist.payment_status = queasy.char1

            if num_entries(queasy.char2, "|") > 1:
                arrival_guestlist.transid_merchant = entry(0, queasy.char2, "|")
                arrival_guestlist.payment_channel = entry(1, queasy.char2, "|")
            else:
                arrival_guestlist.transid_merchant = queasy.char2

            if queasy.number3 == 1:
                arrival_guestlist.payment_method = "DOKU"

            elif queasy.number3 == 2:
                arrival_guestlist.payment_method = "QRIS"
        else:
            arrival_guestlist.payment_status = "PENDING"

        reservation = get_cache (Reservation, {"resnr": [(eq, arrival_guestlist.resnr)]})

        if reservation:
            depo_bal =  to_decimal(reservation.depositgef) - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)
            arrival_guestlist.amount_depo =  to_decimal(reservation.depositgef)
            arrival_guestlist.depo_paid1 =  to_decimal(reservation.depositbez)
            arrival_guestlist.depo_paid2 =  to_decimal(reservation.depositbez2)
            arrival_guestlist.depo_balance =  to_decimal(depo_bal)

        if arrival_guestlist.res_status.lower()  == ("1 - Guest Already Checkin").lower() :

            reservation = get_cache (Reservation, {"resnr": [(eq, arrival_guestlist.resnr)]})

            if reservation:
                arrival_guestlist.payment_status = "SUCCESS"
        else:

            for buff_resline in db_session.query(Buff_resline).filter(
                     (Buff_resline.resnr == arrival_guestlist.resnr)).order_by(Buff_resline._recid).yield_per(100):

                if buff_resline.resstatus == 6 or buff_resline.resstatus == 13:
                    res_flag = True
                break

            if res_flag:
                arrival_guestlist.payment_status = "SUCCESS"
            res_flag = False

        if arrival_guestlist.payment_status.lower()  == ("SUCCESS").lower() :
            arrival_guestlist.preauth_flag = True

        zimmer = get_cache (Zimmer, {"zinr": [(eq, arrival_guestlist.zinr)]})

        if zimmer:

            if matches(himmelsr,r"*smoking*"):
                arrival_guestlist.smoking_room = True

            elif matches(himmelsr,r"*no smoking*"):
                arrival_guestlist.smoking_room = False

            elif matches(himmelsr,r"*non smoking*"):
                arrival_guestlist.smoking_room = False
            else:
                smoking_room = False
        pass
        pass

    return generate_output()