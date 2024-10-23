DEFINE TEMP-TABLE arrive-list
    FIELD resnr         AS INTEGER
    FIELD reslinnr      AS INTEGER
    FIELD rsv-name      AS CHARACTER
    FIELD zinr          AS CHARACTER
    FIELD guest-name    AS CHARACTER
    FIELD guest-email   AS CHARACTER
    FIELD phone-no      AS CHARACTER
    FIELD arrival       AS DATE
    FIELD departure     AS DATE
    FIELD hotelcode     AS CHARACTER
    FIELD mail-eng      AS CHARACTER
    FIELD mail-oth      AS CHARACTER
    FIELD hotel-name    AS CHARACTER
    FIELD hotel-telp    AS CHARACTER
    FIELD hotel-mail    AS CHARACTER
    FIELD link-pci-eng  AS CHARACTER
    FIELD link-pci-oth  AS CHARACTER
.

DEFINE INPUT PARAMETER resno AS INTEGER.
DEFINE INPUT PARAMETER reslinno AS INTEGER.
DEFINE OUTPUT PARAMETER TABLE FOR arrive-list.

DEFINE VARIABLE EN-hotelencrip  AS CHAR      NO-UNDO.
DEFINE VARIABLE OTH-hotelencrip AS CHAR      NO-UNDO.
DEFINE VARIABLE cPersonalKey    AS CHARACTER NO-UNDO.
DEFINE VARIABLE rKey            AS RAW.
DEFINE VARIABLE mMemptrOut      AS MEMPTR.
DEFINE VARIABLE precheckinurl   AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelcode       AS CHAR      NO-UNDO.
DEFINE VARIABLE hotelcode-ok    AS LOGICAL   NO-UNDO.
DEFINE STREAM s1.

DEFINE BUFFER gmember FOR guest.

/*********************************************************************************************/
FOR EACH arrive-list:
    DELETE arrive-list.
END.

FIND FIRST res-line WHERE res-line.resnr EQ resno AND res-line.reslinnr EQ reslinno NO-LOCK NO-ERROR.
IF AVAILABLE res-line THEN
DO:
    FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK.

    CREATE arrive-list.
    ASSIGN
        arrive-list.resnr       = res-line.resnr   
        arrive-list.reslinnr    = res-line.reslinnr
        arrive-list.rsv-name    = reservation.NAME
        arrive-list.zinr        = res-line.zinr
        arrive-list.guest-name  = res-line.NAME        
        arrive-list.arrival     = res-line.ankunft
        arrive-list.departure   = res-line.abreise
    .

    FIND FIRST gmember WHERE gmember.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE gmember THEN
    DO:
        ASSIGN
            arrive-list.guest-email = gmember.email-adr   
            arrive-list.phone-no    = gmember.mobil-tel
        .
    END.

    FIND FIRST queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 7 AND queasy.number2 EQ 5 NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN precheckinurl = queasy.char3.

    FOR EACH queasy WHERE queasy.KEY EQ 216 AND queasy.number1 EQ 8 NO-LOCK:
        IF queasy.number2 EQ 31 THEN hotelcode  = queasy.char3.
        IF queasy.number2 EQ 32 THEN arrive-list.mail-eng   = queasy.char3.
        IF queasy.number2 EQ 33 THEN arrive-list.mail-oth   = queasy.char3.
        IF queasy.number2 EQ 19 THEN arrive-list.hotel-name = queasy.char3.
        IF queasy.number2 EQ 22 THEN arrive-list.hotel-telp = queasy.char3.
        IF queasy.number2 EQ 23 THEN arrive-list.hotel-mail = queasy.char3.
    END.

    IF hotelcode EQ "" THEN hotelcode-ok = NO.
    ELSE hotelcode-ok = YES.
    
    IF NOT hotelcode-ok THEN 
    DO:
        ASSIGN
            arrive-list.link-pci-eng = "HotelCode Not Configured Yet"
            arrive-list.link-pci-oth = "HotelCode Belum Terkonfigurasi Dengan Benar"
        .
    END.
    ELSE
    DO:
        EN-hotelencrip  = CHR(34) + "ENG|" + hotelcode + "|" + STRING(arrive-list.arrival) + "|" + STRING(arrive-list.resnr) + CHR(34).
        OTH-hotelencrip = CHR(34) + "IDN|" + hotelcode + "|" + STRING(arrive-list.arrival) + "|" + STRING(arrive-list.resnr) + CHR(34).

        MESSAGE "Ori String: " EN-hotelencrip VIEW-AS ALERT-BOX INFO BUTTONS OK.
        RUN encryptedText (EN-hotelencrip,"E",OUTPUT EN-hotelencrip).

        MESSAGE "encryptedText: " EN-hotelencrip VIEW-AS ALERT-BOX INFO BUTTONS OK.
        /*
        ASSIGN 
            cPersonalKey    = "97038B14732C6AD1C1ED9EC6FB675AAC2698DF86"
            rKey            = GENERATE-PBE-KEY(cPersonalKey)
            mMemptrOut      = ENCRYPT(EN-hotelencrip, rKey )
            EN-hotelencrip  = BASE64-ENCODE(MMEMPTROUT).
        */

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

        /*arrive-list.link-pci-eng = precheckinurl + "?" + EN-hotelencrip + "&hc=" + hotelcode.*/
        arrive-list.link-pci-eng = precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + EN-hotelencrip.
    
        /*
        mMemptrOut      = ENCRYPT(OTH-hotelencrip, rKey ).
        OTH-hotelencrip = BASE64-ENCODE(MMEMPTROUT).
        */

        RUN encryptedText (OTH-hotelencrip,"E",OUTPUT OTH-hotelencrip).

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

        /*arrive-list.link-pci-oth = precheckinurl + "?" + OTH-hotelencrip + "&hc=" + hotelcode.*/
        arrive-list.link-pci-oth = precheckinurl + "?" + "hc=" + hotelcode + "&ec=" + OTH-hotelencrip.
    END.
END.


/*=============DEFINE PROCEDURE=============*/

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
    MESSAGE foundit
        VIEW-AS ALERT-BOX INFO BUTTONS OK.
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
