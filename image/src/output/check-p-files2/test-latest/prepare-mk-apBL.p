
DEF OUTPUT PARAMETER closed-date AS DATE        NO-UNDO.
DEF OUTPUT PARAMETER rgdatum     AS DATE        NO-UNDO.
DEF OUTPUT PARAMETER p-2000      AS LOGICAL     NO-UNDO.
DEF OUTPUT PARAMETER av-gl-acct  AS LOGICAL     NO-UNDO INIT NO.
DEF OUTPUT PARAMETER ap-acct     AS CHAR        NO-UNDO.
DEF OUTPUT PARAMETER ap-other    AS CHAR        NO-UNDO.
DEF OUTPUT PARAMETER gst-flag    AS LOGICAL     NO-UNDO.

FIND FIRST htparam WHERE paramnr = 558 NO-LOCK .
closed-date = htparam.fdate.

FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
rgdatum = htparam.fdate. 

FIND FIRST htparam WHERE paramnr = 2000 NO-LOCK.
p-2000 = htparam.flogical.


FIND FIRST htparam WHERE paramnr = 986 no-lock. /* AP AcctNo */ 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR.
IF NOT AVAILABLE gl-acct THEN av-gl-acct = NO.
ELSE
DO:
    av-gl-acct = YES.
    ap-acct = gl-acct.fibukonto. 
END.


FIND FIRST htparam WHERE paramnr = 395 no-lock. /* AP Others AcctNo */ 
FIND FIRST gl-acct WHERE gl-acct.fibukonto = htparam.fchar NO-LOCK NO-ERROR. 
IF AVAILABLE gl-acct THEN ap-other = gl-acct.fibukonto. 
ELSE ap-other = ap-acct. 

  /*gst for penang*/
FIND FIRST l-lieferant WHERE l-lieferant.firma = "GST" NO-LOCK NO-ERROR.
IF AVAILABLE l-lieferant THEN ASSIGN gst-flag = YES.
ELSE ASSIGN gst-flag = NO.
