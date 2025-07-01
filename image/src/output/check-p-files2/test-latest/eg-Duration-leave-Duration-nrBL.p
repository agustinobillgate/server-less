
DEF INPUT PARAMETER curr-select AS CHAR.
DEF INPUT PARAMETER duration-Duration-nr AS INT.
DEF INPUT PARAMETER rec-id AS INT.
DEF OUTPUT PARAMETER fl-code AS LOGICAL INIT NO.

DEFINE BUFFER queasy1 FOR eg-Duration.  
FIND FIRST eg-Duration WHERE RECID(eg-Duration) = rec-id.

IF curr-select = "chg" THEN
FIND FIRST queasy1 WHERE queasy1.Duration-nr = duration-Duration-nr AND 
    ROWID(queasy1) NE ROWID(eg-Duration) NO-LOCK NO-ERROR.  
ELSE IF curr-select = "add" THEN
FIND FIRST queasy1 WHERE queasy1.Duration-nr = duration-Duration-nr NO-LOCK NO-ERROR.  
IF AVAILABLE queasy1 THEN fl-code = YES.
