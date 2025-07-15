#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Paramtext, Htparam

rsv_list_data, Rsv_list = create_model("Rsv_list", {"resnr":int, "reslinnr":int, "gastnr":int, "rsv_name":string, "zinr":string, "resline_name":string, "ankunft":date, "abreise":date, "email":string, "idcard_flag":bool, "selected":bool, "status_msg":string, "mci_flag":bool, "pci_flag":bool, "email_sent":bool})

def precheckin_sendemailbl(rsv_list_data:[Rsv_list]):

    prepare_cache ([Queasy, Paramtext, Htparam])

    msg_str = ""
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
    cpersonalkey:string = ""
    rkey:bytes = None
    mmemptrout:bytes = None
    interval_date:int = 0
    arrival_date:date = None
    ci_date:date = None
    ci_date87:date = None
    start_date:date = None
    hotelcode:string = ""
    md5htlcode:string = ""
    en_hotelencrip:string = ""
    oth_hotelencrip:string = ""
    created_date:date = None
    yy:int = 0
    mm:int = 0
    dd:int = 0
    do_it:bool = False
    hotelname:string = ""
    hoteladdress:string = ""
    hotelcity:string = ""
    hoteltelp:string = ""
    hotelemail:string = ""
    hotelwebsite:string = ""
    hotelheaderimg:string = ""
    hotelfooterimg:string = ""
    precheckinurl:string = ""
    php_path:string = ""
    temp_htm_path:string = ""
    put_htm_path:string = ""
    licensenr:string = ""
    queasy = paramtext = htparam = None

    rsv_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, cpersonalkey, rkey, mmemptrout, interval_date, arrival_date, ci_date, ci_date87, start_date, hotelcode, md5htlcode, en_hotelencrip, oth_hotelencrip, created_date, yy, mm, dd, do_it, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, hotelwebsite, hotelheaderimg, hotelfooterimg, precheckinurl, php_path, temp_htm_path, put_htm_path, licensenr, queasy, paramtext, htparam


        nonlocal rsv_list

        return {"msg_str": msg_str}

    def decode_string(in_str:string):

        nonlocal msg_str, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, cpersonalkey, rkey, mmemptrout, interval_date, arrival_date, ci_date, ci_date87, start_date, hotelcode, md5htlcode, en_hotelencrip, oth_hotelencrip, created_date, yy, mm, dd, do_it, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, hotelwebsite, hotelheaderimg, hotelfooterimg, precheckinurl, php_path, temp_htm_path, put_htm_path, licensenr, queasy, paramtext, htparam


        nonlocal rsv_list

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


    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 216) & (Queasy.number1 == 8)).order_by(Queasy._recid).all():

        if queasy.number2 == 19:
            hotelname = queasy.char3

        if queasy.number2 == 20:
            hoteladdress = queasy.char3

        if queasy.number2 == 21:
            hotelcity = queasy.char3

        if queasy.number2 == 22:
            hoteltelp = queasy.char3

        if queasy.number2 == 23:
            hotelemail = queasy.char3

        if queasy.number2 == 24:
            smtp = queasy.char3

        if queasy.number2 == 25:
            port = queasy.char3

        if queasy.number2 == 26:
            username = queasy.char3

        if queasy.number2 == 27:
            password = queasy.char3

        if queasy.number2 == 28:
            security = queasy.char3

        if queasy.number2 == 29:
            interval_date = to_int(queasy.char3)

        if queasy.number2 == 30:
            subject = queasy.char3

        if queasy.number2 == 31:
            hotelcode = queasy.char3

    if smtp == "":
        msg_str = "SMPT Server Not Configured Yet"

        return generate_output()

    if username == "":
        msg_str = "Email Sender Not Configured Yet"

        return generate_output()

    if hotelcode == "":
        msg_str = "hotelcode Not Configured Yet"

        return generate_output()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date87 = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 7)],"number2": [(eq, 2)]})

    if queasy:
        hotelwebsite = queasy.char3

    queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 7)],"number2": [(eq, 3)]})

    if queasy:
        hotelheaderimg = queasy.char3

    queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 7)],"number2": [(eq, 4)]})

    if queasy:
        hotelfooterimg = queasy.char3

    queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 7)],"number2": [(eq, 5)]})

    if queasy:
        precheckinurl = queasy.char3
    php_path = "/usr1/vhp/tmp/" + licensenr + "/send-email-precheckin.php"
    temp_htm_path = "/usr1/vhp/tmp/" + licensenr + "/pre-check-in-template.htm"
    put_htm_path = "/usr1/vhp/tmp/" + licensenr + "/pre-check-in-email.htm"

    for rsv_list in query(rsv_list_data, filters=(lambda rsv_list: rsv_list.selected)):
        en_hotelencrip = chr_unicode(34) + "ENG|" + hotelcode + "|" + to_string(rsv_list.ankunft) + "|" + to_string(rsv_list.resnr) + chr_unicode(34)
        name_from = hotelemail
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
        oth_hotelencrip = chr_unicode(34) + "IDN|" + hotelcode + "|" + to_string(rsv_list.ankunft) + "|" + to_string(rsv_list.resnr) + chr_unicode(34)
        cpersonalkey = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
        rkey = create_cipher_suite(cpersonalkey)
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

        if SEARCH (php_path) != None:
            OS_DELETE VALUE (php_path)
        outfile_tmp = temp_htm_path
        outfile = put_htm_path
        OUTPUT STREAM s1 TO VALUE (outfile)
        INPUT STREAM s2 FROM VALUE (outfile_tmp)
        while True:
            textbody = ""
            strlen = ""
            IMPORT STREAM s2 UNFORMATTED textbody

            if matches(textbody,r"*$URL-hotelwebsite*"):
                textbody = entry(0, textbody, "$") + hotelwebsite + substring(entry(1, textbody, "$") , 16)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$2URL-hotelwebsite*"):
                textbody = entry(0, textbody, "$") + hotelwebsite + substring(entry(1, textbody, "$") , 17)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$EN-GUESTNAME*"):
                textbody = entry(0, textbody, "$") + rsv_list.resline_name + " " + substring(entry(1, textbody, "$") , 12)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$EN-HOTELNAME1*"):

                if matches(entry(1, textbody, "$"),r"*EN-HOTELNAME1*"):
                    textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 13) + "$" + entry(2, textbody, "$") + "$" + entry(3, textbody, "$")

                if matches(entry(1, textbody, "$"),r"*EN-ARRIVALDATE*"):
                    textbody = entry(0, textbody, "$") + to_string(rsv_list.ankunft, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 14) + "$" + entry(2, textbody, "$")

                if matches(entry(1, textbody, "$"),r"*EN-DEPARTDATE*"):
                    textbody = entry(0, textbody, "$") + to_string(rsv_list.abreise, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$EN-RESNO*"):
                textbody = entry(0, textbody, "$") + to_string(rsv_list.resnr) + " " + substring(entry(1, textbody, "$") , 8)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$EN-URLPRECHECKIN*"):
                textbody = entry(0, textbody, "$") + precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + en_hotelencrip + substring(entry(1, textbody, "$") , 16)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$EN-hoteltelp*"):
                textbody = entry(0, textbody, "$") + hoteltelp + " " + substring(entry(1, textbody, "$") , 12)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$EN-hotelemail*"):
                textbody = entry(0, textbody, "$") + hotelemail + " " + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$EN-HOTELNAME2*"):
                textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-GUESTNAME*"):
                textbody = entry(0, textbody, "$") + rsv_list.resline_name + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-HOTELNAME1*"):

                if matches(entry(1, textbody, "$"),r"*OTH-HOTELNAME1*"):
                    textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 14) + "$" + entry(2, textbody, "$") + "$" + entry(3, textbody, "$")

                if matches(entry(1, textbody, "$"),r"*OTH-ARRIVALDATE*"):
                    textbody = entry(0, textbody, "$") + to_string(rsv_list.ankunft, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 15) + "$" + entry(2, textbody, "$")

                if matches(entry(1, textbody, "$"),r"*OTH-DEPARTDATE*"):
                    textbody = entry(0, textbody, "$") + to_string(rsv_list.abreise, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 14)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-HOTELNAME1*"):
                textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 14)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-RESNO*"):
                textbody = entry(0, textbody, "$") + to_string(rsv_list.resnr) + " " + substring(entry(1, textbody, "$") , 9)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-URLPRECHECKIN*"):
                textbody = entry(0, textbody, "$") + precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + oth_hotelencrip + substring(entry(1, textbody, "$") , 21)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-hoteltelp*"):
                textbody = entry(0, textbody, "$") + hoteltelp + " " + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-hotelemail*"):
                textbody = entry(0, textbody, "$") + hotelemail + " " + substring(entry(1, textbody, "$") , 14)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$OTH-HOTELNAME2*"):
                textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 14)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"
            else:
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"
        OUTPUT STREAM s1 CLOSE
        INPUT STREAM s2 CLOSE
        body = FILE outfile
        php_script = "<?php" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';" + chr_unicode(10) + "$mail = new PHPMailer;" + chr_unicode(10) + "$mail->isSMTP();" + chr_unicode(10) + "$mail->Host = '" + smtp + "';" + chr_unicode(10) + "$mail->SMTPAuth = true;" + chr_unicode(10) + "$mail->username = '" + username + "';" + chr_unicode(10) + "$mail->password = '" + password + "';" + chr_unicode(10) + "$mail->SMTPSecure = '" + security + "';" + chr_unicode(10) + "$mail->port = " + port + ";" + chr_unicode(10) + "$mail->setFrom('" + username + "', '" + name_from + "');" + chr_unicode(10) + "$mail->addAddress('" + rsv_list.email + "');" + chr_unicode(10) + "$mail->isHTML(true);" + chr_unicode(10) + "$mail->subject = '" + subject + "';" + chr_unicode(10) + "$mail->body = '" + body + "';" + chr_unicode(10) + "if(!$mail->send()) " + chr_unicode(123) + chr_unicode(10) + " echo 'Message could not be sent.';" + chr_unicode(10) + " echo 'Mailer Error: ' . $mail->ErrorInfo;" + chr_unicode(10) + chr_unicode(125) + " else " + chr_unicode(123) + chr_unicode(10) + " echo 'Message has been sent';" + chr_unicode(10) + chr_unicode(125) + chr_unicode(10) + "?>" + chr_unicode(10)
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 898
        queasy.number1 = rsv_list.resnr
        queasy.number2 = rsv_list.reslinnr
        queasy.char1 = rsv_list.email
        queasy.date1 = get_current_date()


        rsv_list.status_msg = "Email Sent to : " + queasy.char1 + " date : " + to_string(queasy.date1)

        OS_COMMAND VALUE ("php " + php_path)
    msg_str = "Done"

    return generate_output()