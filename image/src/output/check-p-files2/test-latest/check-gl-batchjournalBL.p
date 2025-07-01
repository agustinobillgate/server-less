
DEF INPUT PARAMETER from-date   AS DATE NO-UNDO.
DEF INPUT PARAMETER to-date     AS DATE NO-UNDO.

DEFINE OUTPUT PARAMETER avail-batch AS LOGICAL NO-UNDO INITIAL NO.

DEFINE VARIABLE date1 AS DATE. 
DEFINE VARIABLE date2 AS DATE. 

FIND FIRST htparam WHERE htparam.paramnr = 558 NO-LOCK.    /* LAST Accounting Period */ 
date1 = htparam.fdate + 1. 
FIND FIRST htparam WHERE htparam.paramnr = 597 NO-LOCK.   /* journal closing DATE */ 
date2 = htparam.fdate. 

IF from-date GT date1 THEN date1 = from-date. 
IF to-date LT date2 THEN date2 = to-date.

FIND FIRST gl-jouhdr WHERE gl-jouhdr.activeflag = 0
    AND gl-jouhdr.datum GE date1 AND gl-jouhdr.datum LE date2 
    AND gl-jouhdr.batch = YES NO-LOCK NO-ERROR.
IF AVAILABLE gl-jouhdr THEN DO:
    ASSIGN avail-batch = YES.
END.
