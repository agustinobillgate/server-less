from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Queasy, Htparam

def precheckin_sendemailbl(rsv_list:[Rsv_list]):
    guest_list_list = []
    msg_str = ""
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
    cpersonalkey:str = ""
    rkey:bytes = None
    mmemptrout:bytes = None
    interval_date:int = 0
    arrival_date:date = None
    ci_date:date = None
    ci_date87:date = None
    start_date:date = None
    hotelcode:str = ""
    md5htlcode:str = ""
    en_hotelencrip:str = ""
    oth_hotelencrip:str = ""
    created_date:date = None
    yy:int = 0
    mm:int = 0
    dd:int = 0
    do_it:bool = False
    hotelname:str = ""
    hoteladdress:str = ""
    hotelcity:str = ""
    hoteltelp:str = ""
    hotelemail:str = ""
    hotelwebsite:str = ""
    hotelheaderimg:str = ""
    hotelfooterimg:str = ""
    precheckinurl:str = ""
    otherurlcode:str = ""
    queasy = htparam = None

    arl_list = rsv_list = guest_list = None

    arl_list_list, Arl_list = create_model("Arl_list", {"resnr":int, "reslinnr":int, "gastnr":int, "rsv_name":str, "zinr":str, "resline_name":str, "ankunft":date, "abreise":date, "email":str, "idcard_flag":bool, "selected":bool, "status_msg":str, "mci_flag":bool, "pci_flag":bool})
    rsv_list_list, Rsv_list = create_model_like(Arl_list, {"email_sent":bool})
    guest_list_list, Guest_list = create_model_like(Rsv_list)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest_list_list, msg_str, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, cpersonalkey, rkey, mmemptrout, interval_date, arrival_date, ci_date, ci_date87, start_date, hotelcode, md5htlcode, en_hotelencrip, oth_hotelencrip, created_date, yy, mm, dd, do_it, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, hotelwebsite, hotelheaderimg, hotelfooterimg, precheckinurl, otherurlcode, queasy, htparam


        nonlocal arl_list, rsv_list, guest_list
        nonlocal arl_list_list, rsv_list_list, guest_list_list
        return {"guest-list": guest_list_list, "msg_str": msg_str}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 8)).all():

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

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date87 = htparam.fdate

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 2)).first()

    if queasy:
        hotelwebsite = queasy.char3

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 3)).first()

    if queasy:
        hotelheaderimg = queasy.char3

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 4)).first()

    if queasy:
        hotelfooterimg = queasy.char3

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 5)).first()

    if queasy:
        precheckinurl = queasy.char3

    for rsv_list in query(rsv_list_list, filters=(lambda rsv_list :rsv_list.SELECTED)):
        en_hotelencrip = "ENG|" + hotelcode + "|" + to_string(rsv_list.ankunft) + "|" + to_string(rsv_list.resnr)
        name_from = "Reservation@" + hotelname
        cpersonalkey = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
        rkey = GENERATE_PBE_KEY (cpersonalkey)
        mmemptrout = ENCRYPT (en_hotelencrip, rkey)
        en_hotelencrip = BASE64_ENCODE (mmemptrout)


        pass

        if SEARCH ("/usr1/vhp/tmp/send_email_precheckin.php") != None:
            OS_DELETE VALUE ("/usr1/vhp/tmp/send_email_precheckin.php")
        outfile_tmp = "/usr1/vhp/tmp/pre_check_in_template.htm"
        outfile = "/usr1/vhp/tmp/pre_check_in_email.htm"
        OUTPUT STREAM s1 TO VALUE (outfile)
        INPUT STREAM s2 FROM VALUE (outfile_tmp)
        REPEAT:
        textbody = ""
        strlen = ""
        IMPORT STREAM s2 UNFORMATTED textbody

        if re.match(".*\$URL_hotelwebsite.*",textbody):
            textbody = entry(0, textbody, "$") + hotelwebsite + substring(entry(1, textbody, "$") , 16)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$2URL_hotelwebsite.*",textbody):
            textbody = entry(0, textbody, "$") + hotelwebsite + substring(entry(1, textbody, "$") , 17)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$EN_GUESTNAME.*",textbody):
            textbody = entry(0, textbody, "$") + rsv_list.resline_name + " " + substring(entry(1, textbody, "$") , 12)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$EN_HOTELNAME1.*",textbody):

            if re.match(".*EN_HOTELNAME1.*",entry(1, textbody, "$")):
                textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 13) + "$" + entry(2, textbody, "$") + "$" + entry(3, textbody, "$")

            if re.match(".*EN_ARRIVALDATE.*",entry(1, textbody, "$")):
                textbody = entry(0, textbody, "$") + to_string(rsv_list.ankunft, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 14) + "$" + entry(2, textbody, "$")

            if re.match(".*EN_DEPARTDATE.*",entry(1, textbody, "$")):
                textbody = entry(0, textbody, "$") + to_string(rsv_list.abreise, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$EN_RESNO.*",textbody):
            textbody = entry(0, textbody, "$") + to_string(rsv_list.resnr) + " " + substring(entry(1, textbody, "$") , 8)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$EN_URLPRECHECKIN.*",textbody):
            textbody = entry(0, textbody, "$") + precheckinurl + "?" + en_hotelencrip + substring(entry(1, textbody, "$") , 16)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$EN_hoteltelp.*",textbody):
            textbody = entry(0, textbody, "$") + hoteltelp + " " + substring(entry(1, textbody, "$") , 12)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$EN_hotelemail.*",textbody):
            textbody = entry(0, textbody, "$") + hotelemail + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$EN_HOTELNAME2.*",textbody):
            textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_GUESTNAME.*",textbody):
            textbody = entry(0, textbody, "$") + rsv_list.resline_name + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_HOTELNAME1.*",textbody):

            if re.match(".*OTH_HOTELNAME1.*",entry(1, textbody, "$")):
                textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 14) + "$" + entry(2, textbody, "$") + "$" + entry(3, textbody, "$")

            if re.match(".*OTH_ARRIVALDATE.*",entry(1, textbody, "$")):
                textbody = entry(0, textbody, "$") + to_string(rsv_list.ankunft, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 15) + "$" + entry(2, textbody, "$")

            if re.match(".*OTH_DEPARTDATE.*",entry(1, textbody, "$")):
                textbody = entry(0, textbody, "$") + to_string(rsv_list.abreise, "99/99/9999") + " " + substring(entry(1, textbody, "$") , 14)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_HOTELNAME1.*",textbody):
            textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 14)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_RESNO.*",textbody):
            textbody = entry(0, textbody, "$") + to_string(rsv_list.resnr) + " " + substring(entry(1, textbody, "$") , 9)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_URLPRECHECKIN.*",textbody):
            otherurlcode = entry(1, textbody, "$")
            otherurlcode = entry(2, otherurlcode, "-")
            otherurlcode = substring(otherurlcode, 0, 3)
            oth_hotelencrip = "IDN|" + hotelcode + "|" + to_string(rsv_list.ankunft) + "|" + to_string(rsv_list.resnr)
            cpersonalkey = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
            rkey = GENERATE_PBE_KEY (cpersonalkey)
            mmemptrout = ENCRYPT (oth_hotelencrip, rkey)
            oth_hotelencrip = BASE64_ENCODE (mmemptrout)


            textbody = entry(0, textbody, "$") + precheckinurl + "?" + oth_hotelencrip + substring(entry(1, textbody, "$") , 21)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_hoteltelp.*",textbody):
            textbody = entry(0, textbody, "$") + hoteltelp + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_hotelemail.*",textbody):
            textbody = entry(0, textbody, "$") + hotelemail + " " + substring(entry(1, textbody, "$") , 14)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$OTH_HOTELNAME2.*",textbody):
            textbody = entry(0, textbody, "$") + hotelname + " " + substring(entry(1, textbody, "$") , 14)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"
        else:
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"
    OUTPUT STREAM s1 CLOSE
    INPUT STREAM s2 CLOSE
    body = FILE outfile    php_script = "<?php" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/PHPMailerAutoload.php';" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/class.smtp.php';" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/class.phpmailer.php';" + chr(10) + "$mail  ==  new PHPMailer;" + chr(10) + "$mail->isSMTP();" + chr(10) + "$mail->Host  ==  '" + smtp + "';" + chr(10) + "$mail->SMTPAuth  ==  true;" + chr(10) + "$mail->username  ==  '" + username + "';" + chr(10) + "$mail->password  ==  '" + password + "';" + chr(10) + "$mail->SMTPSecure  ==  '" + security + "';" + chr(10) + "$mail->port  ==  " + port + ";" + chr(10) + "$mail->setFrom('" + username + "', '" + name_from + "');" + chr(10) + "$mail->addAddress('" + rsv_list.email + "');" + chr(10) + "$mail->isHTML(true);" + chr(10) + "$mail->subject  ==  '" + subject + "';" + chr(10) + "$mail->body  ==  '" + body + "';" + chr(10) + "if(!$mail->send()) " + chr(123) + chr(10) + "    echo 'Message could not be sent.';" + chr(10) + "    echo 'Mailer Error: ' . $mail->ErrorInfo;" + chr(10) + chr(125) + " else " + chr(123) + chr(10) + "    echo 'Message has been sent';" + chr(10) + chr(125) + chr(10) + "?>" + chr(10)
    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 898
    queasy.number1 = rsv_list.resnr
    queasy.number2 = rsv_list.reslinnr
    queasy.char1 = rsv_list.email
    queasy.date1 = get_current_date()


    rsv_list.status_msg = "Email Sent to : " + queasy.char1 + " date : " + to_string(queasy.date1)
    COPY_LOB php_script TO FILE "/usr1/vhp/tmp/send_email_precheckin.php"
    OS_COMMAND VALUE ("php /usr1/vhp/tmp/send_email_precheckin.php")
    msg_str = "Done"

    return generate_output()