
DEF OUTPUT PARAMETER segmtype-exist AS LOGICAL INITIAL NO.
DEF OUTPUT PARAMETER long-digit     AS LOGICAL.
DEF OUTPUT PARAMETER to-date        AS DATE.
DEF OUTPUT PARAMETER tdate          AS DATE.
DEF OUTPUT PARAMETER fdate          AS DATE.
DEF OUTPUT PARAMETER opening-date   AS DATE.

FIND FIRST htparam WHERE paramnr = 246 NO-LOCK. 
long-digit = htparam.flogical. 

FIND FIRST segment WHERE segment.betriebsnr GT 0 NO-LOCK NO-ERROR. 
IF AVAILABLE segment THEN segmtype-exist = YES. 
 
FIND FIRST htparam WHERE paramnr = 110 NO-LOCK. 
to-date = htparam.fdate - 1. 
tdate  = htparam.fdate - 1.
fdate  = DATE(MONTH(tdate), 1, YEAR(tdate)).

FIND FIRST htparam WHERE paramnr = 186.
opening-date = htparam.fdate.
