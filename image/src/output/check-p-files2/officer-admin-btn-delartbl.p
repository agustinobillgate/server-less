
DEF INPUT  PARAMETER rec-id   AS INT.
DEF OUTPUT PARAMETER err-code AS INT INIT 0.

FIND FIRST queasy WHERE RECID(queasy) = rec-id.

FIND FIRST nation WHERE nation.untergruppe = queasy.number3 NO-LOCK NO-ERROR. 
IF AVAILABLE nation THEN 
DO: 
  err-code = 1.
  RETURN NO-APPLY. 
END. 
DO: 
  FIND CURRENT queasy EXCLUSIVE-LOCK. 
  delete queasy.
END.
