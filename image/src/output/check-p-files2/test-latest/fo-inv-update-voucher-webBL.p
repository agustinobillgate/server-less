DEFINE INPUT PARAMETER new-voucher  AS CHARACTER.
DEFINE INPUT PARAMETER bline-recid  AS INTEGER.
DEFINE INPUT PARAMETER bline-desc   AS CHARACTER.
DEFINE INPUT PARAMETER art-num      AS INTEGER.
DEFINE INPUT PARAMETER dept-num     AS INTEGER.
DEFINE INPUT PARAMETER bill-num     AS INTEGER.
DEFINE INPUT PARAMETER bill-date    AS DATE.
DEFINE OUTPUT PARAMETER error-msg   AS CHARACTER.

DEFINE VARIABLE curr-voucher    AS CHARACTER NO-UNDO.
DEFINE VARIABLE desc-str        AS CHARACTER NO-UNDO.
DEFINE VARIABLE room-num        AS CHARACTER NO-UNDO.
DEFINE VARIABLE art-type        AS INTEGER NO-UNDO.
DEFINE VARIABLE found-it        AS LOGICAL NO-UNDO.
DEFINE VARIABLE resno           AS INTEGER NO-UNDO.
DEFINE VARIABLE reslinno        AS INTEGER NO-UNDO.
DEFINE VARIABLE i               AS INTEGER NO-UNDO.
DEFINE VARIABLE str             AS CHARACTER NO-UNDO.

FIND FIRST artikel WHERE artikel.artnr EQ art-num
    AND artikel.departement EQ dept-num NO-LOCK NO-ERROR.
IF AVAILABLE artikel THEN art-type = artikel.artart.

IF art-type EQ 5 OR art-type EQ 8 OR art-type EQ 9 THEN
DO:
    error-msg = "Article Type is not support.".
    RETURN.
END.

FIND FIRST bill-line WHERE RECID(bill-line) EQ bline-recid NO-LOCK NO-ERROR.
IF NOT AVAILABLE bill-line THEN
DO:
    error-msg = "Selected bill not found.".
    RETURN.
END.

IF NUM-ENTRIES(bline-desc,"/") GT 1 THEN
DO:
    desc-str = ENTRY(1, bline-desc, "/").
    curr-voucher = TRIM(ENTRY(2, bline-desc, "/")).
END.

FIND FIRST bill WHERE bill.rechnr EQ bill-num NO-LOCK NO-ERROR.
IF AVAILABLE bill THEN
DO:
    ASSIGN
        resno = bill.resnr
        reslinno = bill.reslinnr
        .
END.

/***# Update Bill-Line #***/
FIND CURRENT bill-line EXCLUSIVE-LOCK.
IF NUM-ENTRIES(bill-line.bezeich,"/") GT 1 THEN
DO:
    ENTRY(2, bill-line.bezeich, "/") = new-voucher.
END.
FIND CURRENT bill-line NO-LOCK.
room-num = bill-line.zinr.
RELEASE bill-line.


/***# Update Billjournal #***/
FOR EACH billjournal WHERE billjournal.rechnr EQ bill-num
    AND billjournal.artnr EQ art-num
    AND billjournal.departement EQ dept-num
    AND billjournal.bill-datum EQ bill-date
    AND billjournal.zinr EQ room-num EXCLUSIVE-LOCK:
            
    IF NUM-ENTRIES(billjournal.bezeich,"/") GT 1 THEN
    DO:
        IF ENTRY(2, billjournal.bezeich, "/") EQ curr-voucher THEN
        DO:
            ENTRY(2, billjournal.bezeich, "/") = new-voucher.
            found-it = YES.
        END.           
    END.   

    IF found-it THEN
    DO:
        found-it = NO.
        LEAVE.
    END.
END.
RELEASE billjournal.

/***# Update Debitor #***/
IF art-type EQ 2 OR art-type EQ 7 THEN
DO:
    FOR EACH debitor WHERE debitor.rechnr EQ bill-num
        AND debitor.rgdatum EQ bill-date
        AND debitor.artnr EQ art-num
        AND debitor.zinr EQ room-num EXCLUSIVE-LOCK:

        IF resno NE 0 AND reslinno NE 0 THEN    /*Guest Bill*/
        DO:
            IF NUM-ENTRIES(debitor.vesrcod,";") GT 1 THEN
            DO:
                IF ENTRY(2, debitor.vesrcod, ";") EQ curr-voucher THEN
                DO:
                    ENTRY(2, debitor.vesrcod, ";") = new-voucher.
                    found-it = YES.
                END.
            END.
        END.
        ELSE    /*NS or MB*/
        DO:
            IF NUM-ENTRIES(debitor.vesrcod,";") GT 1 THEN
            DO:
                DO i = 1 TO NUM-ENTRIES(debitor.vesrcod,";"):
                    str = ENTRY(i, debitor.vesrcod, ";").
                    IF str EQ curr-voucher THEN
                    DO:
                        ENTRY(i, debitor.vesrcod, ";") = new-voucher.
                        found-it = YES.
                        LEAVE.
                    END.
                END.
            END.
            ELSE
            DO:
                debitor.vesrcod = new-voucher.
                found-it = YES.
            END.
        END.
        
        IF found-it THEN
        DO:
            found-it = NO.
            LEAVE.
        END.
    END.
    RELEASE debitor.
END.

