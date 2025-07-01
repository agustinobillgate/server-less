DEFINE OUTPUT PARAMETER from-date   AS DATE.

DEFINE VARIABLE bill-date  AS DATE NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 110 NO-LOCK.
ASSIGN
  bill-date = htparam.fdate
  from-date = bill-date - 80
  from-date = DATE(MONTH(from-date), 1, YEAR(from-date)).
