DEFINE TEMP-TABLE l-hauptgrp-list
    FIELD endkum  LIKE l-hauptgrp.endkum
    FIELD bezeich LIKE l-hauptgrp.bezeich.

DEF INPUT  PARAMETER link-in        AS LOGICAL.
DEF OUTPUT PARAMETER f-int          AS INTEGER INIT 0.
DEF OUTPUT PARAMETER jtype          AS INTEGER INIT 0.
DEF OUTPUT PARAMETER last-acctdate  AS DATE.
DEF OUTPUT PARAMETER acct-date      AS DATE.
DEF OUTPUT PARAMETER close-year     AS DATE.
DEF OUTPUT PARAMETER TABLE FOR l-hauptgrp-list.

FIND FIRST htparam WHERE htparam.paramnr = 1012 NO-LOCK.
IF htparam.paramgr = 38 AND htparam.feldtyp = 1 AND htparam.finteger GT 0 THEN
    f-int = htparam.finteger.


IF link-in THEN 
DO: 
  FIND FIRST htparam WHERE paramnr = 269 NO-LOCK. 
  jtype = 6. 
  /*MThide from-grp grpname. */
END. 
ELSE  /* link-out */ 
DO: 
  FIND FIRST htparam WHERE paramnr = 1035 NO-LOCK. 
  jtype = 3. 
END.

last-acctdate = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* CURRENT Accounting Period */ 
acct-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 795 NO-LOCK. 
close-year = htparam.fdate.

FOR EACH l-hauptgrp:
    CREATE l-hauptgrp-list.
    ASSIGN
      l-hauptgrp-list.endkum  = l-hauptgrp.endkum
      l-hauptgrp-list.bezeich = l-hauptgrp.bezeich.
END.
