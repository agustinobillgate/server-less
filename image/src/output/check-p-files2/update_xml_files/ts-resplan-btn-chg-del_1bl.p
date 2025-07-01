DEF TEMP-TABLE t-queasy
    FIELD char1   LIKE queasy.char1
    FIELD char2   LIKE queasy.char2
    FIELD number3 LIKE queasy.number3
    FIELD rec-id  AS INT.

DEF INPUT  PARAMETER s-recid AS INT.
DEF INPUT  PARAMETER curr-dept AS INT.
DEF INPUT  PARAMETER table-no AS INT.
DEF OUTPUT PARAMETER flag-code AS INT.
DEF OUTPUT PARAMETER deposit-pay AS DECIMAL.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.

DEFINE VARIABLE deposit-amt AS DECIMAL NO-UNDO.
DEFINE VARIABLE guest-no    AS INTEGER NO-UNDO.
DEFINE VARIABLE ns-billno   AS INTEGER NO-UNDO.
DEFINE VARIABLE depoart     AS INTEGER NO-UNDO.
DEFINE VARIABLE rsv-date    AS DATE    NO-UNDO.

DEFINE BUFFER buffq251 FOR queasy.
DEFINE BUFFER queasy251 FOR queasy.
DEFINE BUFFER buff-hbill FOR h-bill.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart = htparam.finteger.

FIND FIRST queasy WHERE RECID(queasy) EQ s-recid NO-LOCK.
CREATE t-queasy.
ASSIGN
    t-queasy.char1   = queasy.char1
    t-queasy.char2   = queasy.char2
    t-queasy.number3 = queasy.number3
    t-queasy.rec-id  = RECID(queasy)
    .

ASSIGN
    deposit-amt = queasy.deci1
    guest-no    = INTEGER(ENTRY(3, queasy.char2, "&&"))
    ns-billno   = INTEGER(queasy.deci2)
    rsv-date    = queasy.date1
    .

/*FD Dec 02, 2022 => Check h-bill*/
FIND FIRST buffq251 WHERE buffq251.KEY EQ 251
    AND buffq251.number2 EQ s-recid NO-LOCK NO-ERROR.
IF AVAILABLE buffq251 THEN
DO:
    FIND FIRST buff-hbill WHERE RECID(buff-hbill) EQ buffq251.number1 NO-LOCK NO-ERROR.
    IF AVAILABLE buff-hbill THEN
    DO:
        IF buff-hbill.flag EQ 1 THEN
        DO:
            flag-code = 2.            
            RETURN.
        END.    
        ELSE
        DO:
            flag-code = 3.            
            RETURN.
        END.
    END.
END.

FIND FIRST h-bill WHERE h-bill.flag EQ 0
    AND h-bill.tischnr EQ table-no
    AND h-bill.departement EQ curr-dept NO-LOCK NO-ERROR.
IF AVAILABLE h-bill THEN
DO:
    FIND FIRST queasy251 WHERE queasy251.KEY EQ 251
        AND queasy251.number1 EQ INT(RECID(h-bill))
        AND queasy251.number2 EQ s-recid NO-LOCK NO-ERROR.
    IF AVAILABLE queasy251 THEN
    DO:
        IF h-bill.rechnr NE 0 THEN
        DO:        
            FIND FIRST h-bill-line WHERE h-bill-line.rechnr EQ h-bill.rechnr
                AND h-bill-line.departement EQ h-bill.departement NO-LOCK NO-ERROR.
            IF AVAILABLE h-bill-line THEN
            DO:
                IF h-bill-line.bill-datum EQ rsv-date THEN
                DO:
                    flag-code = 3.
                    RETURN.
                END.
            END.
        END.
    END.    
END.

/*FD Dec 02, 2022 => Check Deposit and Payment*/
FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ guest-no 
    AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
    AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:
    FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
        AND bill-line.artnr NE depoart NO-LOCK NO-ERROR.
    IF AVAILABLE bill-line THEN
    DO:
        deposit-pay = bill-line.betrag.
    END.
END.

IF deposit-amt NE 0 AND deposit-pay NE 0 THEN
DO:
    flag-code = 1.
    RETURN.
END.
