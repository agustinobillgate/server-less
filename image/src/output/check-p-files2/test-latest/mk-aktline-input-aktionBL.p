
DEF INPUT  PARAMETER t-aktion AS CHAR.
DEF OUTPUT PARAMETER t-aktionscode AS INT.

FIND FIRST akt-code WHERE akt-code.aktiongrup = 1 
    AND akt-code.bezeich = t-aktion NO-LOCK.
t-aktionscode = akt-code.aktionscode.
