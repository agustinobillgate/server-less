#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Guest, Zimkateg, Reservation, Res_line, History, Guestseg, Nation, Bill, Mc_guest, Mc_types

setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})

def pj_depart_2bl(pvilanguage:int, case_type:int, disptype:int, curr_date:date, froom:string, troom:string, setup_list_data:[Setup_list]):

    prepare_cache ([Htparam, Guest, Zimkateg, Reservation, Res_line, Nation, Bill, Mc_guest, Mc_types])

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
    lvcarea:string = "PJ-depart"
    all_remark:string = ""
    htparam = guest = zimkateg = reservation = res_line = history = guestseg = nation = bill = mc_guest = mc_types = None

    str_list = s_list = cl_list = setup_list = None

    str_list_data, Str_list = create_model("Str_list", {"flag":int, "line1":string, "line2":string, "address":string})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "nr":int, "vip":string, "resnr":int, "name":string, "groupname":string, "rmno":string, "qty":int, "arrive":string, "depart":string, "rmcat":string, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "outstand":Decimal, "bemerk":string, "bemerk01":string, "bemerk02":string, "bemerk03":string, "bemerk04":string, "bemerk05":string, "bemerk06":string, "bemerk07":string, "bemerk08":string, "email":string, "email_adr":string, "tot_night":int, "ratecode":string, "full_name":string, "address":string, "memberno":string, "membertype":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_data, s_list_data, cl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal pvilanguage, case_type, disptype, curr_date, froom, troom


        nonlocal str_list, s_list, cl_list, setup_list
        nonlocal str_list_data, s_list_data, cl_list_data

        return {"tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "str-list": str_list_data, "s-list": s_list_data, "cl-list": cl_list_data}

    def create_departure():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_data, s_list_data, cl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal pvilanguage, case_type, disptype, curr_date, froom, troom


        nonlocal str_list, s_list, cl_list, setup_list
        nonlocal str_list_data, s_list_data, cl_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        gmember = None
        str:string = ""
        do_it:bool = False
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
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.groupname, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.resstatus == 8 and (res_line.ankunft == res_line.abreise):

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False
                do_it = True

                if do_it:
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if res_line.zinr == "":
                        cl_list.rmno = "#" + to_string(res_line.zimmeranz)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus <= 2 or res_line.resstatus == 5 or res_line.resstatus == 6 or (res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0):
                        cl_list.qty = res_line.zimmeranz
                        tot_rm = tot_rm + res_line.zimmeranz
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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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


        elif disptype == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.name, Reservation.groupname, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.resstatus == 8 and (res_line.ankunft == res_line.abreise):

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False
                do_it = True

                if do_it:
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if res_line.zinr == "":
                        cl_list.rmno = "#" + to_string(res_line.zimmeranz)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus <= 2 or res_line.resstatus == 5 or res_line.resstatus == 6 or (res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0):
                        cl_list.qty = res_line.zimmeranz
                        tot_rm = tot_rm + res_line.zimmeranz
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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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


        elif disptype == 2:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5) | (Res_line.resstatus == 6) | (Res_line.resstatus == 13) | (Res_line.resstatus == 8)) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Res_line.zinr, Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                do_it = True

                if res_line.resstatus == 8 and (res_line.ankunft == res_line.abreise):

                    history = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"gesamtumsatz": [(gt, 0)]})

                    if not history:
                        do_it = False
                do_it = True

                if do_it:
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if res_line.zinr == "":
                        cl_list.rmno = "#" + to_string(res_line.zimmeranz)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    if res_line.resstatus <= 2 or res_line.resstatus == 5 or res_line.resstatus == 6 or (res_line.resstatus == 8 and (res_line.erwachs + res_line.gratis) > 0):
                        cl_list.qty = res_line.zimmeranz
                        tot_rm = tot_rm + res_line.zimmeranz
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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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

    def create_departure1():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_data, s_list_data, cl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal pvilanguage, case_type, disptype, curr_date, froom, troom


        nonlocal str_list, s_list, cl_list, setup_list
        nonlocal str_list_data, s_list_data, cl_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        gmember = None
        do_it:bool = False
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
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.groupname, Res_line.name, Res_line.zinr).all():
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 2:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Res_line.zinr, Res_line.name).all():
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


        elif disptype == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.name, Reservation.groupname, Res_line.name, Res_line.zinr).all():
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                    if mc_guest:
                        cl_list.memberno = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            cl_list.membertype = mc_types.bezeich
                    tot_a = tot_a + res_line.erwachs
                    tot_c = tot_c + res_line.kind1 + res_line.kind2
                    tot_co = tot_co + res_line.gratis


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

    def create_actual():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_data, s_list_data, cl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal pvilanguage, case_type, disptype, curr_date, froom, troom


        nonlocal str_list, s_list, cl_list, setup_list
        nonlocal str_list_data, s_list_data, cl_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        gmember = None
        do_it:bool = False
        Gmember =  create_buffer("Gmember",Guest)
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()

        if disptype == 2:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Res_line.zinr, Res_line.name).all():
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        cl_list.qty = 1
                        tot_rm = tot_rm + 1
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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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


        elif disptype == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.name, Reservation.groupname, Res_line.name, Res_line.zinr).all():
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        cl_list.qty = 1
                        tot_rm = tot_rm + 1
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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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


        elif disptype == 1:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.resstatus == 8) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.groupname, Res_line.name, Res_line.zinr).all():
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
                    cl_list.kurzbez = zimkateg.kurzbez
                    cl_list.bezeich = zimkateg.bezeichnung
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

                    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                    if setup_list:
                        cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                    else:
                        cl_list.rmcat = zimkateg.kurzbez
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(i - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            cl_list.ratecode = substring(str, 6)
                            break

                    if guest.karteityp != 0:
                        cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                    if gmember.telefon != "":
                        cl_list.company = cl_list.company + ";" + gmember.telefon

                    if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                        cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                        cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                    if cl_list.nat == "":
                        cl_list.nat = "?"
                    else:

                        nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                        if nation:
                            cl_list.nation = nation.bezeich

                    if (res_line.erwachs + res_line.gratis) > 0:
                        cl_list.qty = 1
                        tot_rm = tot_rm + 1
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
                    cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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

    def create_expected():

        nonlocal tot_rm, tot_a, tot_c, tot_co, str_list_data, s_list_data, cl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, lvcarea, all_remark, htparam, guest, zimkateg, reservation, res_line, history, guestseg, nation, bill, mc_guest, mc_types
        nonlocal pvilanguage, case_type, disptype, curr_date, froom, troom


        nonlocal str_list, s_list, cl_list, setup_list
        nonlocal str_list_data, s_list_data, cl_list_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        gmember = None
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
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.groupname, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


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
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
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

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                if setup_list:
                    cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                else:
                    cl_list.rmcat = zimkateg.kurzbez
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        cl_list.ratecode = substring(str, 6)
                        break

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if gmember.telefon != "":
                    cl_list.company = cl_list.company + ";" + gmember.telefon

                if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                    cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                    cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                if res_line.resstatus == 6:
                    tot_rm = tot_rm + 1
                    cl_list.qty = 1
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
                cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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


        elif disptype == 3:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Reservation.name, Reservation.groupname, Res_line.name, Res_line.zinr).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


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
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
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

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                if setup_list:
                    cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                else:
                    cl_list.rmcat = zimkateg.kurzbez
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        cl_list.ratecode = substring(str, 6)
                        break

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if gmember.telefon != "":
                    cl_list.company = cl_list.company + ";" + gmember.telefon

                if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                    cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                    cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                if res_line.resstatus == 6:
                    tot_rm = tot_rm + 1
                    cl_list.qty = 1
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
                cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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


        elif disptype == 2:

            res_line_obj_list = {}
            res_line = Res_line()
            zimkateg = Zimkateg()
            reservation = Reservation()
            guest = Guest()
            gmember = Guest()
            for res_line.ankunft, res_line.abreise, res_line.resnr, res_line.reslinnr, res_line.name, res_line.zinr, res_line.erwachs, res_line.kind1, res_line.kind2, res_line.gratis, res_line.arrangement, res_line.flight_nr, res_line.setup, res_line.zimmer_wunsch, res_line.abreisezeit, res_line.zimmeranz, res_line.resstatus, res_line.bemerk, res_line.active_flag, res_line._recid, zimkateg.kurzbez, zimkateg.bezeichnung, zimkateg._recid, reservation.groupname, reservation._recid, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest.karteityp, guest._recid, guest.gastnr, guest.nation1, guest.email_adr, guest.adresse1, guest.adresse2, guest.adresse3, guest.telefon, gmember.name, gmember.vorname1, gmember.anrede1, gmember.anredefirma, gmember.karteityp, gmember._recid, gmember.gastnr, gmember.nation1, gmember.email_adr, gmember.adresse1, gmember.adresse2, gmember.adresse3, gmember.telefon in db_session.query(Res_line.ankunft, Res_line.abreise, Res_line.resnr, Res_line.reslinnr, Res_line.name, Res_line.zinr, Res_line.erwachs, Res_line.kind1, Res_line.kind2, Res_line.gratis, Res_line.arrangement, Res_line.flight_nr, Res_line.setup, Res_line.zimmer_wunsch, Res_line.abreisezeit, Res_line.zimmeranz, Res_line.resstatus, Res_line.bemerk, Res_line.active_flag, Res_line._recid, Zimkateg.kurzbez, Zimkateg.bezeichnung, Zimkateg._recid, Reservation.groupname, Reservation._recid, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest.karteityp, Guest._recid, Guest.gastnr, Guest.nation1, Guest.email_adr, Guest.adresse1, Guest.adresse2, Guest.adresse3, Guest.telefon, Gmember.name, Gmember.vorname1, Gmember.anrede1, Gmember.anredefirma, Gmember.karteityp, Gmember._recid, Gmember.gastnr, Gmember.nation1, Gmember.email_adr, Gmember.adresse1, Gmember.adresse2, Gmember.adresse3, Gmember.telefon).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).filter(
                     (Res_line.active_flag == 1) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13)) & (Res_line.abreise == curr_date) & (((Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())) | ((Res_line.zinr >= (froom).lower() )))).order_by(Res_line.zinr, Res_line.name).all():
                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


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
                cl_list.kurzbez = zimkateg.kurzbez
                cl_list.bezeich = zimkateg.bezeichnung
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

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                if setup_list:
                    cl_list.rmcat = zimkateg.kurzbez + setup_list.char
                else:
                    cl_list.rmcat = zimkateg.kurzbez
                for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                    str = entry(i - 1, res_line.zimmer_wunsch, ";")

                    if substring(str, 0, 6) == ("$CODE$").lower() :
                        cl_list.ratecode = substring(str, 6)
                        break

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if gmember.telefon != "":
                    cl_list.company = cl_list.company + ";" + gmember.telefon

                if (cl_list.etd.lower()  == ("0000").lower()  or cl_list.etd.lower()  == "") and res_line.abreisezeit != 0:
                    cl_list.etd = to_string(res_line.abreisezeit, "HH:MM")
                    cl_list.etd = substring(cl_list.etd, 0, 2) + substring(cl_list.etd, 3, 2)

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                if res_line.resstatus == 6:
                    tot_rm = tot_rm + 1
                    cl_list.qty = 1
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
                cl_list.pax = to_string(cl_list.a, "9") + "/" + to_string(cl_list.c, "9")

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


    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

    if htparam.finteger != 0:
        vipnr1 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

    if htparam.finteger != 0:
        vipnr2 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

    if htparam.finteger != 0:
        vipnr3 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

    if htparam.finteger != 0:
        vipnr4 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

    if htparam.finteger != 0:
        vipnr5 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

    if htparam.finteger != 0:
        vipnr6 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

    if htparam.finteger != 0:
        vipnr7 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

    if htparam.finteger != 0:
        vipnr8 = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

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