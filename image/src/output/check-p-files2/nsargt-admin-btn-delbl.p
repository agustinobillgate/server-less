
DEF INPUT PARAMETER rec-id AS INT.
DEF INPUT PARAMETER q1-list-argtnr AS INT.
DEF OUTPUT PARAMETER err AS INT INIT 0.
DEF OUTPUT PARAMETER art-dept AS INT INIT 0.
DEF OUTPUT PARAMETER art-bez AS CHAR.

DEFINE buffer artikel1 FOR artikel. 

FIND FIRST artikel1 WHERE artikel1.artart = 0 
  AND artikel1.artgrp = q1-list-argtnr NO-LOCK NO-ERROR. 
IF AVAILABLE artikel1 THEN 
DO: 
  err = 1.
  art-dept = artikel1.departement.
  art-bez = artikel1.bezeich.
  RETURN NO-APPLY. 
END. 

FOR EACH argt-line WHERE argt-line.argtnr = q1-list-argtnr EXCLUSIVE-LOCK: 
    delete argt-line. 
END.
RELEASE argt-line.

FIND FIRST arrangement WHERE RECID(arrangement) = rec-id NO-LOCK.
FIND CURRENT arrangement EXCLUSIVE-LOCK. 
delete arrangement. 
RELEASE argt-line.
