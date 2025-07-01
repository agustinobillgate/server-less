DEFINE TEMP-TABLE t-h-bill LIKE h-bill /*FD*/
    FIELD rec-id AS INT.

DEFINE INPUT PARAMETER pvILanguage      AS INTEGER  NO-UNDO.
DEFINE INPUT PARAMETER curr-dept        AS INTEGER.
DEFINE INPUT PARAMETER curr-date        AS DATE.
DEFINE INPUT PARAMETER s-recid          AS INTEGER.
DEFINE OUTPUT PARAMETER err-flag        AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER msg-str         AS CHARACTER INIT "".
DEFINE OUTPUT PARAMETER check-ok        AS LOGICAL INIT NO.
DEFINE OUTPUT PARAMETER rec-id          AS INTEGER.
DEFINE OUTPUT PARAMETER hbill-no        AS INTEGER.

{SupertransBL.i} 
DEFINE VARIABLE lvCAREA AS CHAR INITIAL "ts-restdeposit-pay". 

DEFINE VARIABLE table-no        AS INTEGER NO-UNDO.
DEFINE VARIABLE pax             AS INTEGER NO-UNDO.
DEFINE VARIABLE gastno          AS INTEGER NO-UNDO.
DEFINE VARIABLE ns-billno       AS INTEGER NO-UNDO.
DEFINE VARIABLE curr-zeit       AS INTEGER NO-UNDO.
DEFINE VARIABLE ft-h            AS INTEGER NO-UNDO.
DEFINE VARIABLE ft-m            AS INTEGER NO-UNDO.
DEFINE VARIABLE from-time       AS INTEGER NO-UNDO.
DEFINE VARIABLE depo-amount     AS DECIMAL NO-UNDO.
DEFINE VARIABLE nsbill-saldo    AS DECIMAL NO-UNDO.
DEFINE VARIABLE bill-date       AS DATE    NO-UNDO. 
DEFINE VARIABLE rsv-date        AS DATE    NO-UNDO.

DEFINE BUFFER buffq251 FOR queasy.
DEFINE BUFFER queasy251 FOR queasy.
DEFINE BUFFER buff-hbill FOR h-bill.

FIND FIRST htparam WHERE htparam.paramnr EQ 110 NO-LOCK. 
bill-date = htparam.fdate.

FIND FIRST queasy WHERE RECID(queasy) EQ s-recid NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN
DO:
    ASSIGN
        ns-billno   = INTEGER(queasy.deci2)
        gastno      = INTEGER(ENTRY(3, queasy.char2, "&&")) 
        ft-h        = INTEGER(SUBSTR(queasy.char1, 1, 2))
        ft-m        = INTEGER(SUBSTR(queasy.char1, 3, 2))
        rsv-date    = queasy.date1
        depo-amount = queasy.deci1
        table-no    = queasy.number2
    .   
END.

IF ns-billno EQ 0 THEN
DO:
    err-flag = YES.
    msg-str = translateExtended ("Please posting deposit first for Open the Bill.",lvCAREA,"").
    RETURN.
END.

FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ gastno 
    AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
    AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:        
    FOR EACH bill-line WHERE bill-line.rechnr EQ bill.rechnr NO-LOCK:    
        nsbill-saldo = nsbill-saldo + bill-line.betrag.
    END.

    IF nsbill-saldo NE 0 THEN /*Not Balance*/
    DO:
        err-flag = YES.
        msg-str = translateExtended ("Nonstay Bill not balance. Open Bill not possible.",lvCAREA,"").
        RETURN.
    END.    
END.

from-time = (ft-h * 3600) + ft-m * 60.
curr-zeit = TIME.

IF bill-date EQ rsv-date THEN
DO:
    IF curr-zeit LT from-time THEN
    DO:
        err-flag = YES.
        msg-str = translateExtended ("Not yet entered the Reservation Time. Open Bill not possible.",lvCAREA,"").
        RETURN.
    END.
END.
ELSE IF bill-date LT rsv-date THEN
DO:
    err-flag = YES.
    msg-str = translateExtended ("Not yet entered the Reservation Time. Open Bill not possible.",lvCAREA,"").
    RETURN.
END.

FIND FIRST buffq251 WHERE buffq251.KEY EQ 251
    AND buffq251.number2 EQ s-recid NO-LOCK NO-ERROR.
IF AVAILABLE buffq251 THEN
DO:
    FIND FIRST buff-hbill WHERE RECID(buff-hbill) EQ buffq251.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE buff-hbill THEN
    DO:
        IF buff-hbill.flag EQ 1 THEN
        DO:
            err-flag = YES.
            msg-str = translateExtended ("Bill already closed. Open Bill not possible.",lvCAREA,"").
            RETURN.
        END.        
    END.
END.

FIND FIRST h-bill WHERE h-bill.flag EQ 0
    AND h-bill.tischnr EQ table-no
    AND h-bill.departement EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    IF h-bill.rechnr NE 0 THEN
    DO:
        FIND FIRST queasy251 WHERE queasy251.KEY EQ 251
            AND queasy251.number1 EQ INT(RECID(h-bill)) NO-LOCK NO-ERROR.
        IF AVAILABLE queasy251 THEN
        DO:
            err-flag = YES.
            msg-str = translateExtended ("Bill already open for this table.",lvCAREA,"").
            RETURN.    
        END.

        FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr
            AND h-bill-line.departement EQ h-bill.departement NO-LOCK NO-ERROR.
        IF AVAILABLE h-bill-line THEN
        DO:
            IF h-bill-line.bill-datum EQ rsv-date THEN
            DO:
                rec-id = RECID(h-bill).
                hbill-no = h-bill.rechnr.

                msg-str = translateExtended ("Bill already open for this table. Do you want join Deposit to Bill No",lvCAREA,"")
                    + " " + STRING(h-bill.rechnr) + " - " + h-bill.bilname + "?"
                    + CHR(10) + "Yes = Join the Bill." 
                    + CHR(10) + "No = Create a New Bill and Move Existing Bill." 
                    .
                RETURN.
            END.
        END.
    END.
END.
check-ok = YES.
