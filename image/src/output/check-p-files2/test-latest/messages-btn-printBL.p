
DEF OUTPUT PARAMETER brief-briefnr AS INT.
DEF OUTPUT PARAMETER avail-brief   AS LOGICAL INIT NO.

FIND FIRST htparam WHERE paramnr = 434 NO-LOCK. 
FIND FIRST brief WHERE brief.briefnr = htparam.finteger NO-LOCK NO-ERROR. 
IF AVAILABLE brief THEN 
DO: 
    avail-brief = YES.
    brief-briefnr = brief.briefnr.
END.
