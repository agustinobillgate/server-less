
DEFINE INPUT PARAMETER adjust-flag  AS LOGICAL. 
DEF OUTPUT PARAMETER f-int          AS INTEGER INIT 0.
DEF OUTPUT PARAMETER datum          AS DATE.
DEF OUTPUT PARAMETER last-acctdate  AS DATE.
DEF OUTPUT PARAMETER acct-date      AS DATE.
DEF OUTPUT PARAMETER close-year     AS DATE.
DEF OUTPUT PARAMETER avail-queasy   AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER gst-flag       AS LOGICAL NO-UNDO.

FIND FIRST htparam WHERE htparam.paramnr = 1012 NO-LOCK.
IF htparam.paramgr = 38 AND htparam.feldtyp = 1 AND htparam.finteger GT 0 THEN
    f-int = htparam.finteger.


IF NOT adjust-flag THEN 
  FIND FIRST htparam WHERE paramnr = 372 no-lock.   /* journal posting DATE */ 
ELSE 
  FIND FIRST htparam WHERE paramnr = 795 no-lock.   /* LAST year closing DATE */ 
datum = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 558 no-lock.   /* LAST Accounting Period */ 
last-acctdate = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* CURRENT Accounting Period */ 
acct-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 795 NO-LOCK. 
close-year = htparam.fdate. 

FIND FIRST queasy WHERE queasy.key = 108 NO-LOCK NO-ERROR. 
IF NOT AVAILABLE queasy THEN avail-queasy = NO.
ELSE avail-queasy = YES.


/*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.
