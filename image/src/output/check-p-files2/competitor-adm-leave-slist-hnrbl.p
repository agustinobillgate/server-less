
DEF INPUT  PARAMETER slist-hnr          AS INT.
DEF OUTPUT PARAMETER avail-akt-code     AS LOGICAL INIT NO.
DEF OUTPUT PARAMETER akt-code-bezeich   AS CHAR.

FIND FIRST akt-code WHERE akt-code.aktiongrup = 4 
    AND akt-code.aktionscode = slist-hnr NO-LOCK NO-ERROR.
IF AVAILABLE akt-code THEN 
DO:
    avail-akt-code = YES.
    akt-code-bezeich = akt-code.bezeich.
END.
    
