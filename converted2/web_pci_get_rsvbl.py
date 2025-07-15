#using conversion tools version: 1.0.0.45

from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Guest, Res_line, Htparam, Zimmer, Guestbook, Bresline, Arrangement, Waehrung, Zimkateg, Queasy, Mc_guest, Mc_types, Reslin_queasy

def web_pci_get_rsvbl(resno:int):
    msg_str = ""
    result_message = ""
    arrival_guest_list = []
    ci_date:date = None
    billdate:date = None
    loopi:int = 0
    str:str = ""
    curr_arrive:str = ""
    curr_depart:str = ""
    pos:int = 0
    pos1:int = 0
    ccname:str = ""
    ccnr:str = ""
    expire_date:str = ""
    s1:str = ""
    curr_birth:str = ""
    curr_expireid:str = ""
    post_it:bool = False
    pdafirstdate:date = None
    pdalastdate:date = None
    vat_art:decimal = to_decimal("0.0")
    service_art:decimal = to_decimal("0.0")
    vat2_art:decimal = to_decimal("0.0")
    fact_art:decimal = to_decimal("0.0")
    fcost:decimal = to_decimal("0.0")
    service:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    vat2:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    totrsvamt:decimal = to_decimal("0.0")
    tot_room:int = 0
    occ_room:int = 0
    occ_perc:decimal = to_decimal("0.0")
    occ1:decimal = None
    occ2:decimal = to_decimal("0.0")
    curr_co_date:date = None
    price_decimal:int = 0
    stat_list:List[str] = create_empty_list(10,"")
    guest = res_line = htparam = zimmer = guestbook = bresline = arrangement = waehrung = zimkateg = queasy = mc_guest = mc_types = reslin_queasy = None

    arrival_guest = fix_cost = bguest = rline = None

    arrival_guest_list, Arrival_guest = create_model("Arrival_guest", {"utype":str, "uid":str, "rmstaystatus":str, "rmsmoking":str, "rmtype":str, "rmno":str, "rmqty":str, "rmfloor":str, "rmdesc":str, "rmstatus":str, "rm_maxperson":str, "rate_view":str, "rate_code":str, "rate_prepaid":str, "rate_desc":str, "pax_age":str, "pax_count":str, "arrive":str, "depart":str, "code_guaranteed":str, "cc_number":str, "cc_code":str, "expire_date":str, "tamount_before":str, "tamount_after":str, "tamount_currency":str, "tamount_decimal":str, "member_id":str, "member_bonus":str, "member_travel":str, "member_program":str, "member_point":str, "gcomment_view":str, "gcomment_desc":str, "guest_type":str, "guest_context":str, "guest_id":str, "guest_birth":str, "guest_sex":str, "guest_fname":str, "guest_mname":str, "guest_lname":str, "guest_sname":str, "guest_pname":str, "guest_phone":str, "guest_ccountry":str, "guest_carea":str, "guest_email":str, "guest_addtype":str, "guest_address":str, "guest_city":str, "guest_pcode":str, "guest_prov":str, "guest_country":str, "guest_company":str, "guest_doc_country":str, "guest_doc_nation":str, "guest_expire":str, "guest_effective":str, "guest_birthdate":str, "guest_gender":str, "guest_cardno":str, "guest_cardtype":str, "guest_member_name":str, "guest_member_expire":str, "guest_member_effective":str, "guest_member_id":str, "spr_code":str, "spr_name":str, "spr_desc":str, "total_rsv_amount":str, "rsv_number":int, "rsvline_number":int, "argt_code":str, "room_sharer":str, "accompaying_guest":str, "image_flag":str, "arrival_time":str, "occupancy_today":str})
    fix_cost_list, Fix_cost = create_model("Fix_cost", {"resnr":str, "reslinnr":str, "fc_ratecode":str, "fc_rstatus":str, "fc_inclusive":str, "fc_name":str, "fc_quantity":str, "fc_type":str, "fc_exdate":str, "fc_efdate":str, "fc_amtbefore":str, "fc_amtafter":str, "fc_curr":str, "fc_decimal":str, "fc_tax_code":str, "fc_tax_decimal":str, "fc_tax_amount":str})

    Bguest = create_buffer("Bguest",Guest)
    Rline = create_buffer("Rline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, result_message, arrival_guest_list, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, bresline, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_list, fix_cost_list

        return {"msg_str": msg_str, "result_message": result_message, "arrival-guest": arrival_guest_list}

    def calc_occ():

        nonlocal msg_str, result_message, arrival_guest_list, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, bresline, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_list, fix_cost_list

        do_it:bool = False
        bresline = None
        Bresline =  create_buffer("Bresline",Res_line)

        if occ1 == None:

            for bresline in db_session.query(Bresline).filter(
                     (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.ankunft <= ci_date) & (Bresline.abreise > ci_date) & (Bresline.l_zuordnung[inc_value(2)] == 0)).order_by(Bresline._recid).all():
                do_it = True

                if bresline.zinr != "":

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == bresline.zinr)).first()
                    do_it = zimmer.sleeping

                if do_it:
                    occ_room = occ_room + bresline.zimmeranz
            occ1 =  to_decimal(occ_room) / to_decimal(tot_room) * to_decimal("100")

        for bresline in db_session.query(Bresline).filter(
                     (Bresline.active_flag <= 1) & (Bresline.resstatus <= 6) & (Bresline.resstatus != 3) & (Bresline.resstatus != 4) & (Bresline.resstatus != 12) & (Bresline.resstatus != 11) & (Bresline.resstatus != 13) & (Bresline.ankunft <= curr_co_date) & (Bresline.abreise > curr_co_date) & (Bresline.l_zuordnung[inc_value(2)] == 0)).order_by(Bresline._recid).all():
            do_it = True

            if bresline.zinr != "":

                zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == bresline.zinr)).first()
                do_it = zimmer.sleeping

            if do_it:
                occ_room = occ_room + bresline.zimmeranz
        occ2 =  to_decimal(occ_room) / to_decimal(tot_room) * to_decimal("100")

        if occ1 > occ2:
            occ_perc =  to_decimal(occ1)
        else:
            occ_perc =  to_decimal(occ2)


    def search_by_resnr():

        nonlocal msg_str, result_message, arrival_guest_list, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, bresline, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_list, fix_cost_list

        voucher_found:bool = False
        curr_i:int = 0
        curr_str:str = ""
        voucherno:str = ""
        total_pax:int = 0
        voucher_found = True

        if voucher_found:

            for res_line in db_session.query(Res_line).filter(
                     (Res_line.resnr == resno) & ((Res_line.resstatus <= 2) | (Res_line.resstatus == 5)) & (Res_line.active_flag == 0)).order_by(Res_line._recid).all():

                arrangement = db_session.query(Arrangement).filter(
                         (Arrangement.arrangement == res_line.arrangement)).first()
                result_message = "0 - Reservation Found Success."
                total_pax = 0
                total_pax = res_line.erwachs + kind1
                curr_arrive = to_string(res_line.ankunft, "99/99/9999")
                curr_depart = to_string(res_line.abreise, "99/99/9999")


                arrival_guest = Arrival_guest()
                arrival_guest_list.append(arrival_guest)

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

                waehrung = db_session.query(Waehrung).filter(
                         (Waehrung.waehrungsnr == res_line.betriebsnr)).first()

                if waehrung:
                    arrival_guest.tamount_currency = waehrung.wabkurz

                if res_line.zinr != "":
                    arrival_guest.rmno = res_line.zinr

                    zimmer = db_session.query(Zimmer).filter(
                             (Zimmer.zinr == res_line.zinr)).first()

                    if zimmer:

                        if matches(zimmer.himmelsr,r"*NS*") or matches(zimmer.himmelsr,r"*Non Smoking*"):
                            arrival_guest.rmsmoking = "TRUE"

                        zimkateg = db_session.query(Zimkateg).filter(
                                 (Zimkateg.zikatnr == zimmer.zikatnr)).first()

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

                    queasy = db_session.query(Queasy).filter(
                             (Queasy.key == 2) & (Queasy.char1 == arrival_guest.rate_code)).first()

                    if queasy:
                        arrival_guest.rate_desc = queasy.char2

                bguest = db_session.query(Bguest).filter(
                         (Bguest.gastnr == res_line.gastnrmember)).first()

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
                        pos = 1 + get_index(bguest.ausweis_nr2, "\\")
                        ccname = trim(substring(bguest.ausweis_nr2, 0, pos - 1))
                        s1 = trim(substring(bguest.ausweis_nr2, pos + 1 - 1, length(bguest.ausweis_nr2) - pos))
                        pos1 = 1 + get_index(s1, "\\")

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

                    mc_guest = db_session.query(Mc_guest).filter(
                             (Mc_guest.gastnr == bguest.gastnr)).first()

                    if mc_guest:
                        arrival_guest.member_id = mc_guest.cardnum
                        arrival_guest.member_bonus = " "
                        arrival_guest.member_travel = " "
                        arrival_guest.member_point = " "
                        arrival_guest.guest_member_name = bguest.name
                        arrival_guest.guest_member_expire = to_string(mc_guest.tdate, "99/99/9999")
                        arrival_guest.guest_member_effective = to_string(mc_guest.created_date, "99/99/9999")
                        arrival_guest.guest_member_id = mc_guest.cardnum

                        mc_types = db_session.query(Mc_types).filter(
                                 (Mc_types.nr == mc_guest.nr)).first()

                        if mc_types:
                            arrival_guest.member_program == mc_types.bezeich

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("specialRequest").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).first()

                if reslin_queasy:
                    arrival_guest.spr_code = reslin_queasy.char3
                    arrival_guest.spr_name = reslin_queasy.char3


                    for loopi in range(1,num_entries(reslin_queasy.char3, ";")  + 1) :

                        queasy = db_session.query(Queasy).filter(
                                 (Queasy.key == 189) & (Queasy.char1 == entry(loopi - 1, reslin_queasy.char3, ";"))).first()

                        if queasy and queasy.logi3 :
                            arrival_guest.spr_desc = entry(loopi - 1, reslin_queasy.char3, ";") + ";" + arrival_guest.spr_desc

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr)).order_by(Reslin_queasy.date1).all():
                    totrsvamt =  to_decimal(totrsvamt) + to_decimal(reslin_queasy.deci1)


                arrival_guest.total_rsv_amount = to_string(totrsvamt)

            arrival_guest = query(arrival_guest_list, first=True)

            if not arrival_guest:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.resnr == resno) & (Res_line.active_flag == 1)).order_by(Res_line._recid).all():

                    if res_line.resstatus == 6:
                        result_message = "2 - Guest Already Checkin."

                    return
        else:
            result_message = "1 - Booking Code Not Found."


    def check_fixleist_posted(artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal msg_str, result_message, arrival_guest_list, ci_date, billdate, loopi, str, curr_arrive, curr_depart, pos, pos1, ccname, ccnr, expire_date, s1, curr_birth, curr_expireid, post_it, pdafirstdate, pdalastdate, vat_art, service_art, vat2_art, fact_art, fcost, service, vat, vat2, fact, totrsvamt, tot_room, occ_room, occ_perc, occ1, occ2, curr_co_date, price_decimal, stat_list, guest, res_line, htparam, zimmer, guestbook, bresline, arrangement, waehrung, zimkateg, queasy, mc_guest, mc_types, reslin_queasy
        nonlocal resno
        nonlocal bguest, rline


        nonlocal arrival_guest, fix_cost, bguest, rline
        nonlocal arrival_guest_list, fix_cost_list

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

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
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

    for arrival_guest in query(arrival_guest_list):

        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == arrival_guest.rmno)).first()

        if zimmer:
            arrival_guest.rmstatus = stat_list[zimmer.zistatus + 1 - 1]

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == arrival_guest.rsv_number) & (Res_line.resstatus == 11) & (Res_line.zinr == arrival_guest.rmno) & (Res_line.active_flag == 0)).first()

        if res_line:

            if res_line.l_zuordnung[2] != 0:
                arrival_guest.accompaying_guest = res_line.name
            else:
                arrival_guest.room_sharer = res_line.name

        guestbook = db_session.query(Guestbook).filter(
                 (Guestbook.gastnr == to_int(arrival_guest.guest_id))).first()

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

    for arrival_guest in query(arrival_guest_list):
        arrival_guest.occupancy_today = to_string(occ_perc)

    return generate_output()