#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 17/10/2025
# .NAME -> .name
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date, time
from functions.intevent_1 import intevent_1
from functions.create_historybl import create_historybl
from models import Bill, Res_line, Zimmer, Htparam, Mealcoup, Zimkateg, Resplan, Messages, Queasy, Guest, Reslin_queasy

def move_room_1bl(pvilanguage:int, recid1:int, moved_room:string, ci_date:date, user_init:string, movereason:string):

    prepare_cache ([Bill, Res_line, Zimmer, Htparam, Mealcoup, Zimkateg, Resplan, Messages, Reslin_queasy])

    changed = False
    msg_str = ""
    resnr:int = 0
    reslinnr:int = 0
    res_mode:string = ""
    lvcarea:string = "check-room-roomplan"
    bill = res_line = zimmer = htparam = mealcoup = zimkateg = resplan = messages = queasy = guest = reslin_queasy = None

    bbuff = None

    Bbuff = create_buffer("Bbuff",Bill)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        return {"changed": changed, "msg_str": msg_str}

    def move_room():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        prev_zinr:string = ""
        resline = None
        move_str:string = ""
        Resline =  create_buffer("Resline",Res_line)
        resnr = res_line.resnr
        reslinnr = res_line.reslinnr

        if res_line.resstatus == 6 or res_line.resstatus == 13:
            res_mode = "inhouse"
        else:
            res_mode = "modify"

        if res_mode  == ("inhouse") :

            zimmer = get_cache (Zimmer, {"zinr": [(eq, moved_room)]})

            if res_line.abreise == ci_date:
                zimmer.zistatus = 3
            else:
                zimmer.zistatus = 5
            pass
        pass
        min_resplan()

        if res_line.resstatus == 6:
            rmchg_sharer(res_line.zinr, moved_room)

            htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

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

            htparam = get_cache (Htparam, {"paramnr": [(eq, 307)]})

            if htparam.flogical:
                move_str = "Move in|" + prev_zinr


                get_output(intevent_1(1, moved_room, move_str, res_line.resnr, res_line.reslinnr))
            get_output(create_historybl(res_line.resnr, res_line.reslinnr, prev_zinr, "roomchg", user_init, movereason))

            resline = db_session.query(Resline).filter(
                         (Resline.resnr == res_line.resnr) & ((Resline.active_flag == 0) | (Resline.active_flag == 1)) & (Resline.resstatus != 12) & (Resline.zinr == (prev_zinr))).first()

            if not resline:

                mealcoup = get_cache (Mealcoup, {"zinr": [(eq, prev_zinr)],"activeflag": [(eq, True)]})

                if mealcoup:
                    mealcoup.zinr = res_line.zinr
                    pass


    def min_resplan():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        beg_datum:date = None
        i:int = 0
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})

        if zimmer and (not zimmer.sleeping):
            pass
        else:
            i = rline.resstatus

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rline.zikatnr)]})

            if res_mode  == ("inhouse") :
                beg_datum = get_current_date()
            else:
                beg_datum = rline.ankunft
            curr_date = beg_datum
            while curr_date >= beg_datum and curr_date < rline.abreise:

                resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                if resplan:
                    pass
                    resplan.anzzim[i - 1] = resplan.anzzim[i - 1] - rline.zimmeranz
                    pass
                pass
                curr_date = curr_date + timedelta(days=1)


    def rmchg_sharer(act_zinr:string, new_zinr:string):

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        res_recid1:int = 0
        res_line1 = None
        res_line2 = None
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        curr_datum:date = None
        end_datum:date = None
        new_zkat = None
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        New_zkat =  create_buffer("New_zkat",Zimkateg)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

        if htparam:
            beg_datum = htparam.fdate
        end_datum = beg_datum
        res_recid1 = 0

        for messages in db_session.query(Messages).filter(
                     (Messages.zinr == (act_zinr)) & (Messages.resnr == res_line.resnr) & (Messages.reslinnr >= 1)).order_by(Messages._recid).all():
            messages.zinr = new_zinr

        for res_line1 in db_session.query(Res_line1).filter(
                     (Res_line1.resnr == resnr) & (Res_line1.zinr == (act_zinr)) & (Res_line1.resstatus == 13)).order_by(Res_line1._recid).all():

            if end_datum <= res_line1.abreise:
                res_recid1 = res_line1._recid
                end_datum = res_line1.abreise

        if res_line.resstatus == 6 and res_recid1 == 0:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, act_zinr)]})
            zimmer.zistatus = 2
            pass

        if res_line.resstatus == 6 and res_recid1 != 0:

            res_line1 = get_cache (Res_line, {"_recid": [(eq, res_recid1)]})

            for res_line2 in db_session.query(Res_line2).filter(
                             (Res_line2.resnr == resnr) & (Res_line2.zinr == (act_zinr)) & (Res_line2.resstatus == 13) & (Res_line2.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line2._recid).all():

                zimmer = get_cache (Zimmer, {"zinr": [(eq, new_zinr)]})

                new_zkat = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                if new_zkat.zikatnr != res_line2.zikatnr:
                    for curr_datum in date_range(beg_datum,(res_line2.abreise - timedelta(days=1))) :

                        resplan = get_cache (Resplan, {"zikatnr": [(eq, res_line2.zikatnr)],"datum": [(eq, curr_datum)]})

                        if resplan:
                            pass
                            resplan.anzzim[12] = resplan.anzzim[12] - 1
                            pass
                            pass

                        resplan = get_cache (Resplan, {"zikatnr": [(eq, new_zkat.zikatnr)],"datum": [(eq, curr_datum)]})

                        if not resplan:
                            resplan = Resplan()
                            db_session.add(resplan)

                            resplan.datum = curr_datum
                            resplan.zikatnr = new_zkat.zikatnr
                        resplan.anzzim[12] = resplan.anzzim[12] + 1
                        pass
                        pass

                for bill in db_session.query(Bill).filter(
                                 (Bill.resnr == resnr) & (Bill.parent_nr == res_line2.reslinnr)).order_by(Bill._recid).all():

                    bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                    bbuff.zinr = new_zinr
                    pass
                    pass
                res_line2.zinr = new_zinr
                res_line2.zikatnr = new_zkat.zikatnr
                res_line2.setup = zimmer.setup


                pass

            for res_line2 in db_session.query(Res_line2).filter(
                             (Res_line2.resnr == resnr) & (Res_line2.zinr == (act_zinr)) & (Res_line2.resstatus == 12)).order_by(Res_line2._recid).all():
                res_line2.zinr = new_zinr
                res_line2.zikatnr = new_zkat.zikatnr
                res_line2.setup = zimmer.setup


                pass

            zimmer = get_cache (Zimmer, {"zinr": [(eq, act_zinr)]})
            zimmer.zistatus = 2
            pass


    def update_billzinr():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        old_zinr:string = ""
        parent_nr:int = 0
        resline = None
        Resline =  create_buffer("Resline",Res_line)
        old_zinr = res_line.zinr

        for bill in db_session.query(Bill).filter(
                 (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():

            bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
            bbuff.zinr = moved_room
            pass
            pass

            resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

            if resline.resstatus == 12:
                pass
                resline.zinr = moved_room
                pass
            pass

        if res_line.active_flag == 1:

            for bill in db_session.query(Bill).filter(
                     (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 1)).order_by(Bill._recid).all():

                bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                bbuff.zinr = moved_room
                pass
                pass

                resline = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

                if resline.resstatus == 12:
                    pass
                    resline.zinr = moved_room
                    pass
                pass

    def rmchg_ressharer(act_zinr:string, new_zinr:string):

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        new_zkat = None
        res_line2 = None
        rline2 = None
        curr_datum:date = None
        New_zkat =  create_buffer("New_zkat",Zimkateg)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Rline2 =  create_buffer("Rline2",Res_line)

        zimmer = get_cache (Zimmer, {"zinr": [(eq, moved_room)]})

        for rline2 in db_session.query(Rline2).filter(
                 (Rline2.resnr == resnr) & (Rline2.zinr != "") & (Rline2.zinr == (act_zinr)) & (Rline2.resstatus == 11)).order_by(Rline2._recid).all():

            res_line2 = get_cache (Res_line, {"_recid": [(eq, rline2._recid)]})

            if zimmer.zikatnr != res_line2.zikatnr:
                for curr_datum in date_range(res_line2.ankunft,(res_line2.abreise - timedelta(days=1))) :

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, res_line2.zikatnr)],"datum": [(eq, curr_datum)]})

                    if resplan:
                        pass
                        resplan.anzzim[10] = resplan.anzzim[10] - 1
                        pass
                        pass

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, zimmer.zikatnr)],"datum": [(eq, curr_datum)]})

                    if not resplan:
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_datum
                        resplan.zikatnr = zimmer.zikatnr
                    resplan.anzzim[10] = resplan.anzzim[10] + 1
                    pass
                    pass
            res_line2.zinr = new_zinr
            res_line2.zikatnr = zimmer.zikatnr
            pass
            pass


    def update_resline():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        qsy = None
        rline = None
        Qsy =  create_buffer("Qsy",Queasy)
        Rline =  create_buffer("Rline",Res_line)

        if res_line.active_flag == 1:

            queasy = get_cache (Queasy, {"key": [(eq, 24)],"char1": [(eq, res_line.zinr)]})
            while None != queasy:

                qsy = db_session.query(Qsy).filter(
                         (Qsy._recid == queasy._recid)).first()
                qsy.char1 = moved_room
                pass

                curr_recid = queasy._recid
                queasy = db_session.query(Queasy).filter(
                         (Queasy.key == 24) & (Queasy.char1 == res_line.zinr) & (Queasy._recid > curr_recid)).first()

        zimmer = get_cache (Zimmer, {"zinr": [(eq, moved_room)]})
        res_line.zikatnr = zimmer.zikatnr
        res_line.zinr = zimmer.zinr
        res_line.setup = zimmer.setup
        res_line.reserve_char = to_string(get_current_date()) + to_string(get_current_time_in_seconds(), "HH:MM") + user_init
        res_line.changed = ci_date
        res_line.changed_id = user_init


        pass

        rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"kontakt_nr": [(eq, res_line.reslinnr)],"l_zuordnung[2]": [(eq, 1)]})
        while None != rline:
            pass
            rline.zinr = moved_room

            curr_recid = rline._recid
            rline = db_session.query(Rline).filter(
                     (Rline.resnr == res_line.resnr) & (Rline.kontakt_nr == res_line.reslinnr) & (Rline.l_zuordnung[inc_value(2)] == 1) & (Rline._recid > curr_recid)).first()


    def add_resplan():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        curr_date:date = None
        beg_datum:date = None
        end_datum:date = None
        i:int = 0
        anz:int = 0
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        rline = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})

        if zimmer and (not zimmer.sleeping):
            pass
        else:
            i = rline.resstatus

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rline.zikatnr)]})

            if res_mode  == ("inhouse") :
                beg_datum = get_current_date()
            else:
                beg_datum = rline.ankunft
            end_datum = rline.abreise - timedelta(days=1)
            curr_date = beg_datum
            for curr_date in date_range(beg_datum,end_datum) :

                resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                if not resplan:
                    resplan = Resplan()
                    db_session.add(resplan)

                    resplan.datum = curr_date
                    resplan.zikatnr = zimkateg.zikatnr
                anz = resplan.anzzim[i - 1] + rline.zimmeranz
                pass
                resplan.anzzim[i - 1] = anz
                pass
                pass


    def res_changes():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        do_it:bool = False
        guest1 = None
        cid:string = " "
        cdate:string = " "
        Guest1 =  create_buffer("Guest1",Guest)

        if trim(res_line.changed_id) != "":
            cid = res_line.changed_id
            cdate = to_string(res_line.changed)

        elif length(res_line.reserve_char) >= 14:
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
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(" ", "x(3)") + ";"
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()
        pass


    def add_keycard():

        nonlocal changed, msg_str, resnr, reslinnr, res_mode, lvcarea, bill, res_line, zimmer, htparam, mealcoup, zimkateg, resplan, messages, queasy, guest, reslin_queasy
        nonlocal pvilanguage, recid1, moved_room, ci_date, user_init, movereason
        nonlocal bbuff


        nonlocal bbuff

        maxkey:int = 2
        errcode:int = 0
        i:int = 0
        anz0:int = 0
        answer:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 926)]})
        anz0 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 927)]})

        if htparam.finteger != 0:
            maxkey = htparam.finteger
        msg_str = msg_str + chr_unicode(2) + translateExtended ("The Keycard has been created (Qty =", lvcarea, "") + " " + to_string(res_line.betrieb_gast) + ") " + translateExtended ("and can be replaced now.", lvcarea, "")

    res_line = get_cache (Res_line, {"_recid": [(eq, recid1)]})

    if res_line:
        move_room()
        changed = True

    return generate_output()