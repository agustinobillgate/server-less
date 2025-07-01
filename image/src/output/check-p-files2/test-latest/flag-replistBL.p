
DEF INPUT PARAMETER s-resnr     AS INT.
DEF INPUT PARAMETER s-reslinnr  AS INT.
DEF INPUT PARAMETER s-ind       AS INT.
DEF INPUT PARAMETER s-done      AS LOGICAL.
DEF INPUT PARAMETER s-recid     AS INTEGER.

FIND FIRST reslin-queasy WHERE reslin-queasy.KEY = "flag" 
    AND reslin-queasy.resnr = s-resnr
    AND reslin-queasy.reslinnr = s-reslinnr
    AND RECID(reslin-queasy) = s-recid NO-LOCK NO-ERROR. 
IF AVAILABLE reslin-queasy THEN 
DO TRANSACTION: 
    FIND CURRENT reslin-queasy EXCLUSIVE-LOCK. 
    IF s-ind = 1 THEN reslin-queasy.deci1 = INTEGER(s-done).
    ELSE IF s-ind = 2 THEN reslin-queasy.deci2 = INTEGER(s-done).
    ELSE IF s-ind = 3 THEN reslin-queasy.deci3 = INTEGER(s-done).
    FIND CURRENT reslin-queasy NO-LOCK. 
END.
