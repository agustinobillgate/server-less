DEFINE TEMP-TABLE rsv-list  
    FIELD resnr             LIKE res-line.resnr  
    FIELD reslinnr          LIKE res-line.reslinnr 
    FIELD gastnr            LIKE guest.gastnr
    FIELD rsv-name          LIKE reservation.name  
    FIELD zinr              LIKE res-line.zinr   
    FIELD resline-name      LIKE res-line.name  
    FIELD ankunft           LIKE res-line.ankunft  
    FIELD abreise           LIKE res-line.abreise 
    FIELD email             LIKE guest.email-adr
    FIELD idcard-flag       AS LOGICAL
    FIELD SELECTED          AS LOGICAL
    FIELD status-msg        AS CHAR
    FIELD mci-flag          AS LOGICAL
    FIELD pci-flag          AS LOGICAL
    FIELD email-sent        AS LOGICAL
    .  


DEFINE INPUT PARAMETER TABLE FOR rsv-list.
DEFINE OUTPUT PARAMETER msg-str AS CHAR.

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

DEFINE VARIABLE cPersonalKey   AS CHARACTER NO-UNDO.
DEFINE VARIABLE rKey           AS RAW.
DEFINE VARIABLE mMemptrOut     AS MEMPTR.
                               
DEFINE VARIABLE interval-date   AS INT      NO-UNDO.
DEFINE VARIABLE arrival-date    AS DATE     NO-UNDO.
DEFINE VARIABLE ci-date         AS DATE     NO-UNDO.
DEFINE VARIABLE ci-date87       AS DATE     NO-UNDO.
DEFINE VARIABLE start-date      AS DATE     NO-UNDO.
DEFINE VARIABLE hotelcode       AS CHAR     NO-UNDO.
DEFINE VARIABLE md5htlcode      AS CHAR     NO-UNDO.
DEFINE VARIABLE EN-hotelencrip  AS CHAR     NO-UNDO.
DEFINE VARIABLE OTH-hotelencrip AS CHAR     NO-UNDO.

DEFINE VARIABLE created-date   AS DATE      NO-UNDO.
DEFINE VARIABLE yy             AS INTEGER   NO-UNDO.
DEFINE VARIABLE mm             AS INTEGER   NO-UNDO.
DEFINE VARIABLE dd             AS INTEGER   NO-UNDO.
DEFINE VARIABLE do-it          AS LOGICAL   NO-UNDO.

DEFINE VARIABLE hotelname      AS CHAR      NO-UNDO.
DEFINE VARIABLE hoteladdress   AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelcity      AS CHAR      NO-UNDO.
DEFINE VARIABLE hoteltelp      AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelemail     AS CHAR      NO-UNDO.

DEFINE VARIABLE hotelwebsite   AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelheaderimg AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelfooterimg AS CHAR      NO-UNDO.
DEFINE VARIABLE precheckinurl  AS CHAR      NO-UNDO.

DEFINE VARIABLE php-path AS CHAR NO-UNDO.
DEFINE VARIABLE temp-htm-path AS CHAR NO-UNDO.
DEFINE VARIABLE put-htm-path AS CHAR NO-UNDO.

DEFINE VARIABLE licenseNr AS CHARACTER.

DEFINE STREAM s1.
DEFINE STREAM s2.

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
    IF queasy.number2 EQ 29 THEN interval-date  = INT(queasy.char3).
    IF queasy.number2 EQ 30 THEN subject        = queasy.char3.
    IF queasy.number2 EQ 31 THEN hotelcode      = queasy.char3.
END.

IF smtp EQ "" THEN
DO:
    msg-str = "SMPT Server Not Configured Yet".
    RETURN.
END.
IF username EQ "" THEN
DO:
    msg-str = "Email Sender Not Configured Yet".
    RETURN.
END.
IF hotelcode EQ "" THEN
DO:
    msg-str = "HotelCode Not Configured Yet".
    RETURN.
END.

FIND FIRST paramtext WHERE txtnr = 243 NO-LOCK NO-ERROR. 
IF AVAILABLE paramtext AND paramtext.ptexte NE "" THEN RUN decode-string(ptexte, OUTPUT licenseNr). 

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK NO-ERROR.
ci-date87 = htparam.fdate.

/*==========================================================================================================*/
/*PROCEDURE SEND EMAIL*/
/*==========================================================================================================*/

FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 7 AND queasy.number2 EQ 2 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN hotelwebsite = queasy.char3.

FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 7 AND queasy.number2 EQ 3 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN hotelheaderimg = queasy.char3. 

FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 7 AND queasy.number2 EQ 4 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN hotelfooterimg = queasy.char3. 

FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 7 AND queasy.number2 EQ 5 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN precheckinurl = queasy.char3. 

php-path      = "/usr1/vhp/tmp/" + licenseNr + "/send-email-precheckin.php".
temp-htm-path = "/usr1/vhp/tmp/" + licenseNr + "/pre-check-in-template.htm".
put-htm-path  = "/usr1/vhp/tmp/" + licenseNr + "/pre-check-in-email.htm".

FOR EACH rsv-list WHERE rsv-list.SELECTED EQ YES:
    EN-hotelencrip  = CHR(34) + "ENG|" + hotelcode + "|" + STRING(rsv-list.ankunft) + "|" + STRING(rsv-list.resnr) + CHR(34).
    name-from       = hotelemail.

    /**/
    ASSIGN 
        cPersonalKey    = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
        rKey            = GENERATE-PBE-KEY(cPersonalKey)
        mMemptrOut      = ENCRYPT(EN-hotelencrip, rKey )
        EN-hotelencrip  = BASE64-ENCODE(MMEMPTROUT).    
    /**/
    /*RUN encryptedText (EN-hotelencrip,"E",OUTPUT EN-hotelencrip).*/
    IF EN-hotelencrip MATCHES "*$*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,"$","%24").
    IF EN-hotelencrip MATCHES "*&*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,"&","%26").
    IF EN-hotelencrip MATCHES "*+*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,"+","%2B").
    IF EN-hotelencrip MATCHES "*,*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,",","%2C").
    IF EN-hotelencrip MATCHES "*/*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,"/","%2F").
    IF EN-hotelencrip MATCHES "*:*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,":","%3A").
    IF EN-hotelencrip MATCHES "*;*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,";","%3B").
    IF EN-hotelencrip MATCHES "*=*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,"=","%3D").
    IF EN-hotelencrip MATCHES "*?*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,"?","%3F").
    IF EN-hotelencrip MATCHES "*@*" THEN EN-hotelencrip = REPLACE(EN-hotelencrip,"@","%40").

    OTH-hotelencrip = CHR(34) + "IDN|" + hotelcode + "|" + STRING(rsv-list.ankunft) + "|" + STRING(rsv-list.resnr) + CHR(34).
    /**/
    ASSIGN 
        cPersonalKey    = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
        rKey            = GENERATE-PBE-KEY(cPersonalKey)
        mMemptrOut      = ENCRYPT(OTH-hotelencrip,rKey)
        OTH-hotelencrip = BASE64-ENCODE(mMemptrOut). /**/

    /*RUN encryptedText (OTH-hotelencrip,"E",OUTPUT OTH-hotelencrip).*/
    IF OTH-hotelencrip MATCHES "*$*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,"$","%24").
    IF OTH-hotelencrip MATCHES "*&*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,"&","%26").
    IF OTH-hotelencrip MATCHES "*+*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,"+","%2B").
    IF OTH-hotelencrip MATCHES "*,*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,",","%2C").
    IF OTH-hotelencrip MATCHES "*/*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,"/","%2F").
    IF OTH-hotelencrip MATCHES "*:*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,":","%3A").
    IF OTH-hotelencrip MATCHES "*;*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,";","%3B").
    IF OTH-hotelencrip MATCHES "*=*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,"=","%3D").
    IF OTH-hotelencrip MATCHES "*?*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,"?","%3F").
    IF OTH-hotelencrip MATCHES "*@*" THEN OTH-hotelencrip = REPLACE(OTH-hotelencrip,"@","%40").
    
    IF SEARCH(php-path) NE ? THEN OS-DELETE VALUE(php-path).
    
    outfile-tmp = temp-htm-path.
    outfile     = put-htm-path.
        
    OUTPUT STREAM s1 TO VALUE(outfile).
    INPUT STREAM s2 FROM VALUE(outfile-tmp).
    
    REPEAT:
        textbody = "".
        strlen   = "".
        IMPORT STREAM s2 UNFORMATTED textbody.
        /*===========HEADER&FOOTER==============*/
        
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
        /*ELSE IF textbody MATCHES ("*$URL-HEADERIMAGE*") THEN 
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
        END.*/
        /*===========BODY==============*/
        ELSE IF textbody MATCHES ("*$EN-GUESTNAME*") THEN 
        DO:
            textbody = ENTRY(1, textbody, "$") + rsv-list.resline-name + " " + SUBSTRING(ENTRY(2, textbody, "$"),13).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-HOTELNAME1*") THEN /*Another Keyword in template body*/
        DO:
            IF ENTRY(2, textbody, "$") MATCHES ("*EN-HOTELNAME1*") THEN
            textbody = ENTRY(1, textbody, "$") + hotelname + " " + SUBSTRING(ENTRY(2, textbody, "$"),14) + "$" + ENTRY(3, textbody, "$") + "$" + ENTRY(4, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*EN-ARRIVALDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(rsv-list.ankunft, "99/99/9999") + " " + SUBSTRING(ENTRY(2, textbody, "$"),15) + "$" + ENTRY(3, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*EN-DEPARTDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(rsv-list.abreise, "99/99/9999") + " " + SUBSTRING(ENTRY(2, textbody, "$"),14).

            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-RESNO*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + STRING(rsv-list.resnr) + " " + SUBSTRING(ENTRY(2, textbody, "$"),9).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$EN-URLPRECHECKIN*") THEN /*HOTEL PCI URL*/ 
        DO:
            textbody = ENTRY(1, textbody, "$") + precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + EN-hotelencrip + SUBSTRING(ENTRY(2, textbody, "$"),17).
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
            textbody = ENTRY(1, textbody, "$") + rsv-list.resline-name  + SUBSTRING(ENTRY(2, textbody, "$"),14).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-HOTELNAME1*") THEN /*Another Keyword in template body*/
        DO:
            IF ENTRY(2, textbody, "$") MATCHES ("*OTH-HOTELNAME1*") THEN
            textbody = ENTRY(1, textbody, "$") + hotelname + " " + SUBSTRING(ENTRY(2, textbody, "$"),15) + "$" + ENTRY(3, textbody, "$") + "$" + ENTRY(4, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*OTH-ARRIVALDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(rsv-list.ankunft,"99/99/9999") + " " + SUBSTRING(ENTRY(2, textbody, "$"),16) + "$" + ENTRY(3, textbody, "$").
            IF ENTRY(2, textbody, "$") MATCHES ("*OTH-DEPARTDATE*") THEN
            textbody = ENTRY(1, textbody, "$") + STRING(rsv-list.abreise,"99/99/9999") + " " + SUBSTRING(ENTRY(2, textbody, "$"),15).

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
            textbody = ENTRY(1, textbody, "$") + STRING(rsv-list.resnr) + " " + SUBSTRING(ENTRY(2, textbody, "$"),10).
            strlen   = STRING(LENGTH(textbody)).
            IF strlen EQ "0" OR strlen EQ "" THEN strlen = "1".
            PUT STREAM s1 textbody FORMAT "x(" + strlen + ")" SKIP.
        END.
        ELSE IF textbody MATCHES ("*$OTH-URLPRECHECKIN*") THEN /*Another Keyword in template body*/
        DO:
            textbody = ENTRY(1, textbody, "$") + precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + OTH-hotelencrip + SUBSTRING(ENTRY(2, textbody, "$"),22).
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
    "$mail->setFrom('" + username + "', '" + name-from + "');"      + CHR(10) +
    "$mail->addAddress('" + rsv-list.email + "');"                    + CHR(10) +
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

    CREATE queasy.
    ASSIGN
        queasy.KEY = 898
        queasy.number1 = rsv-list.resnr
        queasy.number2 = rsv-list.reslinnr
        queasy.char1   = rsv-list.email
        queasy.date1   = TODAY.

    rsv-list.status-msg = "Email Sent to : " + queasy.char1 + " date : " + STRING(queasy.date1).
    /**/
    COPY-LOB php-script TO FILE php-path.
    OS-COMMAND VALUE("php " + php-path).

END.
msg-str = "Done".

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
/*
PROCEDURE encryptedText:
    DEFINE INPUT PARAMETER input-string AS CHAR.
    DEFINE INPUT PARAMETER task-mode    AS CHAR.
    DEFINE OUTPUT PARAMETER mess-result AS CHAR.
    
    DEFINE VARIABLE filebat AS CHAR.
    DEFINE VARIABLE filestr AS LONGCHAR.
    DEFINE VARIABLE foundit AS LOGICAL.
    DEFINE VARIABLE loopint AS INTEGER.
    
    filebat = "/usr1/vhp/etc/endecrypt.bat".
    
    IF task-mode EQ "E" THEN 
    DO:
        OUTPUT STREAM s1 TO VALUE(filebat).
        PUT STREAM s1 UNFORMATTED "python3 /usr1/vhp/etc/checkEncrypt.py E " + input-string. 
        OUTPUT STREAM s1 CLOSE.
    END.
    ELSE IF task-mode EQ "D" THEN 
    DO:
        OUTPUT STREAM s1 TO VALUE(filebat).
        PUT STREAM s1 UNFORMATTED "python3 /usr1/vhp/etc/checkEncrypt.py D " + input-string. 
        OUTPUT STREAM s1 CLOSE.
    END.
    
    OS-COMMAND SILENT VALUE("sudo bash " + filebat).
    foundit = NO.
    loopint = 5.
    REPEAT:
        IF SEARCH ("/usr1/vhp/etc/output.txt") NE ? THEN
        DO:
            foundit = YES.
            loopint = 99. 
        END.
        PAUSE 1.
        loopint = loopint + 1.
        IF loopint GT 5 THEN LEAVE.
    END.
    IF foundit THEN
    DO:
        COPY-LOB FILE "/usr1/vhp/etc/output.txt" TO filestr.
        mess-result = STRING(filestr).
    END.
    ELSE
    DO:
        mess-result = "process failed".
    END.
END.
*/
