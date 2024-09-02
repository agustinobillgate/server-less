from functions.additional_functions import *
import decimal
from datetime import date
from functions.selforder_prepare_sendbillbl import selforder_prepare_sendbillbl
import re
from sqlalchemy import func
from models import Paramtext, Queasy, Hoteldpt

def selforder_send_billbl(dept:int, session_parameter:str, guest_email:str, tableno:int):
    mess_result = ""
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
    outletname:str = ""
    totalamount:str = ""
    transidmerchant:str = ""
    datetimetrans:str = ""
    guest_name:str = ""
    pax:int = 0
    room:str = ""
    total_service:decimal = 0
    total_tax:decimal = 0
    total_price:decimal = 0
    total_payment:decimal = 0
    grandtotamount:decimal = 0
    paymoethod:str = ""
    paytipe:str = ""
    hotel_copybill:str = ""
    licensenr:str = ""
    php_path:str = ""
    temp_htm_path:str = ""
    put_htm_path:str = ""
    user_name:str = ""
    dept_name:str = ""
    sessionexpired:bool = False
    hold_payment:bool = False
    bill_number:int = 0
    payment_method:str = ""
    payment_status:str = ""
    payment_type:str = ""
    payment_date:date = None
    payment_time:str = ""
    trans_id_merchant:str = ""
    payment_channel:str = ""
    result_message:str = ""
    hotelwebsite:str = ""
    bgcolor_code:str = ""
    totaldiscount:decimal = 0
    subtotal:decimal = 0
    paytotal_amount:decimal = 0
    pay_amount:decimal = 0
    pay_descr:str = ""
    date_str:str = ""
    paramtext = queasy = hoteldpt = None

    ordered_item = None

    ordered_item_list, Ordered_item = create_model("Ordered_item", {"table_nr":int, "order_nr":int, "nr":int, "bezeich":str, "qty":int, "sp_req":str, "confirm":bool, "remarks":str, "order_date":str, "price":decimal, "subtotal":decimal, "subtotalprice":decimal, "artnr":int, "service":decimal, "tax":decimal, "bill_date":date, "order_status":str, "count_amount":bool, "posted":bool, "article_type":str, "pricetaxserv":decimal, "webpost_flag":bool, "hbline_recid":int, "hbline_time":int, "item_str":str, "bline_str":str, "cancel_str":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt


        nonlocal ordered_item
        nonlocal ordered_item_list
        return {"mess_result": mess_result}

    def decode_string(in_str:str):

        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt


        nonlocal ordered_item
        nonlocal ordered_item_list

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

    def selforder_cek_payment_gatewaybl():

        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt


        nonlocal ordered_item
        nonlocal ordered_item_list

        ptime:int = 0

        if dept == None:
            dept = 0

        if session_parameter == None:
            session_parameter = ""

        if session_parameter == "":
            result_message = "1_sessionParameter can't be Null"

            return

        if dept == 0:
            result_message = "2_outletNo can't be set to 0"

            return
        check_payment()

        if result_message.lower()  == "1_Data Not FOund":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 223) &  (Queasy.number1 == dept) &  (Queasy.betriebsnr == to_int(session_parameter))).first()

            if queasy:
                payment_status = queasy.char1

                if queasy.number3 == 1:
                    payment_type = "MIDTRANS"

                elif queasy.number3 == 2:
                    payment_type = "DOKU"

                elif queasy.number3 == 3:
                    payment_type = "QRIS"
                payment_date = queasy.date1
                ptime = to_int(queasy.deci1)
                payment_time = to_string(ptime, "HH:MM:SS")

                if num_entries(queasy.char2, "|") > 2:
                    payment_channel = entry(0, queasy.char2, "|")
                    trans_id_merchant = entry(2, queasy.char2, "|")
                    payment_type = entry(1, queasy.char2, "|")
                else:
                    trans_id_merchant = queasy.char2
                result_message = "0_Operation Success"
            else:
                result_message = "1_Data Not FOund"

    def check_payment():

        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt


        nonlocal ordered_item
        nonlocal ordered_item_list

        ptime:int = 0

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 223) &  (Queasy.number1 == dept) &  (func.lower(Queasy.char3) == (session_parameter).lower())).first()

        if queasy:
            payment_status = queasy.char1

            if queasy.number3 == 1:
                payment_type = "MIDTRANS"

            elif queasy.number3 == 2:
                payment_type = "DOKU"

            elif queasy.number3 == 3:
                payment_type = "QRIS"
            payment_date = queasy.date1
            ptime = to_int(queasy.deci1)
            payment_time = to_string(ptime, "HH:MM:SS")

            if num_entries(queasy.char2, "|") > 2:
                payment_channel = entry(0, queasy.char2, "|")
                trans_id_merchant = entry(2, queasy.char2, "|")
                payment_type = entry(1, queasy.char2, "|")
            else:
                trans_id_merchant = queasy.char2
            result_message = "0_Operation Success"
        else:
            result_message = "1_Data Not FOund"

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(ptexte)
    php_path = "/usr1/vhp/tmp/" + licensenr + "/send_email_selforder.php"
    temp_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhponlineorder_keyword.html"
    put_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhponlineorder.html"

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

        if queasy.number2 == 30:
            subject = queasy.char3

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 216) &  (Queasy.number1 == 7) &  (Queasy.number2 == 2)).first()

    if queasy:
        hotelwebsite = queasy.char3

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.number2 == 3) &  (Queasy.betriebsnr == dept)).first()

    if queasy:
        bgcolor_code = queasy.char2

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 222) &  (Queasy.number1 == 1) &  (Queasy.number2 == 20) &  (Queasy.betriebsnr == dept)).first()

    if queasy:
        hotel_copybill = queasy.char2

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()

    if hoteldpt:
        outletname = hoteldpt.depart
    name_from = outletname.upper() + "@" + hotelname.upper()
    mess_result, user_name, dept_name, guest_name, pax, room, total_tax, total_service, total_price, total_payment, grandtotamount, sessionexpired, hold_payment, bill_number, payment_method, ordered_item_list = get_output(selforder_prepare_sendbillbl("01", dept, tableno, session_parameter))
    mess_result = ""
    selforder_cek_payment_gatewaybl()
    result_message = ""

    if SEARCH (php_path) != None:
        OS_DELETE VALUE (php_path)
    outfile_tmp = temp_htm_path
    outfile = put_htm_path
    OUTPUT STREAM s1 TO VALUE (outfile)
    INPUT STREAM s2 FROM VALUE (outfile_tmp)
    subject = "E_Invoice " + dept_name + "@" + hotelname + "-" + trans_id_merchant + "-" + to_string(bill_number)
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
        textbody = "Rp " + to_string(- total_payment, ">>>,>>>,>>9.99")
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$hotelname.*",textbody):
        textbody = hotelname
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$outletname.*",textbody):
        textbody = dept_name
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$hoteladdress.*",textbody):
        textbody = entry(0, textbody, "$") + hoteladdress + " " + substring(entry(1, textbody, "$") , 12)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$hotelPhone.*",textbody):
        textbody = entry(0, textbody, "$") + hoteltelp + " " + substring(entry(1, textbody, "$") , 11)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$hotelemail.*",textbody):
        textbody = entry(0, textbody, "$") + hotelemail
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$hotelWeb.*",textbody):
        textbody = entry(0, textbody, "$") + hotelwebsite + " " + substring(entry(1, textbody, "$") , 8)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$transidmerchant.*",textbody):
        textbody = entry(0, textbody, "$") + trans_id_merchant + " " + substring(entry(1, textbody, "$") , 15)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$datetimetrans.*",textbody):

        if payment_date == None:
            date_str = ""
        else:
            date_str = to_string(payment_date)
        textbody = entry(0, textbody, "$") + date_str + " " + payment_time + " " + substring(entry(1, textbody, "$") , 13)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$guestName.*",textbody):
        textbody = entry(0, textbody, "$") + guest_name + " " + substring(entry(1, textbody, "$") , 9)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$guestEmail.*",textbody):
        textbody = entry(0, textbody, "$") + guest_email + " " + substring(entry(1, textbody, "$") , 10)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$tableNr.*",textbody):
        textbody = entry(0, textbody, "$") + to_string(tableno) + " " + substring(entry(1, textbody, "$") , 7)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$pax.*",textbody):
        textbody = entry(0, textbody, "$") + to_string(pax) + " " + substring(entry(1, textbody, "$") , 3)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*loopitem.*",textbody):

        for ordered_item in query(ordered_item_list, filters=(lambda ordered_item :ordered_item.article_type.lower()  == "SALES" and ordered_item.subtotal != 0)):
            subtotal = subtotal + ordered_item.subtotal
            textbody = '<tr class == "loopitem">' + chr(10) + '<td class == "td20">' + chr(10) + '<div class == "rowSpace">' + chr(10) + '<span>' + to_string(ordered_item.qty) + '</span>' + chr(10) + '<span>x</span>' + chr(10) + '</div>' + chr(10) + '</td>' + chr(10) + '<td class == "td40" style == "text_align: left">' + chr(10) + '<div class == "rowSpace">' + ordered_item.bezeich + '</div>' + chr(10) + '</td>' + chr(10) + '<td class == "td40" style == "text_align: right">' + chr(10) + '<div class == "rowSpace">' + to_string(ordered_item.subtotal, ">>,>>>,>>9.99") + '</div>' + chr(10) + '</td>' + chr(10) + '</tr>'
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

    elif re.match(".*\$discountTotal.*",textbody):

        for ordered_item in query(ordered_item_list, filters=(lambda ordered_item :re.match(".*discount.*",ordered_item.article_type))):
            totaldiscount = totaldiscount + ordered_item.subtotal
        textbody = entry(0, textbody, "$") + to_string(totaldiscount, "->>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 13)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"
        totaldiscount = 0

    elif re.match(".*\$subtotal.*",textbody):
        textbody = entry(0, textbody, "$") + to_string(subtotal - totaldiscount, ">>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 8)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*\$serviceCharge.*",textbody):

        if total_service != 0:
            textbody = entry(0, textbody, "$") + to_string(total_service, ">>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

    elif re.match(".*\$governmentTax.*",textbody):

        if total_tax != 0:
            textbody = entry(0, textbody, "$") + to_string(total_tax, ">>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

    elif re.match(".*\$grandTotalAmount.*",textbody):
        textbody = entry(0, textbody, "$") + to_string(- total_payment, ">>>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 16)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*paymentTotalAmount.*",textbody):
        textbody = entry(0, textbody, "$") + to_string(total_payment, "->>>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 18)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"

    elif re.match(".*looppayment.*",textbody):

        for ordered_item in query(ordered_item_list, filters=(lambda ordered_item :re.match(".*PAYMENT.*",ordered_item.article_type))):
            textbody = '<tr class == "looppayment">' + chr(10) + '<td class == "td20">' + chr(10) + '<div class == "rowSpace"></div>' + chr(10) + '</td>' + chr(10) + '<td class == "td40" style == "text_align: left">' + chr(10) + '<div class == "rowSpace">' + ordered_item.bezeich + '</div>' + chr(10) + '</td>' + chr(10) + '<td class == "td40" style == "text_align: right">' + chr(10) + '<div class == "rowSpace">' + to_string(ordered_item.subtotal, "->>>,>>>,>>9.99") + '</div>' + chr(10) + '</td>' + chr(10) + '</tr>'
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

        for ordered_item in query(ordered_item_list, filters=(lambda ordered_item :re.match(".*VOUCHER.*",ordered_item.article_type))):
            textbody = '<tr class == "looppayment">' + chr(10) + '<td class == "td20">' + chr(10) + '<div class == "rowSpace"></div>' + chr(10) + '</td>' + chr(10) + '<td class == "td40" style == "text_align: left">' + chr(10) + '<div class == "rowSpace">' + ordered_item.bezeich.upper() + '</div>' + chr(10) + '</td>' + chr(10) + '<td class == "td40" style == "text_align: right">' + chr(10) + '<div class == "rowSpace">' + to_string(ordered_item.subtotal, "->>>,>>>,>>9.99") + '</div>' + chr(10) + '</td>' + chr(10) + '</tr>'
            strlen = to_string(len(textbody))

            if strlen.lower()  == "0" or strlen.lower()  == "":
                strlen = "1"

    elif re.match(".*\$paymentAmount.*",textbody):
        textbody = entry(0, textbody, "$") + to_string(pay_amount) + " " + substring(entry(1, textbody, "$") , 13)
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"
    else:
        strlen = to_string(len(textbody))

        if strlen.lower()  == "0" or strlen.lower()  == "":
            strlen = "1"
    OUTPUT STREAM s1 CLOSE
    INPUT STREAM s2 CLOSE
    body = FILE outfile    php_script = "<?php" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/PHPMailerAutoload.php';" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/class.smtp.php';" + chr(10) + "require '/usr1/vhp/php_script/PHPMailer/class.phpmailer.php';" + chr(10) + "$mail  ==  new PHPMailer;" + chr(10) + "$mail->isSMTP();" + chr(10) + "$mail->Host  ==  '" + smtp + "';" + chr(10) + "$mail->SMTPAuth  ==  true;" + chr(10) + "$mail->username  ==  '" + username + "';" + chr(10) + "$mail->password  ==  '" + password + "';" + chr(10) + "$mail->SMTPSecure  ==  '" + security + "';" + chr(10) + "$mail->port  ==  " + port + ";" + chr(10) + "$mail->setFrom('" + username + "', '" + name_from + "');" + chr(10) + "$mail->addAddress('" + guest_email + "');" + chr(10) + "$mail->addCC('" + hotel_copybill + "');" + chr(10) + "$mail->isHTML(true);" + chr(10) + "$mail->subject  ==  '" + subject + "';" + chr(10) + "$mail->body  ==  '" + body + "';" + chr(10) + "if(!$mail->send()) " + chr(123) + chr(10) + "    echo 'Message could not be sent.';" + chr(10) + "    echo 'Mailer Error: ' . $mail->ErrorInfo;" + chr(10) + chr(125) + " else " + chr(123) + chr(10) + "    echo 'Message has been sent';" + chr(10) + chr(125) + chr(10) + "?>" + chr(10)
    COPY_LOB php_script TO FILE php_path
    OS_COMMAND VALUE ("php " + php_path)

    return generate_output()