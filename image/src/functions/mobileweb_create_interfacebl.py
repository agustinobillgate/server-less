from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Paramtext, Res_line, Interface, Zimmer, Queasy

def mobileweb_create_interfacebl(rsv_number:int, rsvline_number:int, user_init:str, email:str, guest_phnumber:str, hotel_code:str, room_preference:str, url_mci:str):
    result_message = ""
    lreturn:bool = False
    htlappparam:str = ""
    vhost:str = ""
    vservice:str = ""
    hotel_name:str = ""
    room_number:str = ""
    guest_name:str = ""
    cpersonalkey:str = ""
    rkey:bytes = None
    mmemptrout:bytes = None
    str_text:str = ""
    encrypted_text:str = ""
    paramtext = res_line = interface = zimmer = queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, lreturn, htlappparam, vhost, vservice, hotel_name, room_number, guest_name, cpersonalkey, rkey, mmemptrout, str_text, encrypted_text, paramtext, res_line, interface, zimmer, queasy


        return {"result_message": result_message}

    def decode_string(in_str:str):

        nonlocal result_message, lreturn, htlappparam, vhost, vservice, hotel_name, room_number, guest_name, cpersonalkey, rkey, mmemptrout, str_text, encrypted_text, paramtext, res_line, interface, zimmer, queasy

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return out_str
        s = in_str
        j = ord(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (ord(substring(s, len_ - 1, 1)) - j)


        return generate_inner_output()


    if email == None:
        email = ""

    if guest_phnumber == None:
        guest_phnumber = ""

    if hotel_code == None:
        hotel_code = ""

    if url_mci == None:
        url_mci = ""

    if room_preference == None:
        room_preference = ""

    if guest_phnumber == "":
        result_message = "1 - Phone Number must be filled_in!"

        return generate_output()
    str_text = hotel_code + "|" + to_string(rsv_number) + "|" + to_string(rsvline_number)
    cpersonalkey = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
    rkey = GENERATE_PBE_KEY (cpersonalkey)
    mmemptrout = ENCRYPT (str_text, rkey)
    encrypted_text = BASE64_ENCODE (mmemptrout)


    url_mci = entry(0, url_mci, "?") + "?SMS == " + encrypted_text

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 240)).first()

    if paramtext and paramtext.ptexte != "":
        hotel_name = decode_string(paramtext.ptexte)

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == rsv_number) &  (Res_line.reslinnr == rsvline_number)).first()

    if res_line:
        room_number = res_line.zinr
        guest_name = res_line.name
        interface = Interface()
        db_session.add(interface)

        interface.key = 50
        interface.zinr = room_number
        interface.nebenstelle = ""
        interface.intfield = 0
        interface.decfield = 1
        interface.int_time = get_current_time_in_seconds()
        interface.intdate = get_current_date()
        interface.parameters = hotel_code + ";" + hotel_name + ";" + guest_name + ";" + guest_phnumber + ";" + email + ";" + room_preference + ";" + url_mci
        interface.resnr = rsv_number
        interface.reslinnr = rsvline_number

        if room_number != "":

            zimmer = db_session.query(Zimmer).filter(
                    (func.lower(Zimmer.zinr) == (room_number).lower())).first()

            if zimmer.zistatus != 0:

                queasy = db_session.query(Queasy).filter(
                        (Queasy.key == 162) &  (func.lower(Queasy.char1) == (room_number).lower())).first()

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 162
                    queasy.char1 = room_number


                queasy.char2 = user_init
                queasy.number1 = 0
                queasy.number2 = get_current_time_in_seconds()
                queasy.date2 = get_current_date()

                queasy = db_session.query(Queasy).first()

        res_line = db_session.query(Res_line).first()
        result_message = "0 - Success"
    else:
        result_message = "2 - No Reservation found!"

        return generate_output()