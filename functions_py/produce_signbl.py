#using conversion tools version: 1.0.0.119
#-------------------------------------------
# Rd, 26/11/2025, .CHAR -> .char
# Rd, 26/11/2025, with_for_update
#-------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from functions.checkin_gdprbl import checkin_gdprbl
from functions.view_staycostbl import view_staycostbl
from models import Guest, Archieve, Res_line, Reservation, Queasy, Zimkateg, Htparam, Briefzei, Guest_pr, Mc_guest

def produce_signbl(pvilanguage:int, resno:int, reslino:int, gastno:int):

    prepare_cache ([Guest, Archieve, Res_line, Reservation, Queasy, Zimkateg, Htparam, Briefzei, Guest_pr])

    ct = ""
    term_condition = ""
    gdpractivated = False
    newsactivated = False
    gdpr_flag = False
    euro_flag = False
    member_flag = False
    marketing_flag = False
    newsletter_flag = False
    print_rc_list_data = []
    output_list_data = []
    temp_zimmerwusch:string = ""
    zimmerwunsch:string = ""
    anz:int = 0
    wi_gastnr:int = 0
    ind_gastnr:int = 0
    cc_str:string = ""
    cc_nr:string = ""
    mm:int = 0
    yy:int = 0
    cc_valid:bool = True
    contcode:string = ""
    tmp_str:string = ""
    bb:bytes = None
    image_data:string = ""
    i:int = 0
    str:string = ""
    strgdpr:string = ""
    strmark:string = ""
    strnews:string = ""
    err_flag:int = 0
    guest = archieve = res_line = reservation = queasy = zimkateg = htparam = briefzei = guest_pr = mc_guest = None

    print_rc_list = output_list = rsvguest = None

    print_rc_list_data, Print_rc_list = create_model("Print_rc_list", {"gastno":string, "cr_usr":string, "last_name":string, "first_name":string, "guest_title":string, "room":string, "room_no":string, "room_price":string, "arrival":string, "departure":string, "eta_flight":string, "eta_time":string, "etd_flight":string, "etd_time":string, "no_guest":string, "purpose_stay":string, "guest_address1":string, "guest_address2":string, "guest_address3":string, "guest_country":string, "guest_zip":string, "guest_city":string, "guest_nation":string, "guest_province":string, "guest_id":string, "guest_email":string, "birth_date":string, "company_name":string, "rsv_addr1":string, "rsv_addr2":string, "rsv_addr3":string, "rsv_country":string, "rsv_city":string, "rsv_zip":string, "ccard":string, "mobile_no":string, "bill_instruct":string, "birth_place":string, "expired_id":string, "resnr":string})
    output_list_data, Output_list = create_model("Output_list", {"flag":int, "str":string, "str1":string})

    Rsvguest = create_buffer("Rsvguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ct, term_condition, gdpractivated, newsactivated, gdpr_flag, euro_flag, member_flag, marketing_flag, newsletter_flag, print_rc_list_data, output_list_data, temp_zimmerwusch, zimmerwunsch, anz, wi_gastnr, ind_gastnr, cc_str, cc_nr, mm, yy, cc_valid, contcode, tmp_str, bb, image_data, i, str, strgdpr, strmark, strnews, err_flag, guest, archieve, res_line, reservation, queasy, zimkateg, htparam, briefzei, guest_pr, mc_guest
        nonlocal pvilanguage, resno, reslino, gastno
        nonlocal rsvguest


        nonlocal print_rc_list, output_list, rsvguest
        nonlocal print_rc_list_data, output_list_data

        return {"ct": ct, "term_condition": term_condition, "gdpractivated": gdpractivated, "newsactivated": newsactivated, "gdpr_flag": gdpr_flag, "euro_flag": euro_flag, "member_flag": member_flag, "marketing_flag": marketing_flag, "newsletter_flag": newsletter_flag, "print-rc-list": print_rc_list_data, "output-list": output_list_data}


    archieve = get_cache (Archieve, {"key": [(eq, "send-sign-rc")],"num1": [(eq, resno)],"num2": [(eq, reslino)],"num3": [(eq, gastno)]})

    if archieve and archieve.char[1] != "":
        image_data = archieve.char[1]

    if length(image_data) > 0:
        # bb = image_data.encode('utf-8')
        # ct = base64_encode(bb)
        ct = image_data

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslino)]})

    if res_line:
        zimmerwunsch = res_line.zimmer_wunsch
        print_rc_list = Print_rc_list()
        print_rc_list_data.append(print_rc_list)

        print_rc_list.room_no = to_string(res_line.zinr)
        print_rc_list.arrival = to_string(res_line.ankunft, "99/99/9999")
        print_rc_list.departure = to_string(res_line.abreise, "99/99/9999") + " " + to_string(res_line.abreisezeit, "HH:mm")
        print_rc_list.eta_flight = substring(res_line.flight_nr, 0, 6)
        print_rc_list.eta_time = substring(res_line.flight_nr, 6, 2) + ":" + substring(res_line.flight_nr, 8, 2)
        print_rc_list.etd_flight = substring(res_line.flight_nr, 11, 6)
        print_rc_list.etd_time = substring(res_line.flight_nr, 17, 2) + ":" + substring(res_line.flight_nr, 19, 2)
        print_rc_list.no_guest = to_string(res_line.erwachs + res_line.gratis)
        print_rc_list.gastno = to_string(res_line.gastnrmember)


        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if reservation and reservation.useridanlage != "":
            cr_usr = reservation.useridanlage
        print_rc_list.resnr = to_string(res_line.resnr)
        for anz in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            temp_zimmerwusch = entry(anz - 1, res_line.zimmer_wunsch, ";")

            if substring(temp_zimmerwusch, 0, 8) == ("segm_pur") :
                print_rc_list.purpose_stay = substring(temp_zimmerwusch, 8)

                queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, to_int(print_rc_list.purpose_stay))]})

                if queasy and queasy.char3 != "":
                    print_rc_list.purpose_stay = queasy.char3
                break

        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

        if queasy and queasy.char1 != "":
            print_rc_list.bill_instruct = queasy.char1

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            print_rc_list.room = zimkateg.kurzbez + " / " + to_string(res_line.zimmeranz)

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            print_rc_list.last_name = guest.name
            print_rc_list.first_name = guest.vorname1
            print_rc_list.guest_title = guest.anrede1
            print_rc_list.guest_address1 = trim(guest.adresse1)
            print_rc_list.guest_address2 = trim(guest.adresse2)
            print_rc_list.guest_address3 = trim(guest.adresse3)
            print_rc_list.guest_country = trim(guest.land)
            print_rc_list.guest_zip = to_string(guest.plz)
            print_rc_list.guest_city = trim(guest.wohnort)
            print_rc_list.guest_nation = trim(guest.nation1)
            print_rc_list.guest_province = trim(guest.geburt_ort2)
            print_rc_list.guest_id = trim(guest.ausweis_nr1)
            print_rc_list.guest_email = trim(guest.email_adr)
            print_rc_list.mobile_no = to_string(guest.mobil_telefon, "x(16)")
            print_rc_list.birth_place = to_string(guest.telex, "x(24)")

            if guest.geburtdatum1 != None:
                print_rc_list.birth_date = to_string(guest.geburtdatum1, "99/99/9999")

            if guest.geburtdatum2 != None:
                print_rc_list.expired_id = to_string(guest.geburtdatum2, "99/99/9999")
            cc_str = entry(0, guest.ausweis_nr2, "|")
            cc_nr = entry(1, cc_str, "\\")
            mm = to_int(substring(entry(2, cc_str, "\\") , 0, 2))
            yy = to_int(substring(entry(2, cc_str, "\\") , 2))
            cc_nr = cc_nr + ", " + substring(entry(2, cc_str, "\\") , 0, 2) + "/" +\
                    substring(entry(2, cc_str, "\\") , 2)

            if cc_nr == "":
                cc_valid = False

            if cc_valid:

                if yy < get_year(get_current_date()):
                    cc_valid = False

            if cc_valid:

                if (yy == get_year(get_current_date()) and mm < get_month(get_current_date())):
                    cc_valid = False

            if cc_valid:
                print_rc_list.ccard = cc_nr

        htparam = get_cache (Htparam, {"paramnr": [(eq, 109)]})
        wi_gastnr = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 123)]})
        ind_gastnr = htparam.finteger

        rsvguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        if rsvguest:
            print_rc_list.company_name = to_string((rsvguest.name + ", " + rsvguest.anredefirma) , "x(24)")
            print_rc_list.rsv_addr1 = trim(rsvguest.adresse1)
            print_rc_list.rsv_addr2 = trim(rsvguest.adresse2)
            print_rc_list.rsv_addr3 = trim(rsvguest.adresse3)
            print_rc_list.rsv_city = trim(rsvguest.wohnort)
            print_rc_list.rsv_zip = trim(rsvguest.plz)
            print_rc_list.rsv_country = trim(rsvguest.land)

            if rsvguest.karteityp == 0 or (rsvguest.gastnr == wi_gastnr or rsvguest.gastnr == ind_gastnr):
                print_rc_list.room_price = trim(to_string(res_line.zipreis, ">>>,>>>,>>9.99"))

        htparam = get_cache (Htparam, {"paramnr": [(eq, 51)],"paramgruppe": [(eq, 15)],"reihenfolge": [(eq, 136)]})

        if htparam:

            briefzei = get_cache (Briefzei, {"briefnr": [(eq, htparam.finteger)]})

            if briefzei:
                term_condition = briefzei.texte
        contcode = ""

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

        if guest_pr:
            contcode = guest_pr.code
            tmp_str = res_line.zimmer_wunsch

            if matches(tmp_str,r"*$CODE$*"):
                tmp_str = substring(tmp_str, get_index(tmp_str, "$CODE$") + 6 - 1)
                contcode = substring(tmp_str, 0, get_index(tmp_str, ";") - 1)

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, res_line.gastnr)]})

        if mc_guest:
            member_flag = True
        else:
            member_flag = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 346)]})

        if htparam and htparam.bezeichnung  != ("Not Used") :
            gdpractivated = htparam.flogical
        else:
            gdpractivated = False

        if gdpractivated:
            for i in range(1,num_entries(zimmerwunsch, ";") - 1 + 1) :
                str = entry(i - 1, zimmerwunsch, ";")

                if substring(str, 0, 4) == ("GDPR") :
                    strgdpr = substring(str, 4)

            if strgdpr  == ("YES") :
                gdpr_flag = True
            else:
                gdpr_flag = False

            if gdpr_flag == False:
                err_flag = get_output(checkin_gdprbl(gastno))

                if err_flag == 1:
                    gdpr_flag = True
                    euro_flag = True

            if gdpr_flag :
                euro_flag = True

                # res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslino)],"gastnrmember": [(eq, gastno)]})
                res_line = db_session.query(Res_line).filter(Res_line.resnr == resno, 
                                                             Res_line.reslinnr == reslino, Res_line.gastnrmember == gastno).with_for_update().first()

                if res_line:

                    if not matches(res_line.zimmer_wunsch,r"*GDPR*"):
                        res_line.zimmer_wunsch = res_line.zimmer_wunsch + "GDPRyes;"
        else:
            gdpr_flag = False

        htparam = get_cache (Htparam, {"paramnr": [(eq, 477)]})

        if htparam and htparam.bezeichnung  != ("Not Used") :
            newsactivated = htparam.flogical
        else:
            newsactivated = False

        if newsactivated:
            for i in range(1,num_entries(zimmerwunsch, ";") - 1 + 1) :
                str = entry(i - 1, zimmerwunsch, ";")

                if substring(str, 0, 9) == ("MARKETING") :
                    strmark = substring(str, 9)

                if substring(str, 0, 10) == ("NEWSLETTER") :
                    strnews = substring(str, 10)

            if strmark  == ("YES") :
                marketing_flag = True
            else:
                marketing_flag = False

            if strnews  == ("YES") :
                newsletter_flag = True
            else:
                newsletter_flag = False
                
        output_list_data = get_output(view_staycostbl(pvilanguage, resno, reslino, contcode))

    return generate_output()