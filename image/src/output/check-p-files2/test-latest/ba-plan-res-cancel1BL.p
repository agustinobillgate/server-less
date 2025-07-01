
DEF INPUT  PARAMETER pvILanguage AS INTEGER NO-UNDO.
DEF INPUT  PARAMETER t-resnr     AS INT.
DEF INPUT  PARAMETER t-reslinnr  AS INT.
DEF OUTPUT PARAMETER msg-str1    AS CHAR INIT "".
DEF OUTPUT PARAMETER msg-str2    AS CHAR INIT "".
DEF OUTPUT PARAMETER msg-str3    AS CHAR INIT "".

DEFINE BUFFER bk-resline FOR bk-reser. 
DEFINE BUFFER resline    FOR bk-reser.
DEFINE BUFFER mainres    FOR bk-veran. 
DEFINE BUFFER gast       FOR guest. 

DEF VAR ci-date AS DATE.

{SupertransBL.i}   
DEF VAR lvCAREA AS CHAR INITIAL "ba-plan".

FIND FIRST htparam WHERE htparam.paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 

FIND FIRST resline WHERE resline.veran-nr = t-resnr
    AND resline.veran-resnr = t-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE resline THEN 
DO: 
    IF (resline.datum = ci-date) AND (resline.resstatus = 1) THEN 
    DO: 
        msg-str1 = translateExtended ("Can not cancel today's guaranted reservation.",lvCAREA,"").
        RETURN NO-APPLY. 
    END. 
    FIND FIRST mainres WHERE mainres.veran-nr = resline.veran-nr 
        USE-INDEX vernr-ix NO-LOCK.

    IF (mainres.deposit-payment[1] + mainres.deposit-payment[2] 
        + mainres.deposit-payment[3] + mainres.deposit-payment[4] 
        + mainres.deposit-payment[5] + mainres.deposit-payment[6] 
        + mainres.deposit-payment[7] + mainres.deposit-payment[8] 
        + mainres.deposit-payment[9]) GT 0 THEN 
    DO: 
        FIND FIRST bk-resline WHERE bk-resline.veran-nr = mainres.veran-nr 
            AND bk-resline.veran-resnr NE t-reslinnr 
            AND bk-resline.resstatus = 1 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE bk-resline THEN 
        DO: 
            msg-str1 = translateExtended ("Deposit exists, cancel reservation not possible.",lvCAREA,"").
            RETURN NO-APPLY. 
        END. 
    END. 
    ELSE DO: /*ITA 120318*/
        FIND FIRST bk-reser WHERE bk-reser.veran-nr = mainres.veran-nr 
            AND bk-reser.veran-resnr = t-reslinnr
            AND bk-reser.resstatus LE 3 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE bk-reser THEN DO:
            msg-str1 = translateExtended ("Deposit exists, cancel reservation not possible.",lvCAREA,"").
            RETURN NO-APPLY. 
        END.
    END.

    IF mainres.rechnr > 0 THEN 
    DO: 
        FIND FIRST bk-resline WHERE bk-resline.veran-nr = mainres.veran-nr 
            AND bk-resline.veran-resnr NE t-reslinnr 
            AND bk-resline.resstatus LE 2 NO-LOCK NO-ERROR. /* mnaufal - change validation from eq 1 to le 2*/
        IF NOT AVAILABLE bk-resline THEN 
        DO: 
            FIND FIRST bill WHERE bill.rechnr EQ mainres.rechnr
                AND bill.flag EQ 0 NO-LOCK NO-ERROR.    /*ADD Validation Ticket #5F4E76*/
            IF AVAILABLE bill THEN
            DO:
                msg-str1 = translateExtended ("Bill exists, cancel reservation not possible.",lvCAREA,"").
                RETURN NO-APPLY. 
            END.           
        END. 
    END. 

    FIND FIRST gast WHERE gast.gastnr = mainres.gastnr NO-LOCK. 
    FIND FIRST bk-raum WHERE bk-raum.raum = resline.raum NO-LOCK.

    msg-str2 = "&Q" + translateExtended ("Do you really want to cancel reservation of",lvCAREA,"")
             + CHR(10)
             + gast.name + translateExtended (" - Room:",lvCAREA,"") + " " + bk-raum.bezeich 
             + CHR(10)
             + translateExtended ("Date:",lvCAREA,"") + " " + STRING(resline.datum) + " - " + STRING(resline.bis-datum) 
             + translateExtended ("  Time:",lvCAREA,"") + " " + STRING(resline.von-zeit,"99:99") 
             + " - " + STRING(resline.bis-zeit,"99:99") + "?".

    msg-str3 = "&Q" + translateExtended ("Do you want to cancel all reservation of this reservation number ",lvCAREA,"") 
             + CHR(10)
             + translateExtended ("ResNr:",lvCAREA,"") + " " + STRING(resline.veran-nr) + "?".
END.
