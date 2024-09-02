from functions.additional_functions import *
import decimal
from datetime import date
from functions.create_forecast_history_1bl import create_forecast_history_1bl
import re
from models import Nation, Sourccod, Segment

def cr_fproduct_1bl(pvilanguage:int, op_type:int, printer_nr:int, call_from:int, txt_file:str, fr_date:date, to_date:date, disptype:int, cardtype:int, stattype:int, rev_calc:int, exc_oral6pm:bool, excl_comp:bool, vhp_limited:bool, scin:bool):
    output_list1_list = []
    output_list2_list = []
    lvcarea:str = "rm_fproduct"
    report_title:str = ""
    tot_room:int = 0
    tot_pax:int = 0
    tot_logis:decimal = 0
    tot_bfast:decimal = 0
    tot_lunch:decimal = 0
    tot_dinner:decimal = 0
    tot_misc:decimal = 0
    tot_rmonly:decimal = 0
    tot_zipreis:decimal = 0
    tot_fcost:decimal = 0
    nation = sourccod = segment = None

    output_list2 = output_list1 = t_list = to_list = tot_list = None

    output_list2_list, Output_list2 = create_model("Output_list2", {"flag":int, "firmen_nr":int, "refno":str, "avrg_amount":str, "name":str, "str2":str, "str4":str, "fcost":str, "name1":str, "zinr":str, "pax":str, "exp_rev":str, "curr":str, "loc_curr":str, "lodg":str, "bfast":str, "lunch":str, "dinner":str, "oth_rev":str})
    output_list1_list, Output_list1 = create_model_like(Output_list2)
    t_list_list, T_list = create_model("T_list", {"resnr":int, "reslinnr":int, "logis_guaranteed":decimal, "bfast_guaranteed":decimal, "lunch_guaranteed":decimal, "dinner_guaranteed":decimal, "misc_guaranteed":decimal, "pax_guaranteed":int, "room_guaranteed":int, "logis_tentative":decimal, "bfast_tentative":decimal, "lunch_tentative":decimal, "dinner_tentative":decimal, "misc_tentative":decimal, "pax_tentative":int, "room_tentative":int, "rsv_karteityp":int, "rsv_name":str, "rsv_nationnr":int, "guest_karteityp":int, "guest_name":str, "guest_nationnr":int, "sob":int, "resstatus":int, "currency":str, "zipreis":decimal, "flag_history":bool, "firmen_nr":int, "steuernr":str, "segmentcode":int, "segmentbez":str, "fcost":decimal})
    to_list_list, To_list = create_model("To_list", {"nationnr":int, "sob":int, "resnr":int, "gastnr":int, "firmen_nr":int, "refno":str, "name":str, "room":int, "pax":int, "zipreis":decimal, "curr":str, "logis":decimal, "rmonly":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "proz":decimal, "avrgrate":decimal, "guest_nationnr":int, "segmentcode":int, "segmentbez":str, "fcost":decimal})
    tot_list_list, Tot_list = create_model("Tot_list", {"curr":str, "zipreis":decimal, "room":int, "pax":int, "logis":decimal, "rmonly":decimal, "bfast":decimal, "lunch":decimal, "dinner":decimal, "misc":decimal, "proz":decimal, "fcost":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list1_list, output_list2_list, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_list, output_list1_list, t_list_list, to_list_list, tot_list_list
        return {"output-list1": output_list1_list, "output-list2": output_list2_list}

    def query_to_list():

        nonlocal output_list1_list, output_list2_list, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_list, output_list1_list, t_list_list, to_list_list, tot_list_list


        to_list_list.clear()

        t_list = query(t_list_list, filters=(lambda t_list :t_list.flag_history), first=True)

        if t_list:

            if disptype == 1 and cardtype != 3:

                if stattype == 0:

                    for t_list in query(t_list_list, filters=(lambda t_list :t_list.flag_history and t_list.rsv_karteityp == cardtype)):
                        create_to_list1()


                elif stattype == 1:

                    for t_list in query(t_list_list, filters=(lambda t_list :t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus != 3)):
                        create_to_list1()


                elif stattype == 3:

                    for t_list in query(t_list_list, filters=(lambda t_list :t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus == 3)):
                        create_to_list1()

            else:

                if stattype == 0:

                    for t_list in query(t_list_list, filters=(lambda t_list :t_list.flag_history)):
                        create_to_list2()


                elif stattype == 1:

                    for t_list in query(t_list_list, filters=(lambda t_list :t_list.flag_history and t_list.resstatus != 3)):
                        create_to_list2()


                elif stattype == 3:

                    for t_list in query(t_list_list, filters=(lambda t_list :t_list.flag_history and t_list.resstatus == 3)):
                        create_to_list2()


        if disptype == 1 and cardtype != 3:

            if stattype == 0:

                for t_list in query(t_list_list, filters=(lambda t_list :not t_list.flag_history and t_list.rsv_karteityp == cardtype)):
                    create_to_list1()


            elif stattype == 1:

                for t_list in query(t_list_list, filters=(lambda t_list :not t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus != 3)):
                    create_to_list1()


            elif stattype == 3:

                for t_list in query(t_list_list, filters=(lambda t_list :not t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus == 3)):
                    create_to_list1()

        else:

            if stattype == 0:

                for t_list in query(t_list_list, filters=(lambda t_list :not t_list.flag_history)):
                    create_to_list2()


            elif stattype == 1:

                for t_list in query(t_list_list, filters=(lambda t_list :not t_list.flag_history and t_list.resstatus != 3)):
                    create_to_list2()


            elif stattype == 3:

                for t_list in query(t_list_list, filters=(lambda t_list :not t_list.flag_history and t_list.resstatus == 3)):
                    create_to_list2()


    def create_to_list1():

        nonlocal output_list1_list, output_list2_list, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_list, output_list1_list, t_list_list, to_list_list, tot_list_list

        to_list = query(to_list_list, filters=(lambda to_list :to_list.name == t_list.rsv_name and to_list.curr == t_list.currency), first=True)

        if not to_list:
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.firmen_nr = t_list.firmen_nr
            to_list.refNo = t_list.steuernr
            to_list.name = t_list.rsv_name
            to_list.curr = t_list.currency
            to_list.resnr = t_list.resnr


        assign_to_list()

    def create_to_list2():

        nonlocal output_list1_list, output_list2_list, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_list, output_list1_list, t_list_list, to_list_list, tot_list_list

        if disptype == 1:

            to_list = query(to_list_list, filters=(lambda to_list :to_list.name == t_list.rsv_name and to_list.curr == t_list.currency), first=True)

        elif disptype == 2:

            to_list = query(to_list_list, filters=(lambda to_list :to_list.guest_nationnr == t_list.guest_nationnr and to_list.curr == t_list.currency), first=True)

        elif disptype == 3:

            to_list = query(to_list_list, filters=(lambda to_list :to_list.sob == t_list.sob and to_list.curr == t_list.currency), first=True)

        elif disptype == 4:

            to_list = query(to_list_list, filters=(lambda to_list :to_list.segmentcode == t_list.segmentcode and to_list.curr == t_list.currency), first=True)

        if not to_list:
            to_list = To_list()
            to_list_list.append(to_list)

            to_list.name = t_list.rsv_name
            to_list.nationnr = t_list.rsv_nationnr
            to_list.sob = t_list.sob
            to_list.curr = t_list.currency
            to_list.firmen_nr = t_list.firmen_nr
            to_list.refNo = t_list.steuernr
            to_list.resnr = t_list.resnr
            to_list.guest_nationnr = t_list.guest_nationnr
            to_list.segmentcode = t_list.segmentcode

            if disptype == 2:

                if t_list.guest_nationnr != 999:

                    nation = db_session.query(Nation).filter(
                            (Nationnr == t_list.guest_nationnr)).first()

                    if re.match(";",nation.bezeich):
                        to_list.name = entry(0, nation.bezeich, ";")


                    else:
                        to_list.name = nation.bezeich


                else:
                    to_list.name = "UNKNOWN"

            elif disptype == 3:

                if t_list.sob != 999:

                    sourccod = db_session.query(Sourccod).filter(
                            (Sourccod.source_code == t_list.sob)).first()
                    to_list.name = sourccod.bezeich


                else:
                    to_list.name = "UNKNOWN"

            elif disptype == 4:

                if t_list.segmentcode > 0:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == t_list.segmentcode)).first()

                    if segment:
                        to_list.name = segment.bezeich


                    else:
                        to_list.name = "UNKNOWN"


                else:
                    to_list.name = "UNKNOWN"


        assign_to_list()

    def assign_to_list():

        nonlocal output_list1_list, output_list2_list, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_list, output_list1_list, t_list_list, to_list_list, tot_list_list

        if not t_list.flag_history:

            if stattype == 1:

                if t_list.resstatus != 3:
                    to_list.bfast = to_list.bfast + t_list.bfast_guaranteed
                    to_list.lunch = to_list.lunch + t_list.lunch_guaranteed
                    to_list.dinner = to_list.dinner + t_list.dinner_guaranteed
                    to_list.misc = to_list.misc + t_list.misc_guaranteed
                    to_list.room = to_list.room + t_list.room_guaranteed
                    to_list.pax = to_list.pax + t_list.pax_guaranteed
                    to_list.rmonly = to_list.rmonly + t_list.logis_guaranteed
                    to_list.logis = to_list.logis + t_list.logis_guaranteed + t_list.bfast_guaranteed + t_list.lunch_guaranteed +\
                            t_list.dinner_guaranteed + t_list.misc_guaranteed
                    to_list.zipreis = to_list.zipreis + t_list.zipreis
                    to_list.fcost = to_list.fcost + t_list.fcost

            elif stattype == 3:

                if t_list.resstatus == 3:
                    to_list.bfast = to_list.bfast + t_list.bfast_tentative
                    to_list.lunch = to_list.lunch + t_list.lunch_tentative
                    to_list.dinner = to_list.dinner + t_list.dinner_tentative
                    to_list.misc = to_list.misc + t_list.misc_tentative
                    to_list.room = to_list.room + t_list.room_tentative
                    to_list.pax = to_list.pax + t_list.pax_tentative
                    to_list.rmonly = to_list.rmonly + t_list.logis_tentative
                    to_list.logis = to_list.logis + t_list.logis_tentative + t_list.bfast_tentative + t_list.lunch_tentative +\
                            t_list.dinner_tentative + t_list.misc_tentative
                    to_list.zipreis = to_list.zipreis + t_list.zipreis
                    to_list.fcost = to_list.fcost + t_list.fcost

            elif stattype == 0:
                to_list.bfast = to_list.bfast + t_list.bfast_guaranteed + t_list.bfast_tentative
                to_list.lunch = to_list.lunch + t_list.lunch_guaranteed + t_list.lunch_tentative
                to_list.dinner = to_list.dinner + t_list.dinner_guaranteed + t_list.dinner_tentative
                to_list.misc = to_list.misc + t_list.misc_guaranteed + t_list.misc_tentative
                to_list.room = to_list.room + t_list.room_guaranteed + t_list.room_tentative
                to_list.pax = to_list.pax + t_list.pax_guaranteed + t_list.pax_tentative
                to_list.rmonly = to_list.rmonly + t_list.logis_guaranteed + t_list.logis_tentative
                to_list.logis = to_list.logis + t_list.logis_guaranteed + t_list.logis_tentative + t_list.bfast_guaranteed + t_list.bfast_tentative + t_list.lunch_guaranteed +\
                        t_list.lunch_tentative + t_list.dinner_guaranteed + t_list.dinner_tentative + t_list.misc_tentative + t_list.misc_guaranteed
                to_list.zipreis = to_list.zipreis + t_list.zipreis
                to_list.fcost = to_list.fcost + t_list.fcost


        else:
            to_list.bfast = to_list.bfast + t_list.bfast_guaranteed
            to_list.lunch = to_list.lunch + t_list.lunch_guaranteed
            to_list.dinner = to_list.dinner + t_list.dinner_guaranteed
            to_list.misc = to_list.misc + t_list.misc_guaranteed
            to_list.room = to_list.room + t_list.room_guaranteed
            to_list.pax = to_list.pax + t_list.pax_guaranteed
            to_list.rmonly = to_list.rmonly + t_list.logis_guaranteed
            to_list.logis = to_list.logis + t_list.logis_guaranteed + t_list.bfast_guaranteed + t_list.lunch_guaranteed +\
                    t_list.dinner_guaranteed + t_list.misc_guaranteed
            to_list.zipreis = to_list.zipreis + t_list.zipreis
            to_list.fcost = to_list.fcost + t_list.fcost

    def create_tot_list():

        nonlocal output_list1_list, output_list2_list, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_list, output_list1_list, t_list_list, to_list_list, tot_list_list


        tot_list_list.clear()

        for to_list in query(to_list_list):

            tot_list = query(tot_list_list, filters=(lambda tot_list :tot_list.curr == to_list.curr), first=True)

            if not tot_list:
                tot_list = Tot_list()
                tot_list_list.append(tot_list)

                tot_list.curr = to_list.curr


            tot_list.logis = tot_list.logis + to_list.logis
            tot_list.zipreis = tot_list.zipreis + to_list.zipreis
            tot_list.rmonly = tot_list.rmonly + to_list.rmonly
            tot_list.bfast = tot_list.bfast + to_list.bfast
            tot_list.lunch = tot_list.lunch + to_list.lunch
            tot_list.dinner = tot_list.dinner + to_list.dinner
            tot_list.misc = tot_list.misc + to_list.misc
            tot_list.proz = tot_list.proz + to_list.proz
            tot_list.room = tot_list.room + to_list.room
            tot_list.pax = tot_list.pax + to_list.pax
            tot_list.fcost = tot_list.fcost + to_list.fcost
            tot_room = tot_room + to_list.room
            tot_pax = tot_pax + to_list.pax
            tot_logis = tot_logis + to_list.logis
            tot_bfast = tot_bfast + to_list.bfast
            tot_lunch = tot_lunch + to_list.lunch
            tot_dinner = tot_dinner + to_list.dinner
            tot_misc = tot_misc + to_list.misc
            tot_rmonly = tot_rmonly + to_list.rmonly
            tot_zipreis = tot_zipreis + to_list.zipreis
            tot_fcost = tot_fcost + to_list.fcost

    def create_browse():

        nonlocal output_list1_list, output_list2_list, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_list, output_list1_list, t_list_list, to_list_list, tot_list_list


        output_list1_list.clear()
        output_list2_list.clear()

        if rev_calc == 1:

            for to_list in query(to_list_list):
                output_list1 = Output_list1()
                output_list1_list.append(output_list1)

                output_list1.firmen_nr = to_list.firmen_nr
                output_list1.refNo = to_list.refNo
                output_list1.avrg_amount = to_string(to_list.rmonly / to_list.room, "->>>,>>>,>>9.99")
                output_list1.fcost = to_string(to_list.fcost, "->>>,>>>,>>9.99")
                output_list1.name1 = to_string(to_list.name, "x(32)")
                output_list1.zinr = to_string(to_list.room, ">>,>>9")
                output_list1.pax = to_string(to_list.pax, ">>,>>9")
                output_list1.exp_rev = to_string(to_list.zipreis, ">>>,>>>,>>>,>>9.99")
                output_list1.curr = to_string(to_list.curr, "x(4)")
                output_list1.loc_curr = to_string(to_list.logis, ">>>,>>>,>>>,>>9.99")
                output_list1.lodg = to_string(to_list.rmonly, ">>,>>>,>>>,>>9.99")
                output_list1.bfast = to_string(to_list.bfast, ">,>>>,>>>,>>9.99")
                output_list1.lunch = to_string(to_list.lunch, ">,>>>,>>>,>>9.99")
                output_list1.dinner = to_string(to_list.dinner, ">,>>>,>>>,>>9.99")
                output_list1.oth_rev = to_string(to_list.misc, ">,>>>,>>>,>>9.99")


            output_list1 = Output_list1()
            output_list1_list.append(output_list1)

            output_list1.avrg_amount = fill("-", 15)
            output_list1.fcost = fill("-", 15)
            output_list1.name1 = fill("-", 32)
            output_list1.zinr = fill("-", 6)
            output_list1.pax = fill("-", 6)
            output_list1.exp_rev = fill("-", 18)
            output_list1.curr = fill("-", 4)
            output_list1.loc_curr = fill("-", 18)
            output_list1.lodg = fill("-", 17)
            output_list1.bfast = fill("-", 16)
            output_list1.lunch = fill("-", 16)
            output_list1.dinner = fill("-", 16)
            output_list1.oth_rev = fill("-", 16)

            for tot_list in query(tot_list_list):
                output_list1 = Output_list1()
                output_list1_list.append(output_list1)

                output_list1.avrg_amount = to_string(tot_list.rmonly / tot_list.room, "->>>,>>>,>>9.99")
                output_list1.fcost = to_string(tot_list.fcost, "->>>,>>>,>>9.99")
                output_list1.name1 = to_string("T o t a l  " + tot_list.curr, "x(32)")
                output_list1.zinr = to_string(tot_list.room, ">>,>>9")
                output_list1.pax = to_string(tot_list.pax, ">>,>>9")
                output_list1.exp_rev = to_string(tot_list.zipreis, ">>>,>>>,>>>,>>9.99")
                output_list1.curr = "    "
                output_list1.loc_curr = to_string(tot_list.logis, ">>>,>>>,>>>,>>9.99")
                output_list1.lodg = to_string(tot_list.rmonly, ">>,>>>,>>>,>>9.99")
                output_list1.bfast = to_string(tot_list.bfast, ">,>>>,>>>,>>9.99")
                output_list1.lunch = to_string(tot_list.lunch, ">,>>>,>>>,>>9.99")
                output_list1.dinner = to_string(tot_list.dinner, ">,>>>,>>>,>>9.99")
                output_list1.oth_rev = to_string(tot_list.misc, ">,>>>,>>>,>>9.99")


            output_list1 = Output_list1()
            output_list1_list.append(output_list1)

            output_list1.avrg_amount = fill("-", 15)
            output_list1.fcost = fill("-", 15)
            output_list1.name1 = fill("-", 32)
            output_list1.zinr = fill("-", 6)
            output_list1.pax = fill("-", 6)
            output_list1.exp_rev = fill("-", 18)
            output_list1.curr = fill("-", 4)
            output_list1.loc_curr = fill("-", 18)
            output_list1.lodg = fill("-", 17)
            output_list1.bfast = fill("-", 16)
            output_list1.lunch = fill("-", 16)
            output_list1.dinner = fill("-", 16)
            output_list1.oth_rev = fill("-", 16)
            output_list1 = Output_list1()
            output_list1_list.append(output_list1)

            output_list1.avrg_amount = to_string(tot_rmonly / tot_room, "->>>,>>>,>>9.99")
            output_list1.fcost = to_string(tot_fcost, "->>>,>>>,>>9.99")
            output_list1.name1 = to_string("T o t a l", "x(32)")
            output_list1.zinr = to_string(tot_room, ">>,>>9")
            output_list1.pax = to_string(tot_pax, ">>,>>9")
            output_list1.exp_rev = "                  "
            output_list1.curr = "    "
            output_list1.loc_curr = to_string(tot_logis, ">>>,>>>,>>>,>>9.99")
            output_list1.lodg = to_string(tot_rmonly, ">>,>>>,>>>,>>9.99")
            output_list1.bfast = to_string(tot_bfast, ">,>>>,>>>,>>9.99")
            output_list1.lunch = to_string(tot_lunch, ">,>>>,>>>,>>9.99")
            output_list1.dinner = to_string(tot_dinner, ">,>>>,>>>,>>9.99")
            output_list1.oth_rev = to_string(tot_misc, ">,>>>,>>>,>>9.99")


        else:

            for to_list in query(to_list_list):
                output_list2 = Output_list2()
                output_list2_list.append(output_list2)

                output_list2.firmen_nr = to_list.firmen_nr
                output_list2.refNo = to_list.refNo
                output_list2.avrg_amount = to_string(to_list.rmonly / to_list.room, "->>>,>>>,>>9.99")
                output_list2.fcost = to_string(to_list.fcost, "->>>,>>>,>>9.99")
                output_list2.name1 = to_string(to_list.name, "x(32)")
                output_list2.zinr = to_string(to_list.room, ">>,>>9")
                output_list2.pax = to_string(to_list.pax, ">>,>>9")
                output_list2.exp_rev = to_string(to_list.zipreis, ">>>,>>>,>>>,>>9.99")
                output_list2.curr = to_string(to_list.curr, "x(4)")
                output_list2.loc_curr = to_string(to_list.logis, ">>>,>>>,>>>,>>9.99")
                output_list2.lodg = to_string(to_list.rmonly, ">>,>>>,>>>,>>9.99")


            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

            output_list2.avrg_amount = fill("-", 15)
            output_list2.fcost = fill("-", 15)
            output_list2.name1 = fill("-", 32)
            output_list2.zinr = fill("-", 6)
            output_list2.pax = fill("-", 6)
            output_list2.exp_rev = fill("-", 18)
            output_list2.curr = fill("-", 4)
            output_list2.loc_curr = fill("-", 18)
            output_list2.lodg = fill("-", 17)

            for tot_list in query(tot_list_list):
                output_list2 = Output_list2()
                output_list2_list.append(output_list2)

                output_list2.avrg_amount = to_string(tot_list.rmonly / tot_list.room, "->>>,>>>,>>9.99")
                output_list2.fcost = to_string(tot_list.fcost, "->>>,>>>,>>9.99")
                output_list2.name1 = to_string("T o t a l  " + tot_list.curr, "x(32)")
                output_list2.zinr = to_string(tot_list.room, ">>,>>9")
                output_list2.pax = to_string(tot_list.pax, ">>,>>9")
                output_list2.exp_rev = to_string(tot_list.zipreis, ">>>,>>>,>>>,>>9.99")
                output_list2.curr = "    "
                output_list2.loc_curr = to_string(tot_list.logis, ">>>,>>>,>>>,>>9.99")
                output_list2.lodg = to_string(tot_list.rmonly, ">>,>>>,>>>,>>9.99")


            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

            output_list2.avrg_amount = fill("-", 15)
            output_list2.fcost = fill("-", 15)
            output_list2.name1 = fill("-", 32)
            output_list2.zinr = fill("-", 6)
            output_list2.pax = fill("-", 6)
            output_list2.exp_rev = fill("-", 18)
            output_list2.curr = fill("-", 4)
            output_list2.loc_curr = fill("-", 18)
            output_list2.lodg = fill("-", 17)
            output_list2 = Output_list2()
            output_list2_list.append(output_list2)

            output_list2.avrg_amount = to_string(tot_rmonly / tot_room, "->>>,>>>,>>9.99")
            output_list2.fcost = to_string(tot_fcost, "->>>,>>>,>>9.99")
            output_list2.name1 = to_string("T o t a l", "x(32)")
            output_list2.zinr = to_string(tot_room, ">>,>>9")
            output_list2.pax = to_string(tot_pax, ">>,>>9")
            output_list2.exp_rev = "                  "
            output_list2.curr = "    "
            output_list2.loc_curr = to_string(tot_logis, ">>>,>>>,>>>,>>9.99")
            output_list2.lodg = to_string(tot_rmonly, ">>,>>>,>>>,>>9.99")


    t_list_list = get_output(create_forecast_history_1bl(fr_date, to_date, excl_comp, vhp_limited, scin))

    if op_type == 0:
        query_to_list()

        for to_list in query(to_list_list):

            if to_list.room != 0:
                to_list.avrgrate = to_list.logis / to_list.room

            if tot_logis != 0:
                to_list.proz = to_list.logis / tot_logis * 100
        create_tot_list()
        create_browse()

    return generate_output()