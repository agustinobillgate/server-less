
DEF INPUT  PARAMETER resnr AS INTEGER. 
DEF OUTPUT PARAMETER ci-date AS DATE.
DEF OUTPUT PARAMETER res-name AS CHAR.

FIND FIRST htparam WHERE paramnr = 87 NO-LOCK. 
ci-date = htparam.fdate. 
FIND FIRST reservation WHERE reservation.resnr = resnr NO-LOCK.
res-name = reservation.name.
