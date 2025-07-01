
DEF OUTPUT PARAMETER from-date AS DATE.
DEF OUTPUT PARAMETER to-date   AS DATE.

DEFINE VARIABLE ci-date AS DATE NO-UNDO. 
FIND FIRST htparam WHERE paramnr = 87 no-lock.  /*Invoicing DATE */ 
ci-date = htparam.fdate. 

IF from-date = ? THEN
DO:
  from-date = htparam.fdate. 
  to-date = htparam.fdate + 1. 
END.
