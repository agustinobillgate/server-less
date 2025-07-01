
DEFINE TEMP-TABLE ordered-item    
    FIELD table-nr      AS INTEGER  
    FIELD order-nr      AS INTEGER  
    FIELD nr            AS INTEGER FORMAT ">>>" LABEL "No"
    FIELD bezeich       AS CHARACTER FORMAT "x(35)"
    FIELD qty           AS INTEGER FORMAT "->>>" 
    FIELD sp-req        AS CHARACTER FORMAT "x(40)"
    FIELD confirm       AS LOGICAL
    FIELD remarks       AS CHAR FORMAT "x(20)" LABEL "Remarks"
    FIELD order-date    AS CHAR 
    FIELD price         AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD subtotal      AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD subtotalprice AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD artnr         AS INT
    FIELD service       AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD tax           AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD bill-date     AS DATE
    FIELD order-status  AS CHAR
    FIELD count-amount  AS LOGICAL
    FIELD posted        AS LOGICAL
    FIELD article-type  AS CHAR /*SALES,PAYMENT,DISCOUNT FOOD,BEV,OTHER,VOUCHER,VOID*/
    FIELD priceTaxServ  AS DECIMAL FORMAT "->>>,>>>,>>>,>>>"
    FIELD webpost-flag  AS LOGICAL
    FIELD hbline-recid  AS INT
    FIELD hbline-time   AS INT
    FIELD item-str      AS CHAR
    FIELD bline-str     AS CHAR
    FIELD cancel-str    AS CHARACTER
    .
    
/**/
DEFINE INPUT PARAMETER dept              AS INT.
DEFINE INPUT PARAMETER session-parameter AS CHAR.
DEFINE INPUT PARAMETER guest-email       AS CHAR NO-UNDO.
DEFINE INPUT PARAMETER tableNo           AS INT.

DEFINE OUTPUT PARAMETER mess-result AS CHAR.

/*
DEFINE VARIABLE dept              AS INT.
DEFINE VARIABLE session-parameter AS CHAR.
DEFINE VARIABLE guest-email       AS CHAR NO-UNDO.
DEFINE VARIABLE tableNo           AS INT.
DEFINE VARIABLE mess-result       AS CHAR.

dept              = 1.
session-parameter = "540".
guest-email       = "dodyoktavianto@sindata.net".
tableNo           = 50.
*/
/* 
MESSAGE "dept : "   + string(dept)              SKIP          
        "param: "   + string(session-parameter) SKIP 
        "email: "   + string(guest-email)       SKIP    
        "tableNo: " + string(tableNo)                    
    VIEW-AS ALERT-BOX INFO BUTTONS OK.
   */

DEFINE VARIABLE php-script     AS LONGCHAR NO-UNDO.
DEFINE VARIABLE smtp           AS CHAR     NO-UNDO.
DEFINE VARIABLE username       AS CHAR     NO-UNDO.
DEFINE VARIABLE password       AS CHAR     NO-UNDO.
DEFINE VARIABLE security       AS CHAR     NO-UNDO.
DEFINE VARIABLE port           AS CHAR     NO-UNDO.
DEFINE VARIABLE email-from     AS CHAR     NO-UNDO.
DEFINE VARIABLE name-from      AS CHAR     NO-UNDO.
DEFINE VARIABLE email-to       AS CHAR     NO-UNDO.
DEFINE VARIABLE subject        AS CHAR     NO-UNDO.
DEFINE VARIABLE body           AS LONGCHAR NO-UNDO.
DEFINE VARIABLE textbody       AS CHAR     NO-UNDO.
DEFINE VARIABLE outfile        AS CHAR     NO-UNDO.
DEFINE VARIABLE outfile-tmp    AS CHAR     NO-UNDO.
DEFINE VARIABLE strlen         AS CHAR.    
DEFINE VARIABLE hotelname      AS CHAR     NO-UNDO.
DEFINE VARIABLE hoteladdress   AS CHAR     NO-UNDO.
DEFINE VARIABLE hotelcity      AS CHAR     NO-UNDO.
DEFINE VARIABLE hoteltelp      AS CHAR     NO-UNDO.
DEFINE VARIABLE hotelemail     AS CHAR     NO-UNDO.
DEFINE VARIABLE outletname     AS CHAR     NO-UNDO.

DEFINE VARIABLE totalamount     AS CHAR    NO-UNDO.
DEFINE VARIABLE transidmerchant AS CHAR    NO-UNDO.
DEFINE VARIABLE datetimetrans   AS CHAR    NO-UNDO.
DEFINE VARIABLE guest-name      AS CHAR    NO-UNDO.
DEFINE VARIABLE pax             AS INT     NO-UNDO.
DEFINE VARIABLE room            AS CHAR    NO-UNDO.
DEFINE VARIABLE total-service   AS DECIMAL NO-UNDO.
DEFINE VARIABLE total-tax       AS DECIMAL NO-UNDO.
DEFINE VARIABLE total-price     AS DECIMAL NO-UNDO.
DEFINE VARIABLE total-payment   AS DECIMAL NO-UNDO.
DEFINE VARIABLE grandtotamount  AS DECIMAL NO-UNDO.
DEFINE VARIABLE paymoethod      AS CHAR    NO-UNDO.
DEFINE VARIABLE paytipe         AS CHAR    NO-UNDO.
DEFINE VARIABLE hotel-copybill  AS CHAR    NO-UNDO.

DEFINE VARIABLE licenseNr       AS CHARACTER.
DEFINE VARIABLE php-path        AS CHAR NO-UNDO.
DEFINE VARIABLE temp-htm-path   AS CHAR NO-UNDO.
DEFINE VARIABLE put-htm-path    AS CHAR NO-UNDO.

DEFINE VARIABLE user-name       AS CHAR NO-UNDO.
DEFINE VARIABLE dept-name       AS CHAR NO-UNDO.

DEFINE VARIABLE sessionExpired  AS LOGICAL.
DEFINE VARIABLE hold-payment    AS LOGICAL.
DEFINE VARIABLE bill-number     AS INT.
DEFINE VARIABLE payment-method  AS CHAR.

DEFINE VARIABLE payment-status    AS CHAR.
DEFINE VARIABLE payment-type      AS CHAR.
DEFINE VARIABLE payment-date      AS DATE.
DEFINE VARIABLE payment-time      AS CHAR.
DEFINE VARIABLE trans-id-merchant AS CHAR.
DEFINE VARIABLE payment-channel   AS CHAR.
DEFINE VARIABLE result-message    AS CHAR.

DEFINE VARIABLE hotelwebsite   AS CHAR NO-UNDO.

DEFINE VARIABLE bgcolor-code    AS CHAR.
DEFINE VARIABLE totaldiscount   AS DECIMAL NO-UNDO.
DEFINE VARIABLE subtotal        AS DECIMAL NO-UNDO.
DEFINE VARIABLE paytotal-amount AS DECIMAL NO-UNDO.
DEFINE VARIABLE pay-amount      AS DECIMAL NO-UNDO.
DEFINE VARIABLE pay-descr       AS CHAR NO-UNDO.

DEFINE STREAM s1.
DEFINE STREAM s2.


FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN RUN decode-string(ptexte, OUTPUT licenseNr). 
/**/
php-path      = "/usr1/vhp/tmp/" + licenseNr + "/send-email-selforder.php".
temp-htm-path = "/usr1/vhp/tmp/" + licenseNr + "/vhponlineorder-keyword.html".
put-htm-path  = "/usr1/vhp/tmp/" + licenseNr + "/vhponlineorder.html".

/*
php-path      = "C:\VHPSource\_works\!VHPSELFORDER\mail\send-email-selforder.php".
temp-htm-path = "C:\VHPSource\_works\!VHPSELFORDER\mail\vhponlineorder-keyword.html".
put-htm-path  = "C:\VHPSource\_works\!VHPSELFORDER\mail\vhponlineorder.html".
*/
FOR EACH queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 8 NO-LOCK:
    IF queasy.number2 EQ 19 THEN hotelname      = queasy.char3.
    IF queasy.number2 EQ 20 THEN hoteladdress   = queasy.char3.
    IF queasy.number2 EQ 21 THEN hotelcity      = queasy.char3.
    IF queasy.number2 EQ 22 THEN hoteltelp      = queasy.char3.
    IF queasy.number2 EQ 23 THEN hotelemail     = queasy.char3.
    IF queasy.number2 EQ 24 THEN smtp           = queasy.char3.
    IF queasy.number2 EQ 25 THEN port           = queasy.char3.
    IF queasy.number2 EQ 26 THEN username       = queasy.char3.
    IF queasy.number2 EQ 27 THEN password       = queasy.char3.
    IF queasy.number2 EQ 28 THEN security       = queasy.char3.
    IF queasy.number2 EQ 30 THEN subject        = queasy.char3.
END.
FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 7 AND queasy.number2 EQ 2 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN hotelwebsite = queasy.char3.
FIND FIRST queasy WHERE queasy.KEY EQ 222 
    AND queasy.number1 EQ 1 
    AND queasy.number2 EQ 3
    AND queasy.betriebsnr EQ dept NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN bgcolor-code = queasy.char2.

FIND FIRST queasy WHERE queasy.KEY EQ 222 
    AND queasy.number1 EQ 1 
    AND queasy.number2 EQ 20
    AND queasy.betriebsnr EQ dept NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN hotel-copybill = queasy.char2.

FIND FIRST hoteldpt WHERE hoteldpt.num EQ dept NO-LOCK NO-ERROR.
IF AVAILABLE hoteldpt THEN outletname = hoteldpt.depart.

name-from = CAPS(outletname) + "@" + CAPS(hotelname). 

RUN selforder-prepare-sendbillbl.p ("01",dept,tableNo,session-parameter, 
                                    OUTPUT mess-result,OUTPUT user-name,OUTPUT dept-name,OUTPUT guest-name,
                                    OUTPUT pax,OUTPUT room,OUTPUT total-tax,OUTPUT total-service,
                                    OUTPUT total-price,OUTPUT total-payment,OUTPUT grandtotamount,
                                    OUTPUT sessionExpired,OUTPUT hold-payment,OUTPUT bill-number,
                                    OUTPUT payment-method, 
                                    OUTPUT TABLE ordered-item).
mess-result = "".
RUN selforder-cek-payment-gatewaybl.
result-message = "".

IF SEARCH(php-path) NE ? THEN OS-DELETE VALUE(php-path).
outfile-tmp = temp-htm-path.
outfile     = put-htm-path.

OUTPUT STREAM s1 TO VALUE(outfile).
INPUT STREAM s2 FROM VALUE(outfile-tmp).

subject = "E-Invoice " + dept-name + "@" + hotelname + "-" + trans-id-merchant + "-" + STRING(bill-number).

REPEAT:
    textbody = "".
    strlen   = "".
    IMPORT STREAM s2 UNFORMATTED textbody.
    /*===========HEADER==============*/
    
    IF textbody MATCHES ("*$bgColor*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + " " + bgcolor-code + ";".
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$totalAmount*") THEN 
    DO:
        textbody = "Rp " + STRING(- total-payment,">>>,>>>,>>9.99"). 
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$hotelName*") THEN 
    DO:
        textbody = hotelname.
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$OUTLETNAME*") THEN 
    DO:
        textbody = dept-name.
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$hotelAddress*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + hoteladdress + " " + SUBSTRING(ENTRY(2, textbody, "$"),13).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$hotelPhone*") THEN
    DO:
        textbody = ENTRY(1, textbody, "$") + hoteltelp + " " + SUBSTRING(ENTRY(2, textbody, "$"),12).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$hotelEmail*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + hotelemail.
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$hotelWeb*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + hotelwebsite + " " + SUBSTRING(ENTRY(2, textbody, "$"),9).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$transIdMerchant*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + trans-id-merchant + " " + SUBSTRING(ENTRY(2, textbody, "$"),16).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$dateTimeTrans*") THEN 
    DO:
        DEF VAR date-str AS CHAR.
        IF payment-date EQ ? THEN date-str = "".
        ELSE date-str = STRING(payment-date).

        textbody = ENTRY(1, textbody, "$") + date-str + " " + payment-time + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$guestName*") THEN
    DO:
        textbody = ENTRY(1, textbody, "$") + guest-name + " " + SUBSTRING(ENTRY(2, textbody, "$"),10).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$guestEmail*") THEN
    DO:
        textbody = ENTRY(1, textbody, "$") + guest-email + " " + SUBSTRING(ENTRY(2, textbody, "$"),11).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$tableNr*") THEN
    DO:
        textbody = ENTRY(1, textbody, "$") + STRING(tableno) + " " + SUBSTRING(ENTRY(2, textbody, "$"),8).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE IF textbody MATCHES ("*$pax*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + STRING(pax) + " " + SUBSTRING(ENTRY(2, textbody, "$"),4).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    /*LOOP HERE FOR ITEM*/
    ELSE IF textbody MATCHES ("*loopitem*") THEN 
    DO:
        FOR EACH ordered-item WHERE ordered-item.article-type EQ "SALES" AND ordered-item.subtotal NE 0 :
            subtotal = subtotal + ordered-item.subtotal.
            textbody =  '<tr class="loopitem">' + CHR(10) +
                            '<td class="td20">' + CHR(10) +
                                '<div class="rowSpace">' + CHR(10) +
                                    '<span>' + STRING(ordered-item.qty) + '</span>' + CHR(10) +
                                    '<span>x</span>' + CHR(10) +
                                '</div>' + CHR(10) +
                            '</td>' + CHR(10) +
                            '<td class="td40" style="text-align: left">' + CHR(10) +
                                '<div class="rowSpace">' + ordered-item.bezeich + '</div>' + CHR(10) +
                            '</td>' + CHR(10) +
                            '<td class="td40" style="text-align: right">' + CHR(10) +
                                '<div class="rowSpace">' + STRING(ordered-item.subtotal,">>,>>>,>>9.99") + '</div>' + CHR(10) +
                            '</td>' + CHR(10) +
                        '</tr>'. 

            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
    END.
    /**/
    ELSE IF textbody MATCHES ("*$discountTotal*") THEN
    DO:
        FOR EACH ordered-item WHERE ordered-item.article-type MATCHES "*discount*":
            totaldiscount = totaldiscount + ordered-item.subtotal.
        END.
        textbody = ENTRY(1, textbody, "$") + STRING(totaldiscount,"->>,>>>,>>9.99") + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        totaldiscount = 0.
    END. 
    ELSE IF textbody MATCHES ("*$subTotal*") THEN
    DO:
        textbody = ENTRY(1, textbody, "$") + STRING(subtotal - totaldiscount,">>,>>>,>>9.99") + " " + SUBSTRING(ENTRY(2, textbody, "$"),9).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END. 
    ELSE IF textbody MATCHES ("*$serviceCharge*") THEN
    DO:
        IF total-service NE 0 THEN
        DO:
            textbody = ENTRY(1, textbody, "$") + STRING(total-service,">>,>>>,>>9.99") + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.        
    END.
    ELSE IF textbody MATCHES ("*$governmentTax*") THEN 
    DO:
        IF total-tax NE 0 THEN
        DO:
            textbody = ENTRY(1, textbody, "$") + STRING(total-tax,">>,>>>,>>9.99") + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.        
    END.
    ELSE IF textbody MATCHES ("*$grandTotalAmount*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + STRING(- total-payment,">>>,>>>,>>9.99") + " " + SUBSTRING(ENTRY(2, textbody, "$"),17).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END. 
    ELSE IF textbody MATCHES ("*paymentTotalAmount*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + STRING(total-payment,"->>>,>>>,>>9.99") + " " + SUBSTRING(ENTRY(2, textbody, "$"),19).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END. 

    /*LOOP HERE FOR PAYMENT*/
    ELSE IF textbody MATCHES ("*looppayment*") THEN 
    DO:
        FOR EACH ordered-item WHERE ordered-item.article-type MATCHES "*PAYMENT*":
            textbody = '<tr class="looppayment">' + CHR(10) +
                          '<td class="td20">' + CHR(10) +
                            '<div class="rowSpace"></div>' + CHR(10) +
                          '</td>' + CHR(10) +
                          '<td class="td40" style="text-align: left">' + CHR(10) +
                            '<div class="rowSpace">' + ordered-item.bezeich + '</div>' + CHR(10) +
                          '</td>' + CHR(10) +
                          '<td class="td40" style="text-align: right">' + CHR(10) +
                            '<div class="rowSpace">' + STRING(ordered-item.subtotal,"->>>,>>>,>>9.99") + '</div>' + CHR(10) +
                          '</td>' + CHR(10) +
                       '</tr>'.
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP. 
        END.
        FOR EACH ordered-item WHERE ordered-item.article-type MATCHES "*VOUCHER*":
            textbody = '<tr class="looppayment">' + CHR(10) +
                          '<td class="td20">' + CHR(10) +
                            '<div class="rowSpace"></div>' + CHR(10) +
                          '</td>' + CHR(10) +
                          '<td class="td40" style="text-align: left">' + CHR(10) +
                            '<div class="rowSpace">' + CAPS(ordered-item.bezeich) + '</div>' + CHR(10) +
                          '</td>' + CHR(10) +
                          '<td class="td40" style="text-align: right">' + CHR(10) +
                            '<div class="rowSpace">' + STRING(ordered-item.subtotal,"->>>,>>>,>>9.99") + '</div>' + CHR(10) +
                          '</td>' + CHR(10) +
                       '</tr>'.
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP. 
        END.
    END.
    ELSE IF textbody MATCHES ("*$paymentAmount*") THEN 
    DO:
        textbody = ENTRY(1, textbody, "$") + STRING(pay-amount)  + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
    ELSE
    DO:
        strlen   = STRING(LENGTH(textbody)).
        IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
        PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
    END.
END.

OUTPUT STREAM s1 CLOSE.
INPUT STREAM s2 CLOSE.
COPY-LOB FILE outfile TO body.

php-script =
    "<?php"                                                           + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';"        + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';"   + CHR(10) +
    "$mail = new PHPMailer;"                                          + CHR(10) +
    "$mail->isSMTP();"                                                + CHR(10) +
    "$mail->Host = '" + smtp + "';"                                   + CHR(10) +
    "$mail->SMTPAuth = true;"                                         + CHR(10) +
    "$mail->Username = '" + username + "';"                           + CHR(10) +
    "$mail->Password = '" + password + "';"                           + CHR(10) +
    "$mail->SMTPSecure = '" + security + "';"                         + CHR(10) +
    "$mail->Port = " + port + ";"                                     + CHR(10) +
    "$mail->setFrom('" + username + "', '" + name-from + "');"        + CHR(10) +
    "$mail->addAddress('" + guest-email + "');"                       + CHR(10) +
    "$mail->addCC('" + hotel-copybill + "');"                         + CHR(10) +
    "$mail->isHTML(true);"                                            + CHR(10) +
    "$mail->Subject = '" + subject + "';"                             + CHR(10) +
    "$mail->Body = '" + body + "';"                                   + CHR(10) +
    "if(!$mail->send()) " + CHR(123)                                  + CHR(10) +
    "    echo 'Message could not be sent.';"                          + CHR(10) +
    "    echo 'Mailer Error: ' . $mail->ErrorInfo;"                   + CHR(10) +
    CHR(125) + " else " + CHR(123)                                    + CHR(10) +
    "    echo 'Message has been sent';"                               + CHR(10) +
    CHR(125)                                                          + CHR(10) + 
    "?>"                                                              + CHR(10) 
    .

/**/

COPY-LOB php-script TO FILE php-path.
OS-COMMAND VALUE("php " + php-path). 

PROCEDURE decode-string: 
    DEFINE INPUT PARAMETER in-str   AS CHAR. 
    DEFINE OUTPUT PARAMETER out-str AS CHAR INITIAL "". 
    DEFINE VARIABLE s   AS CHAR. 
    DEFINE VARIABLE j   AS INTEGER. 
    DEFINE VARIABLE len AS INTEGER. 
      s = in-str. 
      j = ASC(SUBSTR(s, 1, 1)) - 70. 
      len = LENGTH(in-str) - 1. 
      s = SUBSTR(in-str, 2, len). 
      DO len = 1 TO LENGTH(s): 
        out-str = out-str + chr(asc(SUBSTR(s,len,1)) - j). 
      END. 
END.

PROCEDURE selforder-cek-payment-gatewaybl:
    DEF VAR ptime AS INT.

    IF dept EQ ? THEN dept = 0.
    IF session-parameter EQ ? THEN session-parameter = "".
    
    IF session-parameter EQ "" THEN
    DO:
        result-message = "1-sessionParameter can't be Null".
        RETURN.
    END.
    IF dept EQ 0 THEN
    DO:
        result-message = "2-outletNo can't be set to 0".
        RETURN.
    END.
    
    RUN check-payment.
    IF result-message EQ "1-Data Not FOund" THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY EQ 223 
            AND queasy.number1 EQ dept 
            AND queasy.betriebsnr EQ INT(session-parameter) NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN
        DO:
            payment-status = queasy.char1.
            IF queasy.number3 EQ 1 THEN payment-type = "MIDTRANS".
            ELSE IF queasy.number3 EQ 2 THEN payment-type = "DOKU".
            ELSE IF queasy.number3 EQ 3 THEN payment-type = "QRIS".
    
            payment-date = queasy.date1.
            ptime = INT(queasy.deci1).
            payment-time = STRING(ptime,"HH:MM:SS").
    
            IF NUM-ENTRIES(queasy.char2,"|") GT 2 THEN
            DO:
                payment-channel   = ENTRY(1,queasy.char2,"|").
                trans-id-merchant = ENTRY(3,queasy.char2,"|").
                payment-type      = ENTRY(2,queasy.char2,"|").
            END.
            ELSE trans-id-merchant = queasy.char2.
    
            result-message = "0-Operation Success".
        END.
        ELSE
        DO:
            result-message = "1-Data Not FOund".
        END.
    END.
END.

PROCEDURE check-payment:
    DEF VAR ptime AS INT.
    FIND FIRST queasy WHERE queasy.KEY EQ 223 
        AND queasy.number1 EQ dept 
        AND queasy.char3 EQ session-parameter NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        payment-status = queasy.char1.
        IF queasy.number3 EQ 1 THEN payment-type = "MIDTRANS".
        ELSE IF queasy.number3 EQ 2 THEN payment-type = "DOKU".
        ELSE IF queasy.number3 EQ 3 THEN payment-type = "QRIS".

        payment-date = queasy.date1.
        ptime = INT(queasy.deci1).
        payment-time = STRING(ptime,"HH:MM:SS").

        IF NUM-ENTRIES(queasy.char2,"|") GT 2 THEN
        DO:
            payment-channel   = ENTRY(1,queasy.char2,"|").
            trans-id-merchant = ENTRY(3,queasy.char2,"|").
            payment-type      = ENTRY(2,queasy.char2,"|").
        END.
        ELSE trans-id-merchant = queasy.char2.

        result-message = "0-Operation Success".
    END.
    ELSE
    DO:
        result-message = "1-Data Not FOund".
    END.
END.
