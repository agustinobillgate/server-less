from functions.additional_functions import *
import decimal
from sqlalchemy import func
from datetime import date
from models import Res_line, Zimkateg, Bediener, Guest, Reservation, Reslin_queasy, Res_history

def res_changesbl(pvilanguage:int, res_mode:str, guestname:str, mr_comment:str, rl_comment:str, user_init:str, earlyci:bool, fixed_rate:bool, reslin_list:[Reslin_list]):
    rtc1:str = "-"
    rtc2:str = "-"
    lvcarea:str = "mk_resline"
    res_line = zimkateg = bediener = guest = reservation = reslin_queasy = res_history = None

    reslin_list = zkbuff1 = zkbuff2 = gbuff = guest1 = None

    reslin_list_list, Reslin_list = create_model_like(Res_line)

    Zkbuff1 = Zimkateg
    Zkbuff2 = Zimkateg
    Gbuff = Guest
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rtc1, rtc2, lvcarea, res_line, zimkateg, bediener, guest, reservation, reslin_queasy, res_history
        nonlocal zkbuff1, zkbuff2, gbuff, guest1


        nonlocal reslin_list, zkbuff1, zkbuff2, gbuff, guest1
        nonlocal reslin_list_list
        return {}

    def res_changes():

        nonlocal rtc1, rtc2, lvcarea, res_line, zimkateg, bediener, guest, reservation, reslin_queasy, res_history
        nonlocal zkbuff1, zkbuff2, gbuff, guest1


        nonlocal reslin_list, zkbuff1, zkbuff2, gbuff, guest1
        nonlocal reslin_list_list

        do_it:bool = False
        cid:str = ""
        cdate:str = ""
        heute:date = None
        zeit:int = 0
        old_bill_adr:str = ""
        new_bill_adr:str = ""
        rstat_list:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", ""]
        Gbuff = Guest
        rstat_list[0] = translateExtended ("Guaranted", lvcarea, "")
        rstat_list[1] = translateExtended ("6 PM", lvcarea, "")
        rstat_list[2] = translateExtended ("Tentative", lvcarea, "")
        rstat_list[3] = translateExtended ("WaitList", lvcarea, "")
        rstat_list[4] = ""
        rstat_list[5] = translateExtended ("Inhouse", lvcarea, "")
        rstat_list[6] = ""
        rstat_list[7] = translateExtended ("Departed", lvcarea, "")
        rstat_list[8] = translateExtended ("Cancelled", lvcarea, "")
        rstat_list[9] = translateExtended ("NoShow", lvcarea, "")
        rstat_list[10] = translateExtended ("ShareRes", lvcarea, "")
        rstat_list[11] = ""
        rstat_list[12] = translateExtended ("RmSharer", lvcarea, "")
        Guest1 = Guest

        if res_mode.lower()  == "new" or res_mode.lower()  == "insert":
            res_changes0()

            return

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == res_line.resnr)).first()

        if res_line.ankunft != reslin_list.ankunft or res_line.abreise != reslin_list.abreise or res_line.zimmeranz != reslin_list.zimmeranz or res_line.erwachs != reslin_list.erwachs or res_line.kind1 != reslin_list.kind1 or res_line.gratis != reslin_list.gratis or res_line.zikatnr != reslin_list.zikatnr or res_line.zinr != reslin_list.zinr or res_line.arrangement != reslin_list.arrangement or res_line.zipreis != reslin_list.zipreis or reslin_list.was_status != to_int(fixed_rate) or res_line.name.lower()  != (guestname).lower()  or res_line.resstatus != reslin_list.resstatus or reservation.bemerk.lower()  != (mr_comment).lower()  or res_line.bemerk.lower()  != (rl_comment).lower()  or res_line.gastnrpay != reslin_list.gastnrpay:
            do_it = True
        heute = get_current_date()
        zeit = get_current_time_in_seconds()

        if trim(res_line.changed_id) != "":
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        elif len(res_line.reserve_char) >= 14:
            cid = substring(res_line.reserve_char, 13)

        if do_it:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "ResChanges"
            reslin_queasy.resnr = reslin_list.resnr
            reslin_queasy.reslinnr = reslin_list.reslinnr
            reslin_queasy.date2 = heute
            reslin_queasy.number2 = zeit


            pass

            if earlyci:
                reslin_queasy.number1 = 1
            reslin_queasy.char3 = to_string(res_line.ankunft) + ";" + to_string(reslin_list.ankunft) + ";" + to_string(res_line.abreise) + ";" + to_string(reslin_list.abreise) + ";" + to_string(res_line.zimmeranz) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(res_line.erwachs) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(res_line.kind1) + ";" + to_string(reslin_list.kind1) + ";" + to_string(res_line.gratis) + ";" + to_string(reslin_list.gratis) + ";" + to_string(res_line.zikatnr) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(res_line.zinr) + ";" + to_string(reslin_list.zinr) + ";"

            if reslin_list.reserve_int == res_line.reserve_int:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.arrangement) + ";" + to_string(reslin_list.arrangement) + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.arrangement) + ";" + to_string(res_line.reserve_int) + ";"
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.zipreis) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(heute) + ";" + to_string(res_line.name) + ";" + to_string(guestname) + ";"

            if reslin_list.was_status == 0:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO", "x(3)") + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"

            if not fixed_rate:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO", "x(3)") + ";"
            else:
                reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"

            reslin_queasy = db_session.query(Reslin_queasy).first()


            if res_line.resstatus != reslin_list.resstatus:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.datum = heute
                res_history.zeit = zeit
                res_history.aenderung = res_line.bemerk
                res_history.action = "Resstatus Changed"

                if reslin_list.resstatus == 5:
                    rstat_list[4] = "Verbal Confirm"
                res_history.aenderung = "Resstatus " + chr(10) + rstat_list[res_line.resstatus - 1] + chr(10) + chr(10) + "*** Changed to:" + chr(10) + chr(10) + rstat_list[reslin_list.resstatus - 1] + " ResNo " + to_string(res_line.resnr) + chr(10) + " RmNo " + to_string(res_line.zinr)

                if bediener:
                    res_history.betriebsnr = bediener.nr


            if (reservation.bemerk != mr_comment) or (res_line.bemerk != rl_comment):
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.datum = heute
                res_history.zeit = zeit
                res_history.aenderung = res_line.bemerk
                res_history.action = "Remark"


                res_history.aenderung = to_string(res_line.resnr) + "-" + reservation.bemerk + chr(10) + res_line.bemerk + chr(10) + chr(10) + "*** Changed to:" + chr(10) + chr(10) + mr_comment + chr(10) + rl_comment

                if bediener:
                    res_history.betriebsnr = bediener.nr


            if (res_line.gastnrpay != reslin_list.gastnrpay) and (res_mode.lower()  == "modify" or res_mode.lower().lower()  == "inhouse" or res_mode.lower().lower()  == "split"):

                gbuff = db_session.query(Gbuff).filter(
                        (Gbuff.gastnr == res_line.gastnrpay)).first()

                if gbuff:
                    old_bill_adr = gbuff.name

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == reslin_list.gastnrpay)).first()

                if guest:
                    new_bill_adr = guest.name
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.resnr = res_line.resnr
                res_history.reslinnr = res_line.reslinnr
                res_history.datum = heute
                res_history.zeit = zeit
                res_history.action = "Bill Receiver Changed"
                res_history.aenderung = old_bill_adr + chr(10) + chr(10) +\
                        "*** Changed to:" + chr(10) + chr(10) +\
                        new_bill_adr + chr(10) + chr(10) +\
                        "*** Rsv No: " + to_string(res_line.resnr) + chr(10) +\
                        "*** Rsv Line No: " + to_string(res_line.reslinnr)

                if bediener:
                    res_history.betriebsnr = bediener.nr

                res_history = db_session.query(Res_history).first()


        if res_line.l_zuordnung[0] != reslin_list.l_zuordnung[0]:

            if res_line.l_zuordnung[0] != 0:

                zkbuff1 = db_session.query(Zkbuff1).filter(
                        (Zkbuff1.zikatnr == res_line.l_zuordnung[0])).first()

            if zkbuff1:
                rtc1 = zkbuff1.kurzbez

            if reslin_list.l_zuordnung[0] != 0:

                zkbuff2 = db_session.query(Zkbuff2).filter(
                        (Zkbuff2.zikatnr == reslin_list.l_zuordnung[0])).first()

            if zkbuff2:
                rtc2 = zkbuff2.kurzbez
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "ResChanges"
            reslin_queasy.resnr = res_line.resnr
            reslin_queasy.reslinnr = res_line.reslinnr
            reslin_queasy.date2 = get_current_date()
            reslin_queasy.number2 = get_current_time_in_seconds()


            reslin_queasy.char3 = to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("RTC changed:") + ";" + to_string(rtc1) + " -> " + to_string(rtc2) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

            reslin_queasy = db_session.query(Reslin_queasy).first()


    def res_changes0():

        nonlocal rtc1, rtc2, lvcarea, res_line, zimkateg, bediener, guest, reservation, reslin_queasy, res_history
        nonlocal zkbuff1, zkbuff2, gbuff, guest1


        nonlocal reslin_list, zkbuff1, zkbuff2, gbuff, guest1
        nonlocal reslin_list_list

        cid:str = ""
        cdate:str = ""
        Guest1 = Guest
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = reslin_list.resnr
        reslin_queasy.reslinnr = reslin_list.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.ankunft) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.abreise) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.zimmeranz) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.erwachs) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.kind1) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.gratis) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zikatnr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.zinr) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.arrangement) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(reslin_list.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(reslin_list.name) + ";" + to_string("New Reservation") + ";"

        if reslin_list.was_status == 0:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"

        if not fixed_rate:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES") + ";"

        reslin_queasy = db_session.query(Reslin_queasy).first()


    reslin_list = query(reslin_list_list, first=True)

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == reslin_list.resnr) &  (Res_line.reslinnr == reslin_list.reslinnr)).first()

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    res_changes()

    return generate_output()