#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpchar import htpchar
from models import Guest, Queasy, Htparam, History, Zimmer, Outorder, Res_line, Reservation, Reslin_queasy, Zimkateg, Guestseg, Segment

def hk_roomlist_1bl(casetype:int, pvilanguage:int, curr_date:date, prog_name:string):

    prepare_cache ([Guest, Queasy, Htparam, History, Zimmer, Res_line, Reservation, Reslin_queasy, Zimkateg, Guestseg, Segment])

    def_cotime = ""
    pr_opt_str = ""
    ci_date = None
    output_list_list = []
    t_history_list = []
    lvcarea:string = "hk-roomlist"
    stat_list:List[string] = create_empty_list(10,"")
    vip_nr:List[int] = create_empty_list(10,0)
    resbemerk:string = ""
    his_bemerk:string = ""
    count_i:int = 0
    guest = queasy = htparam = history = zimmer = outorder = res_line = reservation = reslin_queasy = zimkateg = guestseg = segment = None

    output_list = t_history = gast = None

    output_list_list, Output_list = create_model("Output_list", {"location":string, "active_flag":int, "resnr":int, "reslinnr":int, "service_flag":bool, "flag":int, "ankunft":date, "abreise":date, "zinr":string, "rstat":string, "gstat":string, "floor":int, "inactive":string, "kbezeich":string, "arrival":bool, "inhouse":bool, "zistatus":int, "gastnrmember":int, "gname":string, "company":string, "arrtime":string, "deptime":string, "etd":string, "bemerk":string, "cashbasis":bool, "vip":string, "spreq":string, "norms":int, "pax":int, "rmrate":Decimal, "argt":string, "usr_id":string, "nat":string}, {"active_flag": 99})
    t_history_list, T_history = create_model("T_history", {"ankunft":date, "abreise":date, "zinr":string, "zi_wechsel":bool, "bemerk":string, "gastnr":int})

    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, resbemerk, his_bemerk, count_i, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal casetype, pvilanguage, curr_date, prog_name
        nonlocal gast


        nonlocal output_list, t_history, gast
        nonlocal output_list_list, t_history_list

        return {"def_cotime": def_cotime, "pr_opt_str": pr_opt_str, "ci_date": ci_date, "output-list": output_list_list, "t-history": t_history_list}

    def fill_list():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, resbemerk, his_bemerk, count_i, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal casetype, pvilanguage, curr_date, prog_name
        nonlocal gast


        nonlocal output_list, t_history, gast
        nonlocal output_list_list, t_history_list

        i:int = 0
        anz:int = 0
        off_market:bool = False
        output_list_list.clear()

        for zimmer in db_session.query(Zimmer).order_by((Zimmer.zinr)).all():
            off_market = False

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"betriebsnr": [(eq, 2)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)]})

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
                output_list.inactive = " i"

            if off_market:
                output_list.rstat = stat_list[7]
                output_list.zistatus = 7
            else:
                output_list.rstat = stat_list[zimmer.zistatus + 1 - 1]

            if output_list.zistatus == 6:

                outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)]})

                if outorder and outorder.betriebsnr > 2:
                    output_list.service_flag = True
                    output_list.rstat = stat_list[9]
                    output_list.zistatus = 9

            if (zimmer.zistatus >= 3 and zimmer.zistatus <= 5) or zimmer.zistatus == 8:

                res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, zimmer.zinr)]})

                if res_line:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    output_list = query(output_list_list, filters=(lambda output_list: output_list.zinr == res_line.zinr), first=True)

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
                    output_list.rmrate =  to_decimal(res_line.zipreis)
                    output_list.argt = res_line.arrangement
                    output_list.usr_id = reservation.useridanlage

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                    output_list.vip = check_vip_guest()

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                    if reslin_queasy:
                        output_list.spreq = reslin_queasy.char3 + "," + output_list.spreq

                    queasy = get_cache (Queasy, {"key": [(eq, 24)],"char1": [(eq, res_line.zinr)]})

                    if queasy:
                        output_list.bemerk = output_list.bemerk + chr_unicode(10) + chr_unicode(10) + translateExtended ("Guest Preference:", lvcarea, "") + chr_unicode(10)

                        for queasy in db_session.query(Queasy).filter(
                                 (Queasy.key == 24) & (Queasy.char1 == res_line.zinr)).order_by(Queasy.date1).all():
                            output_list.bemerk = output_list.bemerk + queasy.char3 + chr_unicode(10)

                    if res_line.ankzeit != 0:
                        output_list.arrtime = to_string(res_line.ankzeit, "HH:MM")

                    if res_line.abreisezeit != 0:
                        output_list.deptime = to_string(res_line.abreisezeit, "HH:MM")

                    if substring(res_line.flight_nr, 17, 4) != ("0000").lower()  and substring(res_line.flight_nr, 17, 4) != " ":
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
                             (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.ankunft == ci_date) & (Res_line.zinr == zimmer.zinr)).first()

                    if res_line:

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
                        output_list = Output_list()
                        output_list_list.append(output_list)

                        output_list.resnr = res_line.resnr
                        output_list.reslinnr = res_line.reslinnr
                        output_list.ankunft = res_line.ankunft
                        output_list.abreise = res_line.abreise
                        output_list.active_flag = res_line.active_flag
                        output_list.norms = res_line.zimmeranz
                        output_list.pax = res_line.erwachs
                        output_list.rmrate =  to_decimal(res_line.zipreis)
                        output_list.argt = res_line.arrangement

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                        output_list.vip = check_vip_guest()

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

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
                            output_list.inactive = " i"

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

                        if substring(res_line.flight_nr, 6, 4) != ("0000").lower()  and substring(res_line.flight_nr, 6, 4) != " ":
                            output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

            elif zimmer.zistatus <= 2:

                if zimmer.zistatus == 2:

                    res_line = get_cache (Res_line, {"resstatus": [(eq, 8)],"active_flag": [(eq, 2)],"abreise": [(eq, ci_date)],"zinr": [(eq, zimmer.zinr)]})

                    if res_line:
                        output_list.arrtime = to_string(res_line.ankzeit, "HH:MM")
                        output_list.deptime = to_string(res_line.abreisezeit, "HH:MM")

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                        gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                        output_list = query(output_list_list, filters=(lambda output_list: output_list.zinr == res_line.zinr), first=True)

                        if output_list:

                            if guest.karteityp == 0:
                                output_list.gastnrmember = res_line.gastnrmember
                            output_list.rstat = output_list.rstat + " *"

                res_line = db_session.query(Res_line).filter(
                         ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.zinr == zimmer.zinr)).first()

                if res_line:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

                    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

                    output_list = query(output_list_list, filters=(lambda output_list: output_list.zinr == res_line.zinr), first=True)

                    if guest.karteityp == 0:
                        output_list.gastnrmember = res_line.gastnrmember
                    output_list.bemerk = res_line.bemerk

                    if output_list.gname == "":

                        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
                        output_list.vip = check_vip_guest()

                        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

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

                    elif substring(res_line.flight_nr, 6, 4) != ("0000").lower()  and substring(res_line.flight_nr, 6, 4) != " ":
                        output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.zinr == "") & (Res_line.ankunft == ci_date)).order_by(Res_line.zikatnr, Res_line.name).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.resnr = res_line.resnr
            output_list.reslinnr = res_line.reslinnr
            output_list.active_flag = res_line.active_flag
            output_list.ankunft = res_line.ankunft
            output_list.abreise = res_line.abreise
            output_list.norms = res_line.zimmeranz
            output_list.pax = res_line.erwachs
            output_list.rmrate =  to_decimal(res_line.zipreis)
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

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            output_list.vip = check_vip_guest()

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

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

            if substring(res_line.flight_nr, 6, 4) != ("0000").lower()  and substring(res_line.flight_nr, 6, 4) != " ":
                output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 2) & (Res_line.resstatus == 8) & (Res_line.l_zuordnung[inc_value(2)] == 0) & (Res_line.abreise == ci_date)).order_by(Res_line.zikatnr, Res_line.name).all():

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"betriebsnr": [(eq, 2)],"gespstart": [(le, ci_date)],"gespende": [(ge, ci_date)]})
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
            output_list.rmrate =  to_decimal(res_line.zipreis)
            output_list.argt = res_line.arrangement

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            output_list.vip = check_vip_guest()

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

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

            if substring(res_line.flight_nr, 6, 4) != ("0000").lower()  and substring(res_line.flight_nr, 6, 4) != " ":
                output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)

        for output_list in query(output_list_list, filters=(lambda output_list: output_list.gastnrmember > 0)):

            guest = get_cache (Guest, {"gastnr": [(eq, output_list.gastnrmember)]})

            if guest.bemerkung != "":
                output_list.bemerk = guest.bemerkung + chr_unicode(10) + output_list.bemerk
        fill_cashbasis()


    def fill_arrival():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, resbemerk, his_bemerk, count_i, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal casetype, pvilanguage, curr_date, prog_name
        nonlocal gast


        nonlocal output_list, t_history, gast
        nonlocal output_list_list, t_history_list

        i:int = 0
        anz:int = 0
        off_market:bool = False
        output_list_list.clear()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 0) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.ankunft == curr_date)).order_by(Res_line.zikatnr, Res_line.name).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            gast = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.resnr = res_line.resnr
            output_list.reslinnr = res_line.reslinnr
            output_list.active_flag = res_line.active_flag
            output_list.ankunft = res_line.ankunft
            output_list.abreise = res_line.abreise
            output_list.norms = res_line.zimmeranz
            output_list.pax = res_line.erwachs
            output_list.rmrate =  to_decimal(res_line.zipreis)
            output_list.argt = res_line.arrangement

            if guest.karteityp == 0:
                output_list.gastnrmember = res_line.gastnrmember

            if res_line.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                output_list.location = zimmer.code
                output_list.floor = zimmer.etage
                output_list.zinr = zimmer.zinr
                output_list.kbezeich = zimmer.kbezeich
                output_list.zistatus = zimmer.zistatus

                if not zimmer.sleeping:
                    output_list.inactive = " i"

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

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
            output_list.vip = check_vip_guest()

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

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

            if substring(res_line.flight_nr, 6, 4) != ("0000").lower()  and substring(res_line.flight_nr, 6, 4) != " ":
                output_list.arrtime = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)
        fill_cashbasis()


    def fill_cashbasis():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, resbemerk, his_bemerk, count_i, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal casetype, pvilanguage, curr_date, prog_name
        nonlocal gast


        nonlocal output_list, t_history, gast
        nonlocal output_list_list, t_history_list

        rline = None
        Rline =  create_buffer("Rline",Res_line)

        for output_list in query(output_list_list, filters=(lambda output_list: output_list.resnr > 0)):

            rline = get_cache (Res_line, {"resnr": [(eq, output_list.resnr)],"reslinnr": [(eq, output_list.reslinnr)]})

            if rline and to_int(rline.code) != 0:

                queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(rline.code))]})

                if queasy and queasy.logi1:
                    output_list.cashbasis = True


    def check_vip_guest():

        nonlocal def_cotime, pr_opt_str, ci_date, output_list_list, t_history_list, lvcarea, stat_list, vip_nr, resbemerk, his_bemerk, count_i, guest, queasy, htparam, history, zimmer, outorder, res_line, reservation, reslin_queasy, zimkateg, guestseg, segment
        nonlocal casetype, pvilanguage, curr_date, prog_name
        nonlocal gast


        nonlocal output_list, t_history, gast
        nonlocal output_list_list, t_history_list

        c_vip = ""

        def generate_inner_output():
            return (c_vip)


        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == guest.gastnr) & ((Guestseg.segmentcode == vip_nr[0]) | (Guestseg.segmentcode == vip_nr[1]) | (Guestseg.segmentcode == vip_nr[2]) | (Guestseg.segmentcode == vip_nr[3]) | (Guestseg.segmentcode == vip_nr[4]) | (Guestseg.segmentcode == vip_nr[5]) | (Guestseg.segmentcode == vip_nr[6]) | (Guestseg.segmentcode == vip_nr[7]) | (Guestseg.segmentcode == vip_nr[8]) | (Guestseg.segmentcode == vip_nr[9]))).first()

        if guestseg:

            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

            if segment:
                c_vip = segment.bezeich + " "

        return generate_inner_output()


    stat_list[0] = translateExtended ("Vacant Clean Checked", lvcarea, "")
    stat_list[1] = translateExtended ("Vacant Clean Unchecked", lvcarea, "")
    stat_list[2] = translateExtended ("Vacant Dirty", lvcarea, "")
    stat_list[3] = translateExtended ("Expected Departure", lvcarea, "")
    stat_list[4] = translateExtended ("Occupied Dirty", lvcarea, "")
    stat_list[5] = translateExtended ("Occupied Cleaned", lvcarea, "")
    stat_list[6] = translateExtended ("Out-of-Order", lvcarea, "")
    stat_list[7] = translateExtended ("Off-Market", lvcarea, "")
    stat_list[8] = translateExtended ("Do not Disturb", lvcarea, "")
    stat_list[9] = translateExtended ("Out-of-Service", lvcarea, "")
    ci_date = get_output(htpdate(87))
    def_cotime = get_output(htpchar(925))

    queasy = get_cache (Queasy, {"key": [(eq, 140)],"char1": [(eq, prog_name)]})

    if queasy:
        pr_opt_str = queasy.char3

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})
    vip_nr[0] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})
    vip_nr[1] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})
    vip_nr[2] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})
    vip_nr[3] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})
    vip_nr[4] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})
    vip_nr[5] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})
    vip_nr[6] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})
    vip_nr[7] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})
    vip_nr[8] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})
    vip_nr[9] = htparam.finteger

    if casetype == 1:
        fill_list()
    else:
        fill_arrival()

    for output_list in query(output_list_list):
        resbemerk = output_list.bemerk
        resbemerk = replace_str(resbemerk, chr_unicode(10) , "")
        resbemerk = replace_str(resbemerk, chr_unicode(13) , "")
        resbemerk = replace_str(resbemerk, "~n", "")
        resbemerk = replace_str(resbemerk, "\\n", "")
        resbemerk = replace_str(resbemerk, "~r", "")
        resbemerk = replace_str(resbemerk, "~r~n", "")
        resbemerk = replace_str(resbemerk, "&nbsp;", " ")
        resbemerk = replace_str(resbemerk, "</p>", "</p></p>")
        resbemerk = replace_str(resbemerk, "</p>", chr_unicode(13))
        resbemerk = replace_str(resbemerk, "<BR>", chr_unicode(13))
        resbemerk = replace_str(resbemerk, chr_unicode(10) + chr_unicode(13) , "")
        resbemerk = replace_str(resbemerk, chr_unicode(2) , "")
        resbemerk = replace_str(resbemerk, chr_unicode(3) , "")
        resbemerk = replace_str(resbemerk, chr_unicode(4) , "")

        if length(resbemerk) < 3:
            resbemerk = replace_str(resbemerk, chr_unicode(32) , "")

        if length(resbemerk) < 3:
            resbemerk = ""

        if length(resbemerk) == None:
            resbemerk = ""
        for count_i in range(1,31 + 1) :

            if matches(resbemerk,chr_unicode(count_i)):
                resbemerk = replace_str(resbemerk, chr_unicode(count_i) , "")
        for count_i in range(127,255 + 1) :

            if matches(resbemerk,chr_unicode(count_i)):
                resbemerk = replace_str(resbemerk, chr_unicode(count_i) , "")
        output_list.bemerk = resbemerk
        resbemerk = ""

        for history in db_session.query(History).filter(
                 (History.gastnr == output_list.gastnrmember) & (History.abreise <= get_current_date())).order_by(History._recid).all():
            t_history = T_history()
            t_history_list.append(t_history)

            t_history.ankunft = history.ankunft
            t_history.abreise = history.abreise
            t_history.zinr = history.zinr
            t_history.zi_wechsel = history.zi_wechsel
            t_history.gastnr = history.gastnr


            his_bemerk = history.bemerk
            his_bemerk = replace_str(his_bemerk, chr_unicode(10) , "")
            his_bemerk = replace_str(his_bemerk, chr_unicode(13) , "")
            his_bemerk = replace_str(his_bemerk, "~n", "")
            his_bemerk = replace_str(his_bemerk, "\\n", "")
            his_bemerk = replace_str(his_bemerk, "~r", "")
            his_bemerk = replace_str(his_bemerk, "~r~n", "")
            his_bemerk = replace_str(his_bemerk, "&nbsp;", " ")
            his_bemerk = replace_str(his_bemerk, "</p>", "</p></p>")
            his_bemerk = replace_str(his_bemerk, "</p>", chr_unicode(13))
            his_bemerk = replace_str(his_bemerk, "<BR>", chr_unicode(13))
            his_bemerk = replace_str(his_bemerk, chr_unicode(10) + chr_unicode(13) , "")
            his_bemerk = replace_str(his_bemerk, chr_unicode(2) , "")
            his_bemerk = replace_str(his_bemerk, chr_unicode(3) , "")
            his_bemerk = replace_str(his_bemerk, chr_unicode(4) , "")

            if length(his_bemerk) < 3:
                his_bemerk = replace_str(his_bemerk, chr_unicode(32) , "")

            if length(his_bemerk) < 3:
                his_bemerk = ""

            if length(his_bemerk) == None:
                his_bemerk = ""
            t_history.bemerk = his_bemerk
            his_bemerk = ""

    return generate_output()