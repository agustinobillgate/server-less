#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext, Htparam, Res_line, Guest

def fo_invoice_sendmail_webbl(send_current_bill:bool, bill_number:int, guest_number:int, rsv_number:int, rsvline_number:int, selected_bill_number:int, base64_bill:string):

    prepare_cache ([Paramtext, Htparam, Res_line, Guest])

    mess_str = ""
    send_email = False
    serveraddress:string = ""
    portaddress:string = ""
    username:string = ""
    password:string = ""
    filepath:string = ""
    filepath1:string = ""
    subject:string = ""
    fletter:string = ""
    cc_email:string = ""
    pointer:bytes = None
    security:string = ""
    name_from:string = ""
    bill_location:string = ""
    checkin_date:date = None
    checkout_date:date = None
    guest_name:string = ""
    hotel_name:string = ""
    emailadr:string = ""
    licensenr:string = ""
    paramtext = htparam = res_line = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, send_email, serveraddress, portaddress, username, password, filepath, filepath1, subject, fletter, cc_email, pointer, security, name_from, bill_location, checkin_date, checkout_date, guest_name, hotel_name, emailadr, licensenr, paramtext, htparam, res_line, guest
        nonlocal send_current_bill, bill_number, guest_number, rsv_number, rsvline_number, selected_bill_number, base64_bill

        return {"mess_str": mess_str, "send_email": send_email}

    def sendemail():

        nonlocal mess_str, send_email, serveraddress, portaddress, username, password, filepath, filepath1, subject, fletter, cc_email, pointer, security, name_from, bill_location, checkin_date, checkout_date, guest_name, hotel_name, emailadr, licensenr, paramtext, htparam, res_line, guest
        nonlocal send_current_bill, bill_number, guest_number, rsv_number, rsvline_number, selected_bill_number, base64_bill

        msg_str:string = ""
        gettextbody:string = ""
        lengtext:string = ""
        get_str:string = ""
        emailexist:bool = False
        body:string = ""
        php_script:string = ""
        php_path:string = ""

        if emailadr == "":
            mess_str = "No Email Address For This Guest!"

            return

        if length(emailadr) < 5:
            mess_str = "Incorrect Email Address : " + emailadr

            return
        fletter = "/usr1/vhp/tmp/" + licensenr + "/foinv-body.htm"
        php_path = "/usr1/vhp/tmp/" + licensenr + "/send-invoice-byemail.php"
        OUTPUT STREAM sbody1 TO VALUE (fletter)
        INPUT STREAM sbody2 FROM VALUE ("/usr1/vhp/tmp/" + licensenr + "/foinv-body-tmp.htm")
        while True:
            gettextbody = ""
            lengtext = ""
            IMPORT STREAM sbody2 UNFORMATTED gettextbody

            if matches(gettextbody,r"*$name1*"):
                gettextbody = entry(0, gettextbody, "$") + guest_name + ", <br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == ("0").lower()  or lengtext.lower()  == "":
                    lengtext = "1"

            elif matches(gettextbody,r"*$hotelname1*"):
                gettextbody = entry(0, gettextbody, "$") + hotel_name + ". <br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == ("0").lower()  or lengtext.lower()  == "":
                    lengtext = "1"

            elif matches(gettextbody,r"*$hotelname2*"):
                gettextbody = hotel_name + ". <br><br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == ("0").lower()  or lengtext.lower()  == "":
                    lengtext = "1"

            elif matches(gettextbody,r"*$name2*"):
                gettextbody = entry(0, gettextbody, "$") + guest_name + ", <br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == ("0").lower()  or lengtext.lower()  == "":
                    lengtext = "1"

            elif matches(gettextbody,r"*$hotelname3*"):
                gettextbody = entry(0, gettextbody, "$") + hotel_name + ". <br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == ("0").lower()  or lengtext.lower()  == "":
                    lengtext = "1"

            elif matches(gettextbody,r"*$hotelname4*"):
                gettextbody = hotel_name + ". <br><br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == ("0").lower()  or lengtext.lower()  == "":
                    lengtext = "1"
            else:
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == ("0").lower()  or lengtext.lower()  == "":
                    lengtext = "1"
        OUTPUT STREAM sbody1 CLOSE
        INPUT STREAM sbody2 CLOSE
        body = FILE fletter
        php_script = "<?php" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';" + chr_unicode(10) + "$mail = new PHPMailer;" + chr_unicode(10) + "$mail->isSMTP();" + chr_unicode(10) + "$mail->Host = '" + serveraddress + "';" + chr_unicode(10) + "$mail->SMTPAuth = true;" + chr_unicode(10) + "$mail->username = '" + username + "';" + chr_unicode(10) + "$mail->password = '" + password + "';" + chr_unicode(10) + "$mail->SMTPSecure = '" + security + "';" + chr_unicode(10) + "$mail->Port = " + portaddress + ";" + chr_unicode(10) + "$mail->setFrom('" + username + "', '" + name_from + "');" + chr_unicode(10) + "$mail->addAddress('" + emailadr + "');" + chr_unicode(10) + "$mail->isHTML(true);" + chr_unicode(10) + "$mail->subject = '" + subject + "';" + chr_unicode(10) + "$mail->body = '" + body + "';" + chr_unicode(10) + "$mail->addAttachment('" + bill_location + "');" + chr_unicode(10) + "if(!$mail->send()) " + chr_unicode(123) + chr_unicode(10) + " echo 'Message could not be sent.';" + chr_unicode(10) + " echo 'Mailer Error: ' . $mail->ErrorInfo;" + chr_unicode(10) + chr_unicode(125) + " else " + chr_unicode(123) + chr_unicode(10) + " echo 'Message has been sent';" + chr_unicode(10) + chr_unicode(125) + chr_unicode(10) + "?>" + chr_unicode(10)

        OS_COMMAND VALUE ("php " + php_path)


    def decode_string(in_str:string):

        nonlocal mess_str, send_email, serveraddress, portaddress, username, password, filepath, filepath1, subject, fletter, cc_email, pointer, security, name_from, bill_location, checkin_date, checkout_date, guest_name, hotel_name, emailadr, licensenr, paramtext, htparam, res_line, guest
        nonlocal send_current_bill, bill_number, guest_number, rsv_number, rsvline_number, selected_bill_number, base64_bill

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

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 240)]})

    if not paramtext:

        return generate_output()

    if paramtext.ptexte == "":

        return generate_output()

    if paramtext and paramtext.ptexte != "":
        hotel_name = decode_string(paramtext.ptexte)
    name_from = hotel_name

    htparam = get_cache (Htparam, {"paramnr": [(eq, 2404)]})

    if htparam:

        if htparam.fchar != "" and htparam.fchar != None:
            serveraddress = entry(0, htparam.fchar, ";")
            portaddress = entry(1, htparam.fchar, ";")
            username = entry(2, htparam.fchar, ";")
            password = entry(3, htparam.fchar, ";")
            security = entry(4, htparam.fchar, ";")
            send_email = True


        else:
            send_email = False
            mess_str = "Parameter 2404 Not Set, Send email not available!"

            return generate_output()

    if selected_bill_number == 0:
        selected_bill_number = 1

    res_line = get_cache (Res_line, {"resnr": [(eq, rsv_number)],"reslinnr": [(eq, rsvline_number)]})

    if res_line:

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        if guest.karteityp != 0:
            send_email = False
            mess_str = "This Guest Not Eligible To Receive This Bill! Please Check Bill Receiver!"

            return generate_output()
        emailadr = guest.email_adr
        checkin_date = res_line.ankunft
        checkout_date = res_line.abreise
        guest_name = res_line.name
    subject = "Invoice For Your Stay From " + to_string(checkin_date, "99/99/9999") + " To " + to_string(checkout_date, "99/99/9999") + " At " + hotel_name.upper()
    pointer = base64_decode(base64_bill)

    bill_location = "/usr1/vhp/tmp/" + licensenr + "/Invoice-" + to_string(bill_number) + "-" + to_string(rsv_number) + "-" + to_string(selected_bill_number) + ".pdf"

    if emailadr == "":
        send_email = False
        mess_str = "This Guest Not Eligible To Receive This Bill! Guest Email Still Empty!"

        return generate_output()
    sendemail()
    send_email = True
    mess_str = "Process Done"

    return generate_output()