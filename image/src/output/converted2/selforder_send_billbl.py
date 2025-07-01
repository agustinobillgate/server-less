#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.selforder_prepare_sendbillbl import selforder_prepare_sendbillbl
from models import Paramtext, Queasy, Hoteldpt

def selforder_send_billbl(dept:int, session_parameter:string, guest_email:string, tableno:int):

    prepare_cache ([Paramtext, Queasy, Hoteldpt])

    mess_result = ""
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
    outletname:string = ""
    totalamount:string = ""
    transidmerchant:string = ""
    datetimetrans:string = ""
    guest_name:string = ""
    pax:int = 0
    room:string = ""
    total_service:Decimal = to_decimal("0.0")
    total_tax:Decimal = to_decimal("0.0")
    total_price:Decimal = to_decimal("0.0")
    total_payment:Decimal = to_decimal("0.0")
    grandtotamount:Decimal = to_decimal("0.0")
    paymoethod:string = ""
    paytipe:string = ""
    hotel_copybill:string = ""
    licensenr:string = ""
    php_path:string = ""
    temp_htm_path:string = ""
    put_htm_path:string = ""
    user_name:string = ""
    dept_name:string = ""
    sessionexpired:bool = False
    hold_payment:bool = False
    bill_number:int = 0
    payment_method:string = ""
    payment_status:string = ""
    payment_type:string = ""
    payment_date:date = None
    payment_time:string = ""
    trans_id_merchant:string = ""
    payment_channel:string = ""
    result_message:string = ""
    hotelwebsite:string = ""
    bgcolor_code:string = ""
    totaldiscount:Decimal = to_decimal("0.0")
    subtotal:Decimal = to_decimal("0.0")
    paytotal_amount:Decimal = to_decimal("0.0")
    pay_amount:Decimal = to_decimal("0.0")
    pay_descr:string = ""
    date_str:string = ""
    paramtext = queasy = hoteldpt = None

    ordered_item = None

    ordered_item_list, Ordered_item = create_model("Ordered_item", {"table_nr":int, "order_nr":int, "nr":int, "bezeich":string, "qty":int, "sp_req":string, "confirm":bool, "remarks":string, "order_date":string, "price":Decimal, "subtotal":Decimal, "subtotalprice":Decimal, "artnr":int, "service":Decimal, "tax":Decimal, "bill_date":date, "order_status":string, "count_amount":bool, "posted":bool, "article_type":string, "pricetaxserv":Decimal, "webpost_flag":bool, "hbline_recid":int, "hbline_time":int, "item_str":string, "bline_str":string, "cancel_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt
        nonlocal dept, session_parameter, guest_email, tableno


        nonlocal ordered_item
        nonlocal ordered_item_list

        return {"mess_result": mess_result}

    def decode_string(in_str:string):

        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt
        nonlocal dept, session_parameter, guest_email, tableno


        nonlocal ordered_item
        nonlocal ordered_item_list

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


    def selforder_cek_payment_gatewaybl():

        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt
        nonlocal dept, session_parameter, guest_email, tableno


        nonlocal ordered_item
        nonlocal ordered_item_list

        ptime:int = 0

        if dept == None:
            dept = 0

        if session_parameter == None:
            session_parameter = ""

        if session_parameter == "":
            result_message = "1-sessionParameter can't be Null"

            return

        if dept == 0:
            result_message = "2-outletNo can't be set to 0"

            return
        check_payment()

        if result_message.lower()  == ("1-Data Not FOund").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, dept)],"betriebsnr": [(eq, to_int(session_parameter))]})

            if queasy:
                payment_status = queasy.char1

                if queasy.number3 == 1:
                    payment_type = "MIDtrans"

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
                result_message = "0-Operation Success"
            else:
                result_message = "1-Data Not FOund"


    def check_payment():

        nonlocal mess_result, php_script, smtp, username, password, security, port, email_from, name_from, email_to, subject, body, textbody, outfile, outfile_tmp, strlen, hotelname, hoteladdress, hotelcity, hoteltelp, hotelemail, outletname, totalamount, transidmerchant, datetimetrans, guest_name, pax, room, total_service, total_tax, total_price, total_payment, grandtotamount, paymoethod, paytipe, hotel_copybill, licensenr, php_path, temp_htm_path, put_htm_path, user_name, dept_name, sessionexpired, hold_payment, bill_number, payment_method, payment_status, payment_type, payment_date, payment_time, trans_id_merchant, payment_channel, result_message, hotelwebsite, bgcolor_code, totaldiscount, subtotal, paytotal_amount, pay_amount, pay_descr, date_str, paramtext, queasy, hoteldpt
        nonlocal dept, session_parameter, guest_email, tableno


        nonlocal ordered_item
        nonlocal ordered_item_list

        ptime:int = 0

        queasy = get_cache (Queasy, {"key": [(eq, 223)],"number1": [(eq, dept)],"char3": [(eq, session_parameter)]})

        if queasy:
            payment_status = queasy.char1

            if queasy.number3 == 1:
                payment_type = "MIDtrans"

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
            result_message = "0-Operation Success"
        else:
            result_message = "1-Data Not FOund"


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        licensenr = decode_string(paramtext.ptexte)
    php_path = "/usr1/vhp/tmp/" + licensenr + "/send-email-selforder.php"
    temp_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhponlineorder-keyword.html"
    put_htm_path = "/usr1/vhp/tmp/" + licensenr + "/vhponlineorder.html"

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

        if queasy.number2 == 30:
            subject = queasy.char3

    queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 7)],"number2": [(eq, 2)]})

    if queasy:
        hotelwebsite = queasy.char3

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"number2": [(eq, 3)],"betriebsnr": [(eq, dept)]})

    if queasy:
        bgcolor_code = queasy.char2

    queasy = get_cache (Queasy, {"key": [(eq, 222)],"number1": [(eq, 1)],"number2": [(eq, 20)],"betriebsnr": [(eq, dept)]})

    if queasy:
        hotel_copybill = queasy.char2

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})

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
    subject = "E-Invoice " + dept_name + "@" + hotelname + "-" + trans_id_merchant + "-" + to_string(bill_number)
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
            textbody = "Rp " + to_string(- total_payment, ">>>,>>>,>>9.99")
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$hotelname*"):
            textbody = hotelname
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$outletname*"):
            textbody = dept_name
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$hoteladdress*"):
            textbody = entry(0, textbody, "$") + hoteladdress + " " + substring(entry(1, textbody, "$") , 12)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$hotelPhone*"):
            textbody = entry(0, textbody, "$") + hoteltelp + " " + substring(entry(1, textbody, "$") , 11)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$hotelemail*"):
            textbody = entry(0, textbody, "$") + hotelemail
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$hotelWeb*"):
            textbody = entry(0, textbody, "$") + hotelwebsite + " " + substring(entry(1, textbody, "$") , 8)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$transidmerchant*"):
            textbody = entry(0, textbody, "$") + trans_id_merchant + " " + substring(entry(1, textbody, "$") , 15)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$datetimetrans*"):

            if payment_date == None:
                date_str = ""
            else:
                date_str = to_string(payment_date)
            textbody = entry(0, textbody, "$") + date_str + " " + payment_time + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$guestName*"):
            textbody = entry(0, textbody, "$") + guest_name + " " + substring(entry(1, textbody, "$") , 9)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$guestEmail*"):
            textbody = entry(0, textbody, "$") + guest_email + " " + substring(entry(1, textbody, "$") , 10)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$tableNr*"):
            textbody = entry(0, textbody, "$") + to_string(tableno) + " " + substring(entry(1, textbody, "$") , 7)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$pax*"):
            textbody = entry(0, textbody, "$") + to_string(pax) + " " + substring(entry(1, textbody, "$") , 3)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*loopitem*"):

            for ordered_item in query(ordered_item_list, filters=(lambda ordered_item: ordered_item.article_type.lower()  == ("SALES").lower()  and ordered_item.subtotal != 0)):
                subtotal =  to_decimal(subtotal) + to_decimal(ordered_item.subtotal)
                textbody = '<tr class="loopitem">' + chr_unicode(10) + '<td class="td20">' + chr_unicode(10) + '<div class="rowSpace">' + chr_unicode(10) + '<span>' + to_string(ordered_item.qty) + '</span>' + chr_unicode(10) + '<span>x</span>' + chr_unicode(10) + '</div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '<td class="td40" style="text-align: left">' + chr_unicode(10) + '<div class="rowSpace">' + ordered_item.bezeich + '</div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '<td class="td40" style="text-align: right">' + chr_unicode(10) + '<div class="rowSpace">' + to_string(ordered_item.subtotal, ">>,>>>,>>9.99") + '</div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '</tr>'
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

        elif matches(textbody,r"*$discountTotal*"):

            for ordered_item in query(ordered_item_list, filters=(lambda ordered_item: matches(ordered_item.article_type,r"*discount*"))):
                totaldiscount =  to_decimal(totaldiscount) + to_decimal(ordered_item.subtotal)
            textbody = entry(0, textbody, "$") + to_string(totaldiscount, "->>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 13)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"
            totaldiscount =  to_decimal("0")

        elif matches(textbody,r"*$subtotal*"):
            textbody = entry(0, textbody, "$") + to_string(subtotal - totaldiscount, ">>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 8)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*$serviceCharge*"):

            if total_service != 0:
                textbody = entry(0, textbody, "$") + to_string(total_service, ">>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

        elif matches(textbody,r"*$governmentTax*"):

            if total_tax != 0:
                textbody = entry(0, textbody, "$") + to_string(total_tax, ">>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 13)
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

        elif matches(textbody,r"*$grandTotalAmount*"):
            textbody = entry(0, textbody, "$") + to_string(- total_payment, ">>>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 16)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*paymentTotalAmount*"):
            textbody = entry(0, textbody, "$") + to_string(total_payment, "->>>,>>>,>>9.99") + " " + substring(entry(1, textbody, "$") , 18)
            strlen = to_string(length(textbody))

            if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                strlen = "1"

        elif matches(textbody,r"*looppayment*"):

            for ordered_item in query(ordered_item_list, filters=(lambda ordered_item: matches(ordered_item.article_type,r"*PAYMENT*"))):
                textbody = '<tr class="looppayment">' + chr_unicode(10) + '<td class="td20">' + chr_unicode(10) + '<div class="rowSpace"></div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '<td class="td40" style="text-align: left">' + chr_unicode(10) + '<div class="rowSpace">' + ordered_item.bezeich + '</div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '<td class="td40" style="text-align: right">' + chr_unicode(10) + '<div class="rowSpace">' + to_string(ordered_item.subtotal, "->>>,>>>,>>9.99") + '</div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '</tr>'
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

            for ordered_item in query(ordered_item_list, filters=(lambda ordered_item: matches(ordered_item.article_type,r"*VOUCHER*"))):
                textbody = '<tr class="looppayment">' + chr_unicode(10) + '<td class="td20">' + chr_unicode(10) + '<div class="rowSpace"></div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '<td class="td40" style="text-align: left">' + chr_unicode(10) + '<div class="rowSpace">' + ordered_item.bezeich.upper() + '</div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '<td class="td40" style="text-align: right">' + chr_unicode(10) + '<div class="rowSpace">' + to_string(ordered_item.subtotal, "->>>,>>>,>>9.99") + '</div>' + chr_unicode(10) + '</td>' + chr_unicode(10) + '</tr>'
                strlen = to_string(length(textbody))

                if strlen.lower()  == ("0").lower()  or strlen.lower()  == "":
                    strlen = "1"

        elif matches(textbody,r"*$paymentAmount*"):
            textbody = entry(0, textbody, "$") + to_string(pay_amount) + " " + substring(entry(1, textbody, "$") , 13)
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
    php_script = "<?php" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';" + chr_unicode(10) + "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';" + chr_unicode(10) + "$mail = new PHPMailer;" + chr_unicode(10) + "$mail->isSMTP();" + chr_unicode(10) + "$mail->Host = '" + smtp + "';" + chr_unicode(10) + "$mail->SMTPAuth = true;" + chr_unicode(10) + "$mail->username = '" + username + "';" + chr_unicode(10) + "$mail->password = '" + password + "';" + chr_unicode(10) + "$mail->SMTPSecure = '" + security + "';" + chr_unicode(10) + "$mail->port = " + port + ";" + chr_unicode(10) + "$mail->setFrom('" + username + "', '" + name_from + "');" + chr_unicode(10) + "$mail->addAddress('" + guest_email + "');" + chr_unicode(10) + "$mail->addCC('" + hotel_copybill + "');" + chr_unicode(10) + "$mail->isHTML(true);" + chr_unicode(10) + "$mail->subject = '" + subject + "';" + chr_unicode(10) + "$mail->body = '" + body + "';" + chr_unicode(10) + "if(!$mail->send()) " + chr_unicode(123) + chr_unicode(10) + " echo 'Message could not be sent.';" + chr_unicode(10) + " echo 'Mailer Error: ' . $mail->ErrorInfo;" + chr_unicode(10) + chr_unicode(125) + " else " + chr_unicode(123) + chr_unicode(10) + " echo 'Message has been sent';" + chr_unicode(10) + chr_unicode(125) + chr_unicode(10) + "?>" + chr_unicode(10)

    OS_COMMAND VALUE ("php " + php_path)

    return generate_output()