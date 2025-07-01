DEFINE INPUT PARAMETER rml-resnr    AS INT.
DEFINE INPUT PARAMETER rml-reslinnr AS INT.
DEFINE INPUT PARAMETER rml-raum     AS CHAR.
DEFINE INPUT PARAMETER rml-nr       AS INT.
DEFINE INPUT PARAMETER curr-i       AS INT.
DEFINE OUTPUT PARAMETER err         AS INT INIT 0.
DEFINE OUTPUT PARAMETER recid-rl    AS INT.
DEFINE OUTPUT PARAMETER rl-veran-nr AS INT.
DEFINE OUTPUT PARAMETER mess-str    AS CHAR.

DEFINE VARIABLE curr-room     AS CHAR.
DEFINE VARIABLE curr-status   AS INT.

DEFINE BUFFER mainres FOR bk-veran. 
DEFINE BUFFER rl FOR bk-reser. 
DEFINE BUFFER bf FOR bk-func. 
DEFINE BUFFER bk-resline FOR bk-reser. 

curr-room   = rml-raum. 
curr-status = rml-nr.

FIND FIRST rl WHERE rl.veran-nr EQ rml-resnr AND rl.veran-seite EQ rml-reslinnr NO-LOCK NO-ERROR. 
IF AVAILABLE rl THEN
    ASSIGN
    recid-rl    = RECID(rl)
    rl-veran-nr = rl.veran-nr.
IF AVAILABLE rl AND rl.resstatus EQ 1 THEN 
DO: 
    FIND FIRST mainres WHERE mainres.veran-nr EQ rl.veran-nr USE-INDEX vernr-ix NO-LOCK. 
    IF (mainres.deposit-payment[1] + mainres.deposit-payment[2] 
        + mainres.deposit-payment[3] + mainres.deposit-payment[4] 
        + mainres.deposit-payment[5] + mainres.deposit-payment[6] 
        + mainres.deposit-payment[7] + mainres.deposit-payment[8] 
        + mainres.deposit-payment[9]) NE 0 THEN 
    DO: 
        FIND FIRST bk-resline WHERE bk-resline.veran-nr EQ mainres.veran-nr 
        AND bk-resline.veran-resnr NE rml-reslinnr 
        AND bk-resline.resstatus EQ 1 NO-LOCK NO-ERROR. 
        IF NOT AVAILABLE bk-resline THEN 
        DO: 
            err = 1.
            mess-str = "Deposit exists, status change not possible!".
            RETURN. 
        END. 
    END. 
END. 

