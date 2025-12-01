#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added, remark area
# skip -> script OE
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.res_checkin_deposit_paybl import res_checkin_deposit_paybl
from functions.res_checkin1bl import res_checkin1bl
from sqlalchemy import func
from functions.res_checkin2bl import res_checkin2bl
from models import Res_line, Guest, Queasy, Artikel, Waehrung, Guestbook, Zimmer, Paramtext

def mobileweb_res_checkin(rsv_number:int, rsvline_number:int, user_init:string, new_roomno:string, 
                          purposeofstay:string, email:string, guest_phnumber:string, guest_nation:string, 
                          guest_country:string, guest_region:string, vehicle_number:string, preauth_string:string, base64image:string):

    prepare_cache ([Res_line, Guest, Queasy, Artikel, Waehrung, Guestbook, Zimmer, Paramtext])

    checked_in = False
    new_resstatus = 0
    result_message = ""
    self_ci:bool = True
    can_checkin:bool = False
    msg_str:string = ""
    msg_str1:string = ""
    msg_str2:string = ""
    msg_str3:string = ""
    msg_str4:string = ""
    msg_answer:bool = False
    ask_deposit:bool = False
    keycard_flag:bool = False
    mcard_flag:bool = False
    err_number1:int = 0
    err_number2:int = 0
    err_number3:int = 0
    err_number4:int = 0
    q_143:bool = False
    fill_gcfemail:bool = False
    gast_gastnr:int = 0
    flag_report:bool = False
    warn_flag:bool = False
    silenzio:bool = False
    pofstay:int = 0
    pointer:bytes = None
    tmp_zwunsch:string = ""
    bankname:string = ""
    noref:string = ""
    resultmsg:string = ""
    ccnumber:string = ""
    amount:string = ""
    transdat:string = ""
    transid_merchant:string = ""
    mestoken:string = ""
    meskeyword:string = ""
    mesvalue:string = ""
    loop_i:int = 0
    payment_string:string = ""
    payment_type:string = ""
    found_flag:bool = False
    do_it:bool = False
    do_payment:bool = False
    doku_paymentdatetime:string = ""
    doku_purchasecurrency:string = ""
    doku_liability:string = ""
    doku_paymentchannel:string = ""
    doku_amount:string = ""
    doku_paymentcode:string = ""
    doku_mcn:string = ""
    doku_words:string = ""
    doku_resultmsg:string = ""
    doku_verifyid:string = ""
    doku_transidmerchant:string = ""
    doku_bank:string = ""
    doku_statustype:string = ""
    doku_approvalcode:string = ""
    doku_edustatus:string = ""
    doku_threedsecurestatus:string = ""
    doku_verifyscore:string = ""
    doku_currency:string = ""
    doku_responsecode:string = ""
    doku_chname:string = ""
    doku_brand:string = ""
    doku_verifystatus:string = ""
    doku_sessionid:string = ""
    doku_paymenttype:string = ""
    qris_dpmallid:string = ""
    qris_transid:string = ""
    qris_amount:string = ""
    qris_resultmsg:string = ""
    qris_transdatetime:string = ""
    qris_clientid:string = ""
    qris_transidmerchant:string = ""
    qris_responsecode:string = ""
    vhp_artno:int = 0
    vhp_artdep:int = 0
    pg_artstring:string = ""
    pg_artname:string = ""
    pg_artno:int = 0
    bill_date:date = None
    voucher_str:string = ""
    inv_nr:int = 0
    deposit_art:int = 0
    errorflag:bool = False
    deposit_pay:Decimal = to_decimal("0.0")
    deposit_exrate:Decimal = to_decimal("0.0")
    mail_resno:int = 0
    mail_reslinno:int = 0
    mail_transidmerchant:string = ""
    mail_datetimetrans:string = ""
    mail_paymentdesc:string = ""
    mail_totalamount:string = ""
    post_amount:Decimal = to_decimal("0.0")
    paymentcode:int = 0
    check_payment_exist:bool = False
    check_pay_str:string = ""
    res_line = guest = queasy = artikel = waehrung = guestbook = zimmer = paramtext = None

    rline = res_sharer = gbuff = receiver = mappingpg = wcisetup = None

    Rline = create_buffer("Rline",Res_line)
    Res_sharer = create_buffer("Res_sharer",Res_line)
    Gbuff = create_buffer("Gbuff",Guest)
    Receiver = create_buffer("Receiver",Guest)
    Mappingpg = create_buffer("Mappingpg",Queasy)
    Wcisetup = create_buffer("Wcisetup",Queasy)


    db_session = local_storage.db_session
    new_roomno = new_roomno.strip()
    purposeofstay = purposeofstay.strip()
    email = email.strip()
    guest_phnumber = guest_phnumber.strip()
    guest_nation = guest_nation.strip()
    guest_country = guest_country.strip()
    guest_region = guest_region.strip()
    vehicle_number = vehicle_number.strip()
    preauth_string = preauth_string.strip()
    base64image = base64image.strip()



    def generate_output():
        nonlocal checked_in, new_resstatus, result_message, self_ci, can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, msg_answer, ask_deposit, keycard_flag, mcard_flag, err_number1, err_number2, err_number3, err_number4, q_143, fill_gcfemail, gast_gastnr, flag_report, warn_flag, silenzio, pofstay, pointer, tmp_zwunsch, bankname, noref, resultmsg, ccnumber, amount, transdat, transid_merchant, mestoken, meskeyword, mesvalue, loop_i, payment_string, payment_type, found_flag, do_it, do_payment, doku_paymentdatetime, doku_purchasecurrency, doku_liability, doku_paymentchannel, doku_amount, doku_paymentcode, doku_mcn, doku_words, doku_resultmsg, doku_verifyid, doku_transidmerchant, doku_bank, doku_statustype, doku_approvalcode, doku_edustatus, doku_threedsecurestatus, doku_verifyscore, doku_currency, doku_responsecode, doku_chname, doku_brand, doku_verifystatus, doku_sessionid, doku_paymenttype, qris_dpmallid, qris_transid, qris_amount, qris_resultmsg, qris_transdatetime, qris_clientid, qris_transidmerchant, qris_responsecode, vhp_artno, vhp_artdep, pg_artstring, pg_artname, pg_artno, bill_date, voucher_str, inv_nr, deposit_art, errorflag, deposit_pay, deposit_exrate, mail_resno, mail_reslinno, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount, post_amount, paymentcode, check_payment_exist, check_pay_str, res_line, guest, queasy, artikel, waehrung, guestbook, zimmer, paramtext
        nonlocal rsv_number, rsvline_number, user_init, new_roomno, purposeofstay, email, guest_phnumber, guest_nation, guest_country, guest_region, vehicle_number, preauth_string, base64image
        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup


        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup

        return {"checked_in": checked_in, "new_resstatus": new_resstatus, "result_message": result_message}

    def sendmail(resno:int, reslinno:int, transidmerchant:string, datetimetrans:string, paymentdesc:string, totalamount:string):

        nonlocal checked_in, new_resstatus, result_message, self_ci, can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, msg_answer, ask_deposit, keycard_flag, mcard_flag, err_number1, err_number2, err_number3, err_number4, q_143, fill_gcfemail, gast_gastnr, flag_report, warn_flag, silenzio, pofstay, pointer, tmp_zwunsch, bankname, noref, resultmsg, ccnumber, amount, transdat, transid_merchant, mestoken, meskeyword, mesvalue, loop_i, payment_string, payment_type, found_flag, do_it, do_payment, doku_paymentdatetime, doku_purchasecurrency, doku_liability, doku_paymentchannel, doku_amount, doku_paymentcode, doku_mcn, doku_words, doku_resultmsg, doku_verifyid, doku_transidmerchant, doku_bank, doku_statustype, doku_approvalcode, doku_edustatus, doku_threedsecurestatus, doku_verifyscore, doku_currency, doku_responsecode, doku_chname, doku_brand, doku_verifystatus, doku_sessionid, doku_paymenttype, qris_dpmallid, qris_transid, qris_amount, qris_resultmsg, qris_transdatetime, qris_clientid, qris_transidmerchant, qris_responsecode, vhp_artno, vhp_artdep, pg_artstring, pg_artname, pg_artno, bill_date, voucher_str, inv_nr, deposit_art, errorflag, deposit_pay, deposit_exrate, mail_resno, mail_reslinno, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount, post_amount, paymentcode, check_payment_exist, check_pay_str, res_line, guest, queasy, artikel, waehrung, guestbook, zimmer, paramtext
        nonlocal rsv_number, rsvline_number, user_init, new_roomno, purposeofstay, email, guest_phnumber, guest_nation, guest_country, guest_region, vehicle_number, preauth_string, base64image
        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup


        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup

        hotelname:string = ""
        hoteladdress:string = ""
        hotelphone:string = ""
        hotelmail:string = ""
        hotelweb:string = ""
        roomnumber:string = ""
        cidate:string = ""
        codate:string = ""
        guestname:string = ""
        pax:string = ""
        bgcolor_code:string = ""
        licensenr:string = ""
        php_path:string = ""
        temp_htm_path:string = ""
        put_htm_path:string = ""
        php_script:string = ""
        smtp:string = ""
        username:string = ""
        password:string = ""
        security:string = ""
        port:string = ""
        email_from:string = ""
        name_from:string = ""
        guestemail:string = ""
        subject:string = ""
        body:string = ""
        textbody:string = ""
        outfile:string = ""
        outfile_tmp:string = ""
        strlen:string = ""
        hotel_copybill:string = ""

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

        if paramtext and paramtext.ptexte != "":
            licensenr = decode_string(paramtext.ptexte)
        php_path = "/usr1/vhp/tmp/" + licensenr + "/send-email-selfcheckin.php"
        temp_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhpselfcheckin-keyword.html"
        put_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhpselfcheckin.html"

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 216) & (Queasy.number1 == 8)).order_by(Queasy._recid).all():

            if queasy.number2 == 19:
                hotelname = queasy.char3

            if queasy.number2 == 20:
                hoteladdress = queasy.char3

            if queasy.number2 == 22:
                hotelphone = queasy.char3

            if queasy.number2 == 23:
                hotelmail = queasy.char3

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

        queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 7)],"number2": [(eq, 2)]})

        if queasy:
            hotelweb = queasy.char3

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"number2": [(eq, 3)],"betriebsnr": [(eq, 0)]})

        if queasy:
            bgcolor_code = queasy.char2

        queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"number2": [(eq, 20)],"betriebsnr": [(eq, 0)]})

        if queasy:
            hotel_copybill = queasy.char2

        res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        guestemail = guest.email_adr
        roomnumber = res_line.zinr
        cidate = to_string(res_line.ankunft)
        codate = to_string(res_line.abreise)
        guestname = res_line.name
        pax = to_string(res_line.erwachs)
        name_from = "FrontOffice @" + hotelname.upper()
        subject = "E-Invoice Deposit Payment @" + hotelname + "-" + transidmerchant

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

            if matches(textbody,r"*$bgColor*"):
                textbody = entry(0, textbody, "$") + " " + bgcolor_code + ";"
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$totalamount*"):
                textbody = "Rp " + totalamount
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$hotelname*"):
                textbody = hotelname
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$hoteladdress*"):
                textbody = entry(0, textbody, "$") + hoteladdress + " " + substring(entry(1, textbody, "$") , 12)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*Phone*"):
                textbody = "Phone: " + hotelphone + " | email: " + hotelmail
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$hotelweb*"):
                textbody = entry(0, textbody, "$") + hotelweb + " " + substring(entry(1, textbody, "$") , 8)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$transidmerchant*"):
                textbody = entry(0, textbody, "$") + transidmerchant + " " + substring(entry(1, textbody, "$") , 15)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$datetimetrans*"):
                textbody = entry(0, textbody, "$") + datetimetrans + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$resno*"):
                textbody = entry(0, textbody, "$") + to_string(resno) + " " + substring(entry(1, textbody, "$") , 5)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$roomno*"):
                textbody = entry(0, textbody, "$") + roomnumber + " " + substring(entry(1, textbody, "$") , 6)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$cidate*"):
                textbody = entry(0, textbody, "$") + cidate + " " + substring(entry(1, textbody, "$") , 6)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$codate*"):
                textbody = entry(0, textbody, "$") + codate + " " + substring(entry(1, textbody, "$") , 6)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$guestname*"):
                textbody = entry(0, textbody, "$") + guestname + " " + substring(entry(1, textbody, "$") , 9)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$adult*"):
                textbody = entry(0, textbody, "$") + pax + " " + substring(entry(1, textbody, "$") , 5)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$depositAMount*"):
                textbody = entry(0, textbody, "$") + totalamount + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$grandTotalAmount*"):
                textbody = entry(0, textbody, "$") + totalamount + substring(entry(1, textbody, "$") , 16)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*paymentTotalAmount*"):
                textbody = entry(0, textbody, "$") + "-" + totalamount + substring(entry(1, textbody, "$") , 18)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$paymentDescription*"):
                textbody = entry(0, textbody, "$") + paymentdesc + " " + substring(entry(1, textbody, "$") , 18)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            elif matches(textbody,r"*$paymentAmount*"):
                textbody = entry(0, textbody, "$") + "-" + totalamount + substring(entry(1, textbody, "$") , 13)
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
        php_script = "<?php" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';" + chr_unicode(10) + "$mail = new PHPMailer;" + chr_unicode(10) + "$mail->isSMTP();" + chr_unicode(10) + "$mail->Host = '" + smtp + "';" + chr_unicode(10) + "$mail->SMTPAuth = true;" + chr_unicode(10) + "$mail->username = '" + username + "';" + chr_unicode(10) + "$mail->password = '" + password + "';" + chr_unicode(10) + "$mail->SMTPSecure = '" + security + "';" + chr_unicode(10) + "$mail->port = " + port + ";" + chr_unicode(10) + "$mail->setFrom('" + username + "', '" + name_from + "');" + chr_unicode(10) + "$mail->addAddress('" + guestemail + "');" + chr_unicode(10) + "$mail->addCC('" + hotel_copybill + "');" + chr_unicode(10) + "$mail->isHTML(true);" + chr_unicode(10) + "$mail->subject = '" + subject + "';" + chr_unicode(10) + "$mail->body = '" + body + "';" + chr_unicode(10) + "if(!$mail->send()) " + chr_unicode(123) + chr_unicode(10) + " echo 'Message could not be sent.';" + chr_unicode(10) + " echo 'Mailer Error: ' . $mail->ErrorInfo;" + chr_unicode(10) + chr_unicode(125) + " else " + chr_unicode(123) + chr_unicode(10) + " echo 'Message has been sent';" + chr_unicode(10) + chr_unicode(125) + chr_unicode(10) + "?>" + chr_unicode(10)

        OS_COMMAND VALUE ("php " + php_path)


    def decode_string(in_str:string):

        nonlocal checked_in, new_resstatus, result_message, self_ci, can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, msg_answer, ask_deposit, keycard_flag, mcard_flag, err_number1, err_number2, err_number3, err_number4, q_143, fill_gcfemail, gast_gastnr, flag_report, warn_flag, silenzio, pofstay, pointer, tmp_zwunsch, bankname, noref, resultmsg, ccnumber, amount, transdat, transid_merchant, mestoken, meskeyword, mesvalue, loop_i, payment_string, payment_type, found_flag, do_it, do_payment, doku_paymentdatetime, doku_purchasecurrency, doku_liability, doku_paymentchannel, doku_amount, doku_paymentcode, doku_mcn, doku_words, doku_resultmsg, doku_verifyid, doku_transidmerchant, doku_bank, doku_statustype, doku_approvalcode, doku_edustatus, doku_threedsecurestatus, doku_verifyscore, doku_currency, doku_responsecode, doku_chname, doku_brand, doku_verifystatus, doku_sessionid, doku_paymenttype, qris_dpmallid, qris_transid, qris_amount, qris_resultmsg, qris_transdatetime, qris_clientid, qris_transidmerchant, qris_responsecode, vhp_artno, vhp_artdep, pg_artstring, pg_artname, pg_artno, bill_date, voucher_str, inv_nr, deposit_art, errorflag, deposit_pay, deposit_exrate, mail_resno, mail_reslinno, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount, post_amount, paymentcode, check_payment_exist, check_pay_str, res_line, guest, queasy, artikel, waehrung, guestbook, zimmer, paramtext
        nonlocal rsv_number, rsvline_number, user_init, new_roomno, purposeofstay, email, guest_phnumber, guest_nation, guest_country, guest_region, vehicle_number, preauth_string, base64image
        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup


        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup

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

    if guest_nation == None:
        guest_nation = ""

    if guest_country == None:
        guest_country = ""

    if guest_region == None:
        guest_region = ""

    if vehicle_number == None:
        vehicle_number = ""

    if preauth_string == None:
        preauth_string = ""

    if new_roomno == None:
        new_roomno = ""

    if base64image == None:
        base64image = ""

    if user_init == "" or user_init == None:
        result_message = "5 - User Init Can't Be Null!"

        return generate_output()

    if preauth_string.lower()  != "" and preauth_string.lower()  != ("CHECKROOMSTATUS").lower() :
        payment_string = preauth_string

        res_line = get_cache (Res_line, {"resnr": [(eq, rsv_number)],"reslinnr": [(eq, rsvline_number)]})

        if res_line:
            payment_type = entry(0, payment_string, ";")
            preauth_string = substring(payment_string, 5)

            queasy = get_cache (Queasy, {"key": [(eq, 237)],"number1": [(eq, rsv_number)],"number2": [(eq, rsvline_number)]})

            if queasy:
                queasy.char1 = payment_type
                queasy.char3 = preauth_string


            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 237
                queasy.number1 = rsv_number
                queasy.number2 = rsvline_number
                queasy.char1 = payment_type
                queasy.char3 = preauth_string
                queasy.logi1 = False
                queasy.logi2 = False

            if payment_type.lower()  == ("DOKU").lower() :
                paymentcode = 1
                for loop_i in range(1,num_entries(preauth_string, ";")  + 1) :
                    mestoken = entry(loop_i - 1, preauth_string, ";")
                    meskeyword = entry(0, mestoken, "=")
                    mesvalue = entry(1, mestoken, "=")

                    if meskeyword == "PAYMENTDATETIME":
                        doku_paymentdatetime = mesvalue
                    elif meskeyword == "PAYMENTCHANNEL":
                        doku_paymentchannel = mesvalue
                    elif meskeyword == "amount":
                        doku_amount = mesvalue
                    elif meskeyword == "MCN":
                        doku_mcn = mesvalue
                    elif meskeyword == "WORDS":
                        doku_words = mesvalue
                    elif meskeyword == "resultmsg":
                        doku_resultmsg = mesvalue
                    elif meskeyword == "transidmerchant":
                        doku_transidmerchant = mesvalue
                    elif meskeyword == "BANK":
                        doku_bank = mesvalue
                    elif meskeyword == "STATUSTYPE":
                        doku_statustype = mesvalue
                    elif meskeyword == "APPROVALCODE":
                        doku_approvalcode = mesvalue
                    elif meskeyword == "PAYMENTTYPE":
                        doku_paymenttype = mesvalue
                    elif meskeyword == "VERIFYSCORE":
                        doku_verifyscore = mesvalue
                    elif meskeyword == "CHNAME":
                        doku_chname = mesvalue
                    elif meskeyword == "BRAND":
                        doku_brand = mesvalue
                    elif meskeyword == "SESSIONID":
                        doku_sessionid = mesvalue

                queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, rsv_number)],"number2": [(eq, rsvline_number)]})

                if queasy:
                    queasy.char1 = doku_resultmsg
                    queasy.char2 = doku_transidmerchant + "|" + entry(1, queasy.char2, "|")
                    queasy.char3 = preauth_string


                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 223
                    queasy.number1 = rsv_number
                    queasy.number2 = rsvline_number
                    queasy.number3 = paymentcode
                    queasy.char1 = doku_resultmsg
                    queasy.char2 = doku_transidmerchant
                    queasy.char3 = preauth_string


                voucher_str = payment_type + "-" + doku_brand + "-" + doku_bank
                do_payment = False

                if doku_resultmsg.lower()  == ("SUCCESS").lower() :
                    do_payment = True

                if do_payment:
                    mail_transidmerchant = doku_transidmerchant
                    mail_datetimetrans = substring(doku_paymentdatetime, 6, 2) + "/" + substring(doku_paymentdatetime, 4, 2) + "/" + substring(doku_paymentdatetime, 0, 4) + " " + substring(doku_paymentdatetime, 8, 2) + ":" + substring(doku_paymentdatetime, 10, 2) + ":" + substring(doku_paymentdatetime, 12, 2)
                    mail_paymentdesc = doku_bank.upper() + " " + doku_brand.upper()
                    mail_totalamount = to_string(to_decimal(doku_amount) , "->>>,>>>.99")
                    post_amount =  to_decimal(to_decimal(doku_amount))

                    for mappingpg in db_session.query(Mappingpg).filter(
                             (Mappingpg.key == 224) & (Mappingpg.number1 == 1) & (Mappingpg.number2 == 0) & (Mappingpg.logi1)).order_by(Mappingpg._recid).yield_per(100):
                        pg_artstring = doku_paymentchannel
                        pg_artname = entry(0, mappingpg.char1, "-")

                        if pg_artstring.lower()  == (pg_artname).lower() :
                            vhp_artno = to_int(entry(0, mappingpg.char3, "-"))
                            vhp_artdep = mappingpg.number2
                            break

                    if vhp_artno == 0:
                        result_message = "9-No Mapping Found In VHP, Payment Not Posted"

                        return generate_output()

            elif payment_type.lower()  == ("MIDtrans").lower() :
                pass

            elif payment_type.lower()  == ("QRIS").lower() :
                paymentcode = 3
                for loop_i in range(1,num_entries(preauth_string, ";")  + 1) :
                    mestoken = entry(loop_i - 1, preauth_string, ";")
                    meskeyword = entry(0, mestoken, "=")
                    mesvalue = entry(1, mestoken, "=")

                    if meskeyword == "DPMALLID":
                        qris_dpmallid = mesvalue
                    elif meskeyword == "transID":
                        qris_transid = mesvalue
                    elif meskeyword == "amount":
                        qris_amount = mesvalue
                    elif meskeyword == "resultmsg":
                        qris_resultmsg = mesvalue
                    elif meskeyword == "transDATETIME":
                        qris_transdatetime = mesvalue
                    elif meskeyword == "CLIENTID":
                        qris_clientid = mesvalue
                    elif meskeyword == "transidmerchant":
                        qris_transidmerchant = mesvalue
                    elif meskeyword == "RESPONSECODE":
                        qris_responsecode = mesvalue

                queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, rsv_number)],"number2": [(eq, rsvline_number)]})

                if queasy:
                    queasy.char1 = qris_resultmsg
                    queasy.char2 = qris_transidmerchant + "|" + entry(1, queasy.char2, "|")
                    queasy.char3 = preauth_string


                else:
                    queasy = Queasy()
                    db_session.add(queasy)

                    queasy.key = 223
                    queasy.number1 = rsv_number
                    queasy.number2 = rsvline_number
                    queasy.number3 = paymentcode
                    queasy.char1 = qris_resultmsg
                    queasy.char2 = qris_transidmerchant
                    queasy.char3 = preauth_string


                voucher_str = payment_type + "-QRIS"
                do_payment = False

                if qris_resultmsg.lower()  == ("SUCCESS").lower() :
                    do_payment = True

                if do_payment:
                    mail_transidmerchant = qris_transidmerchant
                    mail_datetimetrans = substring(qris_transdatetime, 6, 2) + "/" + substring(qris_transdatetime, 4, 2) + "/" + substring(qris_transdatetime, 0, 4) + " " + substring(qris_transdatetime, 8, 2) + ":" + substring(qris_transdatetime, 10, 2) + ":" + substring(qris_transdatetime, 12, 2)
                    mail_paymentdesc = "QRIS"
                    mail_totalamount = to_string(to_decimal(qris_amount) , "->>>,>>>.99")
                    post_amount =  to_decimal(to_decimal(qris_amount))

                    for mappingpg in db_session.query(Mappingpg).filter(
                             (Mappingpg.key == 224) & (Mappingpg.number1 == 1) & (Mappingpg.number2 == 0) & (Mappingpg.logi1)).order_by(Mappingpg._recid).yield_per(100):
                        pg_artstring = "1"
                        pg_artname = entry(0, mappingpg.char1, "-")

                        if pg_artstring.lower()  == (pg_artname).lower() :
                            vhp_artno = to_int(entry(0, mappingpg.char3, "-"))
                            vhp_artdep = mappingpg.number2
                            break

                    if vhp_artno == 0:
                        result_message = "9-No Mapping Found In VHP, Payment Not Posted"

                        return generate_output()

            if do_payment:
                check_payment_exist = False

                if not check_payment_exist:

                    wcisetup = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 8)],"number2": [(eq, 34)]})

                    if wcisetup:
                        deposit_art = to_int(wcisetup.char3)

                    artikel = get_cache (Artikel, {"artnr": [(eq, deposit_art)],"departement": [(eq, 0)]})

                    if artikel.pricetab:

                        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

                        if waehrung:
                            deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)


                    msg_str, errorflag, deposit_pay = get_output(res_checkin_deposit_paybl(deposit_art, rsv_number, vhp_artno, post_amount, - post_amount, 1, voucher_str, user_init))

                    if not errorflag:
                        sendmail(rsv_number, rsvline_number, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount)
            result_message = "0 - Update PreAuth Success!"

            return generate_output()

    elif preauth_string.lower()  != "" and preauth_string.lower()  == ("CHECKROOMSTATUS").lower() :
        can_checkin = False

        if self_ci:
            silenzio = True
        can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, err_number1, err_number2, err_number3, err_number4, fill_gcfemail, gast_gastnr, q_143, flag_report, warn_flag = get_output(res_checkin1bl(1, rsv_number, rsvline_number, silenzio))

        if msg_str != "":
            result_message = "99 - " + msg_str

            return generate_output()
        err_number1 = 0
        err_number2 = 0

        if err_number1 != 0 or err_number2 != 0 or err_number3 != 0 or err_number4 != 0:

            if err_number1 == 1:
                result_message = "1 - " + msg_str1

                return generate_output()

            if err_number2 == 1:
                result_message = "2 - " + msg_str2

                return generate_output()

            if err_number3 == 1:
                result_message = "3 - " + msg_str3

                return generate_output()

            if err_number4 == 1:
                result_message = "4 - " + msg_str4

                return generate_output()

        if err_number1 == 0 and err_number2 == 0 and err_number3 == 0 and err_number4 == 0:
            can_checkin = True
        checked_in = can_checkin

        if checked_in:
            result_message = "0 - Guest Can Checkin"
        else:
            result_message = "1 - Guest Can not Checkin [" + result_message + "]"

    if purposeofstay != "":

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 143) & (matches(Queasy.char3,"*" + purposeofstay + "*"))).first()

        if queasy:
            pofstay = queasy.number1

    res_line = get_cache (Res_line, {"resnr": [(eq, rsv_number)],"reslinnr": [(eq, rsvline_number)]})

    if res_line:

        if pofstay != None:
            for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                mestoken = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                if substring(mestoken, 0, 8) == ("SEGM_PUR").lower() :
                    meskeyword = substring(mestoken, 0, 8)
                    mesvalue = to_string(pofstay)
                    mestoken = meskeyword + mesvalue
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
                    found_flag = True
                else:
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
            tmp_zwunsch = substring(tmp_zwunsch, 0, length(tmp_zwunsch) - 1)

            if not found_flag:
                tmp_zwunsch = tmp_zwunsch + "SEGM_PUR" + to_string(pofstay) + ";"
            res_line.zimmer_wunsch = tmp_zwunsch


        found_flag = False

        if vehicle_number != "":
            for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                mestoken = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                if entry(0, mestoken, "=") == ("VN").lower() :
                    meskeyword = entry(0, mestoken, "=")
                    mesvalue = vehicle_number
                    mestoken = meskeyword + "=" + mesvalue
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
                    found_flag = True
                else:
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
            tmp_zwunsch = substring(tmp_zwunsch, 0, length(tmp_zwunsch) - 1)

            if not found_flag:
                tmp_zwunsch = tmp_zwunsch + "VN=" + vehicle_number + ";"
            res_line.zimmer_wunsch = tmp_zwunsch


            res_line.bemerk = res_line.bemerk + chr_unicode(10) + chr_unicode(13) + "Vehicle Number = " + vehicle_number

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if guest:
            guest.mobil_telefon = guest_phnumber
            guest.nation1 = guest_nation
            guest.land = guest_country
            guest.geburt_ort2 = guest_region

            if email != "":
                guest.email_adr = email

        if base64image != "":

            guestbook = get_cache (Guestbook, {"gastnr": [(eq, res_line.gastnrmember)]})

            if not guestbook:
                guestbook = Guestbook()
                db_session.add(guestbook)

                guestbook.gastnr = res_line.gastnrmember
                guestbook.zeit = get_current_time_in_seconds()
                guestbook.userinit = user_init
                guestbook.reserve_char[0] = to_string(get_current_time_in_seconds(), "99999") +\
                        to_string(get_year(get_current_date())) +\
                        to_string(get_month(get_current_date()) , "99") +\
                        to_string(get_day(get_current_date()) , "99")


                pointer = base64_decode(base64image)
                guestbook.imagefile = pointer
            pass
            pass

        if res_line.zinr != "":

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if zimmer.zistatus != 0:
                result_message = "6 - Room not ready yet!"
                pass

                return generate_output()
        else:
            result_message = "7 - Room not available yet!"

            return generate_output()
        pass
        pass

    if preauth_string == "":

        if self_ci:
            silenzio = True
        can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, err_number1, err_number2, err_number3, err_number4, fill_gcfemail, gast_gastnr, q_143, flag_report, warn_flag = get_output(res_checkin1bl(1, rsv_number, rsvline_number, silenzio))

        if msg_str != "":
            result_message = "99 - " + msg_str

            return generate_output()

        if err_number1 != 0 or err_number2 != 0 or err_number3 != 0 or err_number4 != 0:

            if err_number1 == 1:
                result_message = "1 - " + msg_str1

                return generate_output()

            if err_number2 == 1:
                result_message = "2 - " + msg_str2

                return generate_output()

            if err_number3 == 1:
                result_message = "3 - " + msg_str3

                return generate_output()

            if err_number4 == 1:
                result_message = "4 - " + msg_str4

                return generate_output()

        if err_number1 == 0 and err_number2 == 0 and err_number3 == 0 and err_number4 == 0:
            can_checkin = True

        if can_checkin:
            new_resstatus, checked_in, ask_deposit, keycard_flag, mcard_flag, msg_str = get_output(res_checkin2bl(1, rsv_number, rsvline_number, user_init, False))

            res_line = get_cache (Res_line, {"resnr": [(eq, rsv_number)],"reslinnr": [(eq, rsvline_number)]})

            res_sharer = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 11)],"zinr": [(eq, res_line.zinr)]})

            if not res_sharer:
                result_message = "00 - " + msg_str
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "MCI;"
                pass
                pass

                return generate_output()
            else:

                for rline in db_session.query(Rline).filter(
                         (Rline.resnr == res_line.resnr) & (Rline.resstatus == 11) & (Rline.active_flag == 0) & (Rline.zinr == res_line.zinr)).order_by(Rline._recid).all():

                    if pofstay != None:
                        rline.zimmer_wunsch = rline.zimmer_wunsch + "SEGM_PUR" + to_string(pofstay) + ";"

                    guest = get_cache (Guest, {"gastnr": [(eq, rline.gastnrmember)]})

                    if guest:
                        guest.mobil_telefon = guest_phnumber
                        guest.nation1 = guest_nation
                        guest.land = guest_country
                        guest.geburt_ort2 = guest_region

                        if email != "":
                            guest.email_adr = email
                    new_resstatus, checked_in, ask_deposit, keycard_flag, mcard_flag, msg_str = get_output(res_checkin2bl(1, rline.resnr, rline.reslinnr, user_init, False))
                    rline.zimmer_wunsch = rline.zimmer_wunsch + "MCI;"


                    result_message = "00 - " + msg_str
                    pass

    return generate_output()