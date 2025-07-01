#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.intevent_1 import intevent_1
from functions.create_history import create_history
from models import Res_line, Reservation, Guest, Bill, Zimmer, Queasy, Zimkateg, Reslin_queasy, Guestseg, Zimplan, Htparam

s_list_list, S_list = create_model("S_list", {"res_recid":int, "resstatus":int, "active_flag":int, "flag":int, "karteityp":int, "zimmeranz":int, "erwachs":int, "kind1":int, "kind2":int, "old_zinr":string, "name":string, "nat":string, "land":string, "zinr":string, "eta":string, "etd":string, "flight1":string, "flight2":string, "rmcat":string, "ankunft":date, "abreise":date, "zipreis":Decimal, "bemerk":string})

def res_gname2_update_res1bl(inp_resnr:int, name:string, fname:string, ftitle:string, name_screen:string, user_init:string, if_flag:bool, ci_date:date, answer:bool, s_list_list:[S_list]):

    prepare_cache ([Res_line, Reservation, Guest, Bill, Zimmer, Queasy, Reslin_queasy, Guestseg, Htparam])

    res_mode:string = ""
    curr_reslinnr:int = 0
    priscilla_active:bool = True
    res_line = reservation = guest = bill = zimmer = queasy = zimkateg = reslin_queasy = guestseg = zimplan = htparam = None

    s_list = t_resline = resline = resline1 = None

    t_resline_list, T_resline = create_model_like(Res_line)

    Resline = create_buffer("Resline",Res_line)
    Resline1 = create_buffer("Resline1",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, queasy, zimkateg, reslin_queasy, guestseg, zimplan, htparam
        nonlocal inp_resnr, name, fname, ftitle, name_screen, user_init, if_flag, ci_date, answer
        nonlocal resline, resline1


        nonlocal s_list, t_resline, resline, resline1
        nonlocal t_resline_list

        return {}

    def update_res1():

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, queasy, zimkateg, reslin_queasy, guestseg, zimplan, htparam
        nonlocal inp_resnr, name, fname, ftitle, name_screen, user_init, if_flag, ci_date, answer
        nonlocal resline, resline1


        nonlocal s_list, t_resline, resline, resline1
        nonlocal t_resline_list

        accbuff = None
        still_error:bool = False
        gcf_found:bool = False
        master_exist:bool = False
        prev_zinr:string = ""
        gastmember:int = 0
        flight_info:string = ""
        Accbuff =  create_buffer("Accbuff",Res_line)

        for s_list in query(s_list_list):

            res_line = get_cache (Res_line, {"_recid": [(eq, s_list.res_recid)]})

            if res_line:
                buffer_copy(res_line, t_resline)

                if priscilla_active:
                    get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
                pass

                if num_entries(s_list.bemerk, chr_unicode(2)) == 2 or s_list.flag != res_line.gastnrmember:

                    if s_list.flag != res_line.gastnrmember:
                        gastmember = s_list.flag
                    else:
                        gastmember = to_int(entry(1, s_list.bemerk, chr_unicode(2)))

                    if gastmember > 0:

                        guest = get_cache (Guest, {"gastnr": [(eq, gastmember)]})

                    elif gastmember == 0:
                        gastmember = create_gcf()

                        guest = get_cache (Guest, {"gastnr": [(eq, gastmember)]})

                    if res_line.gastnrmember != gastmember:
                        pass
                    res_line.gastnrmember = gastmember
                    res_line.name = guest.name + ", " + guest.vorname1 +\
                            " " + guest.anrede1
                    res_line.changed = ci_date
                    res_line.changed_id = user_init


                else:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                pass

                if guest:
                    pass

                    if ((s_list.nat != guest.nation1) and s_list.nat != "") or ((s_list.land != guest.land) and s_list.land != ""):

                        if s_list.nat != "":
                            guest.nation1 = s_list.nat

                        if s_list.land != "":
                            guest.land = s_list.land
                        guest.char2 = user_init
                    pass

                resline = get_cache (Res_line, {"_recid": [(eq, s_list.res_recid)]})

                if resline:

                    if answer:

                        if resline.gastnrpay != guest.gastnr and resline.active_flag == 1:

                            bill = get_cache (Bill, {"resnr": [(eq, resline.resnr)],"reslinnr": [(eq, resline.reslinnr)]})

                            if bill:
                                bill.gastnr = guest.gastnr
                                bill.name = guest.name
                                pass
                                pass
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

                                zimmer = get_cache (Zimmer, {"zinr": [(eq, s_list.zinr)]})

                                if zimmer:
                                    resline.setup = zimmer.setup
                                    resline.zikatnr = zimmer.zikatnr

                            for accbuff in db_session.query(Accbuff).filter(
                                     (accBuff.resnr == resline.resnr) & (accBuff.kontakt_nr == resline.reslinnr) & (accBuff.l_zuordnung[2] == 1)).order_by(Accbuff._recid).all():
                                accbuff.zinr = resline.zinr

                            if resline.active_flag == 1:

                                if resline.resstatus == 6 and if_flag:
                                    get_output(intevent_1(1, resline.zinr, "Change name", resline.resnr, resline.reslinnr))
                                get_output(create_history(resline.resnr, resline.reslinnr, prev_zinr, "roomchg"))

                                for bill in db_session.query(Bill).filter(
                                         (Bill.resnr == resline.resnr) & (Bill.parent_nr == resline.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
                                    bill.zinr = s_list.zinr

                                    resline1 = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

                                    if resline1:

                                        if resline1.resstatus == 12:
                                            pass
                                            resline1.zinr = s_list.zinr
                                            pass
                                    pass
                    resline.changed = ci_date
                    resline.changed_id = user_init
                    pass

                    if t_resline.zinr != resline.zinr:
                        update_qsy171()

                    if t_resline.name != resline.name or t_resline.zinr != resline.zinr:
                        res_changes()


    def update_qsy171():

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, queasy, zimkateg, reslin_queasy, guestseg, zimplan, htparam
        nonlocal inp_resnr, name, fname, ftitle, name_screen, user_init, if_flag, ci_date, answer
        nonlocal resline, resline1


        nonlocal s_list, t_resline, resline, resline1
        nonlocal t_resline_list

        curr_date:date = None
        upto_date:date = None
        curr_i:int = 0
        stat_code:string = ""
        iftask:string = ""
        origcode:string = ""
        cat_flag:bool = False
        roomnr:int = 0
        zikatnr:int = 0
        qsy = None
        zbuff = None
        Qsy =  create_buffer("Qsy",Queasy)
        Zbuff =  create_buffer("Zbuff",Zimkateg)
        for curr_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(curr_i - 1, res_line.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == ("$origcode$").lower() :
                origcode = substring(iftask, 10)
                return

        queasy = get_cache (Queasy, {"key": [(eq, 152)]})

        if queasy:
            cat_flag = True

        zbuff = db_session.query(Zbuff).filter(
                 (Zbuff.zikatnr == res_line.zikatnr)).first()

        if zbuff:

            if cat_flag:
                roomnr = zbuff.typ
            else:
                roomnr = zbuff.zikatnr

        zbuff = db_session.query(Zbuff).filter(
                 (Zbuff.zikatnr == t_resline.zikatnr)).first()

        if zbuff:

            if cat_flag:
                zikatnr = zbuff.typ
            else:
                zikatnr = zbuff.zikatnr
        upto_date = res_line.abreise - timedelta(days=1)

        if upto_date < res_line.ankunft:
            upto_date = res_line.ankunft
        for curr_date in date_range(res_line.ankunft,upto_date) :

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, roomnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

            queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, zikatnr)],"char1": [(eq, "")]})

            if queasy and queasy.logi1 == False and queasy.logi2 == False:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                if qsy:
                    qsy.logi2 = True
                    pass
                    pass

            if origcode != "":

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, roomnr)],"char1": [(eq, origcode)]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass

                queasy = get_cache (Queasy, {"key": [(eq, 171)],"date1": [(eq, curr_date)],"number1": [(eq, zikatnr)],"char1": [(eq, origcode)]})

                if queasy and queasy.logi1 == False and queasy.logi2 == False:

                    qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})

                    if qsy:
                        qsy.logi2 = True
                        pass
                        pass


    def res_changes():

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, queasy, zimkateg, reslin_queasy, guestseg, zimplan, htparam
        nonlocal inp_resnr, name, fname, ftitle, name_screen, user_init, if_flag, ci_date, answer
        nonlocal resline, resline1


        nonlocal s_list, t_resline, resline, resline1
        nonlocal t_resline_list

        cid:string = " "
        cdate:string = " "
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = resline.resnr
        reslin_queasy.reslinnr = resline.reslinnr
        reslin_queasy.date2 = get_current_date()
        reslin_queasy.number2 = get_current_time_in_seconds()


        reslin_queasy.char3 = to_string(t_resline.ankunft) + ";" + to_string(resline.ankunft) + ";" + to_string(t_resline.abreise) + ";" + to_string(resline.abreise) + ";" + to_string(t_resline.zimmeranz) + ";" + to_string(resline.zimmeranz) + ";" + to_string(t_resline.erwachs) + ";" + to_string(resline.erwachs) + ";" + to_string(t_resline.kind1) + ";" + to_string(resline.kind1) + ";" + to_string(t_resline.gratis) + ";" + to_string(resline.gratis) + ";" + to_string(t_resline.zikatnr) + ";" + to_string(resline.zikatnr) + ";" + to_string(t_resline.zinr) + ";" + to_string(resline.zinr) + ";" + to_string(t_resline.arrangement) + ";" + to_string(resline.arrangement) + ";" + to_string(t_resline.zipreis) + ";" + to_string(resline.zipreis) + ";" + to_string(user_init) + ";" + to_string(user_init) + ";" + to_string(get_current_date()) + ";" + to_string(get_current_date()) + ";" + to_string(t_resline.name) + ";" + to_string(resline.name) + ";"
        pass
        pass


    def create_gcf():

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, queasy, zimkateg, reslin_queasy, guestseg, zimplan, htparam
        nonlocal inp_resnr, name, name_screen, user_init, if_flag, ci_date, answer
        nonlocal resline, resline1


        nonlocal s_list, t_resline, resline, resline1
        nonlocal t_resline_list

        curr_gastnr = 0
        i:int = 0
        inp_name:string = ""
        lname:string = ""
        fname:string = ""
        ftitle:string = ""

        def generate_inner_output():
            return (curr_gastnr)

        inp_name = s_list.name


        for i in range(1,num_entries(inp_name, ",")  + 1) :

            if i == 1:
                lname = trim(entry(0, inp_name, ","))
            elif i == 2:
                fname = trim(entry(1, inp_name, ","))
            elif i == 3:
                ftitle = trim(entry(2, inp_name, ","))

        guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()

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


        pass
        guestseg = Guestseg()
        db_session.add(guestseg)

        guestseg.gastnr = guest.gastnr
        guestseg.reihenfolge = 1
        guestseg.segmentcode = reservation.segmentcode


        pass
        pass

        return generate_inner_output()


    def assign_zinr(resline_recid:int, ankunft:date, abreise:date, zinr:string, resstatus:int, gastnrmember:int, bemerk:string, name:string):

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, queasy, zimkateg, reslin_queasy, guestseg, zimplan, htparam
        nonlocal inp_resnr, fname, ftitle, name_screen, user_init, if_flag, ci_date, answer
        nonlocal resline, resline1


        nonlocal s_list, t_resline, resline, resline1
        nonlocal t_resline_list

        room_blocked = False
        sharer:bool = False
        curr_datum:date = None
        beg_datum:date = None
        res_recid:int = 0
        res_line1 = None
        zimplan1 = None
        resline = None

        def generate_inner_output():
            return (room_blocked)

        Res_line1 =  create_buffer("Res_line1",Res_line)
        Zimplan1 =  create_buffer("Zimplan1",Zimplan)
        Resline =  create_buffer("Resline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
        sharer = (resstatus == 11) or (resstatus == 13)

        if zinr != "" and not sharer:

            if res_mode.lower()  == ("inhouse").lower() :
                beg_datum = htparam.fdate
            else:
                beg_datum = ankunft
            room_blocked = False
            for curr_datum in date_range(beg_datum,(abreise - 1)) :

                zimplan1 = db_session.query(Zimplan1).filter(
                         (Zimplan1.datum == curr_datum) & (Zimplan1.zinr == (zinr).lower())).first()

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
                    pass
                    pass
                else:

                    if zimplan1 and (zimplan1.res_recid != resline_recid):

                        resline = get_cache (Res_line, {"_recid": [(eq, zimplan1.res_recid)]})

                        if resline and resline.zinr.lower()  == (zinr).lower()  and resline.active_flag < 2 and resline.ankunft <= zimplan1.datum and resline.abreise > zimplan1.datum:
                            curr_datum = abreise
                            room_blocked = True
                        else:
                            pass
                            zimplan1.res_recid = resline_recid
                            zimplan1.gastnrmember = gastnrmember
                            zimplan1.bemerk = bemerk
                            zimplan1.resstatus = resstatus
                            zimplan1.name = name


                            pass
                            pass

            if room_blocked:
                for curr_datum in date_range(beg_datum,(abreise - 1)) :

                    zimplan = get_cache (Zimplan, {"datum": [(eq, curr_datum)],"zinr": [(eq, zinr)],"res_recid": [(eq, resline_recid)]})

                    if zimplan:
                        db_session.delete(zimplan)
                        pass
            else:

                if resstatus == 6 or resstatus == 13:

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, zinr)]})

                    if abreise > htparam.fdate and zimmer.zistatus == 0:
                        zimmer.zistatus = 5

                    elif abreise > htparam.fdate and zimmer.zistatus == 3:
                        zimmer.zistatus = 4

                    elif abreise == htparam.fdate:

                        res_line1 = db_session.query(Res_line1).filter(
                                 (Res_line1._recid != resline_recid) & (Res_line1.abreise == abreise) & (Res_line1.zinr == zimmer.zinr) & ((Res_line1.resstatus == 6) | (Res_line1.resstatus == 13))).first()

                        if not res_line1:
                            zimmer.zistatus = 3
                    pass
                    pass

        return generate_inner_output()


    def release_zinr(new_zinr:string):

        nonlocal res_mode, curr_reslinnr, priscilla_active, res_line, reservation, guest, bill, zimmer, queasy, zimkateg, reslin_queasy, guestseg, zimplan, htparam
        nonlocal inp_resnr, name, fname, ftitle, name_screen, user_init, if_flag, ci_date, resline, resline1


        nonlocal s_list, t_resline, resline, resline1
        nonlocal t_resline_list

        res_recid1:int = 0
        res_line1 = None
        res_line2 = None
        rline = None
        beg_datum:date = None
        answer:bool = False
        parent_nr:int = 0
        Res_line1 =  create_buffer("Res_line1",Res_line)
        Res_line2 =  create_buffer("Res_line2",Res_line)
        Rline =  create_buffer("Rline",Res_line)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

        rline = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, curr_reslinnr)]})

        if rline.zinr != "":
            beg_datum = rline.ankunft
            res_recid1 = 0

            if res_mode.lower()  == ("delete").lower()  or res_mode.lower()  == ("cancel").lower()  and rline.resstatus == 1:

                res_line1 = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 11)]})

                if res_line1:
                    pass
                    res_line1.resstatus = 1
                    pass
                    res_recid1 = res_line1._recid

            if res_mode.lower()  == ("inhouse").lower() :
                answer = True
                beg_datum = htparam.fdate

                if rline.resstatus == 6 and (rline.zinr.lower()  != (new_zinr).lower()):

                    res_line1 = get_cache (Res_line, {"resnr": [(eq, inp_resnr)],"zinr": [(eq, rline.zinr)],"resstatus": [(eq, 13)]})

                    if res_line1:

                        for res_line2 in db_session.query(Res_line2).filter(
                                 (Res_line2.resnr == inp_resnr) & (Res_line2.zinr == rline.zinr) & (Res_line2.resstatus == 13)).order_by(Res_line2._recid).all():

                            bill = get_cache (Bill, {"resnr": [(eq, inp_resnr)],"reslinnr": [(eq, res_line2.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line2.zinr)]})
                            bill.zinr = new_zinr
                            parent_nr = bill.parent_nr
                            pass

                            for bill in db_session.query(Bill).filter(
                                     (Bill.resnr == inp_resnr) & (Bill.parent_nr == parent_nr) & (Bill.flag == 0) & (Bill.zinr == res_line2.zinr)).order_by(Bill._recid).all():
                                bill.zinr = new_zinr
                                pass
                            res_line2.zinr = new_zinr
                            pass

                        zimmer = get_cache (Zimmer, {"zinr": [(eq, rline.zinr)]})
                        zimmer.zistatus = 2
                        pass

            for zimplan in db_session.query(Zimplan).filter(
                         (Zimplan.zinr == rline.zinr) & (Zimplan.datum >= beg_datum) & (Zimplan.datum < rline.abreise)).order_by(Zimplan._recid).all():

                if res_recid1 != 0:
                    zimplan.res_recid = res_recid1
                else:
                    db_session.delete(zimplan)


    t_resline = T_resline()
    t_resline_list.append(t_resline)


    reservation = get_cache (Reservation, {"resnr": [(eq, inp_resnr)]})

    if not reservation:

        return generate_output()
    update_res1()

    return generate_output()