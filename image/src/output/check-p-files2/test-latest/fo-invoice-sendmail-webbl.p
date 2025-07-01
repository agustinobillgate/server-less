DEFINE INPUT PARAMETER send-current-bill    AS LOGICAL.
DEFINE INPUT PARAMETER bill-number          AS INT.
DEFINE INPUT PARAMETER guest-number         AS INT.
DEFINE INPUT PARAMETER rsv-number           AS INT.
DEFINE INPUT PARAMETER rsvline-number       AS INT.
DEFINE INPUT PARAMETER selected-bill-number AS INT.
DEFINE INPUT PARAMETER base64-bill          AS LONGCHAR.
DEFINE OUTPUT PARAMETER mess-str            AS CHAR.
DEFINE OUTPUT PARAMETER send-email          AS LOGICAL.

DEFINE VARIABLE serveraddress AS CHARACTER.
DEFINE VARIABLE portaddress   AS CHARACTER.
DEFINE VARIABLE username      AS CHARACTER.
DEFINE VARIABLE password      AS CHARACTER.
DEFINE VARIABLE filepath      AS CHARACTER.
DEFINE VARIABLE filepath1     AS CHARACTER.
DEFINE VARIABLE subject       AS CHARACTER. 
DEFINE VARIABLE fletter       AS CHARACTER.
DEFINE VARIABLE cc-email      AS CHARACTER.
DEFINE VARIABLE pointer       AS MEMPTR NO-UNDO.
DEFINE VARIABLE security      AS CHAR NO-UNDO.
DEFINE VARIABLE name-from     AS CHAR NO-UNDO.
DEFINE VARIABLE bill-location AS CHAR NO-UNDO.
DEFINE VARIABLE checkin-date  AS DATE FORMAT "99/99/9999".
DEFINE VARIABLE checkout-date AS DATE FORMAT "99/99/9999".
DEFINE VARIABLE guest-name    AS CHAR.
DEFINE VARIABLE hotel-name    AS CHAR.
DEFINE VARIABLE emailadr      AS CHAR.
DEFINE VARIABLE licenseNr     AS CHARACTER.

DEFINE STREAM sbody1.
DEFINE STREAM sbody2.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT licenseNr). 

FIND FIRST paramtext WHERE txtnr EQ 240 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE paramtext THEN RETURN. 
IF ptexte = "" THEN RETURN. 
IF AVAILABLE paramtext AND ptexte NE "" THEN 
RUN decode-string(ptexte, OUTPUT hotel-name).
name-from = hotel-name.

FIND FIRST htparam WHERE paramnr EQ 2404 NO-LOCK NO-ERROR.
IF AVAILABLE htparam THEN
DO:
    IF htparam.fchar NE "" AND htparam.fchar NE ? THEN
    DO:
        ASSIGN 
        serveraddress = ENTRY(1, htparam.fchar, ";")
        portaddress   = ENTRY(2, htparam.fchar, ";") 
        username      = ENTRY(3, htparam.fchar, ";")
        password      = ENTRY(4, htparam.fchar, ";") 
        security      = ENTRY(5, htparam.fchar, ";") 
        send-email    = YES. 
    END.
    ELSE 
    DO:
        send-email    = NO. 
        mess-str      = "Parameter 2404 Not Set, Send email not available!".
        RETURN.
    END.
END.

IF selected-bill-number EQ 0 THEN selected-bill-number = 1.
FIND FIRST res-line WHERE res-line.resnr EQ rsv-number AND res-line.reslinnr EQ rsvline-number NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrpay NO-LOCK NO-ERROR.
    IF guest.karteityp NE 0 THEN
    DO:
        send-email = NO. 
        mess-str   = "This Guest Not Eligible To Receive This Bill! Please Check Bill Receiver!".
        RETURN.    
    END.
    emailadr      = guest.email-adr.
    checkin-date  = res-line.ankunft.
    checkout-date = res-line.abreise.
    guest-name    = res-line.NAME.
END.
subject = "Invoice For Your Stay From " + STRING(checkin-date,"99/99/9999") + " To " + STRING(checkout-date,"99/99/9999") + " At " +  CAPS(hotel-name).

pointer = BASE64-DECODE(base64-bill).
COPY-LOB pointer TO FILE ("/usr1/vhp/tmp/" + licenseNr + "/Invoice-" + STRING(bill-number) + "-" + STRING(rsv-number) + "-" + STRING(selected-bill-number) + ".pdf").
bill-location = "/usr1/vhp/tmp/" + licenseNr + "/Invoice-" + STRING(bill-number) + "-" + STRING(rsv-number) + "-" + STRING(selected-bill-number) + ".pdf".

IF emailadr EQ "" THEN
DO:
    send-email = NO. 
    mess-str   = "This Guest Not Eligible To Receive This Bill! Guest Email Still Empty!".
    RETURN.
END.

RUN sendemail.
send-email = YES. 
mess-str   = "Process Done".

PROCEDURE sendemail :
    DEFINE VARIABLE msg-str      AS CHARACTER NO-UNDO.
    DEFINE VARIABLE gettextbody  AS CHARACTER NO-UNDO.
    DEFINE VARIABLE lengtext     AS CHARACTER NO-UNDO.
    DEFINE VARIABLE get-str      AS CHARACTER NO-UNDO.
    DEFINE VARIABLE emailexist   AS LOGICAL INIT NO.

    DEFINE VARIABLE body         AS LONGCHAR NO-UNDO.
    DEFINE VARIABLE php-script   AS LONGCHAR NO-UNDO.
    DEFINE VARIABLE php-path     AS CHAR NO-UNDO.

    IF emailadr EQ "" THEN
    DO:
        mess-str = "No Email Address For This Guest!". 
        RETURN.
    END.
    IF LENGTH(emailadr) LT 5 THEN
    DO:
        mess-str = "Incorrect Email Address : " + emailadr. 
        RETURN.
    END.

    /*
    IF SEARCH("/usr1/vhp/tmp/" + licenseNr + "/foinv-body-tmp.htm") EQ ? THEN
    DO:
        mess-str = "Template For Body Email Unavailable In Server". 
        RETURN.
    END.

    IF SEARCH("/usr1/vhp/php-script/PHPMailer") EQ ? THEN
    DO:
        mess-str = "PHPMailer Services Unavailable In Server". 
        RETURN.
    END.*/

    fletter  = "/usr1/vhp/tmp/" + licenseNr + "/foinv-body.htm".
    php-path = "/usr1/vhp/tmp/" + licenseNr + "/send-invoice-byemail.php".

    OUTPUT STREAM sbody1 TO VALUE(fletter).
    INPUT STREAM sbody2 FROM VALUE("/usr1/vhp/tmp/" + licenseNr + "/foinv-body-tmp.htm").
    
    REPEAT:
        gettextbody = "".
        lengtext    = "".
        IMPORT STREAM sbody2 UNFORMATTED gettextbody.
        
        IF gettextbody MATCHES ("*$name1*") THEN 
        DO:
            gettextbody = ENTRY(1, gettextbody, "$") + guest-name + ", <br><br>".
            lengtext    = STRING(LENGTH(gettextbody)).
            IF lengtext EQ "0" OR lengtext EQ "" THEN lengtext = "1".
            PUT STREAM sbody1 gettextbody FORMAT "x(" + lengtext + ")" SKIP.
        END.

        ELSE IF gettextbody MATCHES ("*$hotelname1*") THEN 
        DO:
            gettextbody = ENTRY(1, gettextbody, "$") + hotel-name + ". <br><br>".
            lengtext    = STRING(LENGTH(gettextbody)).
            IF lengtext EQ "0" OR lengtext EQ "" THEN lengtext = "1".
            PUT STREAM sbody1 gettextbody FORMAT "x(" + lengtext + ")" SKIP.
        END.

        ELSE IF gettextbody MATCHES ("*$hotelname2*") THEN 
        DO:
            gettextbody = hotel-name + ". <br><br><br>".
            lengtext    = STRING(LENGTH(gettextbody)).
            IF lengtext EQ "0" OR lengtext EQ "" THEN lengtext = "1".
            PUT STREAM sbody1 gettextbody FORMAT "x(" + lengtext + ")" SKIP.
        END.

        ELSE IF gettextbody MATCHES ("*$name2*") THEN 
        DO:
            gettextbody = ENTRY(1, gettextbody, "$") + guest-name + ", <br><br>".
            lengtext    = STRING(LENGTH(gettextbody)).
            IF lengtext EQ "0" OR lengtext EQ "" THEN lengtext = "1".
            PUT STREAM sbody1 gettextbody FORMAT "x(" + lengtext + ")" SKIP.
        END.

        ELSE IF gettextbody MATCHES ("*$hotelname3*") THEN 
        DO:
            gettextbody = ENTRY(1, gettextbody, "$") + hotel-name + ". <br><br>".
            lengtext    = STRING(LENGTH(gettextbody)).
            IF lengtext EQ "0" OR lengtext EQ "" THEN lengtext = "1".
            PUT STREAM sbody1 gettextbody FORMAT "x(" + lengtext + ")" SKIP.
        END.

        ELSE IF gettextbody MATCHES ("*$hotelname4*") THEN 
        DO:
            gettextbody = hotel-name + ". <br><br><br>".
            lengtext    = STRING(LENGTH(gettextbody)).
            IF lengtext EQ "0" OR lengtext EQ "" THEN lengtext = "1".
            PUT STREAM sbody1 gettextbody FORMAT "x(" + lengtext + ")" SKIP.
        END.

        ELSE
        DO:
            lengtext   = STRING(LENGTH(gettextbody)).
            IF lengtext EQ "0" OR lengtext EQ "" THEN lengtext = "1".
            PUT STREAM sbody1 gettextbody FORMAT "x(" + lengtext + ")" SKIP.
        END.
    END.
    OUTPUT STREAM sbody1 CLOSE.
    INPUT  STREAM sbody2 CLOSE.

    COPY-LOB FILE fletter TO body.

    php-script =
    "<?php"                                                           + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';"        + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';"   + CHR(10) +
    "$mail = new PHPMailer;"                                          + CHR(10) +
    "$mail->isSMTP();"                                                + CHR(10) +
    "$mail->Host = '" + serveraddress + "';"                          + CHR(10) +
    "$mail->SMTPAuth = true;"                                         + CHR(10) +
    "$mail->Username = '" + username + "';"                           + CHR(10) +
    "$mail->Password = '" + password + "';"                           + CHR(10) +
    "$mail->SMTPSecure = '" + security + "';"                         + CHR(10) +
    "$mail->Port = " + portaddress + ";"                              + CHR(10) +
    "$mail->setFrom('" + username + "', '" + name-from + "');"        + CHR(10) +
    "$mail->addAddress('" + emailadr + "');"                          + CHR(10) +
    "$mail->isHTML(true);"                                            + CHR(10) +
    "$mail->Subject = '" + subject + "';"                             + CHR(10) +
    "$mail->Body = '" + body + "';"                                   + CHR(10) +
    "$mail->addAttachment('" + bill-location + "');"                  + CHR(10) +
    "if(!$mail->send()) " + CHR(123)                                  + CHR(10) +
    "    echo 'Message could not be sent.';"                          + CHR(10) +
    "    echo 'Mailer Error: ' . $mail->ErrorInfo;"                   + CHR(10) +
    CHR(125) + " else " + CHR(123)                                    + CHR(10) +
    "    echo 'Message has been sent';"                               + CHR(10) +
    CHR(125)                                                          + CHR(10) + 
    "?>"                                                              + CHR(10) 
    .
    COPY-LOB php-script TO FILE php-path.
    OS-COMMAND VALUE("php " + php-path).

END PROCEDURE.

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
