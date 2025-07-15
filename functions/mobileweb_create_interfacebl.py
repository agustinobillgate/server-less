#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Res_line, Interface, Zimmer, Queasy

def mobileweb_create_interfacebl(rsv_number:int, rsvline_number:int, user_init:string, email:string, guest_phnumber:string, hotel_code:string, room_preference:string, url_mci:string):

    prepare_cache ([Paramtext, Res_line, Interface, Zimmer, Queasy])

    result_message = ""
    lreturn:bool = False
    htlappparam:string = ""
    vhost:string = ""
    vservice:string = ""
    hotel_name:string = ""
    room_number:string = ""
    guest_name:string = ""
    cpersonalkey:string = ""
    rkey:bytes = None
    mmemptrout:bytes = None
    str_text:string = ""
    encrypted_text:string = ""
    paramtext = res_line = interface = zimmer = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal result_message, lreturn, htlappparam, vhost, vservice, hotel_name, room_number, guest_name, cpersonalkey, rkey, mmemptrout, str_text, encrypted_text, paramtext, res_line, interface, zimmer, queasy
        nonlocal rsv_number, rsvline_number, user_init, email, guest_phnumber, hotel_code, room_preference, url_mci

        return {"result_message": result_message}

    def decode_string(in_str:string):

        nonlocal result_message, lreturn, htlappparam, vhost, vservice, hotel_name, room_number, guest_name, cpersonalkey, rkey, mmemptrout, str_text, encrypted_text, paramtext, res_line, interface, zimmer, queasy
        nonlocal rsv_number, rsvline_number, user_init, email, guest_phnumber, hotel_code, room_preference, url_mci

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

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
        result_message = "1 - Phone Number must be filled-in!"

        return generate_output()
    str_text = hotel_code + "|" + to_string(rsv_number) + "|" + to_string(rsvline_number)
    cpersonalkey = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
    rkey = create_cipher_suite(cpersonalkey)
    mmemptrout = encrypt_with_cipher_suite(str_text, rkey)
    encrypted_text = base64_encode(mmemptrout)


    url_mci = entry(0, url_mci, "?") + "?SMS=" + encrypted_text

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 240)]})

    if paramtext and paramtext.ptexte != "":
        hotel_name = decode_string(paramtext.ptexte)

    res_line = get_cache (Res_line, {"resnr": [(eq, rsv_number)],"reslinnr": [(eq, rsvline_number)]})

    if res_line:
        room_number = res_line.zinr
        guest_name = res_line.name
        interface = Interface()
        db_session.add(interface)

        interface.key = 50
        interface.zinr = room_number
        interface.nebenstelle = ""
        interface.intfield = 0
        interface.decfield =  to_decimal("1")
        interface.int_time = get_current_time_in_seconds()
        interface.intdate = get_current_date()
        interface.parameters = hotel_code + ";" + hotel_name + ";" + guest_name + ";" + guest_phnumber + ";" + email + ";" + room_preference + ";" + url_mci
        interface.resnr = rsv_number
        interface.reslinnr = rsvline_number

        if room_number != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, room_number)]})

            if zimmer.zistatus != 0:

                queasy = get_cache (Queasy, {"key": [(eq, 162)],"char1": [(eq, room_number)]})

                if not queasy:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 162
                    queasy.char1 = room_number


                queasy.char2 = user_init
                queasy.number1 = 0
                queasy.number2 = get_current_time_in_seconds()
                queasy.date2 = get_current_date()


                pass
        pass
        result_message = "0 - Success"
    else:
        result_message = "2 - No Reservation found!"

        return generate_output()

    return generate_output()