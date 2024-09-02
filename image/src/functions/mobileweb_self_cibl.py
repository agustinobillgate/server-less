from functions.additional_functions import *
import decimal
from datetime import date
from functions.search_reservationbl import search_reservationbl
from functions.iproom_assignmentbl import iproom_assignmentbl
import re
from models import Res_line, Queasy, Guestbook, Waehrung, Guest, Interface, Reservation, Zimmer

def mobileweb_self_cibl(co_date:date, book_code:str, ch_name:str, early_ci:bool, max_room:int, citime:str, groupflag:bool):
    mess_result = ""
    arrival_guestlist_list = []
    delete_it:int = 0
    err_code:int = 0
    ercode:int = 0
    i:int = 0
    tmp_char:str = ""
    ci_time:str = ""
    depo_bal:decimal = 0
    res_flag:bool = False
    res_line = queasy = guestbook = waehrung = guest = interface = reservation = zimmer = None

    arrival_guest = arrival_guestlist = buff_resline = None

    arrival_guest_list, Arrival_guest = create_model("Arrival_guest", {"i_counter":int, "gastno":int, "resnr":int, "reslinnr":int, "gast":str, "ci":date, "co":date, "rmtype":str, "zinr":str, "argt":str, "adult":str, "child":str, "rmtype_str":str, "room_sharer":bool, "pre_checkin":bool, "argt_str":str, "preference":str, "new_zinr":bool, "zikatnr":int, "l_selected":bool, "kontakt_nr":int, "room_stat":int, "res_status":int})
    arrival_guestlist_list, Arrival_guestlist = create_model("Arrival_guestlist", {"i_counter":int, "gastno":int, "resnr":int, "reslinnr":int, "gast":str, "ci":date, "co":date, "rmtype":str, "zinr":str, "argt":str, "adult":str, "child":str, "rmtype_str":str, "room_sharer":bool, "pre_checkin":bool, "argt_str":str, "preference":str, "new_zinr":bool, "zikatnr":int, "l_selected":bool, "kontakt_nr":int, "guest_email":str, "guest_phnumber":str, "guest_nation":str, "guest_country":str, "guest_region":str, "room_preference":str, "purposeofstay":str, "room_status":str, "image_flag":str, "currency_usage":str, "key_generated":bool, "preauth_flag":bool, "res_status":str, "ifdata_sent":bool, "param_broadcast":str, "wifi_password":str, "payment_method":str, "payment_status":str, "payment_channel":str, "transid_merchant":str, "vehicle_number":str, "smoking_room":bool, "amount_depo":decimal, "depo_paid1":decimal, "depo_paid2":decimal, "depo_balance":decimal})

    Buff_resline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, arrival_guestlist_list, delete_it, err_code, ercode, i, tmp_char, ci_time, depo_bal, res_flag, res_line, queasy, guestbook, waehrung, guest, interface, reservation, zimmer
        nonlocal buff_resline


        nonlocal arrival_guest, arrival_guestlist, buff_resline
        nonlocal arrival_guest_list, arrival_guestlist_list
        return {"mess_result": mess_result, "arrival-guestlist": arrival_guestlist_list}


    if co_date == None:
        mess_result = "99 - CheckOut Date Is Mandatory!"

        return generate_output()

    if citime == "" or citime == None:
        mess_result = "99 - CheckIn Time Is Mandatory! - HH:MM"

        return generate_output()

    if len(citime) != 5:
        mess_result = "99 - CheckIn Time Format Is Invalid, should be [HH:MM]"

        return generate_output()

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 8) &  (Queasy.number2 == 11)).first()

    if queasy:

        if queasy.logi1 :
            ci_time = queasy.char3

            if citime.lower()  < (ci_time).lower() :
                mess_result = "9 - To Early For CheckIn your time is under of earliest checkin time at : " + ci_time + ", Please Go to Front_Desk!"

                return generate_output()
        else:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 216) &  (Queasy.number1 == 8) &  (Queasy.number2 == 2)).first()

            if queasy:
                ci_time = queasy.char3
            else:
                ci_time = "13:00"

            if citime.lower()  < (ci_time).lower() :
                mess_result = "9 - Early CheckIn Not Possible in MCI, Please Go to Front_Desk!"

                return generate_output()
    delete_it, ercode, arrival_guest_list = get_output(search_reservationbl(co_date, book_code, ch_name, early_ci, 1, citime, groupflag))

    if delete_it == 5:
        mess_result = "5 - Group CheckIn Not Possible in MCI, Please Go to Front_Desk!"

        return generate_output()

    if delete_it == 2:
        mess_result = "2 - Reservation Not Splitted Yet, CheckIn Not Possible in MCI, Please Go to Front_Desk!"

        return generate_output()

    arrival_guest = query(arrival_guest_list, first=True)

    if not arrival_guest:
        mess_result = "1 - Reservation Not Found"

        return generate_output()
    arrival_guest_list, err_code = get_output(iproom_assignmentbl(arrival_guest))

    if err_code == 1:
        mess_result = "01 - Room Not Available or Occupied with other reservation, Please Go to Front_Desk!"

    if err_code == 2:
        mess_result = "02 - Room Status still not available, Please Go to Front_Desk!"

    if err_code == 0 and delete_it == 0:
        mess_result = "0 - Find Reservation Success With Room Assignment!"

    for arrival_guest in query(arrival_guest_list):
        arrival_guestlist = Arrival_guestlist()
        arrival_guestlist_list.append(arrival_guestlist)

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
            arrival_guestlist.room_status = "1 Room Already assign or Overlapping"

        if arrival_guest.room_stat == 2:
            arrival_guestlist.room_status = "2 Room Status Not Ready To Checkin"

        if arrival_guest.room_stat == 3:
            arrival_guestlist.room_status = "3 Room With Type Selected Not Available"

        guestbook = db_session.query(Guestbook).filter(
                (Guestbook.gastnr == arrival_guest.gastno)).first()

        if guestbook:
            arrival_guestlist.image_flag = "0 image id already exist"
        else:
            arrival_guestlist.image_flag = "1 image id still empty"

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == arrival_guestlist.resnr) &  (Res_line.reslinnr == arrival_guestlist.reslinnr)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrungsnr == res_line.betriebsnr)).first()
        arrival_guestlist.currency_usage = waehrung.wabkurz

        if res_line.betrieb_gast != 0:
            arrival_guestlist.key_generated = True

        if arrival_guest.res_status == 0:
            arrival_guestlist.res_status = "0 - Guest Not Checkin"
        else:
            arrival_guestlist.res_status = "1 - Guest Already Checkin"

    for arrival_guestlist in query(arrival_guestlist_list):

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == arrival_guestlist.gastno)).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == arrival_guestlist.resnr) &  (Res_line.reslinnr == arrival_guestlist.reslinnr)).first()
        arrival_guestlist.guest_email = guest.email_adr
        arrival_guestlist.guest_phnumber = guest.mobil_telefon
        arrival_guestlist.guest_nation = guest.nation1
        arrival_guestlist.guest_country = guest.land
        arrival_guestlist.guest_region = guest.geburt_ort2


        for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
            tmp_char = entry(i - 1, res_line.zimmer_wunsch, ";")

            if re.match(".*ROOMREF.*",tmp_char):
                arrival_guestlist.room_preference = entry(3, tmp_char, "|")
                arrival_guestlist.room_preference = entry(1, room_preference, " == ")

            if re.match(".*SEGM__PUR.*",tmp_char):
                arrival_guestlist.purposeofstay = substring(tmp_char, 8, 1)

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 143) &  (Queasy.number1 == to_int(arrival_guestlist.purposeofstay))).first()

                if queasy:
                    arrival_guestlist.purposeofstay = queasy.char3

            if re.match(".*VN ==.*",tmp_char):
                arrival_guestlist.vehicle_number = entry(1, tmp_char, " == ")

        interface = db_session.query(Interface).filter(
                (Interface.key == 50) &  (Interface.resnr == arrival_guestlist.resnr) &  (Interface.reslinnr == arrival_guestlist.reslinnr)).first()

        if interface:
            arrival_guestlist.ifdata_sent = True

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 216) &  (Queasy.number1 == 8) &  (Queasy.number2 == 12)).first()

        if queasy:

            if queasy.logi1 :
                arrival_guestlist.wifi_password = guest.name

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == arrival_guestlist.resnr) &  (Queasy.number2 == arrival_guestlist.reslinnr)).first()

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

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == arrival_guestlist.resnr)).first()

        if reservation:
            depo_bal = reservation.depositgef - reservation.depositbez - reservation.depositbez2
            arrival_guestlist.amount_depo = reservation.depositgef
            arrival_guestlist.depo_paid1 = reservation.depositbez
            arrival_guestlist.depo_paid2 = reservation.depositbez2
            arrival_guestlist.depo_balance = depo_bal

        if arrival_guestlist.res_status.lower()  == "1 - Guest Already Checkin":

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == arrival_guestlist.resnr)).first()

            if reservation:
                arrival_guestlist.payment_status = "SUCCESS"
        else:

            for buff_resline in db_session.query(Buff_resline).filter(
                    (Buff_resline.resnr == arrival_guestlist.resnr)).all():

                if buff_resline.resstatus == 6 or buff_resline.resstatus == 13:
                    res_flag = True
                break

            if res_flag:
                arrival_guestlist.payment_status = "SUCCESS"
            res_flag = False

        if arrival_guestlist.payment_status.lower()  == "SUCCESS":
            arrival_guestlist.preAuth_flag = True

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == arrival_guestlist.zinr)).first()

        if zimmer:

            if re.match(".*smoking.*",himmelsr):
                arrival_guestlist.smoking_room = True

            elif re.match(".*no smoking.*",himmelsr):
                arrival_guestlist.smoking_room = False

            elif re.match(".*non smoking.*",himmelsr):
                arrival_guestlist.smoking_room = False
            else:
                smoking_room = False

        res_line = db_session.query(Res_line).first()


    return generate_output()