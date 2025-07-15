#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Res_line, Reservation, Bill, Queasy, Zimkateg, Sourccod, Mc_guest, Mc_types, Htparam, Segment

def get_print_rc_lnlbl(resno:int, reslino:int):

    prepare_cache ([Guest, Res_line, Reservation, Queasy, Zimkateg, Sourccod, Mc_guest, Mc_types, Htparam, Segment])

    print_rc_list_data = []
    temp_zimmerwusch:string = ""
    anz:int = 0
    wi_gastnr:int = 0
    ind_gastnr:int = 0
    cc_str:string = ""
    cc_nr:string = ""
    ccard:string = ""
    mm:int = 0
    yy:int = 0
    cc_valid:bool = True
    guest = res_line = reservation = bill = queasy = zimkateg = sourccod = mc_guest = mc_types = htparam = segment = None

    print_rc_list = rsvguest = None

    print_rc_list_data, Print_rc_list = create_model("Print_rc_list", {"gastno":string, "cr_usr":string, "last_name":string, "first_name":string, "guest_title":string, "room":string, "room_no":string, "room_price":string, "arrival":string, "departure":string, "eta_flight":string, "eta_time":string, "etd_flight":string, "etd_time":string, "no_guest":string, "purpose_stay":string, "guest_address1":string, "guest_address2":string, "guest_address3":string, "guest_country":string, "guest_zip":string, "guest_city":string, "guest_nation":string, "guest_id":string, "guest_email":string, "birth_date":string, "company_name":string, "rsv_addr1":string, "rsv_addr2":string, "rsv_addr3":string, "rsv_country":string, "rsv_city":string, "rsv_zip":string, "ccard":string, "mobile_no":string, "bill_instruct":string, "birth_place":string, "expired_id":string, "resnr":string, "province":string, "phone":string, "telefax":string, "occupation":string, "child1":string, "child2":string, "main_comment":string, "member_comment":string, "depositgef":string, "depositbez":string, "segment":string})

    Rsvguest = create_buffer("Rsvguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal print_rc_list_data, temp_zimmerwusch, anz, wi_gastnr, ind_gastnr, cc_str, cc_nr, ccard, mm, yy, cc_valid, guest, res_line, reservation, bill, queasy, zimkateg, sourccod, mc_guest, mc_types, htparam, segment
        nonlocal resno, reslino
        nonlocal rsvguest


        nonlocal print_rc_list, rsvguest
        nonlocal print_rc_list_data

        return {"print-rc-list": print_rc_list_data}

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslino)]})

    if res_line:
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
        print_rc_list.child1 = to_string(res_line.kind1)
        print_rc_list.child2 = to_string(res_line.kind2)
        print_rc_list.member_comment = to_string(res_line.bemerk)

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if reservation and reservation.useridanlage != "":
            cr_usr = reservation.useridanlage
        print_rc_list.resnr = to_string(res_line.resnr)
        print_rc_list.main_comment = to_string(reservation.bemerk)
        print_rc_list.depositgef = to_string(reservation.depositgef)


        print_rc_list.depositbez = to_string(reservation.depositbez)

        bill = get_cache (Bill, {"resnr": [(eq, resno)],"reslinnr": [(eq, 0)]})

        if bill:
            print_rc_list.depositgef = "0.00"
        for anz in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            temp_zimmerwusch = entry(anz - 1, res_line.zimmer_wunsch, ";")

            if substring(temp_zimmerwusch, 0, 8) == ("segm_pur").lower() :
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

                mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

                if mc_types:
                    print_rc_list.last_name = to_string(guest.name) + "-" + to_string(mc_types.bezeich)
                else:
                    print_rc_list.last_name = to_string(guest.name)
            else:
                print_rc_list.telefax = to_string(guest.fax)

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
                ccard = substring(ccard, 0, 1) +\
                        fill("X", length(ccard) - 5) +\
                        substring(ccard, length(ccard) - 3 - 1)
                print_rc_list.ccard = ccard
                print_rc_list.ccard = print_rc_list.ccard +\
                    ", " +\
                    substring(entry(2, cc_str, "\\") , 0, 2) +\
                    "/" +\
                    substring(entry(2, cc_str, "\\") , 2)

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
                print_rc_list.room_price = "0.00"

            elif res_line.gastnrmember == res_line.gastnrpay or rsvguest.gastnr == wi_gastnr or rsvguest.gastnr == ind_gastnr:
                print_rc_list.room_price = trim(to_string(res_line.zipreis, ">>>,>>>,>>9.99"))

            elif rsvguest.karteityp <= 1:
                print_rc_list.room_price = trim(to_string(res_line.zipreis, ">>>,>>>,>>9.99"))

            segment = get_cache (Segment, {"segmentcode": [(eq, reservation.segmentcode)]})

            if segment:
                print_rc_list.segment = segment.bezeich

    return generate_output()