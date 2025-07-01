
DEF TEMP-TABLE t-gl-jouhdr LIKE gl-jouhdr.

DEF INPUT  PARAMETER sorttype  AS INT.
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date   AS DATE.
DEF OUTPUT PARAMETER TABLE FOR t-gl-jouhdr.

FIND FIRST htparam WHERE paramnr = 558 no-lock.    /* LAST Accounting Period */ 
from-date = htparam.fdate + 1. 
FIND FIRST htparam WHERE paramnr = 597 no-lock.   /* journal closing DATE */ 
to-date = today. 


FOR EACH gl-jouhdr
    WHERE gl-jouhdr.activeflag = sorttype
    AND gl-jouhdr.batch = NO
    AND gl-jouhdr.datum GE from-date
    AND gl-jouhdr.datum LE to-date NO-LOCK
    BY gl-jouhdr.datum BY gl-jouhdr.refno BY gl-jouhdr.bezeich:
    CREATE t-gl-jouhdr.
    BUFFER-COPY gl-jouhdr TO t-gl-jouhdr.
END.
