DEFINE OUTPUT PARAMETER avail-unter     AS LOGICAL  NO-UNDO INIT NO.
DEFINE OUTPUT PARAMETER long-digit      AS LOGICAL  NO-UNDO INIT NO.

FIND FIRST l-untergrup WHERE l-untergrup.betriebsnr = 1 NO-LOCK NO-ERROR. 
avail-unter = AVAILABLE l-untergrup.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

