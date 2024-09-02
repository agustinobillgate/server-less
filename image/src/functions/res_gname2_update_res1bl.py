from functions.additional_functions import *
import decimal
from datetime import date
from functions.intevent_1 import intevent_1
from functions.create_history import create_history
from sqlalchemy import func
from models import Res_line, Reservation, Guest, Bill, Zimmer, Reslin_queasy, Guestseg, Zimplan, Htparam

def res_gname2_update_res1bl(inp_resnr:int, name:str, fname:str, ftitle:str, name_screen:str, user_init:str, if_flag:bool, ci_date:date, answer:bool, s_list:[S_list]):
    res_mode:str = ""
    curr_reslinnr:int = 0
    priscilla_active:bool = True
    res_line = reservation = guest = bill = zimmer = reslin_queasy = guestseg = zimplan = htparam = None

    s_list = t_resline = resline = resline1 = accbuff = res_line1 = zimplan1 = res_line2 = rline = None

    s_list_list, S_list = create_model("S_list", {"res_recid":int, "resstatus":int, "active_flag":int, "flag":int, "karteityp":int, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "old_zinr":str, "name":str, "nat":str, "land":str, "zinr":str, "eta":str, "etd":str, "flight1":str, "flight2":str, "rmcat":str, "ankunft":date, "abreise":date, "zipreis":decimal, "bemerk":str})
    t_resline_list, T_resline = create_model_like(Res_line)

    Resline = Res_line
    Resline1 = Res_line
    Accbuff = Res_line
    Res_line1 = Res_line
    Zimplan1 = Zimplan
    Res_line2 = Res_line
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, reslin_queasy, guestseg, zimplan, htparam
        nonlocal resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline


        nonlocal s_list, t_resline, resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline
        nonlocal s_list_list, t_resline_list
        return {}

    def update_res1():

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, reslin_queasy, guestseg, zimplan, htparam
        nonlocal resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline


        nonlocal s_list, t_resline, resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline
        nonlocal s_list_list, t_resline_list

        still_error:bool = False
        gcf_found:bool = False
        master_exist:bool = False
        prev_zinr:str = ""
        gastmember:int = 0
        flight_info:str = ""
        Accbuff = Res_line

        for s_list in query(s_list_list):

            res_line = db_session.query(Res_line).filter(
                    (Res_line._recid == s_list.res_recid)).first()
            buffer_copy(res_line, t_resline)

            if priscilla_active:
                get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

            if num_entries(s_list.bemerk, chr(2)) == 2:
                gastmember = to_int(entry(1, s_list.bemerk, chr(2)))

                if gastmember > 0:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == gastmember)).first()

                elif gastmember == 0:
                    gastmember = create_gcf()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == gastmember)).first()
                res_line.gastnrmember = gastmember
                res_line.name = guest.name + ", " + guest.vorname1 +\
                        " " + guest.anrede1
                res_line.changed = ci_date
                res_line.changed_id = user_init


            else:

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == res_line.gastnrmember)).first()

            res_line = db_session.query(Res_line).first()

            if ((s_list.nat != guest.nation1) and s_list.nat != "") or ((s_list.land != guest.land) and s_list.land != ""):

                if s_list.nat != "":
                    guest.nation1 = s_list.nat

                if s_list.land != "":
                    guest.land = s_list.land
                guest.char2 = user_init

            guest = db_session.query(Guest).first()

            resline = db_session.query(Resline).filter(
                    (Resline._recid == s_list.res_recid)).first()

            if answer:

                if resline.gastnrpay != guest.gastnr and resline.active_flag == 1:

                    bill = db_session.query(Bill).filter(
                            (Bill.resnr == resline.resnr) &  (Bill.reslinnr == resline.reslinnr)).first()

                    if bill:
                        bill.gastnr = guest.gastnr
                        bill.name = guest.name

                resline.gastnrpay = guest.gastnr
                resline.changed = ci_date
                resline.changed_id = user_init
            flight_info = to_string(s_list.flight1, "x(6)") + to_string(s_list.eta, "x(5)") + to_string(s_list.flight2, "x(6)") + to_string(s_list.etd, "x(5)")

            if resline.flight_nr.lower()  != (flight_info).lower() :
                resline.flight_nr = flight_info
                resline.changed = ci_date
                resline.changed_id = user_init

            if resline.zinr != s_list.zinr:

                if resline.active_flag == 0:
                    res_mode = "Modify"
                else:
                    res_mode = "Inhouse"
                curr_reslinnr = resline.reslinnr

                if s_list.zinr != "":
                    still_error = assign_zinr(resline._recid, resline.ankunft, resline.abreise, s_list.zinr, resline.resstatus, resline.gastnrmember, resline.bemerk, resline.name)

                if not still_error:

                    if resline.zinr != "":
                        release_zinr(s_list.zinr)

                        if res_line.resstatus == 6 and if_flag:
                            get_output(intevent_1(2, resline.zinr, "Move out", resline.resnr, resline.reslinnr))
                    prev_zinr = resline.zinr
                    resline.zinr = s_list.zinr

                    if s_list.zinr != "":

                        zimmer = db_session.query(Zimmer).filter(
                                (Zimmer.zinr == s_list.zinr)).first()
                        resline.setup = zimmer.setup
                        resline.zikatnr = zimmer.zikatnr

                    for accbuff in db_session.query(Accbuff).filter(
                            (accBuff.resnr == resline.resnr) &  (accBuff.kontakt_nr == resline.reslinnr) &  (accBuff.l_zuordnung[2] == 1)).all():
                        accBuff.zinr = resline.zinr

                    if resline.active_flag == 1:

                        if res_line.resstatus == 6 and if_flag:
                            get_output(intevent_1(1, resline.zinr, "Change name", resline.resnr, resline.reslinnr))
                        get_output(create_history(resline.resnr, resline.reslinnr, prev_zinr, "roomchg"))

                        for bill in db_session.query(Bill).filter(
                                (Bill.resnr == resline.resnr) &  (Bill.parent_nr == resline.reslinnr) &  (Bill.flag == 0)).all():
                            bill.zinr = s_list.zinr

                            resline1 = db_session.query(Resline1).filter(
                                    (resline.resnr == bill.resnr) &  (Resline1.reslinnr == bill.reslinnr)).first()

                            if resline1.resstatus == 12:

                                resline1 = db_session.query(Resline1).first()
                                resline1.zinr = s_list.zinr

                                resline1 = db_session.query(Resline1).first()

            resline.changed = ci_date
            resline.changed_id = user_init

            resline = db_session.query(Resline).first()

            if t_resline.name != resline.name or t_resline.zinr != resline.zinr:
                res_changes()

    def res_changes():

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, reslin_queasy, guestseg, zimplan, htparam
        nonlocal resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline


        nonlocal s_list, t_resline, resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline
        nonlocal s_list_list, t_resline_list

        cid:str = ""
        cdate:str = ""
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = resline.resnr
        reslin_queasy.reslinnr = resline.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(t_resline.ankunft) + ";" + to_string(resline.ankunft) + ";" + to_string(t_resline.abreise) + ";" + to_string(resline.abreise) + ";" + to_string(t_resline.zimmeranz) + ";" + to_string(resline.zimmeranz) + ";" + to_string(t_resline.erwachs) + ";" + to_string(resline.erwachs) + ";" + to_string(t_resline.kind1) + ";" + to_string(resline.kind1) + ";" + to_string(t_resline.gratis) + ";" + to_string(resline.gratis) + ";" + to_string(t_resline.zikatnr) + ";" + to_string(resline.zikatnr) + ";" + to_string(t_resline.zinr) + ";" + to_string(resline.zinr) + ";" + to_string(t_resline.arrangement) + ";" + to_string(resline.arrangement) + ";" + to_string(t_resline.zipreis) + ";" + to_string(resline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(t_resline.name) + ";" + to_string(resline.name) + ";"

        reslin_queasy = db_session.query(Reslin_queasy).first()


    def create_gcf():

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, reslin_queasy, guestseg, zimplan, htparam
        nonlocal resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline


        nonlocal s_list, t_resline, resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline
        nonlocal s_list_list, t_resline_list

        curr_gastnr = 0
        i:int = 0
        inp_name:str = ""
        lname:str = ""
        fname:str = ""
        ftitle:str = ""

        def generate_inner_output():
            return curr_gastnr
        inp_name = s_list.name


        for i in range(1,num_entries(inp_name, ",")  + 1) :

            if i == 1:
                lname = trim(entry(0, inp_name, ","))
            elif i == 2:
                fname = trim(entry(1, inp_name, ","))
            elif i == 3:
                ftitle = trim(entry(2, inp_name, ","))


        return generate_inner_output()

    def assign_zinr(resline_recid:int, ankunft:date, abreise:date, zinr:str, resstatus:int, gastnrmember:int, bemerk:str, name:str):

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, reslin_queasy, guestseg, zimplan, htparam
        nonlocal resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline


        nonlocal s_list, t_resline, resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline
        nonlocal s_list_list, t_resline_list

        room_blocked = False
        sharer:bool = False
        curr_datum:date = None
        beg_datum:date = None
        res_recid:int = 0

        def generate_inner_output():
            return room_blocked
        Res_line1 = Res_line
        Zimplan1 = Zimplan
        Resline = Res_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()
        sharer = (resstatus == 11) or (resstatus == 13)

        if zinr != "" and not sharer:

            if res_mode.lower()  == "inhouse":
                beg_datum = htparam.fdate
            else:
                beg_datum = ankunft
            room_blocked = False
            for curr_datum in range(beg_datum,(abreise - 1)  + 1) :

                zimplan1 = db_session.query(Zimplan1).filter(
                        (Zimplan1.datum == curr_datum) &  (func.lower(Zimplan1.(zinr).lower()) == (zinr).lower())).first()

                if (not zimplan1) and (not room_blocked):
                    zimplan = Zimplan()
                    db_session.add(zimplan)

                    zimplan.datum = curr_datum
                    zimplan.zinr = zinr
                    zimplan.res_recid = resline_recid
                    zimplan.gastnrmember = gastnrmember
                    zimplan.bemerk = bemerk
                    zimplan.resstatus = resstatus
                    zimplan.name = name

                    zimplan = db_session.query(Zimplan).first()

                else:

                    if zimplan1 and (zimplan1.res_recid != resline_recid):

                        resline = db_session.query(Resline).filter(
                                (Resline._recid == zimplan1.res_recid)).first()

                        if resline and resline.(zinr).lower().lower()  == (zinr).lower()  and resline.active_flag < 2 and resline.ankunft <= zimplan1.datum and resline.abreise > zimplan1.datum:
                            curr_datum = abreise
                            room_blocked = True
                        else:

                            zimplan1 = db_session.query(Zimplan1).first()
                            zimplan1.res_recid = resline_recid
                            zimplan1.gastnrmember = gastnrmember
                            zimplan1.bemerk = bemerk
                            zimplan1.resstatus = resstatus
                            zimplan1.name = name

                            zimplan1 = db_session.query(Zimplan1).first()


            if room_blocked:
                for curr_datum in range(beg_datum,(abreise - 1)  + 1) :

                    zimplan = db_session.query(Zimplan).filter(
                            (Zimplan.datum == curr_datum) &  (func.lower(Zimplan.(zinr).lower()) == (zinr).lower()) &  (Zimplan.res_recid == resline_recid)).first()

                    if zimplan:
                        db_session.delete(zimplan)

            else:

                if resstatus == 6 or resstatus == 13:

                    zimmer = db_session.query(Zimmer).filter(
                            (func.lower(Zimmer.(zinr).lower()) == (zinr).lower())).first()

                    if abreise > htparam.fdate and zimmer.zistatus == 0:
                        zimmer.zistatus = 5

                    elif abreise > htparam.fdate and zimmer.zistatus == 3:
                        zimmer.zistatus = 4
                    else:

                        if abreise == htparam.fdate:

                            res_line1 = db_session.query(Res_line1).filter(
                                    (Res_line1._recid != resline_recid) &  (Res_line1.abreise == abreise) &  (Res_line1.zinr == zimmer.zinr) &  ((Res_line1.resstatus == 6) |  (Res_line1.resstatus == 13))).first()

                            if not res_line1:
                                zimmer.zistatus = 3

                    zimmer = db_session.query(Zimmer).first()

        return generate_inner_output()

    def release_zinr(new_zinr:str):

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, reslin_queasy, guestseg, zimplan, htparam
        nonlocal resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline


        nonlocal s_list, t_resline, resline, resline1, accbuff, res_line1, zimplan1, res_line2, rline
        nonlocal s_list_list, t_resline_list

        res_recid1:int = 0
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        Res_line1 = Res_line
        Res_line2 = Res_line
        Rline = Res_line

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 87)).first()

        rline = db_session.query(Rline).filter(
                (Rline.resnr == inp_resnr) &  (Rline.reslinnr == curr_reslinnr)).first()

        if rline.zinr != "":
            beg_datum = rline.ankunft
            res_recid1 = 0

            if res_mode.lower()  == "delete" or res_mode.lower()  == "cancel" and rline.resstatus == 1:

                res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1.resnr == inp_resnr) &  (Res_line1.zinr == rline.zinr) &  (Res_line1.resstatus == 11)).first()

                if res_line1:

                    res_line1 = db_session.query(Res_line1).first()
                    res_line1.resstatus = 1

                    res_line1 = db_session.query(Res_line1).first()
                    res_recid1 = res_line1._recid

        if res_mode.lower()  == "inhouse":
            answer = True
            beg_datum = htparam.fdate

            if rline.resstatus == 6 and (rline.zinr != new_zinr):

                res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1.resnr == inp_resnr) &  (Res_line1.zinr == rline.zinr) &  (Res_line1.resstatus == 13)).first()

                if res_line1:

                    for res_line2 in db_session.query(Res_line2).filter(
                            (Res_line2.resnr == inp_resnr) &  (Res_line2.zinr == rline.zinr) &  (Res_line2.resstatus == 13)).all():

                        bill = db_session.query(Bill).filter(
                                (Bill.resnr == inp_resnr) &  (Bill.reslinnr == res_line2.reslinnr) &  (Bill.flag == 0) &  (Bill.zinr == res_line2.zinr)).first()
                        bill.zinr = new_zinr
                        parent_nr = bill.parent_nr

                        bill = db_session.query(Bill).first()

                        for bill in db_session.query(Bill).filter(
                                (Bill.resnr == inp_resnr) &  (Bill.parent_nr == parent_nr) &  (Bill.flag == 0) &  (Bill.zinr == res_line2.zinr)).all():
                            bill.zinr = new_zinr

                        res_line2.zinr = new_zinr


                    zimmer = db_session.query(Zimmer).filter(
                            (Zimmer.zinr == rline.zinr)).first()
                    zimmer.zistatus = 2

                    zimmer = db_session.query(Zimmer).first()

    t_resline = T_resline()
    t_resline_list.append(t_resline)


    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == inp_resnr)).first()
    update_res1()

    guest = db_session.query(Guest).first()

    if guest:
        curr_gastnr = guest.gastnr + 1
    else:
        curr_gastnr = 1
    guest = Guest()
    db_session.add(guest)

    guest.gastnr = curr_gastnr
    guest.karteityp = 0
    guest.nation1 = s_list.nat
    guest.land = s_list.land
    guest.name = lname
    guest.vorname1 = fname
    guest.anrede1 = ftitle
    guest.char1 = user_init

    guest = db_session.query(Guest).first()
    guestseg = Guestseg()
    db_session.add(guestseg)

    guestseg.gastnr = guest.gastnr
    guestseg.reihenfolge = 1
    guestseg.segmentcode = reservation.segmentcode

    guestseg = db_session.query(Guestseg).first()


    for zimplan in db_session.query(Zimplan).filter(
                (Zimplan.zinr == rline.zinr) &  (Zimplan.datum >= beg_datum) &  (Zimplan.datum < rline.abreise)).all():

        if res_recid1 != 0:
            zimplan.res_recid = res_recid1
        else:
            db_session.delete(zimplan)

    return generate_output()