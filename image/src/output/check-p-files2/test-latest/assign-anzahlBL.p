
DEF INPUT PARAMETER resnr AS INT.
DEF OUTPUT PARAMETER anzahl AS INT.

DEF VAR deposit AS LOGICAL.
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR.
IF (reservation.depositbez + reservation.depositbez2) NE 0 
    THEN deposit = YES. 

IF deposit THEN 
DO: 
    FOR EACH res-line WHERE res-line.resnr = resnr 
        AND res-line.active-flag = 0 NO-LOCK: 
      anzahl = anzahl + 1. 
    END.
END. 
