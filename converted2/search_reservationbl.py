from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
import re
from sqlalchemy import func
from models import Res_line, Reservation, Zimkateg, Arrangement, Queasy, Guest, Mc_guest

def search_reservationbl(co_date:date, book_code:str, ch_name:str, early_ci:bool, max_room:int, citime:str, groupflag:bool):
    delete_it = 0
    err_code = 0
    arrival_guest_list = []
    ci_date:date = None
    curr_time:str = ""
    resno:int = 0
    res_line = reservation = zimkateg = arrangement = queasy = guest = mc_guest = None

    arrival_guest = name_list = guest_list = tarrival = rline = None

    arrival_guest_list, Arrival_guest = create_model("Arrival_guest", {"i_counter":int, "gastno":int, "resnr":int, "reslinnr":int, "gast":str, "ci":date, "co":date, "rmtype":str, "zinr":str, "argt":str, "adult":str, "child":str, "rmtype_str":str, "room_sharer":bool, "pre_checkin":bool, "argt_str":str, "preference":str, "new_zinr":bool, "zikatnr":int, "l_selected":bool, "kontakt_nr":int, "room_stat":int, "res_status":int})
    name_list_list, Name_list = create_model("Name_list", {"num_word":int, "word":[str, 9], "num_found":int, "resnr":int, "reslinnr":int, "gastnrmember":int, "same_gastnr":bool})
    guest_list_list, Guest_list = create_model("Guest_list", {"resnr":int, "reslinnr":int, "gastnrmember":int})

    Tarrival = Arrival_guest
    tarrival_list = arrival_guest_list

    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list
        return {"delete_it": delete_it, "err_code": err_code, "arrival-guest": arrival_guest_list}

    def search_by_resnr():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        Rline = Res_line

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).first()

        if res_line:

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()
            arrival_guest = Arrival_guest()
            arrival_guest_list.append(arrival_guest)

            arrival_guest.i_counter = curr_pos
            arrival_guest.resnr = res_line.resnr
            arrival_guest.reslinnr = res_line.reslinnr
            arrival_guest.gastno = res_line.gastnrmember
            arrival_guest.gast = res_line.name
            arrival_guest.ci = res_line.ankunft
            arrival_guest.co = res_line.abreise
            arrival_guest.rmtype = zimkateg.kurzbez
            arrival_guest.rmtype_str = zimkateg.bezeichnung
            arrival_guest.argt = res_line.arrangement
            arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
            arrival_guest.child = to_string(res_line.kind1)
            arrival_guest.zinr = res_line.zinr
            arrival_guest.kontakt_nr = res_line.kontakt_nr

            if res_line.resstatus == 1 or res_line.resstatus == 11:
                arrival_guest.res_status = 0

            elif res_line.resstatus == 6 or res_line.resstatus == 13:
                arrival_guest.res_status = 1

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()

            if arrangement:
                arrival_guest.argt_str = arrangement.argt_bez

            if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                arrival_guest.pre_checkin = True


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if re.match("PCIFLAG.*",messvalue):
                    for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                        mesvalue = entry(loopj - 1, messvalue, "|")

                        if re.match("ROOMREF.*",mesvalue):
                            arrival_guest.preference = entry(1, mesvalue, " == ")


                            return
                    return

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == resno) &  (Rline.active_flag <= 1) &  (Rline.ankunft == ci_date) &  (Rline.abreise == co_date) &  (Rline.l_zuordnung[2] == 0) &  ((Rline.resstatus == 1) |  (Rline.resstatus == 6) |  (Rline.resstatus == 11) |  (Rline.resstatus == 13)) &  (Rline._recid != res_line._recid)).all():
                messvalue = ""
                mesvalue = ""

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == rline.zikatnr)).first()
                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = rline.resnr
                arrival_guest.reslinnr = rline.reslinnr
                arrival_guest.gastno = rline.gastnrmember
                arrival_guest.gast = rline.name
                arrival_guest.ci = rline.ankunft
                arrival_guest.co = rline.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = rline.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(rline.kind1)
                arrival_guest.zinr = rline.zinr
                arrival_guest.kontakt_nr = rline.kontakt_nr

                if rline.resstatus == 1 or rline.resstatus == 11:
                    arrival_guest.res_status = 0

                elif rline.resstatus == 6 or rline.resstatus == 13:
                    arrival_guest.res_status = 1

                if rline.resstatus == 11 or rline.resstatus == 13:
                    arrival_guest.room_sharer = True

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == rline.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if re.match(".*PCIFLAG.*",rline.zimmer_wunsch):
                    arrival_guest.pre_checkin = True


                for loopi in range(1,num_entries(rline.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, rline.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break
        else:
            search_by_voucher()

    def search_by_voucher():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        str:str = ""
        voucher:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        Rline = Res_line

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():
            voucher = ""

            if re.match(".*voucher.*",res_line.zimmer_wunsch):
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 7) == "voucher":
                        voucher = substring(str, 7)


                        break

            if voucher.lower()  == (book_code).lower() :
                resno = res_line.resnr
                reslinno = res_line.reslinnr

                if groupflag:

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == resno)).first()

                    if reservation and reservation.grpflag:
                        delete_it = 5

                        return

            if resno == 0:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                if reservation.vesrdepot.lower()  == (book_code).lower() :
                    resno = res_line.resnr
                    reslinno = res_line.reslinnr

            if resno > 0:
                break

        if resno > 0:

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == resno) &  (Rline.active_flag <= 1) &  (Rline.ankunft == ci_date) &  (Rline.abreise == co_date) &  (Rline.l_zuordnung[2] == 0) &  ((Rline.resstatus == 1) |  (Rline.resstatus == 6) |  (Rline.resstatus == 11) |  (Rline.resstatus == 13))).all():
                messvalue = ""
                mesvalue = ""

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = rline.resnr
                arrival_guest.reslinnr = rline.reslinnr
                arrival_guest.gastno = rline.gastnrmember
                arrival_guest.gast = rline.name
                arrival_guest.ci = rline.ankunft
                arrival_guest.co = rline.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = rline.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(rline.kind1)
                arrival_guest.zinr = rline.zinr
                arrival_guest.kontakt_nr = rline.kontakt_nr

                if rline.resstatus == 1 or rline.resstatus == 11:
                    arrival_guest.res_status = 0

                elif rline.resstatus == 6 or rline.resstatus == 13:
                    arrival_guest.res_status = 1


                for loopi in range(1,num_entries(rline.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, rline.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == rline.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if rline.resstatus == 11 or rline.resstatus == 13:
                    arrival_guest.room_sharer = True

                if re.match(".*PCIFLAG.*",rline.zimmer_wunsch):
                    arrival_guest.pre_checkin = True


        else:
            search_by_guest()

    def search_by_guest():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        gname:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        loopm:int = 0
        str1:str = ""
        loopn:int = 0
        str2:str = ""
        counter:int = 0
        loopk:int = 0
        str3:str = ""
        loopl:int = 0
        str4:str = ""
        curr_gastnr:int = 0
        gastnr_found:int = 0
        curr_name:str = ""
        Rline = Res_line

        if re.match(".*@.*",book_code):
            search_by_email()
        name_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == resno)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return
            name_list = Name_list()
            name_list_list.append(name_list)

            name_list.resnr = res_line.resnr
            name_list.reslinnr = res_line.reslinnr
            name_list.gastnrmember = res_line.gastnrmember


            curr_name = ""


            for loopm in range(1,num_entries(res_line.name, ",")  + 1) :
                str1 = trim(entry(loopm - 1, res_line.name, ","))

                if str1 != "":
                    for loopn in range(1,num_entries(str1, "")  + 1) :
                        str2 = trim(entry(loopn - 1, str1, ""))

                        if (str2).lower()  != "" and curr_name.lower()  != (str2).lower() :

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 141) &  (func.lower(Queasy.char1) == (str2).lower())).first()

                            if not queasy:
                                name_list.num_word = name_list.num_word + 1
                                name_list.word[name_list.num_word - 1] = str2


                            curr_name = str2


        for loopk in range(1,num_entries(trim(book_code) , "")  + 1) :
            str3 = entry(loopk - 1, book_code, "")

            for name_list in query(name_list_list):
                for loopl in range(1,name_list.num_word + 1) :

                    if name_list.word[loopl - 1] != "" and name_list.word[loopl - 1] == (str3).lower() :
                        name_list.word[loopl - 1] = ""
                        name_list.num_found = name_list.num_found + 1


                        break

        for name_list in query(name_list_list, filters=(lambda name_list :name_list.num_word == name_list.num_found)):

            if curr_gastnr != name_list.gastnrmember:
                gastnr_found = gastnr_found + 1

            if curr_gastnr == 0 or (curr_gastnr == name_list.gastnrmember):
                name_list.same_gastnr = True


            curr_gastnr = name_list.gastnrmember

        if (gastnr_found > 1 or gastnr_found == 0):
            search_by_email()
        else:

            for name_list in query(name_list_list, filters=(lambda name_list :name_list.same_gastnr)):

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.resnr == name_list.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0) &  ((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*")) |  (Res_line.resstatus == 6))).all():

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == res_line.zikatnr)).first()
                    arrival_guest = Arrival_guest()
                    arrival_guest_list.append(arrival_guest)

                    curr_pos = curr_pos + 1
                    arrival_guest.i_counter = curr_pos
                    arrival_guest.resnr = res_line.resnr
                    arrival_guest.reslinnr = res_line.reslinnr
                    arrival_guest.gastno = res_line.gastnrmember
                    arrival_guest.gast = res_line.name
                    arrival_guest.ci = res_line.ankunft
                    arrival_guest.co = res_line.abreise
                    arrival_guest.rmtype = zimkateg.kurzbez
                    arrival_guest.rmtype_str = zimkateg.bezeichnung
                    arrival_guest.argt = res_line.arrangement
                    arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                    arrival_guest.child = to_string(res_line.kind1)
                    arrival_guest.zinr = res_line.zinr
                    arrival_guest.kontakt_nr = res_line.kontakt_nr

                    if res_line.resstatus == 1:
                        arrival_guest.res_status = 0

                    elif res_line.resstatus == 6:
                        arrival_guest.res_status = 1

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    if arrangement:
                        arrival_guest.argt_str = arrangement.argt_bez


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if re.match("PCIFLAG.*",messvalue):
                            for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                                mesvalue = entry(loopj - 1, messvalue, "|")

                                if re.match("ROOMREF.*",mesvalue):
                                    arrival_guest.preference = entry(1, mesvalue, " == ")


                                    break
                            break

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    if arrangement:
                        arrival_guest.argt_str = arrangement.argt_bez

                    if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                        arrival_guest.pre_checkin = True

    def search_by_email():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        str:str = ""
        email:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        guest_list_list.clear()

        res_line_obj_list = []
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.email_adr) == (book_code).lower())).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == resno)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return
            guest_list = Guest_list()
            guest_list_list.append(guest_list)

            guest_list.resnr = res_line.resnr
            guest_list.reslinnr = res_line.reslinnr
            guest_list.gastnrmember = res_line.gastnrmember

        for guest_list in query(guest_list_list):

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == guest_list.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = res_line.resnr
                arrival_guest.reslinnr = res_line.reslinnr
                arrival_guest.gastno = res_line.gastnrmember
                arrival_guest.gast = res_line.name
                arrival_guest.ci = res_line.ankunft
                arrival_guest.co = res_line.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = res_line.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(res_line.kind1)
                arrival_guest.zinr = res_line.zinr
                arrival_guest.kontakt_nr = res_line.kontakt_nr

                if res_line.resstatus == 1:
                    arrival_guest.res_status = 0

                elif res_line.resstatus == 6:
                    arrival_guest.res_status = 1

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez


                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                    arrival_guest.pre_checkin = True

        arrival_guest = query(arrival_guest_list, first=True)

        if not arrival_guest:
            search_by_member()

    def search_by_member():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        str:str = ""
        gname:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        Rline = Res_line
        guest_list_list.clear()

        res_line_obj_list = []
        for res_line, mc_guest in db_session.query(Res_line, Mc_guest).join(Mc_guest,(Mc_guest.gastnr == Res_line.gastnrmember) &  (func.lower(Mc_guest.cardnum) == (book_code).lower())).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == resno)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return
            guest_list = Guest_list()
            guest_list_list.append(guest_list)

            guest_list.resnr = res_line.resnr
            guest_list.reslinnr = res_line.reslinnr
            guest_list.gastnrmember = res_line.gastnrmember

        for guest_list in query(guest_list_list):

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == guest_list.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = res_line.resnr
                arrival_guest.reslinnr = res_line.reslinnr
                arrival_guest.gastno = res_line.gastnrmember
                arrival_guest.gast = res_line.name
                arrival_guest.ci = res_line.ankunft
                arrival_guest.co = res_line.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = res_line.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(res_line.kind1)
                arrival_guest.zinr = res_line.zinr
                arrival_guest.kontakt_nr = res_line.kontakt_nr

                if res_line.resstatus == 1:
                    arrival_guest.res_status = 0

                elif res_line.resstatus == 6:
                    arrival_guest.res_status = 1


                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                    arrival_guest.pre_checkin = True

    def search_by_resnr1():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        Rline = Res_line

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6)) &  (Res_line.name.op("~")(ch_name))).first()

        if res_line:

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()
            arrival_guest = Arrival_guest()
            arrival_guest_list.append(arrival_guest)

            arrival_guest.i_counter = curr_pos
            arrival_guest.resnr = res_line.resnr
            arrival_guest.reslinnr = res_line.reslinnr
            arrival_guest.gastno = res_line.gastnrmember
            arrival_guest.gast = res_line.name
            arrival_guest.ci = res_line.ankunft
            arrival_guest.co = res_line.abreise
            arrival_guest.rmtype = zimkateg.kurzbez
            arrival_guest.rmtype_str = zimkateg.bezeichnung
            arrival_guest.argt = res_line.arrangement
            arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
            arrival_guest.child = to_string(res_line.kind1)
            arrival_guest.zinr = res_line.zinr
            arrival_guest.kontakt_nr = res_line.kontakt_nr

            if res_line.resstatus == 1 or res_line.resstatus == 11:
                arrival_guest.res_status = 0

            elif res_line.resstatus == 6 or res_line.resstatus == 13:
                arrival_guest.res_status = 1


            for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                if re.match("PCIFLAG.*",messvalue):
                    for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                        mesvalue = entry(loopj - 1, messvalue, "|")

                        if re.match("ROOMREF.*",mesvalue):
                            arrival_guest.preference = entry(1, mesvalue, " == ")


                            return
                    return

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()

            if arrangement:
                arrival_guest.argt_str = arrangement.argt_bez

            if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                arrival_guest.pre_checkin = True

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == resno) &  (Rline.active_flag <= 1) &  (Rline.ankunft == ci_date) &  (Rline.l_zuordnung[2] == 0) &  ((Rline.resstatus == 1) |  (Rline.resstatus == 6) |  (Rline.resstatus == 11) |  (Rline.resstatus == 13)) &  (Rline._recid != res_line._recid)).all():

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == rline.zikatnr)).first()
                messvalue = ""
                mesvalue = ""


                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = rline.resnr
                arrival_guest.reslinnr = rline.reslinnr
                arrival_guest.gastno = rline.gastnrmember
                arrival_guest.gast = rline.name
                arrival_guest.ci = rline.ankunft
                arrival_guest.co = rline.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = rline.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(rline.kind1)
                arrival_guest.zinr = rline.zinr
                arrival_guest.kontakt_nr = rline.kontakt_nr

                if rline.resstatus == 1 or rline.resstatus == 11:
                    arrival_guest.res_status = 0

                elif rline.resstatus == 6 or rline.resstatus == 13:
                    arrival_guest.res_status = 1


                for loopi in range(1,num_entries(rline.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, rline.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == rline.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if rline.resstatus == 11:
                    arrival_guest.room_sharer = True

                if re.match(".*PCIFLAG.*",rline.zimmer_wunsch):
                    arrival_guest.pre_checkin = True


        else:
            search_by_voucher1()

    def search_by_voucher1():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        str:str = ""
        voucher:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        Rline = Res_line

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6)) &  (Res_line.name.op("~")(ch_name))).all():

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return
            voucher = ""

            if re.match(".*voucher.*",res_line.zimmer_wunsch):
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 7) == "voucher":
                        voucher = substring(str, 7)


                        break

            if voucher.lower()  == (book_code).lower() :
                resno = res_line.resnr
                reslinno = res_line.reslinnr

            if resno == 0:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == res_line.resnr)).first()

                if reservation.vesrdepot.lower()  == (book_code).lower() :
                    resno = res_line.resnr
                    reslinno = res_line.reslinnr

            if resno > 0:
                break

        if resno > 0:

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == resno) &  (Rline.active_flag <= 1) &  (Rline.ankunft == ci_date) &  (Rline.abreise == co_date) &  (Rline.l_zuordnung[2] == 0) &  ((Rline.resstatus == 1) |  (Rline.resstatus == 6) |  (Rline.resstatus == 11) |  (Rline.resstatus == 13))).all():
                messvalue = ""
                mesvalue = ""

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = rline.resnr
                arrival_guest.reslinnr = rline.reslinnr
                arrival_guest.gastno = rline.gastnrmember
                arrival_guest.gast = rline.name
                arrival_guest.ci = rline.ankunft
                arrival_guest.co = rline.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = rline.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(rline.kind1)
                arrival_guest.zinr = rline.zinr
                arrival_guest.kontakt_nr = rline.kontakt_nr

                if rline.resstatus == 1 or rline.resstatus == 11:
                    arrival_guest.res_status = 0

                elif rline.resstatus == 6 or rline.resstatus == 13:
                    arrival_guest.res_status = 1


                for loopi in range(1,num_entries(rline.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, rline.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == rline.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if rline.resstatus == 11 or rline.resstatus == 13:
                    arrival_guest.room_sharer = True

                if re.match(".*PCIFLAG.*",rline.zimmer_wunsch):
                    arrival_guest.pre_checkin = True


        else:
            search_by_guest1()

    def search_by_guest1():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        gname:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        loopm:int = 0
        str1:str = ""
        loopn:int = 0
        str2:str = ""
        counter:int = 0
        loopk:int = 0
        str3:str = ""
        loopl:int = 0
        str4:str = ""
        curr_gastnr:int = 0
        gastnr_found:int = 0
        curr_name:str = ""
        Rline = Res_line

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():
            name_list = Name_list()
            name_list_list.append(name_list)

            name_list.resnr = res_line.resnr
            name_list.reslinnr = res_line.reslinnr
            name_list.gastnrmember = res_line.gastnrmember


            curr_name = ""


            for loopm in range(1,num_entries(res_line.name, ",")  + 1) :
                str1 = trim(entry(loopm - 1, res_line.name, ","))

                if str1 != "":
                    for loopn in range(1,num_entries(str1, "")  + 1) :
                        str2 = trim(entry(loopn - 1, str1, ""))

                        if str2.lower()  != "" and str2.lower()  != (curr_name).lower() :

                            queasy = db_session.query(Queasy).filter(
                                    (Queasy.key == 141) &  (func.lower(Queasy.char1) == (str2).lower())).first()

                            if not queasy:
                                name_list.num_word = name_list.num_word + 1
                                name_list.word[name_list.num_word - 1] = str2


                            curr_name = str2


        for loopk in range(1,num_entries(trim(book_code) , "")  + 1) :
            str3 = entry(loopk - 1, book_code, "")

            for name_list in query(name_list_list):
                for loopl in range(1,name_list.num_word + 1) :

                    if name_list.word[loopl - 1] != "" and name_list.word[loopl - 1] == (str3).lower() :
                        name_list.word[loopl - 1] = ""
                        name_list.num_found = name_list.num_found + 1


                        break

        for name_list in query(name_list_list, filters=(lambda name_list :name_list.num_word == name_list.num_found)):

            if curr_gastnr != name_list.gastnrmember:
                gastnr_found = gastnr_found + 1

            if curr_gastnr == 0 or (curr_gastnr == name_list.gastnrmember):
                name_list.same_gastnr = True


            curr_gastnr = name_list.gastnrmember

        if (gastnr_found > 1 or gastnr_found == 0):
            search_by_email1()
        else:

            for name_list in query(name_list_list, filters=(lambda name_list :name_list.same_gastnr)):

                for res_line in db_session.query(Res_line).filter(
                        (Res_line.resnr == name_list.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():

                    zimkateg = db_session.query(Zimkateg).filter(
                            (Zimkateg.zikatnr == res_line.zikatnr)).first()
                    arrival_guest = Arrival_guest()
                    arrival_guest_list.append(arrival_guest)

                    curr_pos = curr_pos + 1
                    arrival_guest.i_counter = curr_pos
                    arrival_guest.resnr = res_line.resnr
                    arrival_guest.reslinnr = res_line.reslinnr
                    arrival_guest.gastno = res_line.gastnrmember
                    arrival_guest.gast = res_line.name
                    arrival_guest.ci = res_line.ankunft
                    arrival_guest.co = res_line.abreise
                    arrival_guest.rmtype = zimkateg.kurzbez
                    arrival_guest.rmtype_str = zimkateg.bezeichnung
                    arrival_guest.argt = res_line.arrangement
                    arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                    arrival_guest.child = to_string(res_line.kind1)
                    arrival_guest.zinr = res_line.zinr
                    arrival_guest.kontakt_nr = res_line.kontakt_nr

                    if res_line.resstatus == 1:
                        arrival_guest.res_status = 0

                    elif res_line.resstatus == 6:
                        arrival_guest.res_status = 1


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                        messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if re.match("PCIFLAG.*",messvalue):
                            for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                                mesvalue = entry(loopj - 1, messvalue, "|")

                                if re.match("ROOMREF.*",mesvalue):
                                    arrival_guest.preference = entry(1, mesvalue, " == ")


                                    break
                            break

                    arrangement = db_session.query(Arrangement).filter(
                            (Arrangement == res_line.arrangement)).first()

                    if arrangement:
                        arrival_guest.argt_str = arrangement.argt_bez

                    if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                        arrival_guest.pre_checkin = True

    def search_by_email1():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        str:str = ""
        email:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        Rline = Res_line
        guest_list_list.clear()

        res_line_obj_list = []
        for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnrmember) &  (func.lower(Guest.email_adr) == (book_code).lower())).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == resno)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return
            guest_list = Guest_list()
            guest_list_list.append(guest_list)

            guest_list.resnr = res_line.resnr
            guest_list.reslinnr = res_line.reslinnr
            guest_list.gastnrmember = res_line.gastnrmember

        for guest_list in query(guest_list_list):

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == guest_list.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = res_line.resnr
                arrival_guest.reslinnr = res_line.reslinnr
                arrival_guest.gastno = res_line.gastnrmember
                arrival_guest.gast = res_line.name
                arrival_guest.ci = res_line.ankunft
                arrival_guest.co = res_line.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = res_line.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(res_line.kind1)
                arrival_guest.zinr = res_line.zinr
                arrival_guest.kontakt_nr = res_line.kontakt_nr

                if res_line.resstatus == 1:
                    arrival_guest.res_status = 0

                elif res_line.resstatus == 6:
                    arrival_guest.res_status = 1


                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                    arrival_guest.pre_checkin = True

        arrival_guest = query(arrival_guest_list, first=True)

        if not arrival_guest:
            search_by_member1()

    def search_by_member1():

        nonlocal delete_it, err_code, arrival_guest_list, ci_date, curr_time, resno, res_line, reservation, zimkateg, arrangement, queasy, guest, mc_guest
        nonlocal tarrival, rline


        nonlocal arrival_guest, name_list, guest_list, tarrival, rline
        nonlocal arrival_guest_list, name_list_list, guest_list_list

        curr_pos:int = 1
        resno:int = 0
        reslinno:int = 0
        i:int = 0
        str:str = ""
        gname:str = ""
        loopi:int = 0
        loopj:int = 0
        messvalue:str = ""
        mesvalue:str = ""
        Rline = Res_line
        guest_list_list.clear()

        res_line_obj_list = []
        for res_line, mc_guest in db_session.query(Res_line, Mc_guest).join(Mc_guest,(Mc_guest.gastnr == Res_line.gastnrmember) &  (func.lower(Mc_guest.cardnum) == (book_code).lower())).filter(
                (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.abreise == co_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if groupflag:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == resno)).first()

                if reservation and reservation.grpflag:
                    delete_it = 5

                    return
            guest_list = Guest_list()
            guest_list_list.append(guest_list)

            guest_list.resnr = res_line.resnr
            guest_list.reslinnr = res_line.reslinnr
            guest_list.gastnrmember = res_line.gastnrmember

        for guest_list in query(guest_list_list):

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.resnr == guest_list.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.ankunft == ci_date) &  (Res_line.l_zuordnung[2] == 0) &  (((Res_line.resstatus == 1) &  (not Res_line.zimmer_wunsch.op("~")(".*MCI.*"))) |  (Res_line.resstatus == 6))).all():

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

                curr_pos = curr_pos + 1
                arrival_guest.i_counter = curr_pos
                arrival_guest.resnr = res_line.resnr
                arrival_guest.reslinnr = res_line.reslinnr
                arrival_guest.gastno = res_line.gastnrmember
                arrival_guest.gast = res_line.name
                arrival_guest.ci = res_line.ankunft
                arrival_guest.co = res_line.abreise
                arrival_guest.rmtype = zimkateg.kurzbez
                arrival_guest.rmtype_str = zimkateg.bezeichnung
                arrival_guest.argt = res_line.arrangement
                arrival_guest.adult = to_string(res_line.erwachs + res_line.gratis)
                arrival_guest.child = to_string(res_line.kind1)
                arrival_guest.zinr = res_line.zinr
                arrival_guest.kontakt_nr = res_line.kontakt_nr

                if res_line.resstatus == 1:
                    arrival_guest.res_status = 0

                elif res_line.resstatus == 6:
                    arrival_guest.res_status = 1


                for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                    messvalue = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                    if re.match("PCIFLAG.*",messvalue):
                        for loopj in range(1,num_entries(messvalue, "|")  + 1) :
                            mesvalue = entry(loopj - 1, messvalue, "|")

                            if re.match("ROOMREF.*",mesvalue):
                                arrival_guest.preference = entry(1, mesvalue, " == ")


                                break
                        break

                arrangement = db_session.query(Arrangement).filter(
                        (Arrangement == res_line.arrangement)).first()

                if arrangement:
                    arrival_guest.argt_str = arrangement.argt_bez

                if re.match(".*PCIFLAG.*",res_line.zimmer_wunsch):
                    arrival_guest.pre_checkin = True


    ci_date = get_output(htpdate(87))

    if len(book_code) == 11:
        ch_name = "*" + ch_name + "*"
        resno = to_int(entry(0, book_code, " "))

    elif len(book_code) == 10:
        ch_name = "*" + ch_name + "*"
        resno = to_int(substring(book_code, 0, 8))


    else:
        ch_name = "*" + ch_name + "*"
        resno = to_int(book_code)

    if ch_name.lower()  == "" or ch_name.lower()  == "* *":

        if resno > 0:
            search_by_resnr()
        else:
            search_by_voucher()
    else:

        if resno > 0:
            search_by_resnr1()
        else:
            search_by_voucher1()

    return generate_output()