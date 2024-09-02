from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.intevent_1 import intevent_1
from functions.create_historybl import create_historybl
import re
from models import Bill, Res_line, Zimmer, Htparam, Mealcoup, Zimkateg, Resplan, Messages, Queasy, Guest, Reslin_queasy

def move_room_1bl(pvilanguage:int, recid1:int, moved_room:str, ci_date:date, user_init:str, movereason:str):
    changed = False
    msg_str = ""
    resnr:int = 0
    reslinnr:int = 0
    res_mode:str = ""
    lvcarea:str = "check_room_roomplan"
    bill = res_line = zimmer = htparam = mealcoup = zimkateg = resplan = messages = queasy = guest = reslin_queasy = None

    bbuff = resline = rline = res_line1 = res_line2 = new_zkat = rline2 = qsy = guest1 = None

    Bbuff = Bill
    Resline = Res_line
    Rline = Res_line
    Res_line1 = Res_line
    Res_line2 = Res_line
    New_zkat = Zimkateg
    Rline2 = Res_line
    Qsy = Queasy
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1
        return {"changed": changed, "msg_str": msg_str}

    def move_room():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        prev_zinr:str = ""
        move_str:str = ""
        Resline = Res_line
        resnr = res_line.resnr
        reslinnr = res_line.reslinnr

        if res_line.resstatus == 6 or res_line.resstatus == 13:
            res_mode = "inhouse"
        else:
            res_mode = "modify"

        if res_mode.lower()  == "inhouse":

            zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.zinr) == (moved_room).lower())).first()

            if res_line.abreise == ci_date:
                zimmer.zistatus = 3
            else:
                zimmer.zistatus = 5

            zimmer = db_session.query(Zimmer).first()

        res_line = db_session.query(Res_line).first()
        min_resplan()

        if res_line.resstatus == 6:
            rmchg_sharer(res_line.zinr, moved_room)

            htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 307)).first()

            if htparam.flogical:
                get_output(intevent_1(2, res_line.zinr, "Move out", res_line.resnr, res_line.reslinnr))
            update_billzinr()
        else:
            rmchg_ressharer(res_line.zinr, moved_room)
        prev_zinr = res_line.zinr
        res_changes()
        update_resline()
        add_resplan()

        if res_line.resstatus == 6:

            htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 307)).first()

            if htparam.flogical:
                move_str = "Move in|" + prev_zinr


                get_output(intevent_1(1, moved_room, move_str, res_line.resnr, res_line.reslinnr))
            get_output(create_historybl(res_line.resnr, res_line.reslinnr, prev_zinr, "roomchg", user_init, movereason))

            resline = db_session.query(Resline).filter(
                        (Resline.resnr == res_line.resnr) &  ((Resline.active_flag == 0) |  (Resline.active_flag == 1)) &  (Resline.resstatus != 12) &  (func.lower(Resline.zinr) == (prev_zinr).lower())).first()

            if not resline:

                mealcoup = db_session.query(Mealcoup).filter(
                            (func.lower(Mealcoup.zinr) == (prev_zinr).lower()) &  (Mealcoup.activeflag)).first()

                if mealcoup:
                    mealcoup.zinr = res_line.zinr

                    mealcoup = db_session.query(Mealcoup).first()

        if res_line.betrieb_gast > 0:

            if SESSION:re.match(".*coder ==.*",PARAMETER):
                add_keycard()
            else:
                msg_str = msg_str + chr(2) + translateExtended ("Replace the KeyCard / Qty  == ", lvcarea, "") + " " + to_string(res_line.betrieb_gast)


    def min_resplan():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        curr_date:date = None
        beg_datum:date = None
        i:int = 0
        Rline = Res_line

        rline = db_session.query(Rline).filter(
                (Rline.resnr == resnr) &  (Rline.reslinnr == reslinnr)).first()

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == rline.zinr)).first()

        if zimmer and (not zimmer.sleeping):
            pass
        else:
            i = rline.resstatus

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == rline.zikatnr)).first()

            if res_mode.lower()  == "inhouse":
                beg_datum = get_current_date()
            else:
                beg_datum = rline.ankunft
            curr_date = beg_datum
            while curr_date >= beg_datum and curr_date < rline.abreise:

                resplan = db_session.query(Resplan).filter(
                        (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

                if resplan:

                    resplan = db_session.query(Resplan).first()
                    resplan.anzzim[i - 1] = resplan.anzzim[i - 1] - rline.zimmeranz

                    resplan = db_session.query(Resplan).first()

                curr_date = curr_date + 1

    def rmchg_sharer(act_zinr:str, new_zinr:str):

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        res_recid1:int = 0
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        curr_datum:date = None
        end_datum:date = None
        Res_line1 = Res_line
        Res_line2 = Res_line
        New_zkat = Zimkateg

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        beg_datum = htparam.fdate
        end_datum = beg_datum
        res_recid1 = 0

        for messages in db_session.query(Messages).filter(
                    (func.lower(Messages.zinr) == (act_zinr).lower()) &  (Messages.resnr == res_line.resnr) &  (Messages.reslinnr >= 1)).all():
            messages.zinr = new_zinr

        for res_line1 in db_session.query(Res_line1).filter(
                    (Res_line1.resnr == resnr) &  (func.lower(Res_line1.zinr) == (act_zinr).lower()) &  (Res_line1.resstatus == 13)).all():

            if end_datum <= res_line1.abreise:
                res_recid1 = res_line1._recid
                end_datum = res_line1.abreise

        if res_line.resstatus == 6 and res_recid1 == 0:

            zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.zinr) == (act_zinr).lower())).first()
            zimmer.zistatus = 2

            zimmer = db_session.query(Zimmer).first()

        if res_line.resstatus == 6 and res_recid1 != 0:

            res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1._recid == res_recid1)).first()

            for res_line2 in db_session.query(Res_line2).filter(
                            (Res_line2.resnr == resnr) &  (func.lower(Res_line2.zinr) == (act_zinr).lower()) &  (Res_line2.resstatus == 13) &  (Res_line2.l_zuordnung[2] == 0)).all():

                zimmer = db_session.query(Zimmer).filter(
                                (func.lower(Zimmer.zinr) == (new_zinr).lower())).first()

                new_zkat = db_session.query(New_zkat).filter(
                                (New_zkat.zikatnr == zimmer.zikatnr)).first()

                if new_zkat.zikatnr != res_line2.zikatnr:
                    for curr_datum in range(beg_datum,(res_line2.abreise - 1)  + 1) :

                        resplan = db_session.query(Resplan).filter(
                                        (Resplan.zikatnr == res_line2.zikatnr) &  (Resplan.datum == curr_datum)).first()

                        if resplan:

                            resplan = db_session.query(Resplan).first()
                            resplan.anzzim[12] = resplan.anzzim[12] - 1

                            resplan = db_session.query(Resplan).first()


                        resplan = db_session.query(Resplan).filter(
                                        (Resplan.zikatnr == new_zkat.zikatnr) &  (Resplan.datum == curr_datum)).first()

                        if not resplan:
                            resplan = Resplan()
                            db_session.add(resplan)

                            resplan.datum = curr_datum
                            resplan.zikatnr = new_zkat.zikatnr
                        resplan.anzzim[12] = resplan.anzzim[12] + 1

                        resplan = db_session.query(Resplan).first()


                for bill in db_session.query(Bill).filter(
                                (Bill.resnr == resnr) &  (Bill.parent_nr == res_line2.reslinnr)).all():

                    bbuff = db_session.query(Bbuff).filter(
                                    (Bbuff._recid == bill._recid)).first()
                    bbuff.zinr = new_zinr

                    bbuff = db_session.query(Bbuff).first()

                res_line2.zinr = new_zinr
                res_line2.zikatnr = new_zkat.zikatnr
                res_line2.setup = zimmer.setup


            for res_line2 in db_session.query(Res_line2).filter(
                            (Res_line2.resnr == resnr) &  (func.lower(Res_line2.zinr) == (act_zinr).lower()) &  (Res_line2.resstatus == 12)).all():
                res_line2.zinr = new_zinr
                res_line2.zikatnr = new_zkat.zikatnr
                res_line2.setup = zimmer.setup


            zimmer = db_session.query(Zimmer).filter(
                            (func.lower(Zimmer.zinr) == (act_zinr).lower())).first()
            zimmer.zistatus = 2

            zimmer = db_session.query(Zimmer).first()


    def update_billzinr():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        old_zinr:str = ""
        parent_nr:int = 0
        Resline = Res_line
        old_zinr = res_line.zinr

        for bill in db_session.query(Bill).filter(
                (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():

            bbuff = db_session.query(Bbuff).filter(
                    (Bbuff._recid == bill._recid)).first()
            bbuff.zinr = moved_room

            bbuff = db_session.query(Bbuff).first()


            resline = db_session.query(Resline).filter(
                    (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.reslinnr)).first()

            if resline.resstatus == 12:

                resline = db_session.query(Resline).first()
                resline.zinr = moved_room

                resline = db_session.query(Resline).first()


        if res_line.active_flag == 1:

            for bill in db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 1)).all():

                bbuff = db_session.query(Bbuff).filter(
                        (Bbuff._recid == bill._recid)).first()
                bbuff.zinr = moved_room

                bbuff = db_session.query(Bbuff).first()


                resline = db_session.query(Resline).filter(
                        (Resline.resnr == bill.resnr) &  (Resline.reslinnr == bill.reslinnr)).first()

                if resline.resstatus == 12:

                    resline = db_session.query(Resline).first()
                    resline.zinr = moved_room

                    resline = db_session.query(Resline).first()

    def rmchg_ressharer(act_zinr:str, new_zinr:str):

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        curr_datum:date = None
        New_zkat = Zimkateg
        Res_line2 = Res_line
        Rline2 = Res_line

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.zinr) == (moved_room).lower())).first()

        for rline2 in db_session.query(Rline2).filter(
                (Rline2.resnr == resnr) &  (func.lower(Rline2.zinr) != "") &  (func.lower(Rline2.zinr) == (act_zinr).lower()) &  (Rline2.resstatus == 11)).all():

            res_line2 = db_session.query(Res_line2).filter(
                    (Res_line2._recid == rline2._recid)).first()

            if zimmer.zikatnr != res_line2.zikatnr:
                for curr_datum in range(res_line2.ankunft,(res_line2.abreise - 1)  + 1) :

                    resplan = db_session.query(Resplan).filter(
                            (Resplan.zikatnr == res_line2.zikatnr) &  (Resplan.datum == curr_datum)).first()

                    if resplan:

                        resplan = db_session.query(Resplan).first()
                        resplan.anzzim[10] = resplan.anzzim[10] - 1

                        resplan = db_session.query(Resplan).first()


                    resplan = db_session.query(Resplan).filter(
                            (Resplan.zikatnr == zimmer.zikatnr) &  (Resplan.datum == curr_datum)).first()

                    if not resplan:
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_datum
                        resplan.zikatnr = zimmer.zikatnr
                    resplan.anzzim[10] = resplan.anzzim[10] + 1

                    resplan = db_session.query(Resplan).first()

            res_line2.zinr = new_zinr
            res_line2.zikatnr = zimmer.zikatnr

            res_line2 = db_session.query(Res_line2).first()


    def update_resline():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        Qsy = Queasy
        Rline = Res_line

        if res_line.active_flag == 1:

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 24) &  (Queasy.char1 == res_line.zinr)).first()
            while None != queasy:

                qsy = db_session.query(Qsy).filter(
                        (Qsy._recid == queasy._recid)).first()
                qsy.char1 = moved_room

                qsy = db_session.query(Qsy).first()

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 24) &  (Queasy.char1 == res_line.zinr)).first()

        zimmer = db_session.query(Zimmer).filter(
                (func.lower(Zimmer.zinr) == (moved_room).lower())).first()
        res_line.zikatnr = zimmer.zikatnr
        res_line.zinr = zimmer.zinr
        res_line.setup = zimmer.setup
        res_line.reserve_char = to_string(get_current_date()) + to_string(get_current_time_in_seconds(), "HH:MM") + user_init
        res_line.changed = ci_date
        res_line.changed_id = user_init

        res_line = db_session.query(Res_line).first()

        rline = db_session.query(Rline).filter(
                (Rline.resnr == res_line.resnr) &  (Rline.kontakt_nr == res_line.reslinnr) &  (Rline.l_zuordnung[2] == 1)).first()
        while None != rline:

            rline = db_session.query(Rline).first()
            rline.zinr = moved_room

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == res_line.resnr) &  (Rline.kontakt_nr == res_line.reslinnr) &  (Rline.l_zuordnung[2] == 1)).first()

    def add_resplan():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        curr_date:date = None
        beg_datum:date = None
        end_datum:date = None
        i:int = 0
        anz:int = 0
        Rline = Res_line

        rline = db_session.query(Rline).filter(
                (Rline.resnr == resnr) &  (Rline.reslinnr == reslinnr)).first()

        zimmer = db_session.query(Zimmer).filter(
                (Zimmer.zinr == rline.zinr)).first()

        if zimmer and (not zimmer.sleeping):
            pass
        else:
            i = rline.resstatus

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == rline.zikatnr)).first()

            if res_mode.lower()  == "inhouse":
                beg_datum = get_current_date()
            else:
                beg_datum = rline.ankunft
            end_datum = rline.abreise - 1
            curr_date = beg_datum
            for curr_date in range(beg_datum,end_datum + 1) :

                resplan = db_session.query(Resplan).filter(
                        (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

                if not resplan:
                    resplan = Resplan()
                    db_session.add(resplan)

                    resplan.datum = curr_date
                    resplan.zikatnr = zimkateg.zikatnr
                anz = resplan.anzzim[i - 1] + rline.zimmeranz

                resplan = db_session.query(Resplan).first()
                resplan.anzzim[i - 1] = anz

                resplan = db_session.query(Resplan).first()

    def res_changes():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        do_it:bool = False
        cid:str = ""
        cdate:str = ""
        Guest1 = Guest

        if trim(res_line.changed_id) != "":
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        elif len(res_line.reserve_char) >= 14:
            cid = substring(res_line.reserve_char, 13)
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = resnr
        reslin_queasy.reslinnr = reslinnr
        reslin_queasy.char3 = to_string(res_line.ankunft) + ";" +\
                to_string(res_line.ankunft) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.abreise) + ";" +\
                to_string(res_line.zimmeranz, ">>9") + ";" +\
                to_string(res_line.zimmeranz, ">>9") + ";" +\
                to_string(res_line.erwachs, ">9") + ";" +\
                to_string(res_line.erwachs, ">9") + ";" +\
                to_string(res_line.kind1, ">9") + ";" +\
                to_string(res_line.kind1, ">9") + ";" +\
                to_string(res_line.gratis, ">9") + ";" +\
                to_string(res_line.gratis, ">9") + ";" +\
                to_string(res_line.zikatnr, ">>9") + ";" +\
                to_string(zimmer.zikatnr, ">>9") + ";" +\
                to_string(res_line.zinr, "x(6)") + ";" +\
                to_string(moved_room, "x(6)") + ";" +\
                to_string(res_line.arrangement, "x(5)") + ";" +\
                to_string(res_line.arrangement, "x(5)") + ";"

        if res_line.zipreis <= 9999999:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.zipreis, ">,>>>,>>9.99") + ";" + to_string(res_line.zipreis, ">,>>>,>>9.99") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(res_line.zipreis, ">>>>,>>>,>>9") + ";" + to_string(res_line.zipreis, ">>>>,>>>,>>9") + ";"
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(cid, "x(2)") + ";" + to_string(user_init, "x(2)") + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string(res_line.name, "x(16)") + ";" + to_string(res_line.name, "x(16)") + ";"

        if res_line.was_status == 0:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(" NO", "x(3)") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"
        reslin_queasy.char3 = reslin_queasy.char3 + to_string("   ", "x(3)") + ";"
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


    def add_keycard():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1


        nonlocal bbuff, resline, rline, res_line1, res_line2, new_zkat, rline2, qsy, guest1

        maxkey:int = 2
        errcode:int = 0
        i:int = 0
        anz0:int = 0
        answer:bool = True

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 926)).first()
        anz0 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 927)).first()

        if htparam.finteger != 0:
            maxkey = htparam.finteger
        msg_str = msg_str + chr(2) + translateExtended ("The Keycard has been created (Qty  == ", lvcarea, "") + " " + to_string(res_line.betrieb_gast) + ") " + translateExtended ("and can be replaced now.", lvcarea, "")


    res_line = db_session.query(Res_line).filter(
            (Res_line._recid == recid1)).first()
    move_room()
    changed = True

    return generate_output()