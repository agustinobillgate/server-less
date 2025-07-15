#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.create_forecast_history_1bl import create_forecast_history_1bl
from models import Nation, Sourccod, Segment

def cr_fproduct_1bl(pvilanguage:int, op_type:int, printer_nr:int, call_from:int, txt_file:string, fr_date:date, to_date:date, disptype:int, cardtype:int, stattype:int, rev_calc:int, exc_oral6pm:bool, excl_comp:bool, vhp_limited:bool, scin:bool):

    prepare_cache ([Nation, Sourccod, Segment])

    output_list1_data = []
    output_list2_data = []
    lvcarea:string = "rm-fproduct"
    report_title:string = ""
    tot_room:int = 0
    tot_pax:int = 0
    tot_logis:Decimal = to_decimal("0.0")
    tot_bfast:Decimal = to_decimal("0.0")
    tot_lunch:Decimal = to_decimal("0.0")
    tot_dinner:Decimal = to_decimal("0.0")
    tot_misc:Decimal = to_decimal("0.0")
    tot_rmonly:Decimal = to_decimal("0.0")
    tot_zipreis:Decimal = to_decimal("0.0")
    tot_fcost:Decimal = to_decimal("0.0")
    nation = sourccod = segment = None

    output_list2 = output_list1 = t_list = to_list = tot_list = None

    output_list2_data, Output_list2 = create_model("Output_list2", {"flag":int, "firmen_nr":int, "refno":string, "avrg_amount":string, "name":string, "str2":string, "str4":string, "fcost":string, "name1":string, "zinr":string, "pax":string, "exp_rev":string, "curr":string, "loc_curr":string, "lodg":string, "bfast":string, "lunch":string, "dinner":string, "oth_rev":string})
    output_list1_data, Output_list1 = create_model_like(Output_list2)
    t_list_data, T_list = create_model("T_list", {"resnr":int, "reslinnr":int, "logis_guaranteed":Decimal, "bfast_guaranteed":Decimal, "lunch_guaranteed":Decimal, "dinner_guaranteed":Decimal, "misc_guaranteed":Decimal, "pax_guaranteed":int, "room_guaranteed":int, "logis_tentative":Decimal, "bfast_tentative":Decimal, "lunch_tentative":Decimal, "dinner_tentative":Decimal, "misc_tentative":Decimal, "pax_tentative":int, "room_tentative":int, "rsv_karteityp":int, "rsv_name":string, "rsv_nationnr":int, "guest_karteityp":int, "guest_name":string, "guest_nationnr":int, "sob":int, "resstatus":int, "currency":string, "zipreis":Decimal, "flag_history":bool, "firmen_nr":int, "steuernr":string, "segmentcode":int, "segmentbez":string, "fcost":Decimal})
    to_list_data, To_list = create_model("To_list", {"nationnr":int, "sob":int, "resnr":int, "gastnr":int, "firmen_nr":int, "refno":string, "name":string, "room":int, "pax":int, "zipreis":Decimal, "curr":string, "logis":Decimal, "rmonly":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "proz":Decimal, "avrgrate":Decimal, "guest_nationnr":int, "segmentcode":int, "segmentbez":string, "fcost":Decimal})
    tot_list_data, Tot_list = create_model("Tot_list", {"curr":string, "zipreis":Decimal, "room":int, "pax":int, "logis":Decimal, "rmonly":Decimal, "bfast":Decimal, "lunch":Decimal, "dinner":Decimal, "misc":Decimal, "proz":Decimal, "fcost":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list1_data, output_list2_data, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, fr_date, to_date, disptype, cardtype, stattype, rev_calc, exc_oral6pm, excl_comp, vhp_limited, scin


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_data, output_list1_data, t_list_data, to_list_data, tot_list_data

        return {"output-list1": output_list1_data, "output-list2": output_list2_data}

    def query_to_list():

        nonlocal output_list1_data, output_list2_data, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, fr_date, to_date, disptype, cardtype, stattype, rev_calc, exc_oral6pm, excl_comp, vhp_limited, scin


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_data, output_list1_data, t_list_data, to_list_data, tot_list_data


        to_list_data.clear()

        t_list = query(t_list_data, filters=(lambda t_list: t_list.flag_history), first=True)

        if t_list:

            if disptype == 1 and cardtype != 3:

                if stattype == 0:

                    for t_list in query(t_list_data, filters=(lambda t_list: t_list.flag_history and t_list.rsv_karteityp == cardtype), sort_by=[("rsv_name",False)]):
                        create_to_list1()


                elif stattype == 1:

                    for t_list in query(t_list_data, filters=(lambda t_list: t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus != 3), sort_by=[("rsv_name",False)]):
                        create_to_list1()


                elif stattype == 3:

                    for t_list in query(t_list_data, filters=(lambda t_list: t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus == 3), sort_by=[("rsv_name",False)]):
                        create_to_list1()

            else:

                if stattype == 0:

                    for t_list in query(t_list_data, filters=(lambda t_list: t_list.flag_history), sort_by=[("rsv_name",False)]):
                        create_to_list2()


                elif stattype == 1:

                    for t_list in query(t_list_data, filters=(lambda t_list: t_list.flag_history and t_list.resstatus != 3), sort_by=[("rsv_name",False)]):
                        create_to_list2()


                elif stattype == 3:

                    for t_list in query(t_list_data, filters=(lambda t_list: t_list.flag_history and t_list.resstatus == 3), sort_by=[("rsv_name",False)]):
                        create_to_list2()


        if disptype == 1 and cardtype != 3:

            if stattype == 0:

                for t_list in query(t_list_data, filters=(lambda t_list: not t_list.flag_history and t_list.rsv_karteityp == cardtype), sort_by=[("rsv_name",False)]):
                    create_to_list1()


            elif stattype == 1:

                for t_list in query(t_list_data, filters=(lambda t_list: not t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus != 3), sort_by=[("rsv_name",False)]):
                    create_to_list1()


            elif stattype == 3:

                for t_list in query(t_list_data, filters=(lambda t_list: not t_list.flag_history and t_list.rsv_karteityp == cardtype and t_list.resstatus == 3), sort_by=[("rsv_name",False)]):
                    create_to_list1()

        else:

            if stattype == 0:

                for t_list in query(t_list_data, filters=(lambda t_list: not t_list.flag_history), sort_by=[("rsv_name",False)]):
                    create_to_list2()


            elif stattype == 1:

                for t_list in query(t_list_data, filters=(lambda t_list: not t_list.flag_history and t_list.resstatus != 3), sort_by=[("rsv_name",False)]):
                    create_to_list2()


            elif stattype == 3:

                for t_list in query(t_list_data, filters=(lambda t_list: not t_list.flag_history and t_list.resstatus == 3), sort_by=[("rsv_name",False)]):
                    create_to_list2()

    def create_to_list1():

        nonlocal output_list1_data, output_list2_data, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, fr_date, to_date, disptype, cardtype, stattype, rev_calc, exc_oral6pm, excl_comp, vhp_limited, scin


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_data, output_list1_data, t_list_data, to_list_data, tot_list_data

        to_list = query(to_list_data, filters=(lambda to_list: to_list.name == t_list.rsv_name and to_list.curr == t_list.currency), first=True)

        if not to_list:
            to_list = To_list()
            to_list_data.append(to_list)

            to_list.firmen_nr = t_list.firmen_nr
            to_list.refno = t_list.steuernr
            to_list.name = t_list.rsv_name
            to_list.curr = t_list.currency
            to_list.resnr = t_list.resnr


        assign_to_list()


    def create_to_list2():

        nonlocal output_list1_data, output_list2_data, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, fr_date, to_date, disptype, cardtype, stattype, rev_calc, exc_oral6pm, excl_comp, vhp_limited, scin


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_data, output_list1_data, t_list_data, to_list_data, tot_list_data

        if disptype == 1:

            to_list = query(to_list_data, filters=(lambda to_list: to_list.name == t_list.rsv_name and to_list.curr == t_list.currency), first=True)

        elif disptype == 2:

            to_list = query(to_list_data, filters=(lambda to_list: to_list.guest_nationnr == t_list.guest_nationnr and to_list.curr == t_list.currency), first=True)

        elif disptype == 3:

            to_list = query(to_list_data, filters=(lambda to_list: to_list.sob == t_list.sob and to_list.curr == t_list.currency), first=True)

        elif disptype == 4:

            to_list = query(to_list_data, filters=(lambda to_list: to_list.segmentcode == t_list.segmentcode and to_list.curr == t_list.currency), first=True)

        if not to_list:
            to_list = To_list()
            to_list_data.append(to_list)

            to_list.name = t_list.rsv_name
            to_list.nationnr = t_list.rsv_nationnr
            to_list.sob = t_list.sob
            to_list.curr = t_list.currency
            to_list.firmen_nr = t_list.firmen_nr
            to_list.refno = t_list.steuernr
            to_list.resnr = t_list.resnr
            to_list.guest_nationnr = t_list.guest_nationnr
            to_list.segmentcode = t_list.segmentcode

            if disptype == 2:

                if t_list.guest_nationnr != 999:

                    nation = get_cache (Nation, {"nationnr": [(eq, t_list.guest_nationnr)]})

                    if matches(nation.bezeich,r";"):
                        to_list.name = entry(0, nation.bezeich, ";")


                    else:
                        to_list.name = nation.bezeich


                else:
                    to_list.name = "UNKNOWN"

            elif disptype == 3:

                if t_list.sob != 999:

                    sourccod = get_cache (Sourccod, {"source_code": [(eq, t_list.sob)]})
                    to_list.name = sourccod.bezeich


                else:
                    to_list.name = "UNKNOWN"

            elif disptype == 4:

                if t_list.segmentcode > 0:

                    segment = get_cache (Segment, {"segmentcode": [(eq, t_list.segmentcode)]})

                    if segment:
                        to_list.name = segment.bezeich


                    else:
                        to_list.name = "UNKNOWN"


                else:
                    to_list.name = "UNKNOWN"


        assign_to_list()


    def assign_to_list():

        nonlocal output_list1_data, output_list2_data, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, fr_date, to_date, disptype, cardtype, stattype, rev_calc, exc_oral6pm, excl_comp, vhp_limited, scin


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_data, output_list1_data, t_list_data, to_list_data, tot_list_data

        if not t_list.flag_history:

            if stattype == 1:

                if t_list.resstatus != 3:
                    to_list.bfast =  to_decimal(to_list.bfast) + to_decimal(t_list.bfast_guaranteed)
                    to_list.lunch =  to_decimal(to_list.lunch) + to_decimal(t_list.lunch_guaranteed)
                    to_list.dinner =  to_decimal(to_list.dinner) + to_decimal(t_list.dinner_guaranteed)
                    to_list.misc =  to_decimal(to_list.misc) + to_decimal(t_list.misc_guaranteed)
                    to_list.room = to_list.room + t_list.room_guaranteed
                    to_list.pax = to_list.pax + t_list.pax_guaranteed
                    to_list.rmonly =  to_decimal(to_list.rmonly) + to_decimal(t_list.logis_guaranteed)
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(t_list.logis_guaranteed) + to_decimal(t_list.bfast_guaranteed) + to_decimal(t_list.lunch_guaranteed) +\
                            t_list.dinner_guaranteed + to_decimal(t_list.misc_guaranteed)
                    to_list.zipreis =  to_decimal(to_list.zipreis) + to_decimal(t_list.zipreis)
                    to_list.fcost =  to_decimal(to_list.fcost) + to_decimal(t_list.fcost)

            elif stattype == 3:

                if t_list.resstatus == 3:
                    to_list.bfast =  to_decimal(to_list.bfast) + to_decimal(t_list.bfast_tentative)
                    to_list.lunch =  to_decimal(to_list.lunch) + to_decimal(t_list.lunch_tentative)
                    to_list.dinner =  to_decimal(to_list.dinner) + to_decimal(t_list.dinner_tentative)
                    to_list.misc =  to_decimal(to_list.misc) + to_decimal(t_list.misc_tentative)
                    to_list.room = to_list.room + t_list.room_tentative
                    to_list.pax = to_list.pax + t_list.pax_tentative
                    to_list.rmonly =  to_decimal(to_list.rmonly) + to_decimal(t_list.logis_tentative)
                    to_list.logis =  to_decimal(to_list.logis) + to_decimal(t_list.logis_tentative) + to_decimal(t_list.bfast_tentative) + to_decimal(t_list.lunch_tentative) +\
                            t_list.dinner_tentative + to_decimal(t_list.misc_tentative)
                    to_list.zipreis =  to_decimal(to_list.zipreis) + to_decimal(t_list.zipreis)
                    to_list.fcost =  to_decimal(to_list.fcost) + to_decimal(t_list.fcost)

            elif stattype == 0:
                to_list.bfast =  to_decimal(to_list.bfast) + to_decimal(t_list.bfast_guaranteed) + to_decimal(t_list.bfast_tentative)
                to_list.lunch =  to_decimal(to_list.lunch) + to_decimal(t_list.lunch_guaranteed) + to_decimal(t_list.lunch_tentative)
                to_list.dinner =  to_decimal(to_list.dinner) + to_decimal(t_list.dinner_guaranteed) + to_decimal(t_list.dinner_tentative)
                to_list.misc =  to_decimal(to_list.misc) + to_decimal(t_list.misc_guaranteed) + to_decimal(t_list.misc_tentative)
                to_list.room = to_list.room + t_list.room_guaranteed + t_list.room_tentative
                to_list.pax = to_list.pax + t_list.pax_guaranteed + t_list.pax_tentative
                to_list.rmonly =  to_decimal(to_list.rmonly) + to_decimal(t_list.logis_guaranteed) + to_decimal(t_list.logis_tentative)
                to_list.logis =  to_decimal(to_list.logis) + to_decimal(t_list.logis_guaranteed) + to_decimal(t_list.logis_tentative) + to_decimal(t_list.bfast_guaranteed) + to_decimal(t_list.bfast_tentative) + to_decimal(t_list.lunch_guaranteed) +\
                        t_list.lunch_tentative + to_decimal(t_list.dinner_guaranteed) + to_decimal(t_list.dinner_tentative) + to_decimal(t_list.misc_tentative) + to_decimal(t_list.misc_guaranteed)
                to_list.zipreis =  to_decimal(to_list.zipreis) + to_decimal(t_list.zipreis)
                to_list.fcost =  to_decimal(to_list.fcost) + to_decimal(t_list.fcost)


        else:
            to_list.bfast =  to_decimal(to_list.bfast) + to_decimal(t_list.bfast_guaranteed)
            to_list.lunch =  to_decimal(to_list.lunch) + to_decimal(t_list.lunch_guaranteed)
            to_list.dinner =  to_decimal(to_list.dinner) + to_decimal(t_list.dinner_guaranteed)
            to_list.misc =  to_decimal(to_list.misc) + to_decimal(t_list.misc_guaranteed)
            to_list.room = to_list.room + t_list.room_guaranteed
            to_list.pax = to_list.pax + t_list.pax_guaranteed
            to_list.rmonly =  to_decimal(to_list.rmonly) + to_decimal(t_list.logis_guaranteed)
            to_list.logis =  to_decimal(to_list.logis) + to_decimal(t_list.logis_guaranteed) + to_decimal(t_list.bfast_guaranteed) + to_decimal(t_list.lunch_guaranteed) +\
                    t_list.dinner_guaranteed + to_decimal(t_list.misc_guaranteed)
            to_list.zipreis =  to_decimal(to_list.zipreis) + to_decimal(t_list.zipreis)
            to_list.fcost =  to_decimal(to_list.fcost) + to_decimal(t_list.fcost)


    def create_tot_list():

        nonlocal output_list1_data, output_list2_data, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, fr_date, to_date, disptype, cardtype, stattype, rev_calc, exc_oral6pm, excl_comp, vhp_limited, scin


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_data, output_list1_data, t_list_data, to_list_data, tot_list_data


        tot_list_data.clear()

        for to_list in query(to_list_data):

            tot_list = query(tot_list_data, filters=(lambda tot_list: tot_list.curr == to_list.curr), first=True)

            if not tot_list:
                tot_list = Tot_list()
                tot_list_data.append(tot_list)

                tot_list.curr = to_list.curr


            tot_list.logis =  to_decimal(tot_list.logis) + to_decimal(to_list.logis)
            tot_list.zipreis =  to_decimal(tot_list.zipreis) + to_decimal(to_list.zipreis)
            tot_list.rmonly =  to_decimal(tot_list.rmonly) + to_decimal(to_list.rmonly)
            tot_list.bfast =  to_decimal(tot_list.bfast) + to_decimal(to_list.bfast)
            tot_list.lunch =  to_decimal(tot_list.lunch) + to_decimal(to_list.lunch)
            tot_list.dinner =  to_decimal(tot_list.dinner) + to_decimal(to_list.dinner)
            tot_list.misc =  to_decimal(tot_list.misc) + to_decimal(to_list.misc)
            tot_list.proz =  to_decimal(tot_list.proz) + to_decimal(to_list.proz)
            tot_list.room = tot_list.room + to_list.room
            tot_list.pax = tot_list.pax + to_list.pax
            tot_list.fcost =  to_decimal(tot_list.fcost) + to_decimal(to_list.fcost)
            tot_room = tot_room + to_list.room
            tot_pax = tot_pax + to_list.pax
            tot_logis =  to_decimal(tot_logis) + to_decimal(to_list.logis)
            tot_bfast =  to_decimal(tot_bfast) + to_decimal(to_list.bfast)
            tot_lunch =  to_decimal(tot_lunch) + to_decimal(to_list.lunch)
            tot_dinner =  to_decimal(tot_dinner) + to_decimal(to_list.dinner)
            tot_misc =  to_decimal(tot_misc) + to_decimal(to_list.misc)
            tot_rmonly =  to_decimal(tot_rmonly) + to_decimal(to_list.rmonly)
            tot_zipreis =  to_decimal(tot_zipreis) + to_decimal(to_list.zipreis)
            tot_fcost =  to_decimal(tot_fcost) + to_decimal(to_list.fcost)


    def create_browse():

        nonlocal output_list1_data, output_list2_data, lvcarea, report_title, tot_room, tot_pax, tot_logis, tot_bfast, tot_lunch, tot_dinner, tot_misc, tot_rmonly, tot_zipreis, tot_fcost, nation, sourccod, segment
        nonlocal pvilanguage, op_type, printer_nr, call_from, txt_file, fr_date, to_date, disptype, cardtype, stattype, rev_calc, exc_oral6pm, excl_comp, vhp_limited, scin


        nonlocal output_list2, output_list1, t_list, to_list, tot_list
        nonlocal output_list2_data, output_list1_data, t_list_data, to_list_data, tot_list_data


        output_list1_data.clear()
        output_list2_data.clear()

        if rev_calc == 1:

            for to_list in query(to_list_data):
                output_list1 = Output_list1()
                output_list1_data.append(output_list1)

                output_list1.firmen_nr = to_list.firmen_nr
                output_list1.refno = to_list.refNo
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
            output_list1_data.append(output_list1)

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

            for tot_list in query(tot_list_data, sort_by=[("curr",False)]):
                output_list1 = Output_list1()
                output_list1_data.append(output_list1)

                output_list1.avrg_amount = to_string(tot_list.rmonly / tot_list.room, "->>>,>>>,>>9.99")
                output_list1.fcost = to_string(tot_list.fcost, "->>>,>>>,>>9.99")
                output_list1.name1 = to_string("T o t a l " + tot_list.curr, "x(32)")
                output_list1.zinr = to_string(tot_list.room, ">>,>>9")
                output_list1.pax = to_string(tot_list.pax, ">>,>>9")
                output_list1.exp_rev = to_string(tot_list.zipreis, ">>>,>>>,>>>,>>9.99")
                output_list1.curr = " "
                output_list1.loc_curr = to_string(tot_list.logis, ">>>,>>>,>>>,>>9.99")
                output_list1.lodg = to_string(tot_list.rmonly, ">>,>>>,>>>,>>9.99")
                output_list1.bfast = to_string(tot_list.bfast, ">,>>>,>>>,>>9.99")
                output_list1.lunch = to_string(tot_list.lunch, ">,>>>,>>>,>>9.99")
                output_list1.dinner = to_string(tot_list.dinner, ">,>>>,>>>,>>9.99")
                output_list1.oth_rev = to_string(tot_list.misc, ">,>>>,>>>,>>9.99")


            output_list1 = Output_list1()
            output_list1_data.append(output_list1)

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
            output_list1_data.append(output_list1)

            output_list1.avrg_amount = to_string(tot_rmonly / tot_room, "->>>,>>>,>>9.99")
            output_list1.fcost = to_string(tot_fcost, "->>>,>>>,>>9.99")
            output_list1.name1 = to_string("T o t a l", "x(32)")
            output_list1.zinr = to_string(tot_room, ">>,>>9")
            output_list1.pax = to_string(tot_pax, ">>,>>9")
            output_list1.exp_rev = " "
            output_list1.curr = " "
            output_list1.loc_curr = to_string(tot_logis, ">>>,>>>,>>>,>>9.99")
            output_list1.lodg = to_string(tot_rmonly, ">>,>>>,>>>,>>9.99")
            output_list1.bfast = to_string(tot_bfast, ">,>>>,>>>,>>9.99")
            output_list1.lunch = to_string(tot_lunch, ">,>>>,>>>,>>9.99")
            output_list1.dinner = to_string(tot_dinner, ">,>>>,>>>,>>9.99")
            output_list1.oth_rev = to_string(tot_misc, ">,>>>,>>>,>>9.99")


        else:

            for to_list in query(to_list_data):
                output_list2 = Output_list2()
                output_list2_data.append(output_list2)

                output_list2.firmen_nr = to_list.firmen_nr
                output_list2.refno = to_list.refNo
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
            output_list2_data.append(output_list2)

            output_list2.avrg_amount = fill("-", 15)
            output_list2.fcost = fill("-", 15)
            output_list2.name1 = fill("-", 32)
            output_list2.zinr = fill("-", 6)
            output_list2.pax = fill("-", 6)
            output_list2.exp_rev = fill("-", 18)
            output_list2.curr = fill("-", 4)
            output_list2.loc_curr = fill("-", 18)
            output_list2.lodg = fill("-", 17)

            for tot_list in query(tot_list_data, sort_by=[("curr",False)]):
                output_list2 = Output_list2()
                output_list2_data.append(output_list2)

                output_list2.avrg_amount = to_string(tot_list.rmonly / tot_list.room, "->>>,>>>,>>9.99")
                output_list2.fcost = to_string(tot_list.fcost, "->>>,>>>,>>9.99")
                output_list2.name1 = to_string("T o t a l " + tot_list.curr, "x(32)")
                output_list2.zinr = to_string(tot_list.room, ">>,>>9")
                output_list2.pax = to_string(tot_list.pax, ">>,>>9")
                output_list2.exp_rev = to_string(tot_list.zipreis, ">>>,>>>,>>>,>>9.99")
                output_list2.curr = " "
                output_list2.loc_curr = to_string(tot_list.logis, ">>>,>>>,>>>,>>9.99")
                output_list2.lodg = to_string(tot_list.rmonly, ">>,>>>,>>>,>>9.99")


            output_list2 = Output_list2()
            output_list2_data.append(output_list2)

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
            output_list2_data.append(output_list2)

            output_list2.avrg_amount = to_string(tot_rmonly / tot_room, "->>>,>>>,>>9.99")
            output_list2.fcost = to_string(tot_fcost, "->>>,>>>,>>9.99")
            output_list2.name1 = to_string("T o t a l", "x(32)")
            output_list2.zinr = to_string(tot_room, ">>,>>9")
            output_list2.pax = to_string(tot_pax, ">>,>>9")
            output_list2.exp_rev = " "
            output_list2.curr = " "
            output_list2.loc_curr = to_string(tot_logis, ">>>,>>>,>>>,>>9.99")
            output_list2.lodg = to_string(tot_rmonly, ">>,>>>,>>>,>>9.99")

    t_list_data = get_output(create_forecast_history_1bl(fr_date, to_date, excl_comp, vhp_limited, scin))

    if op_type == 0:
        query_to_list()

        for to_list in query(to_list_data):

            if to_list.room != 0:
                to_list.avrgrate =  to_decimal(to_list.logis) / to_decimal(to_list.room)

            if tot_logis != 0:
                to_list.proz =  to_decimal(to_list.logis) / to_decimal(tot_logis) * to_decimal("100")
        create_tot_list()
        create_browse()

    return generate_output()