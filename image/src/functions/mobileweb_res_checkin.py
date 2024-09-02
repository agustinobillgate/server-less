from functions.additional_functions import *
import decimal
from datetime import date
from functions.res_checkin_deposit_paybl import res_checkin_deposit_paybl
from functions.res_checkin1bl import res_checkin1bl
from functions.res_checkin2bl import res_checkin2bl
import re
from models import Res_line, Guest, Queasy, Artikel, Waehrung, Guestbook, Zimmer, Paramtext

def mobileweb_res_checkin(rsv_number:int, rsvline_number:int, user_init:str, new_roomno:str, purposeofstay:str, email:str, guest_phnumber:str, guest_nation:str, guest_country:str, guest_region:str, vehicle_number:str, preauth_string:str, base64image:str):
    checked_in = False
    new_resstatus = 0
    result_message = ""
    self_ci:bool = True
    can_checkin:bool = False
    msg_str:str = ""
    msg_str1:str = ""
    msg_str2:str = ""
    msg_str3:str = ""
    msg_str4:str = ""
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
    tmp_zwunsch:str = ""
    bankname:str = ""
    noref:str = ""
    resultmsg:str = ""
    ccnumber:str = ""
    amount:str = ""
    transdat:str = ""
    transid_merchant:str = ""
    mestoken:str = ""
    meskeyword:str = ""
    mesvalue:str = ""
    loop_i:int = 0
    payment_string:str = ""
    payment_type:str = ""
    found_flag:bool = False
    do_it:bool = False
    do_payment:bool = False
    doku_paymentdatetime:str = ""
    doku_purchasecurrency:str = ""
    doku_liability:str = ""
    doku_paymentchannel:str = ""
    doku_amount:str = ""
    doku_paymentcode:str = ""
    doku_mcn:str = ""
    doku_words:str = ""
    doku_resultmsg:str = ""
    doku_verifyid:str = ""
    doku_transidmerchant:str = ""
    doku_bank:str = ""
    doku_statustype:str = ""
    doku_approvalcode:str = ""
    doku_edustatus:str = ""
    doku_threedsecurestatus:str = ""
    doku_verifyscore:str = ""
    doku_currency:str = ""
    doku_responsecode:str = ""
    doku_chname:str = ""
    doku_brand:str = ""
    doku_verifystatus:str = ""
    doku_sessionid:str = ""
    doku_paymenttype:str = ""
    qris_dpmallid:str = ""
    qris_transid:str = ""
    qris_amount:str = ""
    qris_resultmsg:str = ""
    qris_transdatetime:str = ""
    qris_clientid:str = ""
    qris_transidmerchant:str = ""
    qris_responsecode:str = ""
    vhp_artno:int = 0
    vhp_artdep:int = 0
    pg_artstring:str = ""
    pg_artname:str = ""
    pg_artno:int = 0
    bill_date:date = None
    voucher_str:str = ""
    inv_nr:int = 0
    deposit_art:int = 0
    errorflag:bool = False
    deposit_pay:decimal = 0
    deposit_exrate:decimal = 0
    mail_resno:int = 0
    mail_reslinno:int = 0
    mail_transidmerchant:str = ""
    mail_datetimetrans:str = ""
    mail_paymentdesc:str = ""
    mail_totalamount:str = ""
    post_amount:decimal = 0
    paymentcode:int = 0
    check_payment_exist:bool = False
    check_pay_str:str = ""
    res_line = guest = queasy = artikel = waehrung = guestbook = zimmer = paramtext = None

    rline = res_sharer = gbuff = receiver = mappingpg = wcisetup = None

    Rline = Res_line
    Res_sharer = Res_line
    Gbuff = Guest
    Receiver = Guest
    Mappingpg = Queasy
    Wcisetup = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal checked_in, new_resstatus, result_message, self_ci, can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, msg_answer, ask_deposit, keycard_flag, mcard_flag, err_number1, err_number2, err_number3, err_number4, q_143, fill_gcfemail, gast_gastnr, flag_report, warn_flag, silenzio, pofstay, pointer, tmp_zwunsch, bankname, noref, resultmsg, ccnumber, amount, transdat, transid_merchant, mestoken, meskeyword, mesvalue, loop_i, payment_string, payment_type, found_flag, do_it, do_payment, doku_paymentdatetime, doku_purchasecurrency, doku_liability, doku_paymentchannel, doku_amount, doku_paymentcode, doku_mcn, doku_words, doku_resultmsg, doku_verifyid, doku_transidmerchant, doku_bank, doku_statustype, doku_approvalcode, doku_edustatus, doku_threedsecurestatus, doku_verifyscore, doku_currency, doku_responsecode, doku_chname, doku_brand, doku_verifystatus, doku_sessionid, doku_paymenttype, qris_dpmallid, qris_transid, qris_amount, qris_resultmsg, qris_transdatetime, qris_clientid, qris_transidmerchant, qris_responsecode, vhp_artno, vhp_artdep, pg_artstring, pg_artname, pg_artno, bill_date, voucher_str, inv_nr, deposit_art, errorflag, deposit_pay, deposit_exrate, mail_resno, mail_reslinno, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount, post_amount, paymentcode, check_payment_exist, check_pay_str, res_line, guest, queasy, artikel, waehrung, guestbook, zimmer, paramtext
        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup


        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup
        return {"checked_in": checked_in, "new_resstatus": new_resstatus, "result_message": result_message}

    def sendmail(resno:int, reslinno:int, transidmerchant:str, datetimetrans:str, paymentdesc:str, totalamount:str):

        nonlocal checked_in, new_resstatus, result_message, self_ci, can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, msg_answer, ask_deposit, keycard_flag, mcard_flag, err_number1, err_number2, err_number3, err_number4, q_143, fill_gcfemail, gast_gastnr, flag_report, warn_flag, silenzio, pofstay, pointer, tmp_zwunsch, bankname, noref, resultmsg, ccnumber, amount, transdat, transid_merchant, mestoken, meskeyword, mesvalue, loop_i, payment_string, payment_type, found_flag, do_it, do_payment, doku_paymentdatetime, doku_purchasecurrency, doku_liability, doku_paymentchannel, doku_amount, doku_paymentcode, doku_mcn, doku_words, doku_resultmsg, doku_verifyid, doku_transidmerchant, doku_bank, doku_statustype, doku_approvalcode, doku_edustatus, doku_threedsecurestatus, doku_verifyscore, doku_currency, doku_responsecode, doku_chname, doku_brand, doku_verifystatus, doku_sessionid, doku_paymenttype, qris_dpmallid, qris_transid, qris_amount, qris_resultmsg, qris_transdatetime, qris_clientid, qris_transidmerchant, qris_responsecode, vhp_artno, vhp_artdep, pg_artstring, pg_artname, pg_artno, bill_date, voucher_str, inv_nr, deposit_art, errorflag, deposit_pay, deposit_exrate, mail_resno, mail_reslinno, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount, post_amount, paymentcode, check_payment_exist, check_pay_str, res_line, guest, queasy, artikel, waehrung, guestbook, zimmer, paramtext
        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup


        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup

        hotelname:str = ""
        hoteladdress:str = ""
        hotelphone:str = ""
        hotelmail:str = ""
        hotelweb:str = ""
        roomnumber:str = ""
        cidate:str = ""
        codate:str = ""
        guestname:str = ""
        pax:str = ""
        bgcolor_code:str = ""
        licensenr:str = ""
        php_path:str = ""
        temp_htm_path:str = ""
        put_htm_path:str = ""
        php_script:str = ""
        smtp:str = ""
        username:str = ""
        password:str = ""
        security:str = ""
        port:str = ""
        email_from:str = ""
        name_from:str = ""
        guestemail:str = ""
        subject:str = ""
        body:str = ""
        textbody:str = ""
        outfile:str = ""
        outfile_tmp:str = ""
        strlen:str = ""
        hotel_copybill:str = ""

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == 243)).first()

        if paramtext and paramtext.ptexte != "":
            licensenr = decode_string(ptexte)
        php_path = "/usr1/vhp/tmp/" + licensenr + "/send_email_selfcheckin.php"
        temp_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhpselfcheckin_keyword.html"
        put_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhpselfcheckin.html"

        for queasy in db_session.query(Queasy).filter(
                (Queasy.key == 216) &  (Queasy.number1 == 8)).all():

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

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 2)).first()

        if queasy:
            hotelweb = queasy.char3

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.number2 == 3) &  (Queasy.betriebsnr == 0)).first()

        if queasy:
            bgcolor_code = queasy.char2

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.number2 == 20) &  (Queasy.betriebsnr == 0)).first()

        if queasy:
            hotel_copybill = queasy.char2

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()
        guestemail = guest.email_adr
        roomnumber = res_line.zinr
        cidate = to_string(res_line.ankunft)
        codate = to_string(res_line.abreise)
        guestname = res_line.name
        pax = to_string(res_line.erwachs)
        name_from = "FrontOffice @" + hotelname.upper()
        subject = "E_Invoice Deposit Payment @" + hotelname + "-" + transidmerchant

        if SEARCH (php_path) != None:
            OS_DELETE VALUE (php_path)
        outfile_tmp = temp_htm_path
        outfile = put_htm_path
        OUTPUT STREAM s1 TO VALUE (outfile)
        INPUT STREAM s2 FROM VALUE (outfile_tmp)
        REPEAT:
        textbody = ""
        strlen = ""
        IMPORT STREAM s2 UNFORMATTED textbody

        if re.match(".*\$bgColor.*",textbody):
            textbody = entry(0, textbody, "$") + " " + bgcolor_code + ";"
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$totalamount.*",textbody):
            textbody = "Rp " + totalamount
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$hotelname.*",textbody):
            textbody = hotelname
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$hoteladdress.*",textbody):
            textbody = entry(0, textbody, "$") + hoteladdress + " " + substring(entry(1, textbody, "$") , 12)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*Phone.*",textbody):
            textbody = "Phone: " + hotelphone + " | email: " + hotelmail
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$hotelweb.*",textbody):
            textbody = entry(0, textbody, "$") + hotelweb + " " + substring(entry(1, textbody, "$") , 8)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$transidmerchant.*",textbody):
            textbody = entry(0, textbody, "$") + transidmerchant + " " + substring(entry(1, textbody, "$") , 15)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$datetimetrans.*",textbody):
            textbody = entry(0, textbody, "$") + datetimetrans + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$resno.*",textbody):
            textbody = entry(0, textbody, "$") + to_string(resno) + " " + substring(entry(1, textbody, "$") , 5)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$roomno.*",textbody):
            textbody = entry(0, textbody, "$") + roomnumber + " " + substring(entry(1, textbody, "$") , 6)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$cidate.*",textbody):
            textbody = entry(0, textbody, "$") + cidate + " " + substring(entry(1, textbody, "$") , 6)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$codate.*",textbody):
            textbody = entry(0, textbody, "$") + codate + " " + substring(entry(1, textbody, "$") , 6)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$guestname.*",textbody):
            textbody = entry(0, textbody, "$") + guestname + " " + substring(entry(1, textbody, "$") , 9)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$adult.*",textbody):
            textbody = entry(0, textbody, "$") + pax + " " + substring(entry(1, textbody, "$") , 5)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$depositAMount.*",textbody):
            textbody = entry(0, textbody, "$") + totalamount + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$grandTotalAmount.*",textbody):
            textbody = entry(0, textbody, "$") + totalamount + substring(entry(1, textbody, "$") , 16)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*paymentTotalAmount.*",textbody):
            textbody = entry(0, textbody, "$") + "-" + totalamount + substring(entry(1, textbody, "$") , 18)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$paymentDescription.*",textbody):
            textbody = entry(0, textbody, "$") + paymentdesc + " " + substring(entry(1, textbody, "$") , 18)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        elif re.match(".*\$paymentAmount.*",textbody):
            textbody = entry(0, textbody, "$") + "-" + totalamount + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"
        else:
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

    def decode_string(in_str:str):

        nonlocal checked_in, new_resstatus, result_message, self_ci, can_checkin, msg_str, msg_str1, msg_str2, msg_str3, msg_str4, msg_answer, ask_deposit, keycard_flag, mcard_flag, err_number1, err_number2, err_number3, err_number4, q_143, fill_gcfemail, gast_gastnr, flag_report, warn_flag, silenzio, pofstay, pointer, tmp_zwunsch, bankname, noref, resultmsg, ccnumber, amount, transdat, transid_merchant, mestoken, meskeyword, mesvalue, loop_i, payment_string, payment_type, found_flag, do_it, do_payment, doku_paymentdatetime, doku_purchasecurrency, doku_liability, doku_paymentchannel, doku_amount, doku_paymentcode, doku_mcn, doku_words, doku_resultmsg, doku_verifyid, doku_transidmerchant, doku_bank, doku_statustype, doku_approvalcode, doku_edustatus, doku_threedsecurestatus, doku_verifyscore, doku_currency, doku_responsecode, doku_chname, doku_brand, doku_verifystatus, doku_sessionid, doku_paymenttype, qris_dpmallid, qris_transid, qris_amount, qris_resultmsg, qris_transdatetime, qris_clientid, qris_transidmerchant, qris_responsecode, vhp_artno, vhp_artdep, pg_artstring, pg_artname, pg_artno, bill_date, voucher_str, inv_nr, deposit_art, errorflag, deposit_pay, deposit_exrate, mail_resno, mail_reslinno, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount, post_amount, paymentcode, check_payment_exist, check_pay_str, res_line, guest, queasy, artikel, waehrung, guestbook, zimmer, paramtext
        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup


        nonlocal rline, res_sharer, gbuff, receiver, mappingpg, wcisetup

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

    if preauth_string.lower()  != "" and preauth_string.lower()  != "CHECKROOMSTATUS":
        payment_string = preauth_string

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == rsv_number) &  (Res_line.reslinnr == rsvline_number)).first()

        if res_line:
            payment_type = entry(0, payment_string, ";")
            preauth_string = substring(payment_string, 5)

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 237) &  (Queasy.number1 == rsv_number) &  (Queasy.number2 == rsvline_number)).first()

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

            if payment_type.lower()  == "DOKU":
                paymentcode = 1
                for loop_i in range(1,num_entries(preauth_string, ";")  + 1) :
                    mestoken = entry(loop_i - 1, preauth_string, ";")
                    meskeyword = entry(0, mestoken, " == ")
                    mesvalue = entry(1, mestoken, " == ")

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

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 223) &  (Queasy.number1 == rsv_number) &  (Queasy.number2 == rsvline_number)).first()

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

            if doku_resultmsg.lower()  == "SUCCESS":
                do_payment = True

            if do_payment:
                mail_transidmerchant = doku_transidmerchant
                mail_datetimetrans = substring(doku_paymentdatetime, 6, 2) + "/" + substring(doku_paymentdatetime, 4, 2) + "/" + substring(doku_paymentdatetime, 0, 4) + " " + substring(doku_paymentdatetime, 8, 2) + ":" + substring(doku_paymentdatetime, 10, 2) + ":" + substring(doku_paymentdatetime, 12, 2)
                mail_paymentdesc = doku_bank.upper() + " " + doku_brand.upper()
                mail_totalamount = to_string(decimal.Decimal(doku_amount) , "->>>,>>>.99")
                post_amount = decimal.Decimal(doku_amount)

                for mappingpg in db_session.query(Mappingpg).filter(
                        (Mappingpg.key == 224) &  (Mappingpg.number1 == 1) &  (Mappingpg.number2 == 0) &  (Mappingpg.logi1)).all():
                    pg_artstring = doku_paymentchannel
                    pg_artname = entry(0, mappingpg.char1, "-")

                    if pg_artstring.lower()  == (pg_artname).lower() :
                        vhp_artno = to_int(entry(0, mappingpg.char3, "-"))
                        vhp_artdep = mappingpg.number2
                        break

                if vhp_artno == 0:
                    result_message = "9_No Mapping Found In VHP, Payment Not Posted"

                    return generate_output()

        elif payment_type.lower()  == "MIDTRANS":
            pass

        elif payment_type.lower()  == "QRIS":
            paymentcode = 3
            for loop_i in range(1,num_entries(preauth_string, ";")  + 1) :
                mestoken = entry(loop_i - 1, preauth_string, ";")
                meskeyword = entry(0, mestoken, " == ")
                mesvalue = entry(1, mestoken, " == ")

                if meskeyword == "DPMALLID":
                    qris_dpmallid = mesvalue
                elif meskeyword == "TRANSID":
                    qris_transid = mesvalue
                elif meskeyword == "amount":
                    qris_amount = mesvalue
                elif meskeyword == "resultmsg":
                    qris_resultmsg = mesvalue
                elif meskeyword == "TRANSDATETIME":
                    qris_transdatetime = mesvalue
                elif meskeyword == "CLIENTID":
                    qris_clientid = mesvalue
                elif meskeyword == "transidmerchant":
                    qris_transidmerchant = mesvalue
                elif meskeyword == "RESPONSECODE":
                    qris_responsecode = mesvalue

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == rsv_number) &  (Queasy.number2 == rsvline_number)).first()

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

        if qris_resultmsg.lower()  == "SUCCESS":
            do_payment = True

        if do_payment:
            mail_transidmerchant = qris_transidmerchant
            mail_datetimetrans = substring(qris_transdatetime, 6, 2) + "/" + substring(qris_transdatetime, 4, 2) + "/" + substring(qris_transdatetime, 0, 4) + " " + substring(qris_transdatetime, 8, 2) + ":" + substring(qris_transdatetime, 10, 2) + ":" + substring(qris_transdatetime, 12, 2)
            mail_paymentdesc = "QRIS"
            mail_totalamount = to_string(decimal.Decimal(qris_amount) , "->>>,>>>.99")
            post_amount = decimal.Decimal(qris_amount)

            for mappingpg in db_session.query(Mappingpg).filter(
                    (Mappingpg.key == 224) &  (Mappingpg.number1 == 1) &  (Mappingpg.number2 == 0) &  (Mappingpg.logi1)).all():
                pg_artstring = "1"
                pg_artname = entry(0, mappingpg.char1, "-")

                if pg_artstring.lower()  == (pg_artname).lower() :
                    vhp_artno = to_int(entry(0, mappingpg.char3, "-"))
                    vhp_artdep = mappingpg.number2
                    break

            if vhp_artno == 0:
                result_message = "9_No Mapping Found In VHP, Payment Not Posted"

                return generate_output()

    if do_payment:
        check_payment_exist = False

        if not check_payment_exist:

            wcisetup = db_session.query(Wcisetup).filter(
                    (Wcisetup.key == 216) &  (Wcisetup.number1 == 8) &  (Wcisetup.number2 == 34)).first()

            if wcisetup:
                deposit_art = to_int(wcisetup.char3)

            artikel = db_session.query(Artikel).filter(
                    (Artikel.artnr == deposit_art) &  (Artikel.departement == 0)).first()

            if artikel.pricetab:

                waehrung = db_session.query(Waehrung).filter(
                        (Waehrungsnr == artikel.betriebsnr)).first()

                if waehrung:
                    deposit_exrate = waehrung.ankauf / waehrung.einheit


            msg_str, errorflag, deposit_pay = get_output(res_checkin_deposit_paybl(deposit_art, rsv_number, vhp_artno, post_amount, - post_amount, 1, voucher_str, user_init))

            if not errorflag:
                sendmail(rsv_number, rsvline_number, mail_transidmerchant, mail_datetimetrans, mail_paymentdesc, mail_totalamount)
    result_message = "0 - Update PreAuth Success!"

    return generate_output()

    elif preauth_string.lower()  != "" and preauth_string.lower()  == "CHECKROOMSTATUS":
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
                (Queasy.key == 143) &  (Queasy.char3.op("~")(".*") + purposeofstay + "*")).first()

        if queasy:
            pofstay = queasy.number1

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == rsv_number) &  (Res_line.reslinnr == rsvline_number)).first()

    if res_line:

        if pofstay != None:
            for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                mestoken = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                if substring(mestoken, 0, 8) == "SEGM__PUR":
                    meskeyword = substring(mestoken, 0, 8)
                    mesvalue = to_string(pofstay)
                    mestoken = meskeyword + mesvalue
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
                    found_flag = True
                else:
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
            tmp_zwunsch = substring(tmp_zwunsch, 0, len(tmp_zwunsch) - 1)

            if not found_flag:
                tmp_zwunsch = tmp_zwunsch + "SEGM__PUR" + to_string(pofstay) + ";"
            res_line.zimmer_wunsch = tmp_zwunsch


        found_flag = False

        if vehicle_number != "":
            for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                mestoken = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

                if entry(0, mestoken, " == ") == "VN":
                    meskeyword = entry(0, mestoken, " == ")
                    mesvalue = vehicle_number
                    mestoken = meskeyword + " == " + mesvalue
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
                    found_flag = True
                else:
                    tmp_zwunsch = tmp_zwunsch + mestoken + ";"
            tmp_zwunsch = substring(tmp_zwunsch, 0, len(tmp_zwunsch) - 1)

            if not found_flag:
                tmp_zwunsch = tmp_zwunsch + "VN == " + vehicle_number + ";"
            res_line.zimmer_wunsch = tmp_zwunsch


            res_line.bemerk = res_line.bemerk + chr(10) + chr(13) + "Vehicle Number  ==  " + vehicle_number

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == res_line.gastnrmember)).first()

        if guest:
            guest.mobil_telefon = guest_phnumber
            guest.nation1 = guest_nation
            guest.land = guest_country
            guest.geburt_ort2 = guest_region

            if email != "":
                guest.email_adr = email

        if base64image != "":

            guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == res_line.gastnrmember)).first()

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
            guestbook = db_session.query(Guestbook).first()


        if res_line.zinr != "":

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if zimmer.zistatus != 0:
                result_message = "6 - Room not ready yet!"

                res_line = db_session.query(Res_line).first()

                return generate_output()
        else:
            result_message = "7 - Room not available yet!"

            return generate_output()

        res_line = db_session.query(Res_line).first()


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

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == rsv_number) &  (Res_line.reslinnr == rsvline_number)).first()

            res_sharer = db_session.query(Res_sharer).filter(
                    (Res_sharer.resnr == res_line.resnr) &  (Res_sharer.reslinnr != res_line.reslinnr) &  (Res_sharer.resstatus == 11) &  (Res_sharer.zinr == res_line.zinr)).first()

            if not res_sharer:
                result_message = "00 - " + msg_str
                res_line.zimmer_wunsch = res_line.zimmer_wunsch + "MCI;"

                res_line = db_session.query(Res_line).first()


                return generate_output()
            else:

                for rline in db_session.query(Rline).filter(
                        (Rline.resnr == res_line.resnr) &  (Rline.resstatus == 11) &  (Rline.active_flag == 0) &  (Rline.zinr == res_line.zinr)).all():

                    if pofstay != None:
                        rline.zimmer_wunsch = rline.zimmer_wunsch + "SEGM__PUR" + to_string(pofstay) + ";"

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == rline.gastnrmember)).first()

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

    OUTPUT STREAM s1 CLOSE
    INPUT STREAM s2 CLOSE
    body = FILE outfile    php_script = "<?php" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/PHPMailerAutoload.php';" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/class.smtp.php';" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/class.phpmailer.php';" + chr(10) + "$mail  ==  new PHPMailer;" + chr(10) + "$mail->isSMTP();" + chr(10) + "$mail->Host  ==  '" + smtp + "';" + chr(10) + "$mail->SMTPAuth  ==  true;" + chr(10) + "$mail->username  ==  '" + username + "';" + chr(10) + "$mail->password  ==  '" + password + "';" + chr(10) + "$mail->SMTPSecure  ==  '" + security + "';" + chr(10) + "$mail->port  ==  " + port + ";" + chr(10) + "$mail->setFrom('" + username + "', '" + name_from + "');" + chr(10) + "$mail->addAddress('" + guestemail + "');" + chr(10) + "$mail->addCC('" + hotel_copybill + "');" + chr(10) + "$mail->isHTML(true);" + chr(10) + "$mail->subject  ==  '" + subject + "';" + chr(10) + "$mail->body  ==  '" + body + "';" + chr(10) + "if(!$mail->send()) " + chr(123) + chr(10) + "    echo 'Message could not be sent.';" + chr(10) + "    echo 'Mailer Error: ' . $mail->ErrorInfo;" + chr(10) + chr(125) + " else " + chr(123) + chr(10) + "    echo 'Message has been sent';" + chr(10) + chr(125) + chr(10) + "?>" + chr(10)
    COPY_LOB php_script TO FILE php_path
    OS_COMMAND VALUE ("php " + php_path)

    return generate_output()