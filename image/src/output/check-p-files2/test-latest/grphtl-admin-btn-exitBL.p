DEFINE TEMP-TABLE htlname like queasy.  

DEF INPUT PARAMETER TABLE FOR htlname.
DEF INPUT PARAMETER case-type AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER rec-id1 AS INT INIT 0.

FIND FIRST htlname.
IF case-type = 1 THEN   /*MT add */
DO:
    CREATE queasy.  
    RUN fill-new-queasy.  
    FIND CURRENT queasy NO-LOCK.
    rec-id1 = RECID(queasy).
END.
ELSE IF case-type = 2 THEN   /*MT chg */
DO:
    FIND FIRST queasy WHERE RECID(queasy) = rec-id.
    FIND CURRENT queasy EXCLUSIVE-LOCK.  
    BUFFER-COPY htlname TO queasy.
END.

PROCEDURE fill-new-queasy:  
  queasy.KEY = 136.  
  BUFFER-COPY htlname EXCEPT KEY TO queasy.
END.  

