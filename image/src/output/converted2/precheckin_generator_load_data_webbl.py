#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Res_line, Reservation, Queasy

def precheckin_generator_load_data_webbl(resno:int, reslinno:int):

    prepare_cache ([Guest, Res_line, Reservation, Queasy])

    arrive_list_list = []
    en_hotelencrip:string = ""
    oth_hotelencrip:string = ""
    cpersonalkey:string = ""
    rkey:bytes = None
    mmemptrout:bytes = None
    precheckinurl:string = ""
    hotelcode:string = ""
    hotelcode_ok:bool = False
    guest = res_line = reservation = queasy = None

    arrive_list = gmember = None

    arrive_list_list, Arrive_list = create_model("Arrive_list", {"resnr":int, "reslinnr":int, "rsv_name":string, "zinr":string, "guest_name":string, "guest_email":string, "phone_no":string, "arrival":date, "departure":date, "hotelcode":string, "mail_eng":string, "mail_oth":string, "hotel_name":string, "hotel_telp":string, "hotel_mail":string, "link_pci_eng":string, "link_pci_oth":string})

    Gmember = create_buffer("Gmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal arrive_list_list, en_hotelencrip, oth_hotelencrip, cpersonalkey, rkey, mmemptrout, precheckinurl, hotelcode, hotelcode_ok, guest, res_line, reservation, queasy
        nonlocal resno, reslinno
        nonlocal gmember


        nonlocal arrive_list, gmember
        nonlocal arrive_list_list

        return {"arrive-list": arrive_list_list}


    arrive_list_list.clear()

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

    if res_line:

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})
        arrive_list = Arrive_list()
        arrive_list_list.append(arrive_list)

        arrive_list.resnr = res_line.resnr
        arrive_list.reslinnr = res_line.reslinnr
        arrive_list.rsv_name = reservation.name
        arrive_list.zinr = res_line.zinr
        arrive_list.guest_name = res_line.name
        arrive_list.arrival = res_line.ankunft
        arrive_list.departure = res_line.abreise

        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if gmember:
            arrive_list.guest_email = gmember.email_adr
            arrive_list.phone_no = gmember.mobil_telefon

        queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 7)],"number2": [(eq, 5)]})

        if queasy:
            precheckinurl = queasy.char3

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216) & (Queasy.number1 == 8)).order_by(Queasy._recid).all():

            if queasy.number2 == 31:
                hotelcode = queasy.char3

            if queasy.number2 == 32:
                arrive_list.mail_eng = queasy.char3

            if queasy.number2 == 33:
                arrive_list.mail_oth = queasy.char3

            if queasy.number2 == 19:
                arrive_list.hotel_name = queasy.char3

            if queasy.number2 == 22:
                arrive_list.hotel_telp = queasy.char3

            if queasy.number2 == 23:
                arrive_list.hotel_mail = queasy.char3

        if hotelcode == "":
            hotelcode_ok = False
        else:
            hotelcode_ok = True

        if not hotelcode_ok:
            arrive_list.link_pci_eng = "hotelcode Not Configured Yet"
            arrive_list.link_pci_oth = "hotelcode Belum Terkonfigurasi Dengan Benar"


        else:
            en_hotelencrip = "ENG|" + hotelcode + "|" + to_string(arrive_list.arrival) + "|" + to_string(arrive_list.resnr)
            oth_hotelencrip = "IDN|" + hotelcode + "|" + to_string(arrive_list.arrival) + "|" + to_string(arrive_list.resnr)
            cpersonalkey = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
            rkey = create_cipher_suite(cpersonalkey)
            mmemptrout = encrypt_with_cipher_suite(en_hotelencrip, rkey)
            en_hotelencrip = base64_encode(mmemptrout)

            if matches(en_hotelencrip,r"*$*"):
                en_hotelencrip = replace_str(en_hotelencrip, "$", "%24")

            if matches(en_hotelencrip,r"*&*"):
                en_hotelencrip = replace_str(en_hotelencrip, "&", "%26")

            if matches(en_hotelencrip,r"*+*"):
                en_hotelencrip = replace_str(en_hotelencrip, "+", "%2B")

            if matches(en_hotelencrip,r"*,*"):
                en_hotelencrip = replace_str(en_hotelencrip, ",", "%2C")

            if matches(en_hotelencrip,r"*"):
                en_hotelencrip = replace_str(en_hotelencrip, "/", "%2F")

            if matches(en_hotelencrip,r"*:*"):
                en_hotelencrip = replace_str(en_hotelencrip, ":", "%3A")

            if matches(en_hotelencrip,r"*;*"):
                en_hotelencrip = replace_str(en_hotelencrip, ";", "%3B")

            if matches(en_hotelencrip,r"*=*"):
                en_hotelencrip = replace_str(en_hotelencrip, "=", "%3D")

            if matches(en_hotelencrip,r"*?*"):
                en_hotelencrip = replace_str(en_hotelencrip, "?", "%3F")

            if matches(en_hotelencrip,r"*@*"):
                en_hotelencrip = replace_str(en_hotelencrip, "@", "%40")
            arrive_list.link_pci_eng = precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + en_hotelencrip
            mmemptrout = encrypt_with_cipher_suite(oth_hotelencrip, rkey)
            oth_hotelencrip = base64_encode(mmemptrout)

            if matches(oth_hotelencrip,r"*$*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, "$", "%24")

            if matches(oth_hotelencrip,r"*&*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, "&", "%26")

            if matches(oth_hotelencrip,r"*+*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, "+", "%2B")

            if matches(oth_hotelencrip,r"*,*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, ",", "%2C")

            if matches(oth_hotelencrip,r"*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, "/", "%2F")

            if matches(oth_hotelencrip,r"*:*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, ":", "%3A")

            if matches(oth_hotelencrip,r"*;*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, ";", "%3B")

            if matches(oth_hotelencrip,r"*=*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, "=", "%3D")

            if matches(oth_hotelencrip,r"*?*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, "?", "%3F")

            if matches(oth_hotelencrip,r"*@*"):
                oth_hotelencrip = replace_str(oth_hotelencrip, "@", "%40")
            arrive_list.link_pci_oth = precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + oth_hotelencrip

    return generate_output()