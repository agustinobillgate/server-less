DEFINE INPUT PARAMETER base64image AS LONGCHAR.
DEFINE INPUT PARAMETER resno       AS INTEGER.
DEFINE OUTPUT PARAMETER mess-result AS CHAR.

DEFINE VARIABLE pointer AS MEMPTR NO-UNDO.
DEFINE VARIABLE imgpath AS CHAR INIT "/usr1/vhp/tmp/".

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

DEFINE VARIABLE hotelname      AS CHAR      NO-UNDO.
DEFINE VARIABLE hoteladdress   AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelcity      AS CHAR      NO-UNDO.
DEFINE VARIABLE hoteltelp      AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelemail     AS CHAR      NO-UNDO.

DEFINE VARIABLE hotelwebsite   AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelheaderimg AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelfooterimg AS CHAR      NO-UNDO.
DEFINE VARIABLE precheckinurl  AS CHAR      NO-UNDO.

DEFINE STREAM s1.
DEFINE STREAM s2.

FIND FIRST paramtext WHERE txtnr = 200 NO-LOCK. 
hotelname = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 201 NO-LOCK. 
hoteladdress = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 202 NO-LOCK. 
hoteladdress = hoteladdress + " " + paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 203 NO-LOCK. 
hotelcity = hoteladdress + " " + paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 204 NO-LOCK. 
hoteltelp = paramtext.ptexte. 
FIND FIRST paramtext WHERE txtnr = 206 NO-LOCK. 
hotelemail = paramtext.ptexte.

imgpath = imgpath + "QRCODE-" + STRING(resno) + ".jpg".
pointer = BASE64-DECODE(base64image).
COPY-LOB pointer TO FILE imgpath.
mess-result = "0 - upload data success.".

/*
RUN send-email.

OS-DELETE VALUE (imgpath).
*/

PROCEDURE send-email:
    name-from  = "Reservation@" + hotelname.
    subject    = "Reminder - Pre Check In Online for your stay at " + hotelname.
    .
    /*
    IF SEARCH("/usr1/vhp/tmp/send-email-precheckin.php") NE ? THEN
    OS-DELETE VALUE("/usr1/vhp/tmp/send-email-precheckin.php").
    
    outfile-tmp = "/usr1/vhp/tmp/pre-check-in-template.htm".
    outfile     = "/usr1/vhp/tmp/pre-check-in-email.htm".
    */
    IF SEARCH("C:\VHPSource\_works\CEKSOURCE\test170820\send-email-precheckin.php") NE ? THEN
    OS-DELETE VALUE("C:\VHPSource\_works\CEKSOURCE\test170820\send-email-precheckin.php").
    
    outfile-tmp = "C:\VHPSource\_works\CEKSOURCE\test170820\pre-check-in-template.htm".
    outfile     = "C:\VHPSource\_works\CEKSOURCE\test170820\pre-check-in-email.htm".

    OUTPUT STREAM s1 TO VALUE(outfile).
    INPUT STREAM s2 FROM VALUE(outfile-tmp).
    
    REPEAT:
        textbody = "".
        strlen   = "".
        IMPORT STREAM s2 UNFORMATTED textbody.
        /*===========HEADER&FOOTER==============*/
        /*
        IF textbody MATCHES ("*$URL-HOTELWEBSITE*") THEN 
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelwebsite + SUBSTRING(ENTRY(2, textbody, "$"),17). /*URL HOTEL WEBSITE*/
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$2URL-HOTELWEBSITE*") THEN 
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelwebsite + SUBSTRING(ENTRY(2, textbody, "$"),18). /*URL HOTEL WEBSITE*/
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$URL-HEADERIMAGE*") THEN 
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelheaderimg + "" + SUBSTRING(ENTRY(2, textbody, "$"),16).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$URL-FOOTERIMAGE*") THEN 
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelfooterimg + "" + SUBSTRING(ENTRY(2, textbody, "$"),16).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        /*===========BODY==============*/
        ELSE IF textbody MATCHES ("*$EN-GUESTNAME*") THEN 
        DO:
            textbody = ENTRY(1, textbody, "$") + guest-list.guestname + " " + SUBSTRING(ENTRY(2, textbody, "$"),13).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-HOTELNAME1*") THEN /*Another Keyword in template body*/
        DO:
            IF ENTRY(2, textbody, "$") MATCHES ("*EN-HOTELNAME1*") THEN
            textbody = ENTRY(1, textbody, "$") + hotelname + " " + SUBSTRING(ENTRY(2, textbody, "$"),14) + "$" + ENTRY(3, textbody, "$") + "$" + ENTRY(4, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*EN-ARRIVALDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(guest-list.ci-date) + " " + SUBSTRING(ENTRY(2, textbody, "$"),15) + "$" + ENTRY(3, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*EN-DEPARTDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(guest-list.ci-date) + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).

            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-RESNO*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + STRING(guest-list.resnr) + " " + SUBSTRING(ENTRY(2, textbody, "$"),9).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-URLPRECHECKIN*") THEN /*HOTEL PCI URL*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + precheckinurl + "?" + EN-hotelencrip + SUBSTRING(ENTRY(2, textbody, "$"),17).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-HOTELTELP*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hoteltelp + " " + SUBSTRING(ENTRY(2, textbody, "$"),13).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-HOTELEMAIL*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelemail + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-HOTELNAME2*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelname + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        /*OTHER LANGUAGE KEYWORD*/
        ELSE IF textbody MATCHES ("*$OTH-GUESTNAME*") THEN 
        DO:
            textbody = ENTRY(1, textbody, "$") + guest-list.guestname  + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-HOTELNAME1*") THEN /*Another Keyword in template body*/
        DO:
            IF ENTRY(2, textbody, "$") MATCHES ("*OTH-HOTELNAME1*") THEN
            textbody = ENTRY(1, textbody, "$") + hotelname + " " + SUBSTRING(ENTRY(2, textbody, "$"),15) + "$" + ENTRY(3, textbody, "$") + "$" + ENTRY(4, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*OTH-ARRIVALDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(guest-list.ci-date) + " " + SUBSTRING(ENTRY(2, textbody, "$"),16) + "$" + ENTRY(3, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*OTH-DEPARTDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(guest-list.ci-date) + " " + SUBSTRING(ENTRY(2, textbody, "$"),15).

            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-HOTELNAME1*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelname + " " + SUBSTRING(ENTRY(2, textbody, "$"),15).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-RESNO*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + STRING(guest-list.resnr) + " " + SUBSTRING(ENTRY(2, textbody, "$"),10).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-URLPRECHECKIN*") THEN /*Another Keyword in template body*/
        DO:
            DEF VAR otherURLCODE AS CHAR.
            otherURLCODE = ENTRY(2,textbody,"$").
            otherURLCODE = ENTRY(3,otherURLCODE,"-").
            
            OTH-hotelencrip = otherURLCODE + "|" + hotelcode + "|" + STRING(guest-list.ci-date) + "|" + STRING(guest-list.resnr).
            
            ASSIGN 
                cPersonalKey    = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
                rKey            = GENERATE-PBE-KEY(cPersonalKey)
                mMemptrOut      = ENCRYPT(OTH-hotelencrip,rKey)
                OTH-hotelencrip = BASE64-ENCODE(mMemptrOut). 

            textbody = ENTRY(1, textbody, "$") + precheckinurl + "?" + OTH-hotelencrip + SUBSTRING(ENTRY(2, textbody, "$"),22).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.

        ELSE IF textbody MATCHES ("*$OTH-HOTELTELP*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hoteltelp + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-HOTELEMAIL*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelemail + " " + SUBSTRING(ENTRY(2, textbody, "$"),15).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-HOTELNAME2*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + hotelname + " " + SUBSTRING(ENTRY(2, textbody, "$"),15).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE
        DO:
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.*/
    END.
    
    OUTPUT STREAM s1 CLOSE.
    INPUT STREAM s2 CLOSE.
    COPY-LOB FILE outfile TO body.
    /*
    php-script =
    "<?php"                                                           + CHR(10) +
    /*"require '/usr1/vhp/php-script/PHPMailer/PHPMailerAutoload.php';" + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/class.smtp.php';"        + CHR(10) +
    "require '/usr1/vhp/php-script/PHPMailer/class.phpmailer.php';"   + CHR(10) +*/
    "require 'C:\vhp11\vhplib\dotr\PHPMailer\PHPMailerAutoload.php';" + CHR(10) +
    "require 'C:\vhp11\vhplib\dotr\PHPMailer\class.smtp.php';"        + CHR(10) +
    "require 'C:\vhp11\vhplib\dotr\PHPMailer\class.phpmailer.php';"   + CHR(10) +
    "$mail = new PHPMailer;"                                          + CHR(10) +
    "$mail->isSMTP();"                                                + CHR(10) +
    "$mail->Host = '" + smtp + "';"                                   + CHR(10) +
    "$mail->SMTPAuth = true;"                                         + CHR(10) +
    "$mail->Username = '" + username + "';"                           + CHR(10) +
    "$mail->Password = '" + password + "';"                           + CHR(10) +
    "$mail->SMTPSecure = '" + security + "';"                         + CHR(10) +
    "$mail->Port = " + port + ";"                                     + CHR(10) +
    "$mail->setFrom('" + email-from + "', '" + name-from + "');"      + CHR(10) +
    "$mail->addAddress('" + guest-list.email + "');"                  + CHR(10) +
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
    . */
    COPY-LOB php-script TO FILE "C:\VHPSource\_works\CEKSOURCE\test170820\send-email-precheckin.php".
    OS-COMMAND VALUE("php C:\VHPSource\_works\CEKSOURCE\test170820\send-email-precheckin.php").
END.
