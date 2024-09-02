from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Bill, Res_line, Guest, Res_history, Resplan, Zimplan, Zimkateg, Zimmer, Outorder

def prepare_mn_startbl(case_type:int, pvilanguage:int):
    mn_stopped = False
    stop_it = False
    arrival_guest = False
    msg_str = ""
    mess_str = ""
    crm_license = False
    banquet_license = False
    na_list_list = []
    lvcarea:str = "mn_start"
    ci_date:date = None
    htparam = bill = res_line = guest = res_history = resplan = zimplan = zimkateg = zimmer = outorder = None

    na_list = rbuff = None

    na_list_list, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "anz":int, "bezeich":str})

    Rbuff = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list
        return {"mn_stopped": mn_stopped, "stop_it": stop_it, "arrival_guest": arrival_guest, "msg_str": msg_str, "mess_str": mess_str, "crm_license": crm_license, "banquet_license": banquet_license, "na-list": na_list_list}

    def check_license_date():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 976)).first()

        if htparam.fdate != None:

            if htparam.fdate < get_current_date():
                stop_it = True
                msg_str = msg_str + chr(2) + translateExtended ("Your License was valid until", lvcarea, "") + " " + to_string(htparam.fdate) + " " + translateExtended ("only.", lvcarea, "") + chr(10) + translateExtended ("Please contact your next Our Technical Support for further information.", lvcarea, "")
        else:
            stop_it = True

        if stop_it:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 999)).first()

            if htparam.flogical:

                htparam = db_session.query(Htparam).filter(
                        (Htparam.paramnr == 996)).first()
                htparam.fchar = ""

                htparam = db_session.query(Htparam).first()

    def check_today_arrival_guest():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list

        answer:bool = False

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 11)) &  (Res_line.ankunft == ci_date)).first()

        if res_line:
            msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Today's arrival guest(s) record found.", lvcarea, "") + chr(10) + translateExtended ("Are you sure you want to proceed the Midnight Program?", lvcarea, "")
            arrival_guest = True
            stop_it = True

            return

    def check_room_sharers():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list


        Rbuff = Res_line

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.resstatus == 13) &  (Res_line.l_zuordnung[2] == 0)).all():

            rbuff = db_session.query(Rbuff).filter(
                    (Rbuff.active_flag == 1) &  (Rbuff.zinr == res_line.zinr) &  (Rbuff.resstatus == 6)).first()

            if not rbuff:
                msg_str = msg_str + chr(2) + translateExtended ("Room sharer(s) with NO MAIN GUEST found! RmNo:", lvcarea, "") + " " + res_line.zinr
                stop_it = True

                return

    def midnite_prog():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list


        reorg_prog()
        check_cancelled_res_line()
        check_delete_res_line()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 105)).first()

        if htparam.fdate < get_current_date():
            htparam.fdate = htparam.fdate + timedelta(days=1)
        ci_date = htparam.fdate

        htparam = db_session.query(Htparam).first()

        htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 87)).first()
        htparam.fdate = ci_date

        htparam = db_session.query(Htparam).first()


    def check_cancelled_res_line():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list


        Rbuff = Res_line

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 9) &  (Res_line.active_flag == 0)).first()
        while None != res_line:

            rbuff = db_session.query(Rbuff).filter(
                        (Rbuff._recid == res_line._recid)).first()
            rbuff.active_flag = 2

            rbuff = db_session.query(Rbuff).first()

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resstatus == 9) &  (Res_line.active_flag == 0)).first()

    def check_delete_res_line():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list


        Rbuff = Res_line

        res_line = db_session.query(Res_line).filter(
                (Res_line.resstatus == 99) &  (Res_line.active_flag <= 2)).first()
        while None != res_line:

            rbuff = db_session.query(Rbuff).filter(
                        (Rbuff._recid == res_line._recid)).first()
            rbuff.active_flag = 2

            rbuff = db_session.query(Rbuff).first()

            res_history = Res_history()
            db_session.add(res_history)

            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Delete ResLine: ResNo " + to_string(res_line.resnr) + " No " +\
                    to_string(res_line.reslinnr) + " - Change ActiveFlag was " +\
                    to_string(res_line.active_flag) + "To 2"
            res_history.action = "Reservation"

            res_history = db_session.query(Res_history).first()

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resstatus == 99) &  (Res_line.active_flag <= 2)).first()

    def reorg_prog():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate
        na_list_list.clear()
        na_list = Na_list()
        na_list_list.append(na_list)

        na_list.reihenfolge = 1
        na_list.bezeich = "Deleting Roomplan Records"
        na_list.flag = 3
        del_roomplan()
        na_list = Na_list()
        na_list_list.append(na_list)

        na_list.reihenfolge = 2
        na_list.bezeich = "Creating Roomplan records"
        na_list.flag = 3
        create_roomplan()
        na_list = Na_list()
        na_list_list.append(na_list)

        na_list.reihenfolge = 3
        na_list.bezeich = "Updating Room Status"
        na_list.flag = 3
        update_rmstatus()

    def del_roomplan():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list

        i:int = 0

        resplan = db_session.query(Resplan).filter(
                (Resplan.datum >= ci_date)).first()

        na_list = query(na_list_list, filters=(lambda na_list :na_list.reihenfolge == 1), first=True)
        while None != resplan:
            i = i + 1
            na_list.anz = na_list.anz + 1

            resplan = db_session.query(Resplan).first()
            db_session.delete(resplan)

            resplan = db_session.query(Resplan).filter(
                    (Resplan.datum >= ci_date)).first()

        zimplan = db_session.query(Zimplan).filter(
                (Zimplan.datum >= ci_date)).first()
        while None != zimplan:
            i = i + 1
            na_list.anz = na_list.anz + 1

            zimplan = db_session.query(Zimplan).first()
            db_session.delete(zimplan)


            zimplan = db_session.query(Zimplan).filter(
                    (Zimplan.datum >= ci_date)).first()

    def create_roomplan():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list

        i:int = 0
        j:int = 0
        anz:int = 0
        beg_datum:date = None
        end_datum:date = None
        curr_date:date = None

        na_list = query(na_list_list, filters=(lambda na_list :na_list.reihenfolge == 2), first=True)

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus != 11) &  (Res_line.ankunft >= ci_date)).all():
            j = res_line.resstatus

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()
            beg_datum = res_line.ankunft
            end_datum = res_line.abreise - 1

            if zimkateg:
                for curr_date in range(beg_datum,end_datum + 1) :

                    resplan = db_session.query(Resplan).filter(
                                (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr
                        resplan.anzzim[j - 1] = res_line.zimmeranz


                        pass

                    elif resplan:

                        resplan = db_session.query(Resplan).first()
                        resplan.anzzim[j - 1] = resplan.anzzim[j - 1] + res_line.zimmeranz

                        resplan = db_session.query(Resplan).first()

            if res_line.zinr != "":
                for curr_date in range(beg_datum,end_datum + 1) :

                    zimplan = db_session.query(Zimplan).filter(
                                (Zimplan.datum == curr_date) &  (Zimplan.zinr == res_line.zinr)).first()

                    if not zimplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        zimplan = Zimplan()
                        db_session.add(zimplan)

                        zimplan.datum = curr_date
                        zimplan.zinr = res_line.zinr
                        zimplan.res_recid = res_line._recid
                        zimplan.gastnrmember = res_line.gastnrmember
                        zimplan.bemerk = res_line.bemerk
                        zimplan.resstatus = res_line.resstatus
                        zimplan.name = res_line.name

                        zimplan = db_session.query(Zimplan).first()


        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.abreise > ci_date) &  (Res_line.resstatus != 12)).all():
            j = res_line.resstatus

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()
            beg_datum = ci_date
            end_datum = res_line.abreise - 1

            if zimkateg:
                for curr_date in range(beg_datum,end_datum + 1) :

                    resplan = db_session.query(Resplan).filter(
                                (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr
                        resplan.anzzim[j - 1] = res_line.zimmeranz


                        pass

                    elif resplan:

                        resplan = db_session.query(Resplan).first()
                        resplan.anzzim[j - 1] = resplan.anzzim[j - 1] + res_line.zimmeranz

                        resplan = db_session.query(Resplan).first()

            if res_line.resstatus == 6:
                for curr_date in range(beg_datum,end_datum + 1) :

                    zimplan = db_session.query(Zimplan).filter(
                                (Zimplan.datum == curr_date) &  (Zimplan.zinr == res_line.zinr)).first()

                    if not zimplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        zimplan = Zimplan()
                        db_session.add(zimplan)

                        zimplan.datum = curr_date
                        zimplan.zinr = res_line.zinr
                        zimplan.res_recid = res_line._recid
                        zimplan.gastnrmember = res_line.gastnrmember
                        zimplan.bemerk = res_line.bemerk
                        zimplan.resstatus = res_line.resstatus
                        zimplan.name = res_line.name

                        zimplan = db_session.query(Zimplan).first()


    def update_rmstatus():

        nonlocal mn_stopped, stop_it, arrival_guest, msg_str, mess_str, crm_license, banquet_license, na_list_list, lvcarea, ci_date, htparam, bill, res_line, guest, res_history, resplan, zimplan, zimkateg, zimmer, outorder
        nonlocal rbuff


        nonlocal na_list, rbuff
        nonlocal na_list_list

        i:int = 0
        ci_date:date = None

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        ci_date = htparam.fdate

        na_list = query(na_list_list, filters=(lambda na_list :na_list.reihenfolge == 3), first=True)

        zimmer = db_session.query(Zimmer).first()
        while None != zimmer:

            if zimmer.personal :

                zimmer = db_session.query(Zimmer).first()
                zimmer.personal = False

                zimmer = db_session.query(Zimmer).first()

            if zimmer.zistatus == 0 or zimmer.zistatus == 1 or zimmer.zistatus == 2:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

            elif zimmer.zistatus == 3:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

                if res_line and res_line.abreise > ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

            elif zimmer.zistatus == 4 or zimmer.zistatus == 5:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

                if res_line and res_line.abreise == ci_date:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 3
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

                elif not res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()
                    zimmer.zistatus = 1
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

            if zimmer.zistatus == 6:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.zinr == zimmer.zinr) &  (Res_line.active_flag == 1) &  (Res_line.resstatus == 6)).first()

                if res_line:
                    i = i + 1
                    na_list.anz = na_list.anz + 1

                    zimmer = db_session.query(Zimmer).first()

                    if res_line.abreise == ci_date:
                        zimmer.zistatus = 3
                    else:
                        zimmer.zistatus = 5
                    zimmer.bediener_nr_stat = 0

                    zimmer = db_session.query(Zimmer).first()

                    outorder = db_session.query(Outorder).filter(
                            (Outorder.zinr == zimmer.zinr)).first()

                    if outorder:
                        db_session.delete(outorder)

            zimmer = db_session.query(Zimmer).first()

        for zimkateg in db_session.query(Zimkateg).all():
            i = 0

            for zimmer in db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr)).all():
                i = i + 1
            zimkateg.maxzimanz = i

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 985)).first()

    if htparam.flogical:
        banquet_license = True

    if case_type == 1:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 105)).first()

        if htparam.fdate >= get_current_date():
            mn_stopped = True

            return generate_output()
        check_license_date()

        if stop_it:
            mn_stopped = True

            return generate_output()
        check_room_sharers()

        if stop_it:
            mn_stopped = True

            return generate_output()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 208)).first()

        if not htparam.flogical:
            mess_str = translateExtended ("Checking Opened Master Bill.", lvcarea, "")

            for bill in db_session.query(Bill).filter(
                    (Bill.flag == 0) &  (Bill.resnr > 0) &  (Bill.reslinnr == 0)).all():

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == bill.resnr) &  (Res_line.active_flag <= 1) &  (Res_line.resstatus != 8) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10)).first()

                if not res_line:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == bill.gastnr)).first()
                    msg_str = msg_str + chr(2) + translateExtended ("Opened master bill found but all guests checked_out:", lvcarea, "") + " " + to_string(bill.rechnr) + " - " + guest.name + chr(10) + translateExtended ("Midnight Program stopped.", lvcarea, "")
                    mn_stopped = True

                    return generate_output()
        check_today_arrival_guest()

        if stop_it:

            return generate_output()
        else:
            case_type = 2

    if case_type == 2:
        midnite_prog()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1459)).first()

        if htparam.paramgruppe == 99 and htparam.flogical:
            crm_license = True

    return generate_output()