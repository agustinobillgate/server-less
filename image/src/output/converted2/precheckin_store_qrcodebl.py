#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext

def precheckin_store_qrcodebl(base64image:string, resno:int):

    prepare_cache ([Paramtext])

    mess_result = ""
    pointer:bytes = None
    imgpath:string = "/usr1/vhp/tmp/"
    php_script:string = ""
    smtp:string = ""
    username:string = ""
    password:string = ""
    security:string = ""
    port:string = ""
    email_from:string = ""
    name_from:string = ""
    email_to:string = ""
    subject:string = ""
    body:string = ""
    textbody:string = ""
    outfile:string = ""
    outfile_tmp:string = ""
    strlen:string = ""
    hotelname:string = ""
    hoteladdress:string = ""
    hotelcity:string = ""
    hoteltelp:string = ""
    hotelemail:string = ""
    hotelwebsite:string = ""
    hotelheaderimg:string = ""
    hotelfooterimg:string = ""
    precheckinurl:string = ""
    paramtext = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, pointer, imgpath, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, hotelwebsite, hotelheaderimg, hotelfooterimg, precheckinurl, paramtext
        nonlocal base64image, resno

        return {"mess_result": mess_result}

    def send_email():

        nonlocal mess_result, pointer, imgpath, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, hotelwebsite, hotelheaderimg, hotelfooterimg, precheckinurl, paramtext
        nonlocal base64image, resno


        name_from = "Reservation@" + hotelname
        subject = "Reminder - Pre Check In Online for your stay at " + hotelname

        if SEARCH ("C:\\VHPSource\\_works\\CEKSOURCE\\test170820\\send-email-precheckin.php") != None:
            OS_DELETE VALUE ("C:\\VHPSource\\_works\\CEKSOURCE\\test170820\\send-email-precheckin.php")
        outfile_tmp = "C:\\VHPSource\\_works\\CEKSOURCE\\test170820\\pre-check-in-template.htm"
        outfile = "C:\\VHPSource\\_works\\CEKSOURCE\\test170820\\pre-check-in-email.htm"
        OUTPUT STREAM s1 TO VALUE (outfile)
        INPUT STREAM s2 FROM VALUE (outfile_tmp)
        while True:
            textbody = ""
            strlen = ""
            IMPORT STREAM s2 UNFORMATTED textbody
        OUTPUT STREAM s1 CLOSE
        INPUT STREAM s2 CLOSE
        body = FILE outfile

        OS_COMMAND VALUE ("php C:\\VHPSource\\_works\\CEKSOURCE\\test170820\\send-email-precheckin.php")

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})
    hotelname = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 201)]})
    hoteladdress = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 202)]})
    hoteladdress = hoteladdress + " " + paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 203)]})
    hotelcity = hoteladdress + " " + paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 204)]})
    hoteltelp = paramtext.ptexte

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 206)]})
    hotelemail = paramtext.ptexte
    imgpath = imgpath + "QRCODE-" + to_string(resno) + ".jpg"
    pointer = base64_decode(base64image)

    mess_result = "0 - upload data success."

    return generate_output()