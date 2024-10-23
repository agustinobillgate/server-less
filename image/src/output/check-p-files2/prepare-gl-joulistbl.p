

DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER close-date AS DATE.
DEF OUTPUT PARAMETER close-year AS DATE.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER curr-yr    AS INTEGER.
DEF OUTPUT PARAMETER from-main  AS INTEGER.
DEF OUTPUT PARAMETER main-bez   AS CHAR.
DEF OUTPUT PARAMETER gst-flag   AS LOGICAL.
DEF OUTPUT PARAMETER cflow-flag AS LOGICAL INIT NO.

FIND FIRST htparam WHERE paramnr = 558 no-lock.    /* LAST Accounting Period */ 
from-date = htparam.fdate + 1. 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
close-date = htparam.fdate. 
FIND FIRST htparam WHERE paramnr = 795 no-lock.   /* LAST closing year DATE */ 
close-year = htparam.fdate. 
close-year = DATE(MONTH(close-year), day(close-year), YEAR(close-year) + 1). 
to-date = TODAY.
curr-yr = YEAR(htparam.fdate) + 1.


FIND FIRST gl-main NO-LOCK. 
IF AVAILABLE gl-main THEN 
DO: 
  from-main = gl-main.code. 
  main-bez = gl-main.bezeich. 
END. 


/*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.

/*for penang*/
FIND FIRST queasy WHERE queasy.KEY = 177 NO-LOCK NO-ERROR.
IF AVAILABLE queasy THEN ASSIGN cflow-flag = YES.

