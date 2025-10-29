#using conversion tools version: 1.0.0.117
"""_yusufwijasena_28/10/2025

    Ticket ID: 588D4B
        _remark_:   - fix python indentation
                    - fix var declaration
                    - changed string to str
                    - fix ("string").lower() to "string"
                    - fix INPUT/OUTPUT STREAM, using with open statement
                    - import subprocess
                    - fix OS-COMMAND & OS-DELETE 
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Paramtext, Htparam, Guest
import subprocess

def ar_printsoa_sendmail_webbl(send_current_bill:bool, guest_number:int, selected_inv_number:int, arrecid_list:str, base64_bill:str):

    prepare_cache ([Paramtext, Htparam, Guest])

    mess_str = ""
    send_email = False
    serveraddress = ""
    portaddress = ""
    username = ""
    password = ""
    filepath = ""
    filepath1 = ""
    subject = ""
    fletter = ""
    cc_email = ""
    pointer:bytes = None
    security = ""
    name_from = ""
    soa_location = ""
    checkin_date:date 
    checkout_date:date 
    guest_name = ""
    hotel_name = ""
    emailadr = ""
    licensenr = ""
    paramtext = htparam = guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, send_email, serveraddress, portaddress, username, password, filepath, filepath1, subject, fletter, cc_email, pointer, security, name_from, soa_location, checkin_date, checkout_date, guest_name, hotel_name, emailadr, licensenr, i, paramtext, htparam, guest
        nonlocal send_current_bill, guest_number, selected_inv_number, arrecid_list, base64_bill

        return {
            "mess_str": mess_str, 
            "send_email": send_email
            }

    def sendemail():
        nonlocal mess_str, send_email, serveraddress, portaddress, username, password, filepath, filepath1, subject, fletter, cc_email, pointer, security, name_from, soa_location, checkin_date, checkout_date, guest_name, hotel_name, emailadr, licensenr, i, paramtext, htparam, guest
        nonlocal send_current_bill, guest_number, selected_inv_number, arrecid_list, base64_bill

        msg_str = ""
        gettextbody = ""
        lengtext = ""
        get_str = ""
        emailexist:bool = False
        body = ""
        php_script = ""
        php_path = ""
        output_path = ""
        result_msg = ""
        full_msg = ""

        if not emailadr :
            mess_str = "No Email Address For This Guest!"

        if length(emailadr) < 5:
            mess_str = "Incorrect Email Address : " + emailadr

        fletter = "/usr1/vhp/tmp/" + licensenr + "/soainv-body.htm"
        php_path = "/usr1/vhp/tmp/" + licensenr + "/send-invoice-byemail.php"
        # OUTPUT STREAM sbody1 TO VALUE (fletter)
        # INPUT STREAM sbody2 FROM VALUE ("/usr1/vhp/tmp/" + licensenr + "/soainv-body-temp.htm")
        with open(fletter, 'w', encoding='utf-8') as sbody1, open("usr1/vhp/tmp/" + licensenr + "/soainv-body-temp.htm", 'r', encoding='utf-8') as sbody2:
            for line in sbody2:
                sbody1.write(line)
                
        while True:
            gettextbody = ""
            lengtext = ""
            # IMPORT STREAM sbody2 UNFORMATTED gettextbody
            with open("usr1/vhp/tmp/" + licensenr + "/soainv-body-temp.htm", 'r', encoding='utf-8') as sbody2:
                gettextbody = gettextbody.strip()

            if matches(gettextbody,r"*$hotelname1*"):
                gettextbody = entry(0, gettextbody, "$") + hotel_name + ", <br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == "0"  or lengtext.lower()  == "":
                    lengtext = "1"
                    break
                
                break

            elif matches(gettextbody,r"*$hotelname2*"):
                gettextbody = hotel_name + ". <br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == "0"  or lengtext.lower()  == "":
                    lengtext = "1"
                    break
                
                break

            elif matches(gettextbody,r"*$hotelname3*"):
                gettextbody = entry(0, gettextbody, "$") + hotel_name + ". <br><br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == "0"  or lengtext.lower()  == "":
                    lengtext = "1"
                    break
                
                break

            elif matches(gettextbody,r"*$hotelname4*"):
                gettextbody = hotel_name + ", <br><br>"
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == "0"  or lengtext.lower()  == "":
                    lengtext = "1"
                    break
                
                break
            
            else:
                lengtext = to_string(length(gettextbody))

                if lengtext.lower()  == "0"  or lengtext.lower()  == "":
                    lengtext = "1"
                    break
                
                break
        # menggunakan with open agar dapat menutup otomatis ketika baris selesai dikerjakan
        # OUTPUT STREAM sbody1 CLOSE
        # INPUT STREAM sbody2 CLOSE
        
        # body = FILE fletter
        with open(fletter, 'r', encoding="utf-8") as sbody:
            body = sbody.read()
            
        php_script = "<?php" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';" + chr_unicode(10) + "try" + chr_unicode(123) + chr_unicode(10) + " $mail = new PHPMailer(true);" + chr_unicode(10) + " $mail->isSMTP();" + chr_unicode(10) + " $mail->Host = '" + serveraddress + "';" + chr_unicode(10) + " $mail->SMTPAuth = true;" + chr_unicode(10) + " $mail->username = '" + username + "';" + chr_unicode(10) + " $mail->password = '" + password + "';" + chr_unicode(10) + " $mail->SMTPSecure = '" + security + "';" + chr_unicode(10) + " $mail->Port = " + portaddress + ";" + chr_unicode(10) + " $mail->setFrom('" + username + "', '" + name_from + "');" + chr_unicode(10) + " $mail->addAddress('" + emailadr + "');" + chr_unicode(10) + " $mail->isHTML(true);" + chr_unicode(10) + " $mail->subject = '" + subject + "';" + chr_unicode(10) + " $mail->body = '" + body + "';" + chr_unicode(10) + " $mail->addAttachment('" + soa_location + "');" + chr_unicode(10) + " $mail->send();" + chr_unicode(10) + " echo 'Message has been sent'. PHP_EOL;" + chr_unicode(10) + chr_unicode(125) + chr_unicode(10) + "catch (phpmailerException $e)" + chr_unicode(123) + chr_unicode(10) + " echo $mail->ErrorInfo . PHP_EOL;" + chr_unicode(10) + chr_unicode(125) + chr_unicode(10) + "catch (Exception $e) " + chr_unicode(123) + chr_unicode(10) + " echo $e->getMessage() . PHP_EOL;" + chr_unicode(10) + chr_unicode(125) + chr_unicode(10) + "?>" + chr_unicode(10)

        output_path = "/usr1/vhp/tmp/" + licensenr + "/php-mail-result.txt"
        
        # OS_COMMAND VALUE ("php " + php_path + " > " + output_path + " 2>&1")
        # INPUT FROM VALUE (output_path)
        # while True:
        #     IMPORT UNFORMATTED result_msg

        #     if result_msg == None:
        #         result_msg = ""
        #     full_msg = full_msg + result_msg
        # INPUT CLOSE
        
        with open(output_path, 'w') as outFile:
            subprocess.run(["php", php_path], stdout = outFile, stderr = subprocess.STDOUT) 
        
        with open(output_path, 'r', encoding="utf-8") as outFile:
            for result_msg in outFile:
                if result_msg == None:
                    result_msg = ""
                full_msg = full_msg + result_msg

        if get_index(entry(0, full_msg, chr_unicode(10)) , "Message has been sent") <= 0:
            send_email = False
            mess_str = full_msg

        # OS_DELETE VALUE (output_path)
        # OS_DELETE VALUE (soa_location)
        
        if os.path.exists(output_path):
            os.remove(output_path)
            
        if os.path.exists(soa_location):
            os.remove(soa_location)


    def decode_string(in_str:string):
        nonlocal mess_str, send_email, serveraddress, portaddress, username, password, filepath, filepath1, subject, fletter, cc_email, pointer, security, name_from, soa_location, checkin_date, checkout_date, guest_name, hotel_name, emailadr, licensenr, i, paramtext, htparam, guest
        nonlocal send_current_bill, guest_number, selected_inv_number, arrecid_list, base64_bill

        out_str = ""
        s = ""
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
        # if htparam.fchar != "" and htparam.fchar != None:
        if not htparam.fchar and not htparam.fchar :
            for i in range(1,num_entries(htparam.fchar, ";")  + 1) :
                if i == 1:
                    serveraddress = entry(0, htparam.fchar, ";")
                elif i == 2:
                    portaddress = entry(1, htparam.fchar, ";")
                elif i == 3:
                    username = entry(2, htparam.fchar, ";")
                elif i == 4:
                    password = entry(3, htparam.fchar, ";")
                elif i == 5:
                    security = entry(4, htparam.fchar, ";")
            send_email = True

            if serveraddress == "":
                send_email = False
                mess_str = "Server Address not set correctly on parameter 2404, Send email not available!"

                return generate_output()

            elif portaddress == "":
                send_email = False
                mess_str = "Port Address not set correctly on parameter 2404, Send email not available!"

                return generate_output()

            elif username == "":
                send_email = False
                mess_str = "username not set correctly on parameter 2404, Send email not available!"

                return generate_output()

            elif password == "":
                send_email = False
                mess_str = "password not set correctly on parameter 2404, Send email not available!"

                return generate_output()

            elif security == "":
                send_email = False
                mess_str = "security not set correctly on parameter 2404, Send email not available!"

                return generate_output()
        else:
            send_email = False
            mess_str = "Parameter 2404 Not Set, Send email not available!"

            return generate_output()

    if selected_inv_number == 0:
        selected_inv_number = 1

    guest = get_cache (Guest, {"gastnr": [(eq, guest_number)]})

    if guest:
        emailadr = guest.email_adr
        guest_name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
    subject = "Invoice Statement of Account At " + hotel_name.upper()
    pointer = base64_decode(base64_bill)

    soa_location = "/usr1/vhp/tmp/" + licensenr + "/Invoice-" + to_string(guest_number) + "-" + arrecid_list + "-" + to_string(selected_inv_number) + ".pdf"

    if emailadr == "":
        send_email = False
        mess_str = "This Guest Not Eligible To Receive This Bill! Guest Email Still Empty!"

        return generate_output()
    sendemail()

    if send_email:
        send_email = True
        mess_str = "Process Done"

    return generate_output()