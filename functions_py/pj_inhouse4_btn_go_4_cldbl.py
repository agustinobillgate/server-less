#using conversion tools version: 1.0.0.48
#-----------------------------------------
# Rd 29/7/2025
# gitlab:840
# 
#-----------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Waehrung, Artikel, Nation, Zkstat, Zinrstat, Paramtext, Guest, Reservation, Zimmer, Sourccod, Arrangement, Bill, Res_line, Guest_pr, Guestseg, Segment, Bill_line, Argt_line, Mc_guest, Mc_types, Reslin_queasy, Genstat

zikat_list_data, Zikat_list = create_model("Zikat_list", {"selected":bool, "zikatnr":int, "kurzbez":string, "bezeich":string})

def pj_inhouse4_btn_go_4_cldbl(sorttype:int, from_date:date, to_date:date, curr_date:date, curr_gastnr:int, froom:string, troom:string, exc_depart:bool, incl_gcomment:bool, incl_rsvcomment:bool, prog_name:string, disp_accompany:bool, zikat_list_data:[Zikat_list]):

    prepare_cache ([Htparam, Waehrung, Artikel, Nation, Zkstat, Zinrstat, Paramtext, Guest, Reservation, Zimmer, Sourccod, Arrangement, Bill, Res_line, Guest_pr, Guestseg, Segment, Bill_line, Argt_line, Mc_guest, Mc_types, Reslin_queasy, Genstat])

    tot_payrm = 0
    tot_rm = 0
    tot_a = 0
    tot_c = 0
    tot_co = 0
    tot_avail = 0
    inactive = 0
    tot_keycard = 0
    cl_list_data = []
    s_list_data = []
    t_buff_queasy_data = []
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    tot_room:int = 0
    all_room:int = 0
    frate:Decimal = to_decimal("0.0")
    exchg_rate:Decimal = 1
    ct:string = ""
    contcode:string = ""
    bfast_art:int = 0
    lunch_art:int = 0
    dinner_art:int = 0
    lundin_art:int = 0
    fb_dept:int = 0
    argt_betrag:Decimal = to_decimal("0.0")
    take_it:bool = False
    prcode:int = 0
    qty:int = 0
    r_qty:int = 0
    lodge_betrag:Decimal = to_decimal("0.0")
    f_betrag:Decimal = to_decimal("0.0")
    s:string = ""
    tot_qty:int = 0
    tot_rev:Decimal = to_decimal("0.0")
    queasy = htparam = waehrung = artikel = nation = zkstat = zinrstat = paramtext = guest = reservation = zimmer = sourccod = arrangement = bill = res_line = guest_pr = guestseg = segment = bill_line = argt_line = mc_guest = mc_types = reslin_queasy = genstat = None

    setup_list = str_list = cl_list = s_list = zinr_list = t_buff_queasy = zikat_list = waehrung1 = artikel1 = nation1 = None

    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})
    str_list_data, Str_list = create_model("Str_list", {"flag":int, "rflag":bool, "line1":string, "line2":string, "line3":string, "company":string}, {"rflag": True})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "karteityp":int, "nr":int, "vip":string, "resnr":int, "firstname":string, "lastname":string, "birthdate":string, "groupname":string, "rmno":string, "qty":int, "arrive":date, "depart":date, "rmcat":string, "ratecode":string, "zipreis":Decimal, "kurzbez":string, "bezeich":string, "a":int, "c":int, "co":int, "pax":string, "nat":string, "nation":string, "argt":string, "company":string, "flight":string, "etd":string, "paym":int, "segm":string, "telefon":string, "mobil_tel":string, "created":date, "createid":string, "bemerk":string, "bemerk1":string, "ci_time":string, "curr":string, "inhousedate":date, "sob":string, "gastnr":int, "lodging":Decimal, "breakfast":Decimal, "lunch":Decimal, "dinner":Decimal, "otherev":Decimal, "rechnr":int, "memberno":string, "membertype":string, "email":string, "localreg":string, "c_zipreis":string, "c_lodging":string, "c_breakfast":string, "c_lunch":string, "c_dinner":string, "c_otherev":string, "c_a":string, "c_c":string, "c_co":string, "c_rechnr":string, "c_resnr":string, "night":string, "city":string, "keycard":string, "co_time":string, "pay_art":string, "etage":int, "zinr_bez":string, "flag_guest":int})
    s_list_data, S_list = create_model("S_list", {"rmcat":string, "bezeich":string, "nat":string, "anz":int, "adult":int, "proz":Decimal, "child":int, "proz_qty":Decimal, "rev":Decimal, "proz_rev":Decimal, "arr":Decimal})
    zinr_list_data, Zinr_list = create_model("Zinr_list", {"resnr":int, "reslinnr":int, "zinr":string, "datum":date, "arrival":date, "departed":date})
    t_buff_queasy_data, T_buff_queasy = create_model_like(Queasy)

    Waehrung1 = create_buffer("Waehrung1",Waehrung)
    Artikel1 = create_buffer("Artikel1",Artikel)
    Nation1 = create_buffer("Nation1",Nation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, frate, exchg_rate, ct, contcode, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, tot_qty, tot_rev, queasy, htparam, waehrung, artikel, nation, zkstat, zinrstat, paramtext, guest, reservation, zimmer, sourccod, arrangement, bill, res_line, guest_pr, guestseg, segment, bill_line, argt_line, mc_guest, mc_types, reslin_queasy, genstat
        nonlocal sorttype, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany
        nonlocal waehrung1, artikel1, nation1


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, zikat_list, waehrung1, artikel1, nation1
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        return {"tot_payrm": tot_payrm, "tot_rm": tot_rm, "tot_a": tot_a, "tot_c": tot_c, "tot_co": tot_co, "tot_avail": tot_avail, "inactive": inactive, "tot_keycard": tot_keycard, "cl-list": cl_list_data, "s-list": s_list_data, "t-buff-queasy": t_buff_queasy_data}

    def bed_setup():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, frate, exchg_rate, ct, contcode, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, tot_qty, tot_rev, queasy, htparam, waehrung, artikel, nation, zkstat, zinrstat, paramtext, guest, reservation, zimmer, sourccod, arrangement, bill, res_line, guest_pr, guestseg, segment, bill_line, argt_line, mc_guest, mc_types, reslin_queasy, genstat
        nonlocal sorttype, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany
        nonlocal waehrung1, artikel1, nation1


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, zikat_list, waehrung1, artikel1, nation1
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data


        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
            setup_list = Setup_list()
            setup_list_data.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199
            setup_list.char = substring(paramtext.notes, 0, 1)


    def create_inhouse():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, frate, exchg_rate, ct, contcode, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, tot_qty, tot_rev, queasy, htparam, waehrung, artikel, nation, zkstat, zinrstat, paramtext, guest, reservation, zimmer, sourccod, arrangement, bill, res_line, guest_pr, guestseg, segment, bill_line, argt_line, mc_guest, mc_types, reslin_queasy, genstat
        nonlocal sorttype, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany
        nonlocal waehrung1, artikel1, nation1


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, zikat_list, waehrung1, artikel1, nation1
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        buff_art = None
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        Buff_art =  create_buffer("Buff_art",Artikel)
        zinr_list_data.clear()

        if from_date == curr_date and to_date == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        tot_qty = 0
        tot_rev =  to_decimal("0")
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        zimmer_obj_list = {}
        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == zimmer.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if zimmer_obj_list.get(zimmer._recid):
                continue
            else:
                zimmer_obj_list[zimmer._recid] = True


            tot_avail = tot_avail + 1

        res_line_obj_list = {}
        for res_line, reservation, guest, gmember, sourccod, arrangement, artikel, bill in db_session.query(Res_line, Reservation, Guest, Gmember, Sourccod, Arrangement, Artikel, Bill).join(Reservation,(Reservation.resnr == Res_line.resnr)).join(Guest,(Guest.gastnr == Reservation.gastnr)).join(Gmember,(Gmember.gastnr == Res_line.gastnrmember)).join(Sourccod,(Sourccod.source_code == Reservation.resart)).join(Arrangement,(Arrangement.arrangement == Res_line.arrangement)).join(Artikel,(Artikel.artnr == Arrangement.argt_artikelnr) & (Artikel.departement == 0)).join(Bill,(Bill.resnr == Res_line.resnr) & (Bill.reslinnr == Res_line.reslinnr) & (Bill.zinr == Res_line.zinr)).filter(
                 (Res_line.active_flag >= actflag1) & (Res_line.active_flag <= actflag2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.ankunft <= from_date) & (Res_line.abreise >= to_date) & (Res_line.zinr >= (froom).lower()) & (Res_line.zinr <= (troom).lower())).order_by(Res_line.zinr, Res_line.ankunft, Res_line.erwachs.desc(), Res_line.name).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == res_line.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if exc_depart and res_line.abreise == to_date:
                pass
            else:

                waehrung1 = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})
                exchg_rate =  to_decimal(waehrung1.ankauf) / to_decimal(waehrung1.einheit)

                if res_line.reserve_dec != 0:
                    frate =  to_decimal(res_line.reserve_dec)
                else:
                    frate =  to_decimal(exchg_rate)

                if res_line.reserve_int != 0:

                    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, guest.gastnr)]})

                if guest_pr:
                    contcode = guest_pr.code
                    ct = res_line.zimmer_wunsch

                    if matches(ct,r"*$CODE$*"):
                        ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
                        contcode = substring(ct, 0, get_index(ct, ";") - 1)

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = segment.bezeich


                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zikat_list.kurzbez + setup_list.char
                cl_list.kurzbez = zikat_list.kurzbez
                cl_list.bezeich = zikat_list.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = res_line.resnr
                cl_list.vip = vip_flag
                cl_list.firstname = right_trim(gmember.vorname1, chr_unicode(10))
                cl_list.firstname = right_trim(cl_list.firstname, chr_unicode(13))
                cl_list.firstname = replace_str(cl_list.firstname, chr_unicode(10) , " ")
                cl_list.lastname = right_trim(gmember.name, chr_unicode(10))
                cl_list.lastname = right_trim(cl_list.lastname, chr_unicode(13))
                cl_list.lastname = replace_str(cl_list.lastname, chr_unicode(10) , " ")

                if gmember.geburtdatum1 == None:
                    cl_list.birthdate = ""
                else:
                    cl_list.birthdate = to_string(gmember.geburtdatum1, "99/99/9999")
                cl_list.rmno = res_line.zinr
                cl_list.zipreis =  to_decimal(res_line.zipreis)
                cl_list.arrive = res_line.ankunft
                cl_list.depart = res_line.abreise
                cl_list.qty = res_line.zimmeranz
                cl_list.a = res_line.erwachs
                cl_list.c = res_line.kind1 + res_line.kind2
                cl_list.co = res_line.gratis
                cl_list.argt = res_line.arrangement
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.co_time = to_string(res_line.abreisezeit, "HH:MM")
                cl_list.paym = reservation.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.inhousedate = res_line.ankunft
                cl_list.sob = sourccod.bezeich
                cl_list.gastnr = gmember.gastnr
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon
                cl_list.email = gmember.email_adr
                cl_list.lodging =  to_decimal(cl_list.zipreis)
                cl_list.rechnr = bill.rechnr
                cl_list.night = to_string(res_line.abreise - res_line.ankunft, ">>>>9")
                cl_list.city = gmember.wohnort
                cl_list.keycard = to_string(res_line.betrieb_gast, ">>>>>9")
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                bill_line_obj_list = {}
                bill_line = Bill_line()
                buff_art = Artikel()
                for bill_line.artnr, bill_line._recid, buff_art.umsatzart, buff_art.zwkum, buff_art._recid in db_session.query(Bill_line.artnr, Bill_line._recid, Buff_art.umsatzart, Buff_art.zwkum, Buff_art._recid).join(Buff_art,(Buff_art.artnr == Bill_line.artnr) & (Buff_art.departement == Bill_line.departement)).filter(
                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.betrag < 0)).order_by(Bill_line._recid).all():
                    if bill_line_obj_list.get(bill_line._recid):
                        continue
                    else:
                        bill_line_obj_list[bill_line._recid] = True

                    if (buff_art.artart == 2 or buff_art.artart == 5 or buff_art.artart == 6 or buff_art.artart == 7):
                        cl_list.pay_art = cl_list.pay_art + to_string(bill_line.artnr) + ","
                cl_list.pay_art = substring(cl_list.pay_art, 0, length(cl_list.pay_art) - 1)

                nation1 = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation1:
                    cl_list.localreg = gmember.nation2 + " - " + nation1.bezeich

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                    artikel1 = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})

                    if not artikel1:
                        take_it = False
                    else:
                        take_it, f_betrag, argt_betrag, qty = get_argtline_rate(contcode, argt_line._recid)

                    if take_it:

                        if artikel1.zwkum == bfast_art and (artikel1.umsatzart == 3 or artikel1.umsatzart >= 5):
                            cl_list.breakfast =  to_decimal(cl_list.breakfast) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                        elif artikel1.zwkum == lunch_art and (artikel1.umsatzart == 3 or artikel1.umsatzart >= 5):
                            cl_list.lunch =  to_decimal(cl_list.lunch) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)

                        elif artikel1.zwkum == dinner_art and (artikel1.umsatzart == 3 or artikel1.umsatzart >= 5):
                            cl_list.dinner =  to_decimal(cl_list.dinner) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)
                        else:
                            cl_list.otherev =  to_decimal(cl_list.otherev) + to_decimal(argt_betrag)
                            cl_list.lodging =  to_decimal(cl_list.lodging) - to_decimal(argt_betrag)
                cl_list.c_zipreis = to_string(cl_list.zipreis, "->>,>>>,>>>,>>9.99")
                cl_list.c_lodging = to_string(cl_list.lodging, "->>,>>>,>>>,>>9.99")
                cl_list.c_breakfast = to_string(cl_list.breakfast, "->>,>>>,>>>,>>9.99")
                cl_list.c_lunch = to_string(cl_list.lunch, "->>,>>>,>>>,>>9.99")
                cl_list.c_dinner = to_string(cl_list.dinner, "->>,>>>,>>>,>>9.99")
                cl_list.c_otherev = to_string(cl_list.otherev, "->>,>>>,>>>,>>9.99")
                cl_list.c_a = to_string(cl_list.a, "9")
                cl_list.c_c = to_string(cl_list.c, "9")
                cl_list.c_co = to_string(cl_list.co, ">9")
                cl_list.c_rechnr = to_string(cl_list.rechnr, ">>>>>9")
                cl_list.c_resnr = to_string(cl_list.resnr, ">>>>>9")

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.memberno = mc_guest.cardnum

                mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                if mc_types:
                    cl_list.membertype = mc_types.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz

                segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if res_line.resstatus == 13 or res_line.zimmerfix:
                    cl_list.qty = 0

                if incl_gcomment:

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:
                        for i in range(1,length(gbuff.bemerkung)  + 1) :

                            if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                cl_list.bemerk = cl_list.bemerk + " "
                            else:
                                cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        for j in range(1,length(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1

                if not incl_gcomment and not incl_rsvcomment:
                    cl_list.bemerk = trim(replace_str(res_line.bemerk, chr_unicode(10) , " "))

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == res_line.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr and zinr_list.arrival == res_line.ankunft and zinr_list.departed == res_line.abreise), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = res_line.zinr

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, res_line.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and res_line.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_rm = tot_rm + res_line.zimmeranz

                    if zimmer.sleeping and res_line.zipreis > 0 and res_line.resstatus != 13:

                        if not queasy:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                        elif queasy and queasy.number3 != res_line.gastnr:
                            tot_payrm = tot_payrm + res_line.zimmeranz

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != res_line.gastnr and res_line.zipreis > 0:
                            tot_rm = tot_rm + res_line.zimmeranz
                        inactive = inactive + 1
                tot_a = tot_a + res_line.erwachs
                tot_c = tot_c + res_line.kind1 + res_line.kind2
                tot_co = tot_co + res_line.gratis
                tot_keycard = tot_keycard + res_line.betrieb_gast

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass

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
            s_list.rev =  to_decimal(s_list.rev) + to_decimal(cl_list.zipreis)
            s_list.arr =  to_decimal(s_list.arr) + to_decimal(cl_list.lodging)
            tot_qty = tot_qty + cl_list.qty
            tot_rev =  to_decimal(tot_rev) + to_decimal(cl_list.zipreis)

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
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")


        for s_list in query(s_list_data):
            s_list.proz_qty = ( to_decimal(s_list.anz) / to_decimal(tot_qty)) * to_decimal("100")
            s_list.proz_rev = ( to_decimal(s_list.rev) / to_decimal(tot_rev)) * to_decimal("100")


    def create_genstat_inhouse():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, frate, exchg_rate, ct, contcode, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, tot_qty, tot_rev, queasy, htparam, waehrung, artikel, nation, zkstat, zinrstat, paramtext, guest, reservation, zimmer, sourccod, arrangement, bill, res_line, guest_pr, guestseg, segment, bill_line, argt_line, mc_guest, mc_types, reslin_queasy, genstat
        nonlocal sorttype, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany
        nonlocal waehrung1, artikel1, nation1


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, zikat_list, waehrung1, artikel1, nation1
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        i:int = 0
        j:int = 0
        vip_flag:string = ""
        nr:int = 0
        str:string = ""
        actflag1:int = 0
        actflag2:int = 0
        do_it:bool = False
        gmember = None
        gbuff = None
        rbuff = None
        buff_art = None
        z:int = 0
        Gmember =  create_buffer("Gmember",Guest)
        Gbuff =  create_buffer("Gbuff",Guest)
        Rbuff =  create_buffer("Rbuff",Reservation)
        Buff_art =  create_buffer("Buff_art",Artikel)
        zinr_list_data.clear()

        if from_date == curr_date and to_date == curr_date:
            actflag1 = 1
            actflag2 = 1
        else:
            actflag1 = 1
            actflag2 = 2
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        tot_qty = 0
        tot_rev =  to_decimal("0")
        s_list_data.clear()
        cl_list_data.clear()
        str_list_data.clear()
        tot_avail = 0

        zkstat_obj_list = {}
        print("Zkstat.")
        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum >= from_date) & (Zkstat.datum <= to_date)).order_by(Zkstat._recid).all():
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == zkstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if zkstat_obj_list.get(zkstat._recid):
                continue
            else:
                zkstat_obj_list[zkstat._recid] = True


            tot_avail = tot_avail + zkstat.anz100

        genstat_obj_list = {}
        # for genstat, reservation, guest, gmember, sourccod in db_session.query(Genstat, Reservation, Guest, Gmember, Sourccod).join(Reservation,(Reservation.resnr == Genstat.resnr)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Gmember,(Gmember.gastnr == Genstat.gastnrmember)).join(Sourccod,(Sourccod.source_code == Reservation.resart)).filter(
        #          (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.zinr >= (froom).lower()) & (Genstat.zinr <= (troom).lower())).order_by(Genstat.zinr, Genstat.datum, Genstat.erwachs.desc(), Gmember.name).all():

        recs = db_session.query(Genstat, Reservation, Guest, Gmember, Sourccod).join(Reservation,(Reservation.resnr == Genstat.resnr)).join(Guest,(Guest.gastnr == Genstat.gastnr)).join(Gmember,(Gmember.gastnr == Genstat.gastnrmember)).join(Sourccod,(Sourccod.source_code == Reservation.resart)).filter(
                 (Genstat.datum >= from_date) & 
                 (Genstat.datum <= to_date) & 
                 (Genstat.zinr >= (froom).lower()) & 
                 (Genstat.zinr <= (troom).lower())).order_by(Genstat.zinr, Genstat.datum, Genstat.erwachs.desc(), Gmember.name).all()
        print("Genstat:", len(recs))
        for genstat, reservation, guest, gmember, sourccod in recs:
            zikat_list = query(zikat_list_data, (lambda zikat_list: zikat_list.zikatnr == genstat.zikatnr and zikat_list.selected), first=True)
            if not zikat_list:
                continue

            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True

            if exc_depart and genstat.res_date[0] <= genstat.datum and genstat.res_date[1] == genstat.datum and genstat.resstatus == 8:
                pass
            else:

                res_line = get_cache (Res_line, {"resnr": [(eq, genstat.resnr)],"reslinnr": [(eq, genstat.res_int[0])]})

                setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

                zimmer = get_cache (Zimmer, {"zinr": [(eq, genstat.zinr)]})

                bill = get_cache (Bill, {"resnr": [(eq, genstat.resnr)]})
                nr = nr + 1
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                         (Guestseg.gastnr == gmember.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
                    vip_flag = replace_str(segment.bezeich, " ", "")
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.nr = nr
                cl_list.rmcat = zikat_list.kurzbez + setup_list.char
                cl_list.kurzbez = zikat_list.kurzbez
                cl_list.bezeich = zikat_list.bezeich
                cl_list.nat = gmember.nation1
                cl_list.resnr = genstat.resnr
                cl_list.vip = vip_flag
                cl_list.firstname = right_trim(gmember.vorname1, chr_unicode(10))
                cl_list.firstname = right_trim(cl_list.firstname, chr_unicode(13))
                cl_list.firstname = replace_str(cl_list.firstname, chr_unicode(10) , " ")
                cl_list.lastname = right_trim(gmember.name, chr_unicode(10))
                cl_list.lastname = right_trim(cl_list.lastname, chr_unicode(13))
                cl_list.lastname = replace_str(cl_list.lastname, chr_unicode(10) , " ")

                if gmember.geburtdatum1 == None:
                    cl_list.birthdate = ""
                else:
                    cl_list.birthdate = to_string(gmember.geburtdatum1, "99/99/9999")
                cl_list.rmno = genstat.zinr
                cl_list.zipreis =  to_decimal(genstat.zipreis)
                cl_list.arrive = genstat.res_date[0]
                cl_list.depart = genstat.res_date[1]
                cl_list.qty = 1
                cl_list.a = genstat.erwachs
                cl_list.c = genstat.kind1 + genstat.kind2 + genstat.kind3
                cl_list.co = genstat.gratis
                cl_list.argt = genstat.argt
                cl_list.flight = substring(res_line.flight_nr, 11, 6)
                cl_list.etd = substring(res_line.flight_nr, 17, 5)
                cl_list.ci_time = to_string(res_line.ankzeit, "HH:MM")
                cl_list.co_time = to_string(res_line.abreisezeit, "HH:MM")
                cl_list.paym = genstat.segmentcode
                cl_list.created = reservation.resdat
                cl_list.createid = reservation.useridanlage
                cl_list.inhousedate = genstat.datum
                cl_list.sob = sourccod.bezeich
                cl_list.gastnr = gmember.gastnr
                cl_list.telefon = gmember.telefon
                cl_list.mobil_tel = gmember.mobil_telefon
                cl_list.email = gmember.email_adr
                cl_list.lodging =  to_decimal(genstat.logis)
                cl_list.rechnr = bill.rechnr
                cl_list.breakfast =  to_decimal(genstat.res_deci[1])
                cl_list.lunch =  to_decimal(genstat.res_deci[2])
                cl_list.dinner =  to_decimal(genstat.res_deci[3])
                cl_list.otherev =  to_decimal(genstat.res_deci[4])
                cl_list.night = to_string(genstat.res_date[1] - genstat.res_date[0], ">>>>9")
                cl_list.city = gmember.wohnort
                cl_list.keycard = to_string(res_line.betrieb_gast, ">>>>>9")
                cl_list.etage = zimmer.etage
                cl_list.zinr_bez = zimmer.bezeich


                cl_list.c_zipreis = to_string(cl_list.zipreis, "->>,>>>,>>>,>>9.99")
                cl_list.c_lodging = to_string(cl_list.lodging, "->>,>>>,>>>,>>9.99")
                cl_list.c_breakfast = to_string(cl_list.breakfast, "->>,>>>,>>>,>>9.99")
                cl_list.c_lunch = to_string(cl_list.lunch, "->>,>>>,>>>,>>9.99")
                cl_list.c_dinner = to_string(cl_list.dinner, "->>,>>>,>>>,>>9.99")
                cl_list.c_otherev = to_string(cl_list.otherev, "->>,>>>,>>>,>>9.99")
                cl_list.c_a = to_string(cl_list.a, "9")
                cl_list.c_c = to_string(cl_list.c, "9")
                cl_list.c_co = to_string(cl_list.co, ">9")
                cl_list.c_rechnr = to_string(cl_list.rechnr, ">>>>>9")
                cl_list.c_resnr = to_string(cl_list.resnr, ">>>>>9")

                if res_line.resstatus != 11 and res_line.resstatus != 13:
                    cl_list.flag_guest = 1


                else:
                    cl_list.flag_guest = 2

                bill_line_obj_list = {}
                bill_line = Bill_line()
                buff_art = Artikel()
                for bill_line.artnr, bill_line._recid, buff_art.umsatzart, buff_art.zwkum, buff_art._recid in db_session.query(Bill_line.artnr, Bill_line._recid, Buff_art.umsatzart, Buff_art.zwkum, Buff_art._recid).join(Buff_art,(Buff_art.artnr == Bill_line.artnr) & (Buff_art.departement == Bill_line.departement)).filter(
                         (Bill_line.rechnr == bill.rechnr) & (Bill_line.betrag < 0)).order_by(Bill_line._recid).all():
                    if bill_line_obj_list.get(bill_line._recid):
                        continue
                    else:
                        bill_line_obj_list[bill_line._recid] = True

                    if (buff_art.artart == 2 or buff_art.artart == 5 or buff_art.artart == 6 or buff_art.artart == 7):
                        cl_list.pay_art = cl_list.pay_art + to_string(bill_line.artnr) + ","
                cl_list.pay_art = substring(cl_list.pay_art, 0, length(cl_list.pay_art) - 1)

                nation1 = get_cache (Nation, {"kurzbez": [(eq, gmember.nation2)]})

                if nation1:
                    cl_list.localreg = gmember.nation2 + " - " + nation1.bezeich

                mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gmember.gastnr)]})

                if mc_guest:
                    cl_list.memberno = mc_guest.cardnum

                    mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                    if mc_types:
                        cl_list.membertype = mc_types.bezeich

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    cl_list.curr = waehrung.wabkurz

                segment = get_cache (Segment, {"segmentcode": [(eq, genstat.segmentcode)]})

                if segment:
                    cl_list.segm = entry(0, segment.bezeich, "$$0")

                if guest.karteityp != 0:
                    cl_list.company = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

                if cl_list.nat == "":
                    cl_list.nat = "?"

                if genstat.resstatus == 13:
                    cl_list.qty = 0

                if incl_gcomment:

                    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                    if gbuff:

                        if gbuff.bemerkung != None:
                            for i in range(1,length(gbuff.bemerkung)  + 1) :

                                if substring(gbuff.bemerkung, i - 1, 1) == chr_unicode(10):
                                    cl_list.bemerk = cl_list.bemerk + " "
                                else:
                                    cl_list.bemerk = cl_list.bemerk + substring(trim(gbuff.bemerkung) , i - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + " || "

                if incl_rsvcomment:

                    rbuff = get_cache (Reservation, {"resnr": [(eq, reservation.resnr)]})

                    if rbuff:
                        for j in range(1,length(rbuff.bemerk)  + 1) :

                            if substring(rbuff.bemerk, j - 1, 1) == chr_unicode(10):
                                cl_list.bemerk1 = cl_list.bemerk1 + " "
                            else:
                                cl_list.bemerk1 = cl_list.bemerk1 + substring(trim(rbuff.bemerk) , j - 1, 1)
                    cl_list.bemerk = cl_list.bemerk + cl_list.bemerk1

                if not incl_gcomment and not incl_rsvcomment:
                    cl_list.bemerk = trim(replace_str(res_line.bemerk, chr_unicode(10) , " "))

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"date1": [(le, genstat.datum)],"date2": [(ge, genstat.datum)]})

                if reslin_queasy:

                    if reslin_queasy.char2 != "":
                        cl_list.ratecode = reslin_queasy.char2
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 6) == ("$CODE$").lower() :
                                cl_list.ratecode = substring(str, 6)
                                break
                cl_list.pax = to_string(cl_list.a, ">9") + "/" + to_string(cl_list.c, "9") + " " + to_string(cl_list.co, "9")

                if cl_list.nat == "":
                    cl_list.nat = "?"
                else:

                    nation = get_cache (Nation, {"kurzbez": [(eq, cl_list.nat)]})

                    if nation:
                        cl_list.nation = nation.bezeich

                zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.zinr == genstat.zinr and zinr_list.resnr == res_line.resnr and zinr_list.reslinnr == res_line.reslinnr and zinr_list.datum == genstat.datum), first=True)

                if not zinr_list:
                    zinr_list = Zinr_list()
                    zinr_list_data.append(zinr_list)

                    zinr_list.resnr = res_line.resnr
                    zinr_list.reslinnr = res_line.reslinnr
                    zinr_list.zinr = genstat.zinr
                    zinr_list.datum = genstat.datum

                    queasy = get_cache (Queasy, {"key": [(eq, 14)],"char1": [(eq, genstat.zinr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                    if zimmer.sleeping and genstat.resstatus != 13:

                        if not queasy:
                            tot_rm = tot_rm + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_rm = tot_rm + 1

                    if zimmer.sleeping and genstat.zipreis > 0 and genstat.resstatus != 13:
                        z = z + 1

                        if not queasy:
                            tot_payrm = tot_payrm + 1

                        elif queasy and queasy.number3 != genstat.gastnr:
                            tot_payrm = tot_payrm + 1

                    elif not zimmer.sleeping:

                        if queasy and queasy.number3 != genstat.gastnr and genstat.zipreis > 0:
                            tot_rm = tot_rm + 1
                        inactive = inactive + 1
                tot_a = tot_a + genstat.erwachs
                tot_c = tot_c + genstat.kind1 + genstat.kind2 + genstat.kind3
                tot_co = tot_co + genstat.gratis
                tot_keycard = tot_keycard + res_line.betrieb_gast

            if not disp_accompany:

                cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.rmno == res_line.zinr and cl_list.resnr == res_line.resnr and cl_list.arrive == res_line.ankunft and cl_list.zipreis == 0 and (cl_list.a + cl_list.c) < 1 and cl_list.co < 1), first=True)

                if cl_list:
                    cl_list_data.remove(cl_list)
                    pass
        print("CL_List.")
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
            s_list.rev =  to_decimal(s_list.rev) + to_decimal(cl_list.zipreis)
            s_list.arr =  to_decimal(s_list.arr) + to_decimal(cl_list.lodging)
            tot_qty = tot_qty + cl_list.qty
            tot_rev =  to_decimal(tot_rev) + to_decimal(cl_list.zipreis)

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

        print("S_List1.")
        if (tot_a + tot_co) != 0:

            for s_list in query(s_list_data, filters=(lambda s_list: s_list.nat != "")):

                nation = get_cache (Nation, {"kurzbez": [(eq, s_list.nat)]})

                if nation:
                    s_list.nat = nation.bezeich
                s_list.proz =  to_decimal(s_list.adult) / to_decimal((tot_a) + to_decimal(tot_co)) * to_decimal("100")

        print("S_List2.")
        for s_list in query(s_list_data):
            s_list.proz_qty = ( to_decimal(s_list.anz) / to_decimal(tot_qty)) * to_decimal("100")
            s_list.proz_rev = ( to_decimal(s_list.rev) / to_decimal(tot_rev)) * to_decimal("100")


    def create_buf_queasy():

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, frate, exchg_rate, ct, contcode, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, tot_qty, tot_rev, queasy, htparam, waehrung, artikel, nation, zkstat, zinrstat, paramtext, guest, reservation, zimmer, sourccod, arrangement, bill, res_line, guest_pr, guestseg, segment, bill_line, argt_line, mc_guest, mc_types, reslin_queasy, genstat
        nonlocal sorttype, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany
        nonlocal waehrung1, artikel1, nation1


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, zikat_list, waehrung1, artikel1, nation1
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data


        t_buff_queasy_data.clear()

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 140) & (Queasy.char1 == (prog_name).lower())).order_by(Queasy._recid).all():
            t_buff_queasy = T_buff_queasy()
            t_buff_queasy_data.append(t_buff_queasy)

            buffer_copy(queasy, t_buff_queasy)


    def get_argtline_rate(contcode:string, argt_recid:int):

        nonlocal tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, tot_keycard, cl_list_data, s_list_data, t_buff_queasy_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, tot_room, all_room, frate, exchg_rate, ct, bfast_art, lunch_art, dinner_art, lundin_art, fb_dept, argt_betrag, take_it, prcode, qty, r_qty, lodge_betrag, f_betrag, s, tot_qty, tot_rev, queasy, htparam, waehrung, artikel, nation, zkstat, zinrstat, paramtext, guest, reservation, zimmer, sourccod, arrangement, bill, res_line, guest_pr, guestseg, segment, bill_line, argt_line, mc_guest, mc_types, reslin_queasy, genstat
        nonlocal sorttype, from_date, to_date, curr_date, curr_gastnr, froom, troom, exc_depart, incl_gcomment, incl_rsvcomment, prog_name, disp_accompany
        nonlocal waehrung1, artikel1, nation1


        nonlocal setup_list, str_list, cl_list, s_list, zinr_list, t_buff_queasy, zikat_list, waehrung1, artikel1, nation1
        nonlocal setup_list_data, str_list_data, cl_list_data, s_list_data, zinr_list_data, t_buff_queasy_data

        add_it = False
        f_betrag = to_decimal("0.0")
        argt_betrag = to_decimal("0.0")
        qty = 0
        curr_zikatnr:int = 0
        argtline = None

        def generate_inner_output():
            return (add_it, f_betrag, argt_betrag, qty)

        Argtline =  create_buffer("Argtline",Argt_line)

        if res_line.l_zuordnung[0] != 0:
            curr_zikatnr = res_line.l_zuordnung[0]
        else:
            curr_zikatnr = res_line.zikatnr

        argtline = get_cache (Argt_line, {"_recid": [(eq, argt_recid)]})

        if argt_line.vt_percnt == 0:

            if argt_line.betriebsnr == 0:
                qty = res_line.erwachs
            else:
                qty = argt_line.betriebsnr

        elif argt_line.vt_percnt == 1:
            qty = res_line.kind1

        elif argt_line.vt_percnt == 2:
            qty = res_line.kind2

        if qty > 0:

            if argtline.fakt_modus == 1:
                add_it = True

            elif argtline.fakt_modus == 2:

                if res_line.ankunft == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 3:

                if (res_line.ankunft + 1) == curr_date:
                    add_it = True

            elif argtline.fakt_modus == 4 and get_day(curr_date) == 1:
                add_it = True

            elif argtline.fakt_modus == 5 and get_day(curr_date + 1) == 1:
                add_it = True

            elif argtline.fakt_modus == 6:

                if (res_line.ankunft + (argtline.intervall - 1)) >= curr_date:
                    add_it = True

        if add_it:

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fargt-line")],"char1": [(eq, "")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"number1": [(eq, argtline.departement)],"number2": [(eq, argtline.argtnr)],"number3": [(eq, argtline.argt_artnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

            if reslin_queasy:
                argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                f_betrag =  to_decimal(argt_betrag)

                waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                if argt_betrag == 0:
                    add_it = False

                return generate_inner_output()

            if contcode != "":

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "argt-line")],"char1": [(eq, contcode)],"number1": [(eq, res_line.reserve_int)],"number2": [(eq, arrangement.argtnr)],"number3": [(eq, argtline.argt_artnr)],"resnr": [(eq, argtline.departement)],"reslinnr": [(eq, curr_zikatnr)],"date1": [(le, curr_date)],"date2": [(ge, curr_date)]})

                if reslin_queasy:
                    argt_betrag =  to_decimal(reslin_queasy.deci1) * to_decimal(qty)
                    f_betrag =  to_decimal(argt_betrag)

                    waehrung = get_cache (Waehrung, {"_recid": [(eq, waehrung1._recid)]})

                    if argt_betrag == 0:
                        add_it = False

                    return generate_inner_output()
            argt_betrag =  to_decimal(argt_line.betrag)

            arrangement = get_cache (Arrangement, {"argtnr": [(eq, argt_line.argtnr)]})

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, arrangement.betriebsnr)]})
            f_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if res_line.betriebsnr != arrangement.betriebsnr:
                argt_betrag =  to_decimal(argt_betrag) * to_decimal((waehrung.ankauf) / to_decimal(waehrung.einheit)) / to_decimal(frate)
            argt_betrag =  to_decimal(argt_betrag) * to_decimal(qty)

            if argt_betrag == 0:
                add_it = False

        return generate_inner_output()


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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})
    bfast_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 126)]})
    fb_dept = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})
    lunch_art = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})
    dinner_art = htparam.finteger
    bed_setup()

    if sorttype == 1:

        if from_date >= curr_date:
            create_inhouse()
        else:
            create_genstat_inhouse()
    create_buf_queasy()

    if to_date < curr_date:

        for zkstat in db_session.query(Zkstat).filter(
                 (Zkstat.datum == to_date)).order_by(Zkstat._recid).all():
            tot_room = tot_room + zkstat.anz100

        zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "tot-rm")],"datum": [(eq, to_date)]})

        if zinrstat:
            all_room = zinrstat.zimmeranz
        inactive = all_room - tot_room

    return generate_output()