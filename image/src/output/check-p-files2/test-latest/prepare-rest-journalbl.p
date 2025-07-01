
DEF TEMP-TABLE t-queasy
    FIELD char2 LIKE queasy.char2.
DEF TEMP-TABLE t-hoteldpt LIKE hoteldpt.

DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER long-digit     AS LOGICAL.
DEF OUTPUT PARAMETER min-dept       AS INT INITIAL 99.
DEF OUTPUT PARAMETER min-art        AS INT.
DEF OUTPUT PARAMETER max-art        AS INT.
DEF OUTPUT PARAMETER from-art       AS INT.
DEF OUTPUT PARAMETER max-dept       AS INT INITIAL 0.
DEF OUTPUT PARAMETER to-art         AS INT INITIAL 9999999.
DEF OUTPUT PARAMETER from-dept      AS INT.
DEF OUTPUT PARAMETER to-dept        AS INT.
DEF OUTPUT PARAMETER depname1       AS CHAR.
DEF OUTPUT PARAMETER depname2       AS CHAR.
DEF OUTPUT PARAMETER avail-queasy   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER TABLE FOR t-queasy.
DEF OUTPUT PARAMETER TABLE FOR t-hoteldpt.

FIND FIRST hoteldpt WHERE hoteldpt.num GT 0 NO-LOCK NO-ERROR.
IF NOT AVAILABLE hoteldpt THEN RETURN NO-APPLY.

FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
from-date = htparam.fdate. 
to-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical.

min-dept = 999.
max-dept = 1.
FOR EACH hoteldpt WHERE hoteldpt.num GE 1 NO-LOCK BY hoteldpt.num: 
  IF min-dept GT hoteldpt.num THEN min-dept = hoteldpt.num.
  IF max-dept LT hoteldpt.num THEN max-dept = hoteldpt.num. 
END.
min-art = 0.    /* e.g. room transfer */ 
max-art = 9999999. 

from-art = min-art. 
to-art = max-art. 
from-dept = min-dept. 
to-dept = max-dept. 

FIND FIRST hoteldpt WHERE hoteldpt.num = from-dept NO-LOCK. 
depname1 = hoteldpt.depart. 
FIND FIRST hoteldpt WHERE hoteldpt.num = to-dept NO-LOCK. 
depname2 = hoteldpt.depart. 


FIND FIRST vhp.queasy WHERE vhp.queasy.key = 10 NO-LOCK NO-ERROR.
IF AVAILABLE vhp.queasy THEN 
DO:
  avail-queasy = YES.
  RUN fill-odTaker.
  /*ENABLE od-taker WITH FRAME frame1.*/
END.

FOR EACH hoteldpt:
    CREATE t-hoteldpt.
    BUFFER-COPY hoteldpt TO t-hoteldpt.
END.

PROCEDURE fill-odTaker:
  FOR EACH queasy WHERE queasy.KEY = 10 NO-LOCK BY queasy.char2:
      CREATE t-queasy.
      ASSIGN t-queasy.char2 = queasy.char2.
    /*MTod-taker:ADD-LAST(queasy.char2) IN FRAME frame1.*/
  END.
  /*MTod-taker:ADD-FIRST("").*/
END.


