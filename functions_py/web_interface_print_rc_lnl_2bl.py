#using conversion tools version: 1.0.0.117
"""_yusufwijasena_29/10/2025

    Ticket ID: 8DE1E7
        _remark_:   - fix python indentation
                    - fix var declaration
                    - add import from functions_py
                    - change string to str
                    - fix ("string").lower() to "string"
"""
from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Res_line, Reslin_queasy, Queasy, Bediener, Arrangement, Reservation, Zimkateg, Sourccod, Mc_guest, Mc_types, Htparam, Segment

def web_interface_print_rc_lnl_2bl(resno:int, reslino:int, user_init:str):

    prepare_cache ([Guest, Res_line, Reslin_queasy, Queasy, Bediener, Arrangement, Reservation, Zimkateg, Sourccod, Mc_guest, Mc_types, Htparam, Segment])

    print_rc_list_data = []
    temp_zimmerwusch = ""
    anz:int = 0
    wi_gastnr:int = 0
    ind_gastnr:int = 0
    cc_str = ""
    cc_nr = ""
    ccard = ""
    mm:int = 0
    yy:int = 0
    cc_valid:bool = True
    loopi:int = 0
    tmp_special_req = ""
    guest = res_line = reslin_queasy = queasy = bediener = arrangement = reservation = zimkateg = sourccod = mc_guest = mc_types = htparam = segment = None

    print_rc_list = rsvguest = None

    print_rc_list_data, Print_rc_list = create_model(
        "Print_rc_list", {
            "gastno":str, 
            "cr_usr":str, 
            "last_name":str, 
            "first_name":str, 
            "guest_title":str, 
            "room":str, 
            "room_no":str, 
            "room_price":str, 
            "arrival":str, 
            "departure":str, 
            "eta_flight":str, 
            "eta_time":str, 
            "etd_flight":str, 
            "etd_time":str, 
            "no_guest":str, 
            "purpose_stay":str,
            "guest_address1":str,
            "guest_address2":str, 
            "guest_address3":str, 
            "guest_country":str, 
            "guest_zip":str,
            "guest_city":str,
            "guest_nation":str,
            "guest_id":str,
            "guest_email":str,
            "birth_date":str,
            "company_name":str,
            "rsv_addr1":str,
            "rsv_addr2":str,
            "rsv_addr3":str,
            "rsv_country":str,
            "rsv_city":str,
            "rsv_zip":str,
            "ccard":str,
            "mobile_no":str,
            "bill_instruct":str,
            "birth_place":str,
            "expired_id":str,
            "resnr":str,
            "province":str,
            "phone":str,
            "telefax":str,
            "occupation":str,
            "child1":str,
            "child2":str,
            "main_comment":str,
            "member_comment":str,
            "depositgef":str,
            "depositbez":str,
            "segment":str,
            "gdpr_flag":str,
            "mark_flag":str,
            "news_flag":str,
            "voucher":str,
            "arr_time":str,
            "dept_time":str,
            "username":str,
            "code_argt":str,
            "special_req":str
            }
        )

    Rsvguest = create_buffer("Rsvguest",Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal print_rc_list_data, temp_zimmerwusch, anz, wi_gastnr, ind_gastnr, cc_str, cc_nr, ccard, mm, yy, cc_valid, loopi, tmp_special_req, guest, res_line, reslin_queasy, queasy, bediener, arrangement, reservation, zimkateg, sourccod, mc_guest, mc_types, htparam, segment
        nonlocal resno, reslino, user_init
        nonlocal rsvguest
        nonlocal print_rc_list, rsvguest
        nonlocal print_rc_list_data

        return {
            "print-rc-list": print_rc_list_data
            }

    res_line = get_cache (Res_line, {
        "resnr": [(eq, resno)],
        "reslinnr": [(eq, reslino)]})

    if res_line:
        print_rc_list = Print_rc_list()
        print_rc_list_data.append(print_rc_list)

        print_rc_list.room_no = to_string(res_line.zinr)
        # print_rc_list.arrival = to_string(ankunft, "99/99/9999")
        # print_rc_list.departure = to_string(abreise, "99/99/9999") + " " + to_string(res_line.abreisezeit, "HH:mm")
        print_rc_list.arrival = to_string(res_line.ankunft, "99/99/9999")
        print_rc_list.departure = to_string(res_line.abreise, "99/99/9999") + " " + to_string(res_line.abreisezeit, "HH:mm")
        print_rc_list.eta_flight = substring(res_line.flight_nr, 0, 6)
        print_rc_list.eta_time = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)
        print_rc_list.etd_flight = substring(res_line.flight_nr, 11, 6)
        print_rc_list.etd_time = substring(res_line.flight_nr, 17, 2) + ":" + substring(res_line.flight_nr, 19, 2)
        print_rc_list.no_guest = to_string(res_line.erwachs + res_line.gratis)
        print_rc_list.gastno = to_string(res_line.gastnrmember)
        print_rc_list.child1 = to_string(res_line.kind1)
        print_rc_list.child2 = to_string(res_line.kind2)
        print_rc_list.member_comment = to_string(res_line.bemerk)
        print_rc_list.arr_time = to_string(res_line.ankzeit, "HH:mm:SS")
        print_rc_list.dept_time = to_string(res_line.abreisezeit, "HH:mm:SS")

        reslin_queasy = get_cache (Reslin_queasy, {
            "key": [(eq, "specialrequest")],
            "resnr": [(eq, res_line.resnr)],
            "reslinnr": [(eq, res_line.reslinnr)]})

        if reslin_queasy:
            if reslin_queasy.char3 != None and trim(reslin_queasy.char3) != "":
                if num_entries(reslin_queasy.char3, ";") <= 1:
                    queasy = get_cache (Queasy, {
                        "key": [(eq, 189)],
                        "char1": [(eq, reslin_queasy.char3)]})

                    if queasy:
                        print_rc_list.special_req = queasy.char3
                else:
                    for loopi in range(1,num_entries(reslin_queasy.char3, ";")  + 1) :
                        tmp_special_req = entry(loopi - 1, reslin_queasy.char3, ";")

                        queasy = get_cache (Queasy, {
                            "key": [(eq, 189)],
                            "char1": [(eq, tmp_special_req)]})

                        if queasy:
                            print_rc_list.special_req = print_rc_list.special_req + queasy.char3 + ";"
                    print_rc_list.special_req = substring(print_rc_list.special_req, 0, length(print_rc_list.special_req) - 1)

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            print_rc_list.username = bediener.username

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement:
            print_rc_list.code_argt = arrangement.arrangement

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if reservation and reservation.useridanlage != "":
            cr_usr = reservation.useridanlage
            
        print_rc_list.resnr = to_string(res_line.resnr)
        print_rc_list.main_comment = to_string(reservation.bemerk)
        print_rc_list.depositgef = to_string(reservation.depositgef)

        print_rc_list.depositbez = to_string(reservation.depositbez)
        for anz in range(1,num_entries(res_line.zimmer_wunsch, ";") ) :
            temp_zimmerwusch = entry(anz - 1, res_line.zimmer_wunsch, ";")

            if substring(temp_zimmerwusch, 0, 8) == "segm_pur" :
                print_rc_list.purpose_stay = substring(temp_zimmerwusch, 8)

                queasy = get_cache (Queasy, {
                    "key": [(eq, 143)],
                    "number1": [(eq, to_int(print_rc_list.purpose_stay))]})

                if queasy and queasy.char3 != "":
                    print_rc_list.purpose_stay = queasy.char3
                break
        for anz in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            temp_zimmerwusch = entry(anz - 1, res_line.zimmer_wunsch, ";")

            if substring(temp_zimmerwusch, 0, 4) == "gdpr" :
                print_rc_list.gdpr_flag = substring(temp_zimmerwusch, 4)

            elif substring(temp_zimmerwusch, 0, 9) == "marketing" :
                print_rc_list.mark_flag = substring(temp_zimmerwusch, 9)

            elif substring(temp_zimmerwusch, 0, 10) == "newsletter" :
                print_rc_list.news_flag = substring(temp_zimmerwusch, 10)

            elif substring(temp_zimmerwusch, 0, 7) == "voucher" :
                print_rc_list.voucher = substring(temp_zimmerwusch, 7)

        queasy = get_cache (Queasy, {
            "key": [(eq, 9)],
            "number1": [(eq, to_int(res_line.code))]})

        if queasy and queasy.char1 != "":
            print_rc_list.bill_instruct = queasy.char1

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            print_rc_list.room = zimkateg.kurzbez + " / " + to_string(res_line.zimmeranz)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            print_rc_list.first_name = guest.vorname1
            print_rc_list.guest_title = guest.anrede1
            print_rc_list.guest_address1 = trim(guest.adresse1)
            print_rc_list.guest_address2 = trim(guest.adresse2)
            print_rc_list.guest_address3 = trim(guest.adresse3)
            print_rc_list.guest_country = trim(guest.land)
            print_rc_list.guest_zip = to_string(guest.plz)
            print_rc_list.guest_city = trim(guest.wohnort)
            print_rc_list.guest_nation = trim(guest.nation1)
            print_rc_list.guest_id = trim(guest.ausweis_nr1)
            print_rc_list.guest_email = trim(guest.email_adr)
            print_rc_list.mobile_no = to_string(guest.mobil_telefon, "x(16)")
            print_rc_list.birth_place = to_string(guest.telex, "x(24)")
            print_rc_list.province = to_string(guest.geburt_ort2)
            print_rc_list.phone = to_string(guest.telefon)
            print_rc_list.occupation = to_string(guest.beruf)

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            if reservation and reservation.resart != 0:
                sourccod = get_cache (Sourccod, {"source_code": [(eq, reservation.resart)]})

                if sourccod:
                    print_rc_list.mobile_no = print_rc_list.mobile_no + ";" + sourccod.bezeich

            mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)]})

            if mc_guest:
                print_rc_list.telefax = to_string(guest.fax) + ";" + to_string(mc_guest.cardnum)
            else:
                print_rc_list.telefax = to_string(guest.fax)

            mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

            if mc_types:
                print_rc_list.last_name = to_string(guest.name) + "-" + to_string(mc_types.bezeich)
            else:
                print_rc_list.last_name = to_string(guest.name)

            if guest.geburtdatum1 != None:
                print_rc_list.birth_date = to_string(guest.geburtdatum1, "99/99/9999")

            if guest.geburtdatum2 != None:
                print_rc_list.expired_id = to_string(guest.geburtdatum2, "99/99/9999")
            cc_str = entry(0, guest.ausweis_nr2, "|")
            ccard = entry(1, cc_str, "\\")
            mm = to_int(substring(entry(2, cc_str, "\\") , 0, 2))
            yy = to_int(substring(entry(2, cc_str, "\\") , 2))
            cc_nr = ccard

            if cc_nr == "":
                cc_valid = False

            if cc_valid:
                if yy < get_year(get_current_date()):
                    cc_valid = False

            if cc_valid:
                if (yy == get_year(get_current_date()) and mm < get_month(get_current_date())):
                    cc_valid = False

            if cc_valid:
                ccard = substring(ccard, 0, 1) + fill("X", length(ccard) - 5) + substring(ccard, length(ccard) - 3 - 1)
                print_rc_list.ccard = ccard
                print_rc_list.ccard = print_rc_list.ccard + ", " + substring(entry(2, cc_str, "\\") , 0, 2) + "/" + substring(entry(2, cc_str, "\\") , 2)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
        wi_gastnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
        ind_gastnr = htparam.finteger

        rsvguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        if rsvguest:
            print_rc_list.company_name = to_string((rsvguest.name + ", " + rsvguest.anredefirma) , "x(50)")
            print_rc_list.rsv_addr1 = trim(rsvguest.adresse1)
            print_rc_list.rsv_addr2 = trim(rsvguest.adresse2)
            print_rc_list.rsv_addr3 = trim(rsvguest.adresse3)
            print_rc_list.rsv_city = trim(rsvguest.wohnort)
            print_rc_list.rsv_zip = trim(rsvguest.plz)
            print_rc_list.rsv_country = trim(rsvguest.land)

            if (rsvguest and rsvguest.karteityp > 1) and (rsvguest.gastnr != wi_gastnr and rsvguest.gastnr != ind_gastnr):
                print_rc_list.room_price = "0"

            elif res_line.gastnrmember == res_line.gastnrpay or rsvguest.gastnr == wi_gastnr or rsvguest.gastnr == ind_gastnr:
                print_rc_list.room_price = trim(to_string(res_line.zipreis, ">>>,>>>,>>9.99"))

            elif rsvguest.karteityp <= 1:
                print_rc_list.room_price = trim(to_string(res_line.zipreis, ">>>,>>>,>>9.99"))

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            if segment:
                print_rc_list.segment = segment.bezeich

    return generate_output()