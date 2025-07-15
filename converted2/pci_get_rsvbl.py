#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Guest, Res_line, Htparam, Zimmer, Guestbook, Arrangement, Waehrung, Zimkateg, Queasy, Mc_guest, Mc_types, Reslin_queasy

def pci_get_rsvbl(resno:int):

    prepare_cache ([Guest, Res_line, Htparam, Arrangement, Waehrung, Zimkateg, Queasy, Mc_guest, Mc_types, Reslin_queasy])

    msg_str = ""
    result_message = ""
    arrival_guest_data = []
    ci_date:date = None
    billdate:date = None
    loopi:int = 0
    str:string = ""
    curr_arrive:string = ""
    curr_depart:string = ""
    pos:int = 0
    pos1:int = 0
    ccname:string = ""
    ccnr:string = ""
    expire_date:string = ""
    s1:string = ""
    curr_birth:string = ""
    curr_expireid:string = ""
    post_it:bool = False
    pdafirstdate:date = None
    pdalastdate:date = None
    vat_art:Decimal = to_decimal("0.0")
    service_art:Decimal = to_decimal("0.0")
    vat2_art:Decimal = to_decimal("0.0")
    fact_art:Decimal = to_decimal("0.0")
    fcost:Decimal = to_decimal("0.0")
    service:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    vat2:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    totrsvamt:Decimal = to_decimal("0.0")
    tot_room:int = 0
    occ_room:int = 0
    occ_perc:Decimal = to_decimal("0.0")
    occ1:Decimal = None
    occ2:Decimal = to_decimal("0.0")
    curr_co_date:date = None
    price_decimal:int = 0
    stat_list:List[string] = create_empty_list(10,"")
    guest = res_line = htparam = zimmer = guestbook = arrangement = waehrung = zimkateg = queasy = mc_guest = mc_types = reslin_queasy = None

    arrival_guest = fix_cost = bguest = rline = None

    arrival_guest_data, Arrival_guest = create_model("Arrival_guest", {"utype":string, "uid":string, "rmstaystatus":string, "rmsmoking":string, "rmtype":string, "rmno":string, "rmqty":string, "rmfloor":string, "rmdesc":string, "rmstatus":string, "rm_maxperson":string, "rate_view":string, "rate_code":string, "rate_prepaid":string, "rate_desc":string, "pax_age":string, "pax_count":string, "arrive":string, "depart":string, "code_guaranteed":string, "cc_number":string, "cc_code":string, "expire_date":string, "tamount_before":string, "tamount_after":string, "tamount_currency":string, "tamount_decimal":string, "member_id":string, "member_bonus":string, "member_travel":string, "member_program":string, "member_point":string, "gcomment_view":string, "gcomment_desc":string, "guest_type":string, "guest_context":string, "guest_id":string, "guest_birth":string, "guest_sex":string, "guest_fname":string, "guest_mname":string, "guest_lname":string, "guest_sname":string, "guest_pname":string, "guest_phone":string, "guest_ccountry":string, "guest_carea":string, "guest_email":string, "guest_addtype":string, "guest_address":string, "guest_city":string, "guest_pcode":string, "guest_prov":string, "guest_country":string, "guest_company":string, "guest_doc_country":string, "guest_doc_nation":string, "guest_expire":string, "guest_effective":string, "guest_birthdate":string, "guest_gender":string, "guest_cardno":string, "guest_cardtype":string, "guest_member_name":string, "guest_member_expire":string, "guest_member_effective":string, "guest_member_id":string, "spr_code":string, "spr_name":string, "spr_desc":string, "total_rsv_amount":string, "rsv_number":int, "rsvline_number":int, "argt_code":string, "room_sharer":string, "accompaying_guest":string, "image_flag":string, "arrival_time":string, "occupancy_today":string})
    fix_cost_data, Fix_cost = create_model("Fix_cost", {"resnr":string, "reslinnr":string, "fc_ratecode":string, "fc_rstatus":string, "fc_inclusive":string, "fc_name":string, "fc_quantity":string, "fc_type":string, "fc_exdate":string, "fc_efdate":string, "fc_amtbefore":string, "fc_amtafter":string, "fc_curr":string, "fc_decimal":string, "fc_tax_code":string, "fc_tax_decimal":string, "fc_tax_amount":string})

    Bguest = create_buffer("Bguest",Guest)
    Rline = create_buffer("Rline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, result_message, arrival_guest_data, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_data, fix_cost_data

        return {"msg_str": msg_str, "result_message": result_message, "arrival-guest": arrival_guest_data}

    def calc_occ():

        nonlocal msg_str, result_message, arrival_guest_data, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_data, fix_cost_data

        do_it:bool = False
        bresline = None
        Bresline =  create_buffer("Bresline",Res_line)

        if occ1 == None:

            for bresline in db_session.query(Bresline).filter(
                     (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.ankunft <= ci_date) & (Bresline.abreise > ci_date) & (Bresline.l_zuordnung[inc_value(2)] == 0)).order_by(Bresline._recid).all():
                do_it = True

                if bresline.zinr != "":

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                    do_it = zimmer.sleeping

                if do_it:
                    occ_room = occ_room + bresline.zimmeranz
            occ1 =  to_decimal(occ_room) / to_decimal(tot_room) * to_decimal("100")

        for bresline in db_session.query(Bresline).filter(
                     (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.ankunft <= curr_co_date) & (Bresline.abreise > curr_co_date) & (Bresline.l_zuordnung[inc_value(2)] == 0)).order_by(Bresline._recid).all():
            do_it = True

            if bresline.zinr != "":

                zimmer = get_cache (Zimmer, {"zinr": [(eq, bresline.zinr)]})
                do_it = zimmer.sleeping

            if do_it:
                occ_room = occ_room + bresline.zimmeranz
        occ2 =  to_decimal(occ_room) / to_decimal(tot_room) * to_decimal("100")

        if occ1 > occ2:
            occ_perc =  to_decimal(occ1)
        else:
            occ_perc =  to_decimal(occ2)


    def search_by_resnr():

        nonlocal msg_str, result_message, arrival_guest_data, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_data, fix_cost_data

        voucher_found:bool = False
        curr_i:int = 0
        curr_str:string = ""
        voucherno:string = ""
        total_pax:int = 0
        voucher_found = True

        if voucher_found:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.active_flag == 0)).order_by(Res_line._recid).all():

                arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
                result_message = "0 - Reservation Found Success."
                total_pax = 0
                total_pax = res_line.erwachs + kind1
                curr_arrive = to_string(res_line.ankunft, "99/99/9999")
                curr_depart = to_string(res_line.abreise, "99/99/9999")


                arrival_guest = Arrival_guest()
                arrival_guest_data.append(arrival_guest)

                arrival_guest.utype = " "
                arrival_guest.uid = to_string(res_line.resnr)
                arrival_guest.rmstaystatus = "Reserved"
                arrival_guest.rmqty = to_string(res_line.zimmeranz)
                arrival_guest.pax_age = " "
                arrival_guest.pax_count = to_string(total_pax)
                arrival_guest.arrive = entry(2, curr_arrive, "/") + "-" + entry(1, curr_arrive, "/") + "-" + entry(0, curr_arrive, "/")
                arrival_guest.depart = entry(2, curr_depart, "/") + "-" + entry(1, curr_depart, "/") + "-" + entry(0, curr_depart, "/")
                arrival_guest.code_guaranteed = " "
                arrival_guest.gcomment_view = "FALSE"
                arrival_guest.gcomment_desc = " "
                arrival_guest.rsv_number = res_line.resnr
                arrival_guest.rsvline_number = res_line.reslinnr
                arrival_guest.tamount_decimal = to_string(price_decimal)
                arrival_guest.argt_code = res_line.arrangement + "-" + arrangement.argt_bez
                arrival_guest.arrival_time = to_string(res_line.ankzeit, "HH:MM:SS")

                waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

                if waehrung:
                    arrival_guest.tamount_currency = waehrung.wabkurz

                if res_line.zinr != "":
                    arrival_guest.rmno = res_line.zinr

                    zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                    if zimmer:

                        if matches(zimmer.himmelsr,r"*NS*") or matches(zimmer.himmelsr,r"*Non Smoking*"):
                            arrival_guest.rmsmoking = "TRUE"

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})

                        if zimkateg:
                            arrival_guest.rmtype = zimkateg.kurzbez
                            arrival_guest.rmdesc = zimkateg.bezeichnung


                        arrival_guest.rmfloor = to_string(zimmer.etage)
                        arrival_guest.rm_maxperson = to_string(zimmer.personen)

                if matches(res_line.zimmer_wunsch,r"*PCIFLAG*"):
                    arrival_guest.gcomment_desc = "GUEST ALREADY PCI"

                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnr) & ((Guest.karteityp == 0) | (Guest.karteityp == 1))).first()

                if guest:
                    arrival_guest.rate_view = "TRUE"
                    arrival_guest.rate_prepaid = "FALSE"


                    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                        str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

                        if substring(str, 0, 6) == ("$CODE$").lower() :
                            arrival_guest.rate_code = substring(str, 6)

                    queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, arrival_guest.rate_code)]})

                    if queasy:
                        arrival_guest.rate_desc = queasy.char2

                bguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if bguest:
                    curr_birth = to_string(bguest.geburtdatum1, "99/99/9999")
                    curr_expireid = to_string(bguest.geburtdatum2, "99/99/9999")
                    arrival_guest.guest_type = "1"
                    arrival_guest.guest_context = " "
                    arrival_guest.guest_id = to_string(bguest.gastnr)
                    arrival_guest.guest_birth = entry(2, curr_birth, "/") + "-" + entry(1, curr_birth, "/") + "-" + entry(0, curr_birth, "/")
                    arrival_guest.guest_sex = bguest.geschlecht
                    arrival_guest.guest_fname = bguest.vorname1
                    arrival_guest.guest_mname = " "
                    arrival_guest.guest_lname = bguest.name
                    arrival_guest.guest_sname = " "
                    arrival_guest.guest_pname = bguest.anrede1
                    arrival_guest.guest_phone = bguest.mobil_telefon
                    arrival_guest.guest_ccountry = " "
                    arrival_guest.guest_carea = " "
                    arrival_guest.guest_email = bguest.email_adr
                    arrival_guest.guest_addtype = " "
                    arrival_guest.guest_address = bguest.adresse1 + " " + bguest.adresse2 + " " + bguest.adresse3
                    arrival_guest.guest_city = bguest.wohnort
                    arrival_guest.guest_pcode = bguest.plz
                    arrival_guest.guest_prov = bguest.geburt_ort2
                    arrival_guest.guest_country = bguest.land
                    arrival_guest.guest_company = " "
                    arrival_guest.guest_doc_country = " "
                    arrival_guest.guest_doc_nation = bguest.nation1
                    arrival_guest.guest_expire = entry(2, curr_expireid, "/") + "-" + entry(1, curr_expireid, "/") + "-" + entry(0, curr_expireid, "/")
                    arrival_guest.guest_effective = " "
                    arrival_guest.guest_birthdate = entry(2, curr_birth, "/") + "-" + entry(1, curr_birth, "/") + "-" + entry(0, curr_birth, "/")
                    arrival_guest.guest_gender = bguest.geschlecht
                    arrival_guest.guest_cardno = bguest.ausweis_nr1
                    arrival_guest.guest_cardtype = ""

                    if bguest.ausweis_nr2 != "":
                        pos = get_index(bguest.ausweis_nr2, "\\")
                        ccname = trim(substring(bguest.ausweis_nr2, 0, pos - 1))
                        s1 = trim(substring(bguest.ausweis_nr2, pos + 1 - 1, length(bguest.ausweis_nr2) - pos))
                        pos1 = get_index(s1, "\\")

                        if pos1 != 0 and pos1 < length(s1):
                            ccnr = trim(substring(s1, 0, pos1 - 1))
                            expire_date = trim(substring(s1, pos1 + 1 - 1, length(s1) - pos1))


                        else:
                            ccnr = s1
                        ccnr = replace_str(ccnr, " ", "")
                        ccnr = "XXXXXXXXXXXX" + substring(ccnr, 12)


                        arrival_guest.cc_number = ccname
                        arrival_guest.cc_code = ccnr
                        arrival_guest.expire_date = expire_date

                    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, bguest.gastnr)]})

                    if mc_guest:
                        arrival_guest.member_id = mc_guest.cardnum
                        arrival_guest.member_bonus = " "
                        arrival_guest.member_travel = " "
                        arrival_guest.member_point = " "
                        arrival_guest.guest_member_name = bguest.name
                        arrival_guest.guest_member_expire = to_string(mc_guest.tdate, "99/99/9999")
                        arrival_guest.guest_member_effective = to_string(mc_guest.created_date, "99/99/9999")
                        arrival_guest.guest_member_id = mc_guest.cardnum

                        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                        if mc_types:
                            arrival_guest.member_program == mc_types.bezeich

                reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

                if reslin_queasy:
                    arrival_guest.spr_code = reslin_queasy.char3
                    arrival_guest.spr_name = reslin_queasy.char3


                    for loopi in range(1,num_entries(reslin_queasy.char3, ";")  + 1) :

                        queasy = get_cache (Queasy, {"key": [(eq, 189)],"char1": [(eq, entry(loopi - 1, reslin_queasy.char3, ";"))]})

                        if queasy and queasy.logi3 :
                            arrival_guest.spr_desc = entry(loopi - 1, reslin_queasy.char3, ";") + ";" + arrival_guest.spr_desc

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy.date1).all():
                    totrsvamt =  to_decimal(totrsvamt) + to_decimal(reslin_queasy.deci1)


                arrival_guest.total_rsv_amount = to_string(totrsvamt)

            arrival_guest = query(arrival_guest_data, first=True)

            if not arrival_guest:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.resnr == resno) & (Res_line.active_flag == 1)).order_by(Res_line._recid).all():

                    if res_line.resstatus == 6:
                        result_message = "2 - Guest Already Checkin."

                    return
        else:
            result_message = "1 - Booking Code Not Found."


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal msg_str, result_message, arrival_guest_data, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_data, fix_cost_data

        post_it = False
        delta:int = 0
        start_date:date = None
        curr_date:date = None

        def generate_inner_output():
            return (post_it)

        curr_date = billdate

        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if lfakt == None:
                delta = 0
            else:
                delta = (lfakt - res_line.ankunft).days

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + timedelta(days=delta)

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    stat_list[0] = "VC"
    stat_list[1] = "VCU"
    stat_list[2] = "VD"
    stat_list[3] = "ED"
    stat_list[4] = "OD"
    stat_list[5] = "OC"
    ci_date = get_output(htpdate(87))
    billdate = get_output(htpdate(110))
    search_by_resnr()

    for arrival_guest in query(arrival_guest_data):

        zimmer = get_cache (Zimmer, {"zinr": [(eq, arrival_guest.rmno)]})

        if zimmer:
            arrival_guest.rmstatus = stat_list[zimmer.zistatus + 1 - 1]

        res_line = get_cache (Res_line, {"resnr": [(eq, arrival_guest.rsv_number)],"resstatus": [(eq, 11)],"zinr": [(eq, arrival_guest.rmno)],"active_flag": [(eq, 0)]})

        if res_line:

            if res_line.l_zuordnung[2] != 0:
                arrival_guest.accompaying_guest = res_line.name
            else:
                arrival_guest.room_sharer = res_line.name

        guestbook = get_cache (Guestbook, {"gastnr": [(eq, to_int(arrival_guest.guest_id))]})

        if guestbook:
            arrival_guest.image_flag = "0 image id already exist"
        else:
            arrival_guest.image_flag = "1 image id still empty"
        curr_co_date = date_mdy(arrival_guest.depart)

    zimmer = db_session.query(Zimmer).filter(
             (Zimmer.sleeping)).first()
    while None != zimmer:
        tot_room = tot_room + 1

        curr_recid = zimmer._recid
        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.sleeping) & (Zimmer._recid > curr_recid)).first()
    calc_occ()

    for arrival_guest in query(arrival_guest_data):
        arrival_guest.occupancy_today = to_string(occ_perc)

    return generate_output()