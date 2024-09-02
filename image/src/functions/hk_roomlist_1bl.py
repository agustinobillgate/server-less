from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpchar import htpchar
from sqlalchemy import func
from models import Guest, Queasy, Htparam, History, Zimmer, Outorder, Res_line, Reservation, Reslin_queasy, Zimkateg, Guestseg, Segment

def hk_roomlist_1bl(casetype:int, pvilanguage:int, curr_date:date, prog_name:str):
    def_cotime = ""
    pr_opt_str = ""
    ci_date = None
    output_list_list = []
    t_history_list = []
    lvcarea:str = "hk_roomlist"
    stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", ""]
    vip_nr:[int] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    guest = queasy = htparam = history = zimmer = outorder = res_line = reservation = reslin_queasy = zimkateg = guestseg = segment = None

    output_list = t_history = gast = rline = None

    output_list_list, Output_list = create_model("Output_list", {"location":str, "active_flag":int, "resnr":int, "reslinnr":int, "service_flag":bool, "flag":int, "ankunft":date, "abreise":date, "zinr":str, "rstat":str, "gstat":str, "floor":int, "inactive":str, "kbezeich":str, "arrival":bool, "inhouse":bool, "zistatus":int, "gastnrmember":int, "gname":str, "company":str, "arrtime":str, "deptime":str, "etd":str, "bemerk":str, "cashbasis":bool, "vip":str, "spreq":str, "norms":int, "pax":int, "rmrate":decimal, "argt":str, "usr_id":str, "nat":str}, {"active_flag": 99})
    t_history_list, T_history = create_model("T_history", {"ankunft":date, "abreise":date, "zinr":str, "zi_wechsel":bool, "bemerk":str, "gastnr":int})

    Gast = Guest
    Rline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal gast, rline


        nonlocal output_list, t_history, gast, rline
        nonlocal output_list_list, t_history_list
        return {"def_cotime": def_cotime, "pr_opt_str": pr_opt_str, "ci_date": ci_date, "output-list": output_list_list, "t-history": t_history_list}

    def fill_list():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal gast, rline


        nonlocal output_list, t_history, gast, rline
        nonlocal output_list_list, t_history_list

        i:int = 0
        anz:int = 0
        off_market:bool = False
        output_list_list.clear()

        for zimmer in db_session.query(Zimmer).all():
            off_market = False

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr == 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).first()

            if outorder:
                off_market = True
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.location = zimmer.code
            output_list.floor = zimmer.etage
            output_list.zinr = zimmer.zinr
            output_list.kbezeich = zimmer.kbezeich
            output_list.zistatus = zimmer.zistatus

            if not zimmer.sleeping:
                output_list.inactive = "  i"

            if off_market:
                output_list.rstat = stat_list[7]
                output_list.zistatus = 7
            else:
                output_list.rstat = stat_list[zimmer.zistatus + 1 - 1]

            if output_list.zistatus == 6:

                outorder = db_session.query(Outorder).filter(
                        (Outorder.zinr == zimmer.zinr)).first()

                if outorder and outorder.betriebsnr > 2:
                    output_list.service_flag = True
                    output_list.rstat = stat_list[9]
                    output_list.zistatus = 9

            if (zimmer.zistatus >= 3 and zimmer.zistatus <= 5) or zimmer.zistatus == 8:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resstatus == 6) &  (Res_line.zinr == zimmer.zinr)).first()

                if res_line:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()

                    gast = db_session.query(Gast).filter(
                            (Gast.gastnr == res_line.gastnr)).first()

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == res_line.resnr)).first()

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.zinr == res_line.zinr), first=True)

                    if guest.karteityp == 0:
                        output_list.gastnrmember = res_line.gastnrmember
                    output_list.inhouse = True
                    output_list.resnr = res_line.resnr
                    output_list.reslinnr = res_line.reslinnr
                    output_list.active_flag = res_line.active_flag
                    output_list.ankunft = res_line.ankunft
                    output_list.abreise = res_line.abreise
                    anz = res_line.erwachs + res_line.gratis
                    output_list.bemerk = res_line.bemerk
                    output_list.norms = res_line.zimmeranz
                    output_list.pax = res_line.erwachs
                    output_list.rmrate = res_line.zipreis
                    output_list.argt = res_line.arrangement
                    output_list.usr_id = reservation.useridanlage

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()
                    output_list.vip = check_vip_guest()

                    reslin_queasy = db_session.query(Reslin_queasy).filter(
                            (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                    if reslin_queasy:
                        output_list.spreq = reslin_queasy.char3 + "," + output_list.spreq

                    queasy = db_session.query(Queasy).filter(
                            (Queasy.key == 24) &  (Queasy.char1 == res_line.zinr)).first()

                    if queasy:
                        output_list.bemerk = output_list.bemerk + chr(10) + chr(10) + translateExtended ("Guest Preference:", lvcarea, "") + chr(10)

                        for queasy in db_session.query(Queasy).filter(
                                (Queasy.key == 24) &  (Queasy.char1 == res_line.zinr)).all():
                            output_list.bemerk = output_list.bemerk + queasy.char3 + chr(10)

                    if res_line.ankzeit != 0:
                        output_list.arrtime = to_string(res_line.ankzeit, "HH:MM")

                    if res_line.abreisezeit != 0:
                        output_list.deptime = to_string(res_line.abreisezeit, "HH:MM")

                    if substring(res_line.flight_nr, 17, 4) != "0000" and substring(res_line.flight_nr, 17, 4) != "    ":
                        output_list.etd = substring(res_line.flight_nr, 17, 2) + ":" + substring(res_line.flight_nr, 19, 2)

                    if output_list.gname == "":
                        output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.company = gast.name
                        output_list.nat = guest.nation1

                    if res_line.ankunft == res_line.abreise:

                        if anz <= 2:
                            for i in range(1,anz + 1) :
                                output_list.gstat = output_list.gstat + "U"
                        else:
                            output_list.gstat = output_list.gstat + to_string(anz) + "U"
                        for i in range(1,res_line.kind1 + 1) :
                            output_list.gstat = output_list.gstat + "u"
                        for i in range(1,res_line.kind2 + 1) :
                            output_list.gstat = output_list.gstat + "C"

                    elif res_line.abreise == get_current_date():

                        if anz <= 2:
                            for i in range(1,anz + 1) :
                                output_list.gstat = output_list.gstat + "D"
                        else:
                            output_list.gstat = output_list.gstat + to_string(anz) + "D"
                        for i in range(1,res_line.kind1 + 1) :
                            output_list.gstat = output_list.gstat + "d"
                        for i in range(1,res_line.kind2 + 1) :
                            output_list.gstat = output_list.gstat + "C"
                    else:

                        if anz <= 2:
                            for i in range(1,anz + 1) :
                                output_list.gstat = output_list.gstat + "R"
                        else:
                            output_list.gstat = output_list.gstat + to_string(anz) + "R"
                        for i in range(1,res_line.kind1 + 1) :
                            output_list.gstat = output_list.gstat + "r"
                        for i in range(1,res_line.kind2 + 1) :
                            output_list.gstat = output_list.gstat + "C"

                if zimmer.zistatus == 3:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (Res_line.ankunft == ci_date) &  (Res_line.zinr == zimmer.zinr)).first()

                    if res_line:

                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember)).first()

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == res_line.gastnr)).first()

                        reservation = db_session.query(Reservation).filter(
                                (Reservation.resnr == res_line.resnr)).first()
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.resnr = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.ankunft = res_line.ankunft
                        output_list.abreise = res_line.abreise
                        output_list.active_flag = res_line.active_flag
                        output_list.norms = res_line.zimmeranz
                        output_list.pax = res_line.erwachs
                        output_list.rmrate = res_line.zipreis
                        output_list.argt = res_line.arrangement

                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember)).first()
                        output_list.vip = check_vip_guest()

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:
                            output_list.spreq = reslin_queasy.char3 + "," + output_list.spreq

                        if guest.karteityp == 0:
                            output_list.gastnrmember = res_line.gastnrmember
                        output_list.location = zimmer.code
                        output_list.floor = zimmer.etage
                        output_list.zinr = zimmer.zinr
                        output_list.kbezeich = zimmer.kbezeich
                        output_list.zistatus = zimmer.zistatus

                        if not zimmer.sleeping:
                            output_list.inactive = "  i"

                        if off_market:
                            output_list.rstat = stat_list[7]
                            output_list.zistatus = 7
                        else:
                            output_list.rstat = stat_list[zimmer.zistatus + 1 - 1]
                        output_list.bemerk = res_line.bemerk

                        if output_list.gname == "":
                            output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                            output_list.company = gast.name
                            output_list.nat = guest.nation1
                        output_list.arrival = True
                        anz = res_line.erwachs + res_line.gratis

                        if anz <= 2:
                            for i in range(1,anz + 1) :
                                output_list.gstat = output_list.gstat + "A"
                        else:
                            output_list.gstat = output_list.gstat + to_string(anz) + "A"
                        anz = res_line.kind1 + res_line.l_zuordnung[3]

                        if anz <= 2:
                            for i in range(1,anz + 1) :
                                output_list.gstat = output_list.gstat + "a"
                        else:
                            output_list.gstat = output_list.gstat + to_string(anz) + "a"
                        for i in range(1,res_line.kind2 + 1) :
                            output_list.gstat = output_list.gstat + "C"

                        if substring(res_line.flight_nr, 6, 4) != "0000" and substring(res_line.flight_nr, 6, 4) != "    ":
                            output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

            elif zimmer.zistatus <= 2:

                if zimmer.zistatus == 2:

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resstatus == 8) &  (Res_line.active_flag == 2) &  (Res_line.abreise == ci_date) &  (Res_line.zinr == zimmer.zinr)).first()

                    if res_line:
                        output_list.arrtime = to_string(res_line.ankzeit, "HH:MM")
                        output_list.deptime = to_string(res_line.abreisezeit, "HH:MM")

                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember)).first()

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == res_line.gastnr)).first()

                        output_list = query(output_list_list, filters=(lambda output_list :output_list.zinr == res_line.zinr), first=True)

                        if output_list:

                            if guest.karteityp == 0:
                                output_list.gastnrmember = res_line.gastnrmember
                            output_list.rstat = output_list.rstat + " *"

                res_line = db_session.query(Res_line).filter(
                        ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (Res_line.active_flag == 0) &  (Res_line.ankunft == ci_date) &  (Res_line.zinr == zimmer.zinr)).first()

                if res_line:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()

                    gast = db_session.query(Gast).filter(
                            (Gast.gastnr == res_line.gastnr)).first()

                    reservation = db_session.query(Reservation).filter(
                            (Reservation.resnr == res_line.resnr)).first()

                    output_list = query(output_list_list, filters=(lambda output_list :output_list.zinr == res_line.zinr), first=True)

                    if guest.karteityp == 0:
                        output_list.gastnrmember = res_line.gastnrmember
                    output_list.bemerk = res_line.bemerk

                    if output_list.gname == "":

                        guest = db_session.query(Guest).filter(
                                (Guest.gastnr == res_line.gastnrmember)).first()
                        output_list.vip = check_vip_guest()

                        reslin_queasy = db_session.query(Reslin_queasy).filter(
                                (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                        if reslin_queasy:
                            output_list.spreq = reslin_queasy.char3 + "," + output_list.spreq


                        output_list.gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                        output_list.company = gast.name
                        output_list.nat = guest.nation1
                    output_list.ankunft = res_line.ankunft
                    output_list.abreise = res_line.abreise
                    output_list.arrival = True


                    anz = res_line.erwachs + res_line.gratis

                    if anz <= 2:
                        for i in range(1,anz + 1) :
                            output_list.gstat = output_list.gstat + "A"
                    else:
                        output_list.gstat = output_list.gstat + to_string(anz) + "A"
                    anz = res_line.kind1 + res_line.l_zuordnung[3]

                    if anz <= 2:
                        for i in range(1,anz + 1) :
                            output_list.gstat = output_list.gstat + "a"
                    else:
                        output_list.gstat = output_list.gstat + to_string(anz) + "a"
                    for i in range(1,res_line.kind2 + 1) :
                        output_list.gstat = output_list.gstat + "C"

                    if res_line.ankzeit != 0:
                        output_list.arrtime = to_string(res_line.ankzeit, "HH:MM")

                    elif substring(res_line.flight_nr, 6, 4) != "0000" and substring(res_line.flight_nr, 6, 4) != "    ":
                        output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (Res_line.zinr == "") &  (Res_line.ankunft == ci_date)).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            gast = db_session.query(Gast).filter(
                    (Gast.gastnr == res_line.gastnr)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.resnr = res_line.resnr
            output_list.reslinnr = res_line.reslinnr
            output_list.active_flag = res_line.active_flag
            output_list.ankunft = res_line.ankunft
            output_list.abreise = res_line.abreise
            output_list.norms = res_line.zimmeranz
            output_list.pax = res_line.erwachs
            output_list.rmrate = res_line.zipreis
            output_list.argt = res_line.arrangement

            if guest.karteityp == 0:
                output_list.gastnrmember = res_line.gastnrmember
            output_list.flag = 1
            output_list.kbezeich = zimkateg.kurzbez
            output_list.zinr = "#" + trim(to_string(res_line.zimmeranz, ">>9"))
            output_list.bemerk = res_line.bemerk
            output_list.gname = res_line.name
            output_list.company = gast.name
            output_list.arrival = True

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()
            output_list.vip = check_vip_guest()

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

            if reslin_queasy:
                output_list.spreq = reslin_queasy.char3 + "," + output_list.spreq


            anz = res_line.erwachs + res_line.gratis

            if anz <= 2:
                for i in range(1,anz + 1) :
                    output_list.gstat = output_list.gstat + "A"
            else:
                output_list.gstat = output_list.gstat + to_string(anz) + "A"
            anz = res_line.kind1 + res_line.l_zuordnung[3]

            if anz <= 2:
                for i in range(1,anz + 1) :
                    output_list.gstat = output_list.gstat + "a"
            else:
                output_list.gstat = output_list.gstat + to_string(anz) + "a"
            for i in range(1,res_line.kind2 + 1) :
                output_list.gstat = output_list.gstat + "C"

            if substring(res_line.flight_nr, 6, 4) != "0000" and substring(res_line.flight_nr, 6, 4) != "    ":
                output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 2) &  (Res_line.resstatus == 8) &  (Res_line.l_zuordnung[2] == 0) &  (Res_line.abreise == ci_date)).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            gast = db_session.query(Gast).filter(
                    (Gast.gastnr == res_line.gastnr)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (Outorder.betriebsnr == 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).first()
            off_market = None != outorder
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.resnr = res_line.resnr
            output_list.reslinnr = res_line.reslinnr
            output_list.active_flag = res_line.active_flag
            output_list.ankunft = res_line.ankunft
            output_list.abreise = res_line.abreise
            output_list.arrtime = to_string(res_line.ankzeit, "HH:MM")
            output_list.deptime = to_string(res_line.abreisezeit, "HH:MM")
            output_list.flag = 2
            output_list.kbezeich = zimkateg.kurzbez
            output_list.zinr = res_line.zinr
            output_list.location = zimmer.code
            output_list.zistatus = zimmer.zistatus
            output_list.bemerk = res_line.bemerk
            output_list.gname = res_line.name
            output_list.company = gast.name
            output_list.arrival = False
            output_list.norms = res_line.zimmeranz
            output_list.pax = res_line.erwachs
            output_list.rmrate = res_line.zipreis
            output_list.argt = res_line.arrangement

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()
            output_list.vip = check_vip_guest()

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

            if reslin_queasy:
                output_list.spreq = reslin_queasy.char3 + "," + output_list.spreq

            if guest.karteityp == 0:
                output_list.gastnrmember = res_line.gastnrmember
            anz = res_line.erwachs + res_line.gratis

            if anz <= 2:
                for i in range(1,anz + 1) :
                    output_list.gstat = output_list.gstat + "*"
            else:
                output_list.gstat = output_list.gstat + to_string(anz) + "*"
            anz = res_line.kind1 + res_line.l_zuordnung[3]

            if anz <= 2:
                for i in range(1,anz + 1) :
                    output_list.gstat = output_list.gstat + "o"
            else:
                output_list.gstat = output_list.gstat + to_string(anz) + "o"
            for i in range(1,res_line.kind2 + 1) :
                output_list.gstat = output_list.gstat + "C"

            if off_market:
                output_list.rstat = stat_list[7]
                output_list.zistatus = 7
            else:
                output_list.rstat = stat_list[zimmer.zistatus + 1 - 1]

            if substring(res_line.flight_nr, 6, 4) != "0000" and substring(res_line.flight_nr, 6, 4) != "    ":
                output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

        for output_list in query(output_list_list, filters=(lambda output_list :output_list.gastnrmember > 0)):

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == output_list.gastnrmember)).first()

            if guest.bemerkung != "":
                output_list.bemerk = guest.bemerkung + chr(10) + output_list.bemerk
        fill_cashbasis()

    def fill_arrival():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal gast, rline


        nonlocal output_list, t_history, gast, rline
        nonlocal output_list_list, t_history_list

        i:int = 0
        anz:int = 0
        off_market:bool = False
        output_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5)) &  (Res_line.ankunft == curr_date)).all():

            zimkateg = db_session.query(Zimkateg).filter(
                    (Zimkateg.zikatnr == res_line.zikatnr)).first()

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            gast = db_session.query(Gast).filter(
                    (Gast.gastnr == res_line.gastnr)).first()
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.resnr = res_line.resnr
            output_list.reslinnr = res_line.reslinnr
            output_list.active_flag = res_line.active_flag
            output_list.ankunft = res_line.ankunft
            output_list.abreise = res_line.abreise
            output_list.norms = res_line.zimmeranz
            output_list.pax = res_line.erwachs
            output_list.rmrate = res_line.zipreis
            output_list.argt = res_line.arrangement

            if guest.karteityp == 0:
                output_list.gastnrmember = res_line.gastnrmember

            if res_line.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                        (Zimmer.zinr == res_line.zinr)).first()
                output_list.location = zimmer.code
                output_list.floor = zimmer.etage
                output_list.zinr = zimmer.zinr
                output_list.kbezeich = zimmer.kbezeich
                output_list.zistatus = zimmer.zistatus

                if not zimmer.sleeping:
                    output_list.inactive = "  i"

                if off_market:
                    output_list.rstat = stat_list[7]
                    output_list.zistatus = 7
                else:
                    output_list.rstat = stat_list[zimmer.zistatus + 1 - 1]
            else:
                output_list.flag = 1
                output_list.kbezeich = zimkateg.kurzbez
                output_list.zinr = "#" + trim(to_string(res_line.zimmeranz, ">>9"))
            output_list.bemerk = res_line.bemerk
            output_list.gname = res_line.name
            output_list.company = gast.name
            output_list.arrival = True

            guest = db_session.query(Guest).filter(
                    (Guest.gastnr == res_line.gastnrmember)).first()
            output_list.vip = check_vip_guest()

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) &  (Reslin_queasy.resnr == res_line.resnr) &  (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

            if reslin_queasy:
                output_list.spreq = reslin_queasy.char3 + "," + output_list.spreq


            anz = res_line.erwachs + res_line.gratis

            if anz <= 2:
                for i in range(1,anz + 1) :
                    output_list.gstat = output_list.gstat + "A"
            else:
                output_list.gstat = output_list.gstat + to_string(anz) + "A"
            anz = res_line.kind1 + res_line.l_zuordnung[3]

            if anz <= 2:
                for i in range(1,anz + 1) :
                    output_list.gstat = output_list.gstat + "a"
            else:
                output_list.gstat = output_list.gstat + to_string(anz) + "a"
            for i in range(1,res_line.kind2 + 1) :
                output_list.gstat = output_list.gstat + "C"

            if substring(res_line.flight_nr, 6, 4) != "0000" and substring(res_line.flight_nr, 6, 4) != "    ":
                output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)
        fill_cashbasis()

    def fill_cashbasis():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal gast, rline


        nonlocal output_list, t_history, gast, rline
        nonlocal output_list_list, t_history_list


        Rline = Res_line

        for output_list in query(output_list_list, filters=(lambda output_list :output_list.resnr > 0)):

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == output_list.resnr) &  (Rline.reslinnr == output_list.reslinnr)).first()

            if rline and to_int(rline.code) != 0:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 9) &  (Queasy.number1 == to_int(rline.code))).first()

                if queasy and queasy.logi1:
                    output_list.cashBasis = True

    def check_vip_guest():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal gast, rline


        nonlocal output_list, t_history, gast, rline
        nonlocal output_list_list, t_history_list

        c_vip = ""

        def generate_inner_output():
            return c_vip

        guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr) &  ((Guestseg.segmentcode == vip_nr[0]) |  (Guestseg.segmentcode == vip_nr[1]) |  (Guestseg.segmentcode == vip_nr[2]) |  (Guestseg.segmentcode == vip_nr[3]) |  (Guestseg.segmentcode == vip_nr[4]) |  (Guestseg.segmentcode == vip_nr[5]) |  (Guestseg.segmentcode == vip_nr[6]) |  (Guestseg.segmentcode == vip_nr[7]) |  (Guestseg.segmentcode == vip_nr[8]) |  (Guestseg.segmentcode == vip_nr[9]))).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                    (Segment.segmentcode == guestseg.segmentcode)).first()

            if segment:
                c_vip = segment.bezeich + " "


        return generate_inner_output()

    stat_list[0] = translateExtended ("Vacant Clean Checked", lvcarea, "")
    stat_list[1] = translateExtended ("Vacant Clean Unchecked", lvcarea, "")
    stat_list[2] = translateExtended ("Vacant Dirty", lvcarea, "")
    stat_list[3] = translateExtended ("Expected Departure", lvcarea, "")
    stat_list[4] = translateExtended ("Occupied Dirty", lvcarea, "")
    stat_list[5] = translateExtended ("Occupied Cleaned", lvcarea, "")
    stat_list[6] = translateExtended ("Out_of_Order", lvcarea, "")
    stat_list[7] = translateExtended ("Off_Market", lvcarea, "")
    stat_list[8] = translateExtended ("Do not Disturb", lvcarea, "")
    stat_list[9] = translateExtended ("Out_of_Service", lvcarea, "")
    ci_date = get_output(htpdate(87))
    def_cotime = get_output(htpchar(925))

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 140) &  (func.lower(Queasy.char1) == (prog_name).lower())).first()

    if queasy:
        pr_opt_str = queasy.char3

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()
    vip_nr[0] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()
    vip_nr[1] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()
    vip_nr[2] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()
    vip_nr[3] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()
    vip_nr[4] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()
    vip_nr[5] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()
    vip_nr[6] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()
    vip_nr[7] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()
    vip_nr[8] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 712)).first()
    vip_nr[9] = htparam.finteger

    if casetype == 1:
        fill_list()
    else:
        fill_arrival()

    for output_list in query(output_list_list):

        for history in db_session.query(History).filter(
                (History.gastnr == output_list.gastnrmember) &  (History.abreise <= get_current_date())).all():
            t_history = T_history()
            t_history_list.append(t_history)

            t_history.ankunft = history.ankunft
            t_history.abreise = history.abreise
            t_history.zinr = history.zinr
            t_history.zi_wechsel = history.zi_wechsel
            t_history.bemerk = history.bemerk
            t_history.gastnr = history.gastnr

    return generate_output()