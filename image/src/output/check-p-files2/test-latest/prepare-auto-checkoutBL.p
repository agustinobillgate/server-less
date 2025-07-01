
DEF INPUT  PARAMETER resnr AS INTEGER. 
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER res-name AS CHAR.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK NO-ERROR. /* Malik Serverless : NO-LOCK -> NO-LOCK NO-ERROR */
IF AVAILABLE reservation THEN
DO:
    res-name = reservation.name.
END.


