DEF TEMP-TABLE t-bediener LIKE bediener.
DEF TEMP-TABLE t-l-ophdr LIKE l-ophdr
    FIELD rec-id AS INT.
DEF TEMP-TABLE t-l-lager
    FIELD lager-nr LIKE l-lager.lager-nr
    FIELD bezeich  LIKE l-lager.bezeich.

DEF OUTPUT PARAMETER wip-acct       AS CHAR.
DEF OUTPUT PARAMETER req-flag       AS LOGICAL.
DEF OUTPUT PARAMETER billdate       AS DATE.
DEF OUTPUT PARAMETER closedate      AS DATE.
DEF OUTPUT PARAMETER mat-closedate  AS DATE.
DEF OUTPUT PARAMETER transdate      AS DATE.
DEF OUTPUT PARAMETER err-code       AS INT INIT 0.
DEF OUTPUT PARAMETER TABLE FOR t-l-lager.
DEF OUTPUT PARAMETER TABLE FOR t-l-ophdr.
DEF OUTPUT PARAMETER TABLE FOR t-bediener.

FIND FIRST htparam WHERE paramnr = 2000 no-lock. /* G/L License */ 
IF htparam.flogical THEN 
DO: 
  FIND FIRST htparam WHERE htparam.paramnr = 1201 NO-LOCK. 
  FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR. 
  IF NOT AVAILABLE gl-acct THEN 
  DO:
    err-code = 1.
    RETURN.
  END. 
  ELSE IF gl-acct.acc-type NE 3 THEN 
  DO:
    err-code = 2.
    RETURN.
  END. 
  wip-acct = htparam.fchar. 
END. 
 
FIND FIRST htparam WHERE paramnr = 475 NO-LOCK. 
req-flag = NOT htparam.flogical. 
 
FIND FIRST htparam WHERE paramnr = 474 NO-LOCK. 
billdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 224 NO-LOCK. 
closedate = htparam.fdate. 
IF billdate GT closedate THEN billdate = closedate. 
 
FIND FIRST htparam WHERE paramnr = 221 NO-LOCK. 
mat-closedate = htparam.fdate. 
 
transdate = billdate. 

FOR EACH l-lager:
    CREATE t-l-lager.
    ASSIGN
    t-l-lager.lager-nr = l-lager.lager-nr
    t-l-lager.bezeich  = l-lager.bezeich.
END.

DO transaction: 
    create l-ophdr. 
    FIND CURRENT l-ophdr NO-LOCK. 
    CREATE t-l-ophdr.
    BUFFER-COPY l-ophdr TO t-l-ophdr.
    ASSIGN t-l-ophdr.rec-id = RECID(l-ophdr).
END. 

FOR EACH bediener:
    CREATE t-bediener.
    BUFFER-COPY bediener TO t-bediener.
END.
