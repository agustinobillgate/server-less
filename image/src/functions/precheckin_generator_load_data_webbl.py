from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Guest, Res_line, Reservation, Queasy

def precheckin_generator_load_data_webbl(resno:int, reslinno:int):
    arrive_list_list = []
    en_hotelencrip:str = ""
    oth_hotelencrip:str = ""
    cpersonalkey:str = ""
    rkey:bytes = None
    mmemptrout:bytes = None
    precheckinurl:str = ""
    hotelcode:str = ""
    hotelcode_ok:bool = False
    guest = res_line = reservation = queasy = None

    arrive_list = gmember = None

    arrive_list_list, Arrive_list = create_model("Arrive_list", {"resnr":int, "reslinnr":int, "rsv_name":str, "zinr":str, "guest_name":str, "guest_email":str, "phone_no":str, "arrival":date, "departure":date, "hotelcode":str, "mail_eng":str, "mail_oth":str, "hotel_name":str, "hotel_telp":str, "hotel_mail":str, "link_pci_eng":str, "link_pci_oth":str})

    Gmember = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal arrive_list_list, en_hotelencrip, oth_hotelencrip, cpersonalkey, rkey, mmemptrout, precheckinurl, hotelcode, hotelcode_ok, guest, res_line, reservation, queasy
        nonlocal gmember


        nonlocal arrive_list, gmember
        nonlocal arrive_list_list
        return {"arrive-list": arrive_list_list}


    arrive_list_list.clear()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

    if res_line:

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == res_line.resnr)).first()
        arrive_list = Arrive_list()
        arrive_list_list.append(arrive_list)

        arrive_list.resnr = res_line.resnr
        arrive_list.reslinnr = res_line.reslinnr
        arrive_list.rsv_name = reservation.name
        arrive_list.zinr = res_line.zinr
        arrive_list.guest_name = res_line.name
        arrive_list.arrival = res_line.ankunft
        arrive_list.departure = res_line.abreise

        gmember = db_session.query(Gmember).filter(
                (Gmember.gastnr == res_line.gastnrmember)).first()

        if gmember:
            arrive_list.guest_email = gmember.email_adr
            arrive_list.phone_no = gmember.mobil_tel

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 5)).first()

        if queasy:
            precheckinurl = queasy.char3

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 216) &  (Queasy.number1 == 8)).all():

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
            rkey = GENERATE_PBE_KEY (cpersonalkey)
            mmemptrout = ENCRYPT (en_hotelencrip, rkey)
            en_hotelencrip = BASE64_ENCODE (mmemptrout)

            if re.match(".*\$.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "$", "%24")

            if re.match(".*&.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "&", "%26")

            if re.match(".*\+.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "+", "%2B")

            if re.match(".*,.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, ",", "%2C")

            if re.match(".*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "/", "%2F")

            if re.match(".*:.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, ":", "%3A")

            if re.match(".*;.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, ";", "%3B")

            if re.match(".* ==.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, " == ", "%3D")

            if re.match(".*?.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "?", "%3F")

            if re.match(".*@.*",en_hotelencrip):
                en_hotelencrip = replace_str(en_hotelencrip, "@", "%40")
            arrive_list.link_pci_eng = precheckinurl + "?" + en_hotelencrip
            mmemptrout = ENCRYPT (oth_hotelencrip, rkey)
            oth_hotelencrip = BASE64_ENCODE (mmemptrout)

            if re.match(".*\$.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "$", "%24")

            if re.match(".*&.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "&", "%26")

            if re.match(".*\+.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "+", "%2B")

            if re.match(".*,.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, ",", "%2C")

            if re.match(".*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "/", "%2F")

            if re.match(".*:.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, ":", "%3A")

            if re.match(".*;.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, ";", "%3B")

            if re.match(".* ==.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, " == ", "%3D")

            if re.match(".*?.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "?", "%3F")

            if re.match(".*@.*",oth_hotelencrip):
                oth_hotelencrip = replace_str(oth_hotelencrip, "@", "%40")
            arrive_list.link_pci_oth = precheckinurl + "?" + oth_hotelencrip

    return generate_output()