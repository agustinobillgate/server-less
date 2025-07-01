
DEF INPUT  PARAMETER r-recid AS INT.
DEF OUTPUT PARAMETER sorttype AS INT.
DEF OUTPUT PARAMETER bk-reser-resstatus AS INT.

FIND FIRST bk-reser WHERE RECID(bk-reser) = r-recid NO-LOCK NO-ERROR. 
IF AVAILABLE bk-reser AND bk-reser.resstatus LE 2 THEN 
DO: 
  sorttype = bk-reser.resstatus.
  bk-reser-resstatus = bk-reser.resstatus.
END. 
