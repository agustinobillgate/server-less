
DEF OUTPUT PARAMETER from-date  AS DATE.
DEF OUTPUT PARAMETER to-date    AS DATE.
DEF OUTPUT PARAMETER from-refno LIKE gl-jouhdr.refno.
DEF OUTPUT PARAMETER ref-bez    AS CHAR.

FIND FIRST htparam WHERE paramnr = 558 no-lock.    /* LAST Accounting Period */ 
from-date = htparam.fdate + 1. 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
to-date = today. 

FIND FIRST gl-jouhdr WHERE gl-jouhdr.datum = from-date NO-LOCK NO-ERROR. 
IF AVAILABLE gl-jouhdr THEN 
DO: 
  from-refno = gl-jouhdr.refno. 
  ref-bez = gl-jouhdr.bezeich. 
END. 
