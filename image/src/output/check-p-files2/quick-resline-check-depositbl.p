
DEF INPUT PARAMETER case-type   AS INTEGER.
DEF INPUT PARAMETER resnr       AS INTEGER.
DEF INPUT PARAMETER gastnr      AS INTEGER.
DEF INPUT PARAMETER deposit     AS DECIMAL.
DEF OUTPUT PARAMETER flag1      AS LOGICAL INIT NO.


IF case-type = 1 THEN
DO :
    FIND FIRST reservation WHERE reservation.resnr = resnr
        AND reservation.gastnr = gastnr EXCLUSIVE-LOCK.
    ASSIGN reservation.depositgef = deposit.
    FIND CURRENT reservation NO-LOCK.
END.
ELSE IF case-type = 2 THEN
DO:
    FIND FIRST reservation WHERE reservation.resnr = resnr
        AND reservation.gastnr = gastnr NO-LOCK.
    IF (reservation.depositbez EQ 0) AND (reservation.depositbez2 EQ 0) THEN 
    DO: 
      /*APPLY "entry" TO deposit. */
      flag1 = YES.
      RETURN NO-APPLY. 
    END. 
END.
