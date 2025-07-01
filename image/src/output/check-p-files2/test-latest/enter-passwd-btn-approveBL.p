
DEF INPUT  PARAMETER q-recid    AS INT.
DEF INPUT  PARAMETER keystr     AS CHAR.
DEF INPUT  PARAMETER q-date1    AS DATE.
DEF INPUT  PARAMETER q-number1  AS INT.
DEF OUTPUT PARAMETER reason     AS CHAR.
DEF OUTPUT PARAMETER q-logi2    AS LOGICAL INIT ?.

DEF BUFFER qbuff FOR queasy.

FIND FIRST qbuff NO-LOCK WHERE qbuff.KEY = 36 AND
  qbuff.char1       = keystr                  AND
  qbuff.date1       = q-date1                 AND
  qbuff.number1     = q-number1               AND
  /*MTqbuff.number2     = INTEGER(q-recid)        AND*/
  qbuff.betriebsnr  = 1 NO-ERROR.

IF NOT AVAILABLE qbuff THEN RETURN.

IF qbuff.logi1 THEN reason = qbuff.char3.
FIND CURRENT qbuff EXCLUSIVE-LOCK.
ASSIGN qbuff.logi1 = YES.
FIND CURRENT qbuff NO-LOCK.
q-logi2 = qbuff.logi2.
