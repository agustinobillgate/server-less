
DEF INPUT  PARAMETER his-recid AS INT.
DEF OUTPUT PARAMETER res-com   AS CHAR.

FIND FIRST res-history WHERE RECID(res-history) = his-recid NO-LOCK. 
IF AVAILABLE res-history THEN
    res-com = res-history.aenderung.
