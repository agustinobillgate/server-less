
DEF TEMP-TABLE segment-list LIKE segment.
DEF TEMP-TABLE segmentstat-list LIKE segmentstat.


DEF OUTPUT PARAMETER price-decimal  AS INTEGER.
DEF OUTPUT PARAMETER bill-date      AS DATE.
DEF OUTPUT PARAMETER from-date      AS DATE.
DEF OUTPUT PARAMETER TABLE FOR segment-list.
DEF OUTPUT PARAMETER TABLE FOR segmentstat-list.

FIND FIRST htparam WHERE htparam.paramnr = 491 NO-LOCK. 
price-decimal = htparam.finteger. 
FIND FIRST htparam WHERE paramnr = 110 no-lock.  /*Invoicing DATE */ 
bill-date = htparam.fdate. 
from-date = bill-date. 


FOR EACH segment WHERE NOT segment.bezeich MATCHES ("*$$0*")
    NO-LOCK BY segment.segmentcode:
    CREATE segment-list.
    BUFFER-COPY segment TO segment-list.
END.


FIND FIRST segment-list NO-LOCK NO-ERROR.
IF AVAILABLE segment-list THEN
DO:
    FOR EACH segmentstat WHERE
        segmentstat.segmentcode = segment-list.segmentcode
        AND segmentstat.datum GE from-date NO-LOCK BY segmentstat.datum:
        CREATE segmentstat-list.
        BUFFER-COPY segmentstat TO segmentstat-list.
    END.
END.
