DEFINE TEMP-TABLE img-idcard NO-UNDO
    FIELD gastnr  AS INTEGER
    FIELD zinr    AS CHAR
    FIELD objfile AS BLOB.

DEFINE INPUT PARAMETER room             AS CHAR.
DEFINE INPUT-OUTPUT PARAMETER res-nr    AS INT.
DEFINE INPUT-OUTPUT PARAMETER reslin-nr AS INT.
DEFINE INPUT PARAMETER checkoutdate     AS DATE.
DEFINE OUTPUT PARAMETER room-status     AS CHAR.
DEFINE OUTPUT PARAMETER res-status      AS CHAR.
DEFINE OUTPUT PARAMETER guest-name      AS CHAR.
DEFINE OUTPUT PARAMETER ci-datetime     AS DATETIME.
DEFINE OUTPUT PARAMETER co-datetime     AS DATETIME.
DEFINE OUTPUT PARAMETER type-ofpay      AS CHAR.
DEFINE OUTPUT PARAMETER oth-deposit     AS DECIMAL.
DEFINE OUTPUT PARAMETER key-done        AS INT.
DEFINE OUTPUT PARAMETER key-status      AS CHAR.
DEFINE OUTPUT PARAMETER guest-phone     AS CHARACTER. 
DEFINE OUTPUT PARAMETER guest-email     AS CHARACTER. 
DEFINE OUTPUT PARAMETER guest-country   AS CHARACTER. 
DEFINE OUTPUT PARAMETER purpose-stay    AS CHARACTER.
DEFINE OUTPUT PARAMETER rsv-deposit     AS DECIMAL.
DEFINE OUTPUT PARAMETER rsv-deposit-str AS CHARACTER.
DEFINE OUTPUT PARAMETER oth-deposit-str AS CHARACTER.

DEFINE OUTPUT PARAMETER TABLE FOR img-idcard.

DEFINE VARIABLE citime     AS CHAR.
DEFINE VARIABLE cotime     AS CHAR.
DEFINE VARIABLE cidate     AS CHAR.
DEFINE VARIABLE codate     AS CHAR.
DEFINE VARIABLE loop-i     AS INT.
DEFINE VARIABLE mestoken   AS CHAR.
DEFINE VARIABLE meskeyword AS CHAR.
DEFINE VARIABLE mesvalue   AS CHAR.
DEFINE VARIABLE lvcs       AS CHAR.
DEFINE VARIABLE lviresnr   AS INT.

IF res-nr NE 0 THEN
DO:
    FIND FIRST res-line WHERE res-line.resnr EQ res-nr 
    AND res-line.reslinnr EQ reslin-nr 
    AND res-line.zinr EQ room NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        RUN assign-it.
    END.
END.
ELSE
DO:
    FIND FIRST res-line WHERE res-line.zinr EQ room 
    AND res-line.abreise EQ checkoutdate NO-LOCK NO-ERROR.
    IF AVAILABLE res-line THEN
    DO:
        RUN assign-it.
    END.
END.

PROCEDURE assign-it:
    FIND FIRST guest WHERE guest.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
    FIND FIRST zimmer WHERE zimmer.zinr EQ res-line.zinr NO-LOCK NO-ERROR.
    FIND FIRST reservation WHERE reservation.resnr EQ res-line.resnr NO-LOCK. 

    IF zimmer.zistatus EQ 0 THEN room-status = "VACANT CLEAN CHECKED".
    ELSE IF zimmer.zistatus EQ 1 THEN room-status = "VACANT CLEAN UNCHECKED".
    ELSE IF zimmer.zistatus EQ 2 THEN room-status = "VACANT DIRTY".
    ELSE IF zimmer.zistatus EQ 3 THEN room-status = "EXPECTED DEPARTURE".
    ELSE IF zimmer.zistatus EQ 4 THEN room-status = "OCCUPIED DIRTY".
    ELSE IF zimmer.zistatus EQ 5 THEN room-status = "OCCUPIED CLEANED".
    ELSE IF zimmer.zistatus EQ 6 THEN room-status = "OUT OF ORDER".
    ELSE IF zimmer.zistatus EQ 7 THEN room-status = "OFF MARKET".
    ELSE IF zimmer.zistatus EQ 8 THEN room-status = "DO NOT DISTURB".

    IF res-line.resstatus EQ 1 THEN res-status = "GUARANTEED RESERVATION".
    ELSE IF res-line.resstatus EQ 2 THEN res-status = "6 PM RESERVATION".
    ELSE IF res-line.resstatus EQ 3 THEN res-status = "TENTATIVE RESERVATION".
    ELSE IF res-line.resstatus EQ 4 THEN res-status = "WAITING LIST RESERVATION".
    ELSE IF res-line.resstatus EQ 5 THEN res-status = "ORAL CONFIRM RESERVATION".
    ELSE IF res-line.resstatus EQ 6 THEN res-status = "RESIDENT GUEST".
    ELSE IF res-line.resstatus EQ 8 THEN res-status = "CHECK OUT GUEST".

    guest-name  = guest.anrede1 + "," + guest.vorname1 + " " + guest.NAME.
    guest-name  = CAPS(guest-name).

    citime = STRING(res-line.ankzeit,"HH:MM:SS").
    cotime = STRING(res-line.abreisezeit,"HH:MM:SS").
    cidate = STRING(DAY(res-line.ankunft)) + "-" + STRING(MONTH(res-line.ankunft)) + "-" + STRING(YEAR(res-line.ankunft)).
    codate = STRING(DAY(res-line.abreise)) + "-" + STRING(MONTH(res-line.abreise)) + "-" + STRING(YEAR(res-line.abreise)).

    ci-datetime = DATETIME(cidate + " " + citime).
    co-datetime = DATETIME(codate + " " + cotime).

    IF res-line.code NE "" AND res-line.CODE NE "0" THEN 
    DO: 
        FIND FIRST queasy WHERE queasy.key EQ 9 
        AND queasy.number1 = INTEGER(res-line.code) NO-LOCK NO-ERROR. 
        IF AVAILABLE queasy THEN type-ofpay = CAPS(queasy.char1). 
    END. 

    rsv-deposit = reservation.depositgef.
    IF rsv-deposit NE 0 THEN
    DO:
        /*FOR EACH billjournal WHERE billjournal.department EQ 0
            AND MONTH(billjournal.bill-datum) EQ MONTH(TODAY)
            AND billjournal.bezeich MATCHES "*deposit*" NO-LOCK:
            lvcs = SUBSTR(billjournal.bezeich, INDEX(billjournal.bezeich,"[#") + 2).
            lviresnr = INTEGER(ENTRY(1,lvcs," ")) NO-ERROR.
            IF lviresnr EQ resnr THEN
            DO:*/
                FIND FIRST artikel WHERE artikel.departement EQ 0 
                    AND (artikel.artart = 2 OR artikel.artart = 5 OR artikel.artart = 6 
                    OR artikel.artart = 7) AND artikel.activeflag = YES 
                    AND artikel.artnr EQ reservation.zahlkonto NO-LOCK NO-ERROR.
                IF AVAILABLE artikel THEN rsv-deposit-str = CAPS(artikel.bezeich).
            /*END.
        END.*/
                
    END.

    key-done    = res-line.betrieb-gast.
    IF key-done NE 0 THEN key-status  = "DUPLICATE KEY".
    ELSE key-status  = "NEW KEY".
    
    FIND FIRST guestbook WHERE guestbook.gastnr EQ res-line.gastnrmember NO-LOCK NO-ERROR.
    IF AVAILABLE guestbook THEN
    DO:
        CREATE img-idcard.
        ASSIGN 
            img-idcard.gastnr  = guestbook.gastnr
            img-idcard.zinr    = res-line.zinr
            img-idcard.objfile = guestbook.imagefile.
    END.
    res-nr        = res-line.resnr.
    reslin-nr     = res-line.reslinnr.
    guest-phone   = guest.mobil-telefon.
    guest-email   = guest.email-adr.
    guest-country = guest.land.

    FIND FIRST nation WHERE nation.kurzbez EQ guest-country NO-LOCK NO-ERROR.
    IF AVAILABLE nation THEN guest-country = nation.bezeich.

    DO loop-i = 1 TO NUM-ENTRIES(res-line.zimmer-wunsch,";"):
        mestoken   = ENTRY(loop-i, res-line.zimmer-wunsch,";").
        IF SUBSTR(mestoken,1,8) EQ "SEGM_PUR" THEN 
        DO:
            meskeyword  = SUBSTR(mestoken,1,8).
            mesvalue    = SUBSTR(mestoken,9,1).
            LEAVE.
        END.
    END.
    IF INT(mesvalue) NE 0 THEN
    DO:
        FIND FIRST queasy WHERE queasy.KEY = 143 AND queasy.number1 EQ INT(mesvalue) NO-LOCK NO-ERROR.
        IF AVAILABLE queasy THEN 
        purpose-stay = queasy.char3.
    END.

    oth-deposit = 0.

    FIND CURRENT res-line.
    FIND CURRENT guest.
    FIND CURRENT zimmer.
    FIND CURRENT reservation.
    RELEASE res-line.     
    RELEASE guest.        
    RELEASE zimmer.       
    RELEASE reservation.  
END.







