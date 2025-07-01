DEF TEMP-TABLE t-tisch
    FIELD tischnr LIKE tisch.tischnr.

DEF INPUT  PARAMETER s-recid AS INT.
DEF INPUT  PARAMETER curr-dept AS INT.
DEF OUTPUT PARAMETER gname AS CHAR.
DEF OUTPUT PARAMETER telefon AS CHAR.
DEF OUTPUT PARAMETER comments AS CHAR.
DEF OUTPUT PARAMETER gastno AS INTEGER.
DEF OUTPUT PARAMETER depo-amount AS DECIMAL.
DEF OUTPUT PARAMETER depo-payment AS DECIMAL.
DEF OUTPUT PARAMETER date-depopay AS DATE.
DEF OUTPUT PARAMETER ns-billno AS INTEGER.
DEF OUTPUT PARAMETER active-deposit AS LOGICAL.
DEF OUTPUT PARAMETER TABLE FOR t-tisch.

DEFINE VARIABLE depoart AS INTEGER NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr EQ 1361 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN depoart = htparam.finteger.

FIND FIRST htparam WHERE htparam.paramnr EQ 588 NO-LOCK NO-ERROR. 
IF AVAILABLE htparam THEN active-deposit = htparam.flogical.

IF s-recid NE 0 THEN
DO:
    FIND FIRST queasy WHERE RECID(queasy) EQ s-recid NO-LOCK NO-ERROR.
    IF AVAILABLE queasy THEN
    DO:
        ASSIGN
            gname       = ENTRY(1, queasy.char2, "&&")
            gastno      = INTEGER(ENTRY(3, queasy.char2, "&&"))
            telefon     = TRIM(SUBSTR(queasy.char1,10))
            comments    = ENTRY(2, queasy.char3, ";")
            depo-amount = queasy.deci1
            ns-billno   = INTEGER(queasy.deci2)
        .

        FIND FIRST bill WHERE bill.rechnr EQ ns-billno AND bill.gastnr EQ gastno 
            AND bill.resnr EQ 0 AND bill.reslinnr EQ 1 
            AND bill.billtyp EQ curr-dept AND bill.flag EQ 1 NO-LOCK NO-ERROR.
        IF AVAILABLE bill THEN
        DO:
            FIND FIRST bill-line WHERE bill-line.rechnr EQ bill.rechnr
                AND bill-line.artnr NE depoart NO-LOCK NO-ERROR.
            IF AVAILABLE bill-line THEN
            DO:
                ASSIGN
                    depo-payment = bill-line.betrag
                    date-depopay = bill-line.bill-datum
                    .
            END.
        END.
    END.    
END.

FOR EACH tisch WHERE departement EQ curr-dept:
    CREATE t-tisch.
    ASSIGN t-tisch.tischnr = tisch.tischnr.
END.
