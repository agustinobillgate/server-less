from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Htparam, Guest, Zimkateg, Reservation, Res_line, History, Guestseg, Nation, Bill, Mc_guest, Mc_types

def pj_depart_2_webbl(pvilanguage:int, case_type:int, disptype:int, curr_date:date, froom:str, troom:str, ota_only:bool, setup_list:[Setup_list]):
    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    str_list_list = []
    s_list_list = []
    cl_list_list = []
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    lvcarea:str = "PJ_depart"
    all_remark:str = ""
    htparam = guest = zimkateg = reservation = res_line = history = guestseg = nation = bill = mc_guest = mc_types = None

    str_list = s_list = cl_list = setup_list = gmember = g_ota = None

    str_list_list, Str_list = create_model("Str_list", {"flag":int, "line1":str, "line2":str, "address":str})
    s_list_list, S_list = create_model("S_list", {"rmcat":str, "bezeich":str, "nat":str, "anz":int, "adult":int, "proz":decimal, "child":int})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":str, "resnr":int, "name":str, "groupname":str, "rmno":str, "qty":int, "arrive":str, "depart":str, "rmcat":str, "kurzbez":str, "bezeich":str, "a":int, "c":int, "co":int, "pax":str, "nat":str, "nation":str, "argt":str, "company":str, "flight":str, "etd":str, "outstand":decimal, "bemerk":str, "bemerk01":str, "bemerk02":str, "bemerk03":str, "bemerk04":str, "bemerk05":str, "bemerk06":str, "bemerk07":str, "bemerk08":str, "email":str, "email_adr":str, "tot_night":int, "ratecode":str, "full_name":str, "address":str, "memberno":str, "membertype":str, "phone_number":str, "mobile_phone":str})
    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})

    Gmember = Guest
    G_ota = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_list, s_list_list, cl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal gmember, g_ota


        nonlocal str_list, s_list, cl_list, setup_list, gmember, g_ota
        nonlocal str_list_list, s_list_list, cl_list_list, setup_list_list
        return {"tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "str-list": str_list_list, "s-list": s_list_list, "cl-list": cl_list_list}

    def create_departure():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_list, s_list_list, cl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal gmember, g_ota


        nonlocal str_list, s_list, cl_list, setup_list, gmember, g_ota
        nonlocal str_list_list, s_list_list, cl_list_list, setup_list_list

        i:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        do_it:bool = False
        Gmember = Guest
        G_ota = Guest
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()

        if disptype == 1:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.resstatus == 8)) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.resstatus == 8 and (res_line.ankunft == res_line.abreise):

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if res_line.zinr == "":
                        cl_list.rmno = "#" + to_string(res_line.zimmeranz)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus <= 2 or res_line.resstatus == 5 or res_line.resstatus == 6 or (res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0):
                        cl_list.qty = res_line.zimmeranz
                        tot_rm = tot_rm + res_line.zimmeranz
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 3:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.resstatus == 8)) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.resstatus == 8 and (res_line.ankunft == res_line.abreise):

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if res_line.zinr == "":
                        cl_list.rmno = "#" + to_string(res_line.zimmeranz)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus <= 2 or res_line.resstatus == 5 or res_line.resstatus == 6 or (res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0):
                        cl_list.qty = res_line.zimmeranz
                        tot_rm = tot_rm + res_line.zimmeranz
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 2:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    ((Res_line.resstatus <= 2) |  (Res_line.resstatus == 5) |  (Res_line.resstatus == 6) |  (Res_line.resstatus == 13) |  (Res_line.resstatus == 8)) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.resstatus == 8 and (res_line.ankunft == res_line.abreise):

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if res_line.zinr == "":
                        cl_list.rmno = "#" + to_string(res_line.zimmeranz)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus <= 2 or res_line.resstatus == 5 or res_line.resstatus == 6 or (res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0):
                        cl_list.qty = res_line.zimmeranz
                        tot_rm = tot_rm + res_line.zimmeranz
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = translateExtended ("UNKNOWN", lvcarea, "")
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_departure1():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_list, s_list_list, cl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal gmember, g_ota


        nonlocal str_list, s_list, cl_list, setup_list, gmember, g_ota
        nonlocal str_list_list, s_list_list, cl_list_list, setup_list_list

        i:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        do_it:bool = False
        Gmember = Guest
        G_ota = Guest
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()

        if disptype == 1:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 8) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        tot_rm = tot_rm + 1
                        cl_list.qty = res_line.zimmeranz
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 2:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 8) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        tot_rm = tot_rm + 1
                        cl_list.qty = res_line.zimmeranz
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 3:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 8) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        tot_rm = tot_rm + 1
                        cl_list.qty = res_line.zimmeranz
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = translateExtended ("UNKNOWN", lvcarea, "")
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_actual():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_list, s_list_list, cl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal gmember, g_ota


        nonlocal str_list, s_list, cl_list, setup_list, gmember, g_ota
        nonlocal str_list_list, s_list_list, cl_list_list, setup_list_list

        i:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        do_it:bool = False
        Gmember = Guest
        G_ota = Guest
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()

        if disptype == 2:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 8) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        cl_list.qty = 1
                        tot_rm = tot_rm + 1
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 3:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 8) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        cl_list.qty = 1
                        tot_rm = tot_rm + 1
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 1:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.resstatus == 8) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if res_line.ankunft == res_line.abreise:

                    history = db_session.query(History).filter(
                            (History.resnr == res_line.resnr) &  (History.reslinnr == res_line.reslinnr) &  (History.gesamtumsatz > 0)).first()

                    if not history:
                        do_it = False
                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        cl_list.qty = 1
                        tot_rm = tot_rm + 1
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = translateExtended ("UNKNOWN", lvcarea, "")
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100


    def create_expected():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_list, s_list_list, cl_list_list, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal gmember, g_ota


        nonlocal str_list, s_list, cl_list, setup_list, gmember, g_ota
        nonlocal str_list_list, s_list_list, cl_list_list, setup_list_list

        i:int = 0
        vip_flag:str = ""
        nr:int = 0
        str:str = ""
        do_it:bool = False
        Gmember = Guest
        G_ota = Guest
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_list.clear()
        cl_list_list.clear()
        str_list_list.clear()

        if disptype == 1:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus == 6:
                        tot_rm = tot_rm + 1
                        cl_list.qty = 1
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 3:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus == 6:
                        tot_rm = tot_rm + 1
                        cl_list.qty = 1
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 2:

            res_line_obj_list = []
            for res_line, zimkateg, reservation, guest, gmember in db_session.query(Res_line, Zimkateg, Reservation, Guest, Gmember).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                    (Res_line.active_flag == 1) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13)) &  (Res_line.abreise == curr_date) &  (((func.lower(Res_line.zinr) >= (froom).lower()) &  (func.lower(Res_line.zinr) <= troom)) |  ((func.lower(Res_line.zinr) >= (froom).lower() )))).all():
                if res_line._recid in res_line_obj_list:
                    continue
                else:
                    res_line_obj_list.append(res_line._recid)


                do_it = True

                if ota_only:

                    g_ota = db_session.query(G_ota).filter(
                            (G_ota.gastnr == reservation.gastnr) &  (G_ota.karteityp == 2) &  (G_ota.steuernr != "")).first()

                    if g_ota:
                        do_it = True

                        if re.match(".*e1_booking.*",g_ota.name):
                            do_it = False
                    else:
                        do_it = False

                if do_it:
                    nr = nr + 1
                    vip_flag = ""

                    guestseg = db_session.query(Guestseg).filter(
                            (Guestseg.gastnr == gmember.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                    if guestseg:
                        vip_flag = "VIP"
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.nr = nr
                    cl_list.groupname = reservation.groupname
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeich
                    cl_list.nat = gmember.nation1
                    cl_list.resnr = res_line.resnr
                    cl_list.vip = vip_flag
                    cl_list.name = res_line.name
                    cl_list.rmno = res_line.zinr
                    cl_list.arrive = to_string(res_line.ankunft, "99/99/99")
                    cl_list.depart = to_string(res_line.abreise, "99/99/99")
                    cl_list.a = res_line.erwachs
                    cl_list.c = res_line.kind1 + res_line.kind2
                    cl_list.co = res_line.gratis
                    cl_list.argt = res_line.arrangement
                    cl_list.flight = substring(res_line.flight_nr, 11, 6)
                    cl_list.etd = substring(res_line.flight_nr, 17, 5)
                    cl_list.email_adr = gmember.email_adr
                    cl_list.address = gmember.adresse1 + ", " + gmember.adresse2 + ", " + gmember.adresse3

                    setup_list = query(setup_list_list, filters=(lambda setup_list :setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == "$CODE$":
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.phone_number = gmember.telefon

                    if gmember.mobil_tel != "":
                        cl_list.mobile_phone = gmember.mobil_tel

                    if (cl_list.etd == "0000" or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = db_session.query(Nation).filter(
                                (Nation.kurzbez == cl_list.nat)).first()

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus == 6:
                        tot_rm = tot_rm + 1
                        cl_list.qty = 1
                    for i in range(1,len(res_line.bemerk)  + 1) :

                        if substring(res_line.bemerk, i - 1, 1) == chr (10):
                            cl_list.bemerk = cl_list.bemerk + " "
                        else:
                            cl_list.bemerk = cl_list.bemerk + substring(trim(res_line.bemerk) , i - 1, 1)
                    all_remark = res_line.bemerk
                    all_remark = replace_str(all_remark, chr(10) , " ")
                    all_remark = replace_str(all_remark, chr(13) , " ")
                    cl_list.bemerk01 = to_string(substring(all_remark, 0, 255))
                    cl_list.bemerk02 = to_string(substring(all_remark, 255, 255))
                    cl_list.bemerk03 = to_string(substring(all_remark, 510, 255))
                    cl_list.bemerk04 = to_string(substring(all_remark, 765, 255))
                    cl_list.bemerk05 = to_string(substring(all_remark, 1020, 255))
                    cl_list.bemerk06 = to_string(substring(all_remark, 1275, 255))
                    cl_list.bemerk07 = to_string(substring(all_remark, 1530, 255))
                    cl_list.bemerk08 = to_string(substring(all_remark, 1785, 255))
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    if res_line.active_flag == 1:

                        for bill in db_session.query(Bill).filter(
                                (Bill.zinr == res_line.zinr) &  (Bill.parent_nr == res_line.reslinnr) &  (Bill.flag == 0)).all():
                            cl_list.outstand = cl_list.outstand + bill.saldo


                    mc_guest = db_session.query(Mc_guest).filter(
                            (Mc_guest.gastnr == gmember.gastnr)).first()

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        for cl_list in query(cl_list_list):

            s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == cl_list.kurzbez), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.rmcat == ""), first=True)

                if s_list:
                    s_list.rmcat = cl_list.kurzbez
                    s_list.bezeich = cl_list.bezeich

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)

                s_list.rmcat = cl_list.kurzbez
                s_list.bezeich = cl_list.bezeich
            s_list.anz = s_list.anz + cl_list.qty

            s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == cl_list.nat), first=True)

            if not s_list:

                s_list = query(s_list_list, filters=(lambda s_list :s_list.nat == ""), first=True)

                if s_list:
                    s_list.nat = cl_list.nat

            if not s_list:
                s_list = S_list()
                s_list_list.append(s_list)


                if s_list:
                    s_list.nat = cl_list.nat
            s_list.adult = s_list.adult + cl_list.a + cl_list.co
            s_list.child = s_list.child + cl_list.c

        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_list, filters=(lambda s_list :s_list.nat != "")):

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == s_list.nat)).first()

                if nation:
                    s_list.nat = nation.bezeich
                else:
                    s_list.nat = translateExtended ("UNKNOWN", lvcarea, "")
                s_list.proz = s_list.adult / (tot_a + tot_co) * 100

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 700)).first()

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 701)).first()

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 702)).first()

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 703)).first()

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 704)).first()

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 705)).first()

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 706)).first()

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 707)).first()

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 708)).first()

    if htparam.finteger != 0:
        vipnr9 = htparam.finteger

    if case_type == 1:
        create_departure()
    elif case_type == 2:
        create_departure1()
    elif case_type == 3:
        create_actual()
    elif case_type == 4:
        create_expected()

    return generate_output()