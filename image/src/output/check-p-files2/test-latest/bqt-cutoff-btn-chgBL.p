
DEF INPUT  PARAMETER o-resnr        AS INT.
DEF INPUT  PARAMETER o-reslinnr     AS INT.
DEF INPUT  PARAMETER o-resstatus    AS INT.
DEF OUTPUT PARAMETER recid-bk-reser AS INT.
DEF OUTPUT PARAMETER msg-it         AS LOGICAL INIT NO.

IF o-resstatus = 1 THEN
DO:
    FIND FIRST bk-veran WHERE bk-veran.veran-nr = o-resnr 
        USE-INDEX vernr-ix NO-LOCK. 
    IF (bk-veran.deposit-payment[1] + bk-veran.deposit-payment[2] 
        + bk-veran.deposit-payment[3] + bk-veran.deposit-payment[4] 
        + bk-veran.deposit-payment[5] + bk-veran.deposit-payment[6] 
        + bk-veran.deposit-payment[7] + bk-veran.deposit-payment[8] 
        + bk-veran.deposit-payment[9]) NE 0 THEN 
    DO: 
        FIND FIRST bk-reser WHERE bk-reser.veran-nr = bk-veran.veran-nr 
        AND bk-reser.veran-resnr NE o-reslinnr 
        AND bk-reser.resstatus = 1 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE bk-reser THEN 
        DO: 
            msg-it = YES.
        END. 
    END.
END.
IF msg-it THEN RETURN NO-APPLY.
FIND FIRST bk-reser WHERE bk-reser.veran-nr = o-resnr
  AND bk-reser.veran-seite = o-reslinnr NO-LOCK NO-ERROR. /* Malik Serverless 597 add if available */
IF AVAILABLE bk-reser THEN 
DO:
    ASSIGN
        recid-bk-reser = RECID(bk-reser).
END.
