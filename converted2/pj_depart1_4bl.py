#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Reservation, Res_line, History, Guestseg, Reslin_queasy, Nation, Bill, Mc_guest, Mc_types

setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})
zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

def pj_depart1_4bl(pvilanguage:int, case_type:int, disptype:int, fdate:date, tdate:date, froom:string, troom:string, disp_accompany:bool, setup_list_data:[Setup_list], zikat_list_data:[Zikat_list]):

    prepare_cache ([Guest, Reservation, Res_line, Reslin_queasy, Nation, Bill, Mc_guest, Mc_types])

    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    str_list_data = []
    s_list_data = []
    cl_list_data = []
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    all_remark:string = ""
    curr_zinr:string = ""
    lvcarea:string = "PJ-depart"
    guest = reservation = res_line = history = guestseg = reslin_queasy = nation = bill = mc_guest = mc_types = None

    str_list = s_list = cl_list = setup_list = zikat_list = None

    str_list_data, Str_list = create_model("Str_list", {"flag":int, "line1":string, "line2":string, "address":string})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":string, "depart":string, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "outstand":Decimal, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "email":string, "email_adr":string, "tot_night":int, "ratecode":string, "full_name":string, "address":string, "memberno":string, "membertype":string, "zipreis":Decimal, "ci_time":string, "co_time":string, "local_reg":string, "spreq":string, "birthd":date, "ktpid":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_data, s_list_data, cl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, all_remark, curr_zinr, lvcarea, guest, reservation, res_line, history, guestseg, reslin_queasy, nation, bill, mc_guest, mc_types
        nonlocal pvilanguage, case_type, disptype, fdate, tdate, froom, troom, disp_accompany


        nonlocal str_list, s_list, cl_list, setup_list, zikat_list
        nonlocal str_list_data, s_list_data, cl_list_data

        return {"tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "str-list": str_list_data, "s-list": s_list_data, "cl-list": cl_list_data}

    def create_departure0():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_data, s_list_data, cl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, all_remark, curr_zinr, lvcarea, guest, reservation, res_line, history, guestseg, reslin_queasy, nation, bill, mc_guest, mc_types
        nonlocal pvilanguage, case_type, disptype, fdate, tdate, froom, troom, disp_accompany


        nonlocal str_list, s_list, cl_list, setup_list, zikat_list
        nonlocal str_list_data, s_list_data, cl_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        gmember = None
        do_it:bool = False
        str:string = ""
        Gmember =  create_buffer("Gmember",Guest)
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()

        if disptype == 1:

            res_line_obj_list = {}
            for res_line, reservation, guest, gmember in db_session.query(Res_line, Reservation, Guest, Gmember).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11)) & (Res_line.abreise >= fdate) & (Res_line.abreise <= tdate) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.groupname, Res_line.name, Res_line.zinr).all():
                zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False
                do_it = True

                if do_it:

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                             (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.rmcat = zikat_list.kurzbez + setup_list.char
                    cl_list.kurzbez = zikat_list.kurzbez
                    cl_list.bezeich = zikat_list.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    curr_zinr = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email = guest.email_adr
                    cl_list.email_adr = gmember.email_adr
                    cl_list.tot_night = (res_line.abreise - res_line.ankunft)
                    cl_list.full_name = (guest.name + ", " + guest.vorname1 +\
                            guest.anredefirma + " " + guest.anrede1)
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3
                    cl_list.zipreis =  to_decimal(res_line.zipreis)
                    cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                    cl_list.co_time = to_string(res_line.abreisezeit, "HH:MM")
                    cl_list.birthd = gmember.geburtdatum1
                    cl_list.ktpid = gmember.ausweis_nr1

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                    if reslin_queasy:
                        cl_list.spreq = reslin_queasy.char3


                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                    if nation:
                        cl_list.local_reg = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        tot_rm = tot_rm + 1
                        cl_list.qty = res_line.zimmeranz
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "99") + "/" + to_string(cl_list.c, "99")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                 (Bill.zinr == res_line.zinr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
                            cl_list.outstand =  to_decimal(cl_list.outstand) + to_decimal(bill.saldo)


                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis

                if not disp_accompany:

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.curr_zinr == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrive) == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_data.remove(cl_list)
                        pass
                        nr = nr - 1


        elif disptype == 2:

            res_line_obj_list = {}
            for res_line, reservation, guest, gmember in db_session.query(Res_line, Reservation, Guest, Gmember).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11)) & (Res_line.abreise >= fdate) & (Res_line.abreise <= tdate) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Res_line.zinr, Res_line.name).all():
                zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False
                do_it = True

                if do_it:

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                             (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.rmcat = zikat_list.kurzbez + setup_list.char
                    cl_list.kurzbez = zikat_list.kurzbez
                    cl_list.bezeich = zikat_list.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    curr_zinr = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email = guest.email_adr
                    cl_list.email_adr = gmember.email_adr
                    cl_list.tot_night = (res_line.abreise - res_line.ankunft)
                    cl_list.full_name = (guest.name + ", " + guest.vorname1 +\
                            guest.anredefirma + " " + guest.anrede1)
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3
                    cl_list.zipreis =  to_decimal(res_line.zipreis)
                    cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                    cl_list.co_time = to_string(res_line.abreisezeit, "HH:MM")
                    cl_list.birthd = gmember.geburtdatum1
                    cl_list.ktpid = gmember.ausweis_nr1

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                    if reslin_queasy:
                        cl_list.spreq = reslin_queasy.char3


                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                    if nation:
                        cl_list.local_reg = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        tot_rm = tot_rm + 1
                        cl_list.qty = res_line.zimmeranz
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "99") + "/" + to_string(cl_list.c, "99")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                 (Bill.zinr == res_line.zinr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
                            cl_list.outstand =  to_decimal(cl_list.outstand) + to_decimal(bill.saldo)


                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis

                if not disp_accompany:

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.curr_zinr == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrive) == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_data.remove(cl_list)
                        pass
                        nr = nr - 1


        elif disptype == 3:

            res_line_obj_list = {}
            for res_line, reservation, guest, gmember in db_session.query(Res_line, Reservation, Guest, Gmember).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11)) & (Res_line.abreise >= fdate) & (Res_line.abreise <= tdate) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.name, Reservation.groupname, Res_line.name, Res_line.zinr).all():
                zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False
                do_it = True

                if do_it:

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                             (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.rmcat = zikat_list.kurzbez + setup_list.char
                    cl_list.kurzbez = zikat_list.kurzbez
                    cl_list.bezeich = zikat_list.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    curr_zinr = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email = guest.email_adr
                    cl_list.email_adr = gmember.email_adr
                    cl_list.tot_night = (res_line.abreise - res_line.ankunft)
                    cl_list.full_name = (guest.name + ", " + guest.vorname1 +\
                            guest.anredefirma + " " + guest.anrede1)
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3
                    cl_list.zipreis =  to_decimal(res_line.zipreis)
                    cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                    cl_list.co_time = to_string(res_line.abreisezeit, "HH:MM")
                    cl_list.birthd = gmember.geburtdatum1
                    cl_list.ktpid = gmember.ausweis_nr1

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                    if reslin_queasy:
                        cl_list.spreq = reslin_queasy.char3


                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                    if nation:
                        cl_list.local_reg = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        tot_rm = tot_rm + 1
                        cl_list.qty = res_line.zimmeranz
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "99") + "/" + to_string(cl_list.c, "99")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                 (Bill.zinr == res_line.zinr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
                            cl_list.outstand =  to_decimal(cl_list.outstand) + to_decimal(bill.saldo)


                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis

                if not disp_accompany:

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.curr_zinr == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrive) == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_data.remove(cl_list)
                        pass
                        nr = nr - 1


        elif disptype == 4:

            res_line_obj_list = {}
            for res_line, reservation, guest, gmember in db_session.query(Res_line, Reservation, Guest, Gmember).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8) | (Res_line.resstatus == 11)) & (Res_line.abreise >= fdate) & (Res_line.abreise <= tdate) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Res_line.abreise, Res_line.name, Res_line.zinr).all():
                zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
                if not zikat_list:
                    continue

                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False
                do_it = True

                if do_it:

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                             (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_data.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.rmcat = zikat_list.kurzbez + setup_list.char
                    cl_list.kurzbez = zikat_list.kurzbez
                    cl_list.bezeich = zikat_list.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    curr_zinr = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email = guest.email_adr
                    cl_list.email_adr = gmember.email_adr
                    cl_list.tot_night = (res_line.abreise - res_line.ankunft)
                    cl_list.full_name = (guest.name + ", " + guest.vorname1 +\
                            guest.anredefirma + " " + guest.anrede1)
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3
                    cl_list.zipreis =  to_decimal(res_line.zipreis)
                    cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                    cl_list.co_time = to_string(res_line.abreisezeit, "HH:MM")
                    cl_list.birthd = gmember.geburtdatum1
                    cl_list.ktpid = gmember.ausweis_nr1

                    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                    if reslin_queasy:
                        cl_list.spreq = reslin_queasy.char3


                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    nation = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                    if nation:
                        cl_list.local_reg = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        tot_rm = tot_rm + 1
                        cl_list.qty = res_line.zimmeranz
                    for i in range(1,length(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr_unicode(10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr_unicode(10) , " ")
                    all_remark = replace_str(all_remark, chr_unicode(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "99") + "/" + to_string(cl_list.c, "99")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                 (Bill.zinr == res_line.zinr) & (Bill.parent_nr == res_line.reslinnr) & (Bill.flag == 0)).order_by(Bill._recid).all():
                            cl_list.outstand =  to_decimal(cl_list.outstand) + to_decimal(bill.saldo)


                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis

                if not disp_accompany:

                    cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.curr_zinr == res_line.zinr and cl_list.resnr == res_line.resnr and date_mdy(cl_list.arrive) == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                    if cl_list:
                        cl_list_data.remove(cl_list)
                        pass
                        nr = nr - 1


        for cl_list in query(cl_list_data, sort_by=[("nation",False),("bezeich",False)]):

            s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_data, filters=(lambda s_list: s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_data.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = translateExtended ("UNKNOWN", lvcarea, "")
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")


    create_departure0()

    return generate_output()