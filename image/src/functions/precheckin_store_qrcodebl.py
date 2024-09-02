from functions.additional_functions import *
import decimal
from models import Paramtext

def precheckin_store_qrcodebl(base64image:str, resno:int):
    mess_result = ""
    pointer:bytes = None
    imgpath:str = "/usr1/vhp/tmp/"
    php_script:str = ""
    smtp:str = ""
    username:str = ""
    password:str = ""
    security:str = ""
    port:str = ""
    email_from:str = ""
    name_from:str = ""
    email_to:str = ""
    subject:str = ""
    body:str = ""
    textbody:str = ""
    outfile:str = ""
    outfile_tmp:str = ""
    strlen:str = ""
    hotelname:str = ""
    hoteladdress:str = ""
    hotelcity:str = ""
    hoteltelp:str = ""
    hotelemail:str = ""
    hotelwebsite:str = ""
    hotelheaderimg:str = ""
    hotelfooterimg:str = ""
    precheckinurl:str = ""
    paramtext = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, pointer, imgpath, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, hotelwebsite, hotelheaderimg, hotelfooterimg, precheckinurl, paramtext


        return {"mess_result": mess_result}

    def send_email():

        nonlocal mess_result, pointer, imgpath, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, hotelwebsite, hotelheaderimg, hotelfooterimg, precheckinurl, paramtext


        name_from = "Reservation@" + hotelname
        subject = "Reminder - Pre Check In Online for your stay at " + hotelname

        if SEARCH ("C:\\VHPSource\\__works\\CEKSOURCE\\test170820\\send_email_precheckin.php") != None:
            OS_DELETE VALUE ("C:\\VHPSource\\__works\\CEKSOURCE\\test170820\\send_email_precheckin.php")
        outfile_tmp = "C:\\VHPSource\\__works\\CEKSOURCE\\test170820\\pre_check_in_template.htm"
        outfile = "C:\\VHPSource\\__works\\CEKSOURCE\\test170820\\pre_check_in_email.htm"
        OUTPUT STREAM s1 TO VALUE (outfile)
        INPUT STREAM s2 FROM VALUE (outfile_tmp)
        REPEAT:
        textbody = ""
        strlen = ""
        IMPORT STREAM s2 UNFORMATTED textbody


    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 200)).first()
    hotelname = paramtext.ptext

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 201)).first()
    hoteladdress = paramtext.ptext

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 202)).first()
    hoteladdress = hoteladdress + " " + paramtext.ptext

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 203)).first()
    hotelcity = hoteladdress + " " + paramtext.ptext

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 204)).first()
    hoteltelp = paramtext.ptext

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 206)).first()
    hotelemail = paramtext.ptext
    imgpath = imgpath + "QRCODE-" + to_string(resno) + ".jpg"
    pointer = base64_decode(base64image)
    COPY_LOB pointer TO FILE imgpath
    mess_result = "0 - upload data success."
    OUTPUT STREAM s1 CLOSE
    INPUT STREAM s2 CLOSE
    body = FILE outfile    COPY_LOB php_script TO FILE "C:\\VHPSource\\__works\\CEKSOURCE\\test170820\\send_email_precheckin.php"
    OS_COMMAND VALUE ("php C:\\VHPSource\\__works\\CEKSOURCE\\test170820\\send_email_precheckin.php")

    return generate_output()